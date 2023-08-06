import abc

from databricks_cli.libraries.api import LibrariesApi
from databricks_cli.sdk import ApiClient

from whizbang.data.databricks.databricks_context_base import DatabricksContextBase, IDatabricksContextBase


class IDatabricksLibraryContext(IDatabricksContextBase):
    """"""

    @abc.abstractmethod
    def install_libraries(self, cluster_id, libraries):
        """"""

    @abc.abstractmethod
    def uninstall_libraries(self, cluster_id, libraries):
        """"""

    @abc.abstractmethod
    def cluster_status(self, cluster_id):
        """"""


class DatabricksLibraryContext(DatabricksContextBase, IDatabricksLibraryContext):
    def __init__(self, api_client: ApiClient, api):
        DatabricksContextBase.__init__(self, api_client=api_client, api=api)

    def install_libraries(self, cluster_id, libraries):
        def _install_libraries(api: LibrariesApi, cluster_id, libraries):

            return api.install_libraries(
                cluster_id=cluster_id,
                libraries=libraries
            )
        return self._execute(func=_install_libraries, cluster_id=cluster_id, libraries=libraries)

    def uninstall_libraries(self, cluster_id, libraries):
        def _uninstall_libraries(api: LibrariesApi, cluster_id, libraries):

            return api.uninstall_libraries(
                cluster_id=cluster_id,
                libraries=libraries
            )
        return self._execute(func=_uninstall_libraries, cluster_id=cluster_id, libraries=libraries)

    def cluster_status(self, cluster_id):
        def _cluster_status(api: LibrariesApi, cluster_id):
            return api.cluster_status(cluster_id=cluster_id)

        return self._execute(func=_cluster_status, cluster_id=cluster_id)
