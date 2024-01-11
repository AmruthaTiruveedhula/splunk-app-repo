import sys
import os
dir_path =  os.path.join(os.path.dirname(os.path.realpath(__file__)),"..")
sys.path.append(dir_path)
from apps.apps_accessor import AppsAccessor
from datastores.kvstoreaccessor import KVStoreAccessor
from fields.fields_accessor import FieldsAccessor
from knowledgeobjects.dashboards_accessor import DashboardsAccessor
from knowledgeobjects.savedsearches_accessor import SavedSearchesAccessor

class SplunkObjectsManager:
    def __init__(self, entity=''):
        """
        Initialize SplunkObjectsManager with the specified entity.

        Parameters:
        - entity (str): The type of entity to manage (e.g., "apps", "dashboards", etc.).
        """
        self.entity = entity
        super().__init__()

    def fetch_entities(self):
        """
        Fetch entities from the KVStore.

        Returns:
        - list: A list of entities retrieved from the KVStore.
        """
        kvstore_accessor = KVStoreAccessor(self.entity)
        entities = kvstore_accessor.fetch_data_from_kvstore()
        return entities if entities else {}

    def publish_entities(self):
        """
        Publish entities to the KVStore based on the specified entity type.
        """
        entities = []
        kvstore_accessor = KVStoreAccessor(self.entity)

        # Use factory pattern to create appropriate accessor based on the entity type
        accessor_factory = {
            "apps": AppsAccessor,
            "dashboards": DashboardsAccessor,
            "fields": FieldsAccessor,
            "savedsearches": SavedSearchesAccessor
        }

        accessor_class = accessor_factory.get(self.entity)

        if accessor_class:
            accessor_instance = accessor_class()
            entities = accessor_instance.get_entity_data()

        kvstore_accessor.publish_data_to_kvstore(entities)