import abc

from whizbang.data.databricks.databricks_client_args import DatabricksClientArgs
from whizbang.domain.manager.databricks.databricks_cluster_manager import IDatabricksClusterManager
from whizbang.domain.manager.databricks.databricks_manager_base import DatabricksManagerBase, IDatabricksManager
from whizbang.domain.models.databricks.databricks_library import DatabricksLibrary
from whizbang.domain.models.databricks.databricks_cluster import DatabricksCluster
from whizbang.domain.repository.databricks.databricks_library_repository import IDatabricksLibraryRepository


class IDatabricksLibraryManager(IDatabricksManager):
    @abc.abstractmethod
    def cluster_status(self, client_args: DatabricksClientArgs, cluster: DatabricksCluster):
        """"""


class DatabricksLibraryManager(DatabricksManagerBase, IDatabricksLibraryManager):
    def __init__(self, repository: IDatabricksLibraryRepository, cluster_manager: IDatabricksClusterManager):
        self.cluster_manager = cluster_manager
        DatabricksManagerBase.__init__(self, repository)
        self.repository: IDatabricksLibraryRepository

    def __skip_existing_libraries(self, client_args: DatabricksClientArgs,
                                  libraries: DatabricksLibrary,
                                  cluster: DatabricksCluster):
        libraries_to_install: DatabricksLibrary = libraries
        cluster_status: dict = self.cluster_status(client_args=client_args, cluster=cluster)
        if 'library_statuses' in cluster_status.keys():
            for status in cluster_status['library_statuses']:
                for library in libraries.libraries['libraries']:
                    if library == status['library'] and \
                            (status['status'] == 'INSTALLED' or
                             status['status'] == 'PENDING' or
                             status['status'] == 'INSTALLING'):
                        libraries_to_install.libraries['libraries'].remove(library)
        return libraries_to_install

    def __uninstall_existing_libraries(self, client_args: DatabricksClientArgs,
                                       cluster: DatabricksCluster):
        cluster_status: dict = self.cluster_status(client_args=client_args, cluster=cluster)
        cluster_id = cluster.cluster_dict['cluster_id']
        libraries = []
        if 'library_statuses' in cluster_status.keys():
            for status in cluster_status['library_statuses']:
                libraries.append(status.get("library"))
        to_uninstall = DatabricksLibrary(
            libraries={
                "cluster_id": cluster_id,
                "libraries": libraries
            }
        )
        self.repository.uninstall(client_args=client_args, t_object=to_uninstall)

    def save(self, client_args, libraries: DatabricksLibrary):
        existing_clusters: 'list[DatabricksCluster]' = self.cluster_manager.get(client_args=client_args)
        list_to_terminate: 'list[DatabricksCluster]' = []
        for existing_cluster in existing_clusters:
            if existing_cluster.cluster_dict['cluster_name'] == libraries.libraries['cluster_name']:
                result = self.cluster_manager.start_cluster(client_args=client_args, cluster=existing_cluster)
                cluster_id = existing_cluster.cluster_dict['cluster_id']
                libraries.libraries.update({'cluster_id': cluster_id})
                self.__uninstall_existing_libraries(client_args=client_args, cluster=existing_cluster)
                self.repository.create(client_args=client_args, t_object=libraries)
                if result is not None:
                    list_to_terminate.append(existing_cluster)
        for cluster in list_to_terminate:
            self.cluster_manager.stop_cluster(client_args=client_args, cluster=cluster)

    def cluster_status(self, client_args: DatabricksClientArgs, cluster: DatabricksCluster):
        return self.repository.cluster_status(client_args=client_args, cluster=cluster)
