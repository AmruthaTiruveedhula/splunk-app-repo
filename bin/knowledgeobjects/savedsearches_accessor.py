import os
import sys
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path)
from splunk_rest_client import SplunkRestApiClient

class SavedSearchesAccessor(SplunkRestApiClient):
    def __init__(self):
        super().__init__()

    def get_entity_data(self):
        """
        Retrieve information about saved searches from the Splunk REST API.

        Returns:
        - list: A list of dictionaries containing saved search information.
        """
        # Define the endpoint for retrieving saved search information
        endpoint = "/servicesNS/-/-/saved/searches"

        # Specify parameters for the Splunk REST API request
        params = {'output_mode': 'json'}

        # Retrieve data from the Splunk REST API
        response = self.get_splunk_data(endpoint, params)

        if response:
            # Extract relevant information from the response and format it into a list of dictionaries
            saved_searches = [{'name': entry['name'], 'id': entry.get('id', None), 'author': entry.get('author', None)} for entry in response.get('entry', [])]
            return saved_searches
        else:
            print("No SavedSearches present")
            return []