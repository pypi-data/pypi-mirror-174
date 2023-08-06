"""
Base class for all collector plugins
"""

import json

from abc import abstractmethod
from pathlib import Path
import re
from typing import Any, List, Optional, Union, final
from packageurl import PackageURL  # type: ignore

from hoppr_cyclonedx_models.cyclonedx_1_4 import Component

from hoppr import __version__, plugin_utils
from hoppr.base_plugins.hoppr import HopprPlugin, hoppr_process, hoppr_rerunner
from hoppr.configs.credentials import Credentials
from hoppr.hoppr_types.component_coverage import ComponentCoverage
from hoppr.hoppr_types.cred_object import CredObject
from hoppr.hoppr_types.purl_type import PurlType
from hoppr.result import Result
from hoppr.utils import dedup_list, remove_empty


class BaseCollectorPlugin(HopprPlugin):
    """
    Base class for collector plugins
    """

    default_component_coverage = ComponentCoverage.EXACTLY_ONCE

    def directory_for(
        self,
        purl_type: Union[str, PurlType],
        repo_url: str,
        subdir: Optional[str] = None,
    ) -> Path:
        """
        Identify the directory into which the artifact should be copied
        """

        repo_dir = plugin_utils.dir_name_from_repo_url(repo_url)
        directory = Path(self.context.collect_root_dir, str(purl_type), repo_dir)

        if subdir is not None:
            directory = Path(directory, subdir)

        directory.mkdir(parents=True, exist_ok=True)

        return directory

    @staticmethod
    def check_purl_specified_url(purl: PackageURL, repo_url: str) -> Result:
        """
        Test if a repository_url specified as a purl qualifier is a mis-match with a given repo_url

        If no repository_url is specified, repo_url is fine, no-mismatch, return False

        Otherwise, considered a match if repo_url starts with the purl url (after trimming trailing
        "/"s and URL scheme, if present)
        """
        purl_url = purl.qualifiers.get("repository_url")
        if purl_url is None:
            return Result.success()

        trimmed_purl_url = re.sub(r"(ssh|file|https?)://", "", purl_url).rstrip("/")
        trimmed_repo_url = re.sub(r"(ssh|file|https?)://", "", repo_url).rstrip("/")
        if trimmed_repo_url.startswith(trimmed_purl_url):
            return Result.success()

        return Result.fail(
            f"Purl-specified repository url ({purl.qualifiers.get('repository_url')}) "
            + f"does not match current repo ({repo_url})."
        )


class SerialCollectorPlugin(BaseCollectorPlugin):
    """
    Base class for multi-process collector plugins
    """

    @staticmethod
    def _get_repos(comp: Component) -> List[str]:
        """
        Returns all repos listed in all "hoppr:repository:component_search_sequence" properties
        for this component
        """
        repo_list = []

        for prop in comp.properties or []:
            if prop.name == "hoppr:repository:component_search_sequence":
                search_sequence = json.loads(prop.value or "")
                repo_list.extend(search_sequence.get("Repositories", []))

        return dedup_list(repo_list)

    @abstractmethod
    @hoppr_rerunner
    def collect(self, comp: Any, repo_url: str, creds: CredObject = None):
        """
        This method should attempt to collect a single component from the specified URL
        """

    @final
    @hoppr_process
    def process_component(self, comp: Component) -> Result:
        """
        Copy a component to the local collection directory structure

        A CollectorPlugin will never return a RETRY result, but handles the retry logic internally.
        """

        logger = self.get_logger()

        result = Result.fail(f"No repository found for purl {comp.purl}")

        # for repo_url in self.context.manifest.get_repos():
        for repo_url in self._get_repos(comp):
            logger.info(f"Looking in repository: {repo_url}")

            repo_creds = Credentials.find_credentials(repo_url)
            result = self.collect(comp, repo_url, repo_creds)

            if result.is_success():
                break  ### We found it, no need to try any more repositories

        return result

    @hoppr_process
    def post_stage_process(self):
        for purl_type in self.supported_purl_types:
            directory = Path(self.context.collect_root_dir, purl_type)

            if directory.is_dir():
                remove_empty(directory)

        return Result.success()


class BatchCollectorPlugin(BaseCollectorPlugin):
    """
    Base class for single-process collector plugins
    """

    config_file: Path

    @abstractmethod
    @hoppr_rerunner
    def collect(self, comp: Component):
        """
        This method should attempt to collect all components
        from all manifest repositories or registries that were
        previously configured in the pre stage process.

        Use of a single batch operation (i.e. dynamically constructed
        shell command) is encouraged if supported by the underlying
        collection tool(s).
        """

    @final
    @hoppr_process
    def process_component(self, comp: Component) -> Result:
        """
        Copy a component to the local collection directory structure

        A CollectorPlugin will never return a RETRY result, but handles the retry logic internally.
        """
        logger = self.get_logger()
        logger.info(f"Processing component {comp.purl}")

        return self.collect(comp)
