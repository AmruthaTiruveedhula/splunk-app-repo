import os
import sys
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path)
from splunk_rest_client import SplunkRestApiClient

class KVStoreAccessor(SplunkRestApiClient):

    def __init__(self, collection):
        """
        Initialize the KVStoreAccessor with the specified collection.

        Parameters:
        - collection (str): The name of the KVStore collection.
        """
        super().__init__()
        self.collection = collection
        self.kvstore_url = f"servicesNS/amrutha/splunk-app/storage/collections/data/{collection}"
        self.params = {'output_mode': 'json'}

        # Map collections to their primary keys for reference
        collection_to_primary_key_map = {
            'dashboards': 'id',
            'savedsearches': 'id',
            'apps': 'title',
            'fields': 'field'
        }
        self.primarykey = collection_to_primary_key_map.get(self.collection)

    def fetch_data_from_kvstore(self):
        """
        Fetch data from the KVStore collection.

        Returns:
        - dict: The response containing the data from the KVStore.
        """
        response = self.get_splunk_data(self.kvstore_url, self.params)
        return response

    def publish_data_to_kvstore(self, entities):
        """
        Publish data to the KVStore collection.

        Parameters:
        - entities (list): List of entities to be published to the KVStore.
        """
        existing_entity_ids = self.get_existing_entities()

        for entity in entities:
            if entity[self.primarykey] not in existing_entity_ids:
                self.post_data(entity)

    def post_data(self, data):
        """
        Post data to the KVStore collection.

        Parameters:
        - data (dict): The data to be posted to the KVStore.

        Returns:
        - dict: The response containing information about the posted data.
        """
        headers = {'Content-Type': 'application/json'}
        response = self.post_splunk_data(self.kvstore_url, self.params, headers, data)
        return response

    def get_existing_entities(self):
        """
        Get existing entities (primary keys) from the KVStore collection.

        Returns:
        - set: A set of existing entity primary keys.
        """
        existing_entities = self.fetch_data_from_kvstore()
        return set(entry[self.primarykey] for entry in existing_entities)
