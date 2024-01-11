from splunk.persistconn.application import PersistentServerConnectionApplication
import os
import sys
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path)
from splunktypesense_integrator import SplunkTypesenseIntegrator

class UpdateTypesenseCollection(PersistentServerConnectionApplication):
    def __init__(self, _command_line, _command_arg):
        """
        Initialize the UpdateTypesenseCollection application.

        Parameters:
        - _command_line: Command line arguments.
        - _command_arg: Command line arguments.
        """
        super(PersistentServerConnectionApplication, self).__init__()

    def handle(self, in_string):
        """
        Handle the incoming update request.

        Parameters:
        - in_string (str): The incoming JSON string.

        Returns:
        - dict: A dictionary containing the response payload and status.
        """
        # List of Typesense collections to update
        collections = ['dashboards', 'savedsearches', 'apps', 'fields']

        # Iterate over each collection and update Typesense
        for collection in collections:
            splunk_typesense_integrator = SplunkTypesenseIntegrator(collection)
            splunk_typesense_integrator.index_data_in_typesense()

        # Return success response
        return {'payload': 'success', 'status': 200}

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
        Perform cleanup after handling the update request.
        """
        pass
