import os
import sys
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path)
from splunk_rest_client import SplunkRestApiClient

class DashboardsAccessor(SplunkRestApiClient):
    def __init__(self):
        super().__init__()

    def get_entity_data(self):
        """
        Retrieve information about dashboards from the Splunk REST API.

        Returns:
        - list: A list of dictionaries containing dashboard information.
        """
        # Define the endpoint for retrieving dashboard information
        endpoint = "/servicesNS/-/-/data/ui/views"

        # Specify parameters for the Splunk REST API request
        params = {'output_mode': 'json'}

        # Retrieve data from the Splunk REST API
        response = self.get_splunk_data(endpoint, params)

        if response:
            # Extract relevant information from the response and format it into a list of dictionaries
            dashboards = [{'name': entry['name'], 'id': entry.get('id', None), 'author': entry.get('author', None)} for entry in response.get('entry', [])]
            return dashboards
        else:
            print("No dashboards present")
            return []

