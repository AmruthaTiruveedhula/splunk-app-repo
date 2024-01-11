import typesense
import os
import sys
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path)
from datastores.kvstoreaccessor import KVStoreAccessor
from typesense_client import TypesenseClient

class SplunkTypesenseIntegrator:

    def __init__(self, collection_name):
        """
        Initialize SplunkTypesenseIntegrator with the specified collection name.

        Parameters:
        - collection_name (str): The name of the Typesense collection to integrate with.
        """
        self.collection_name = collection_name
        self.kvstore_accessor = KVStoreAccessor(collection_name)
        self.splunk_data = self.kvstore_accessor.fetch_data_from_kvstore()
        self.client = TypesenseClient().get_typesense_client()
        self.collection = self.client.collections[collection_name]
        collection_to_primary_key_map = {'dashboards': 'id', 'savedsearches': 'id', 'apps': 'title', 'fields': 'field'}
        self.primarykey = collection_to_primary_key_map.get(self.collection_name)

    def index_data_in_typesense(self):
        """
        Index data from the KVStore into Typesense collection.
        """
        for document in self.splunk_data:
            if self.primarykey != 'id':
                document['id'] = document[self.primarykey]
            try:
                self.collection.documents.create(document)
            except typesense.exceptions.ObjectAlreadyExists:
                # Handle the case when the document already exists
                print(f"Document already exists in Typesense.")
                return None

    def search_entity(self, search_query):
        """
        Search for entities in the Typesense collection based on the specified query.

        Parameters:
        - search_query (str): The search query.

        Returns:
        - list or None: List of search results or None if an error occurs.
        """
        search_parameters = {'q': search_query, 'query_by': '*'}
        try:
            search_results = self.collection.documents.search(search_parameters)
            return search_results['hits'] if search_results else None
        except typesense.exceptions.RequestFailed as e:
            print(f"Error during search: {e}")
            return None

if __name__ == "__main__":
    # Example usage
    obj = SplunkTypesenseIntegrator("fields")
    obj.search_entity('eventtype')
