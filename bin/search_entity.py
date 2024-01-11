from splunk.persistconn.application import PersistentServerConnectionApplication
import json
import os
import sys
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path)
from splunktypesense_integrator import SplunkTypesenseIntegrator

class SearchEntity(PersistentServerConnectionApplication):
    def __init__(self, _command_line, _command_arg):
        super(PersistentServerConnectionApplication, self).__init__()
        # Define the collections to search through
        self.collections = ['dashboards', 'savedsearches', 'apps', 'fields']

    def handle(self, in_string):
        """
        Handle the incoming search request.

        Parameters:
        - in_string (str): The incoming JSON string containing the search query.

        Returns:
        - dict: A dictionary containing the search response and status.
        """
        json_data = json.loads(in_string)
        search_query = json_data.get("query", [])[0][1] if "query" in json_data else ""
        response = None

        # Iterate through collections and search using SplunkTypesenseIntegrator
        for collection in self.collections:
            splunktypesense_integrator = SplunkTypesenseIntegrator(collection)
            response = splunktypesense_integrator.search_entity(search_query)
            if response:
                break

        return {'payload': json.dumps(response), 'status': 200}

    def handleStream(self, handle, in_string):
        """
        Handle streaming data (not implemented in this application).

        Parameters:
        - handle: The handle for streaming data.
        - in_string (str): The incoming data string.

        Raises:
        - NotImplementedError: This method is not implemented in this application.
        """
        raise NotImplementedError("PersistentServerConnectionApplication.handleStream")

    def done(self):
        """
        Perform cleanup after handling the search request.
        """
        pass
