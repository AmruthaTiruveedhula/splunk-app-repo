from splunk.persistconn.application import PersistentServerConnectionApplication
import json
import os
import sys
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path)
from manager.splunkobjects_manager import SplunkObjectsManager

class ViewEntity(PersistentServerConnectionApplication):
    def __init__(self, _command_line, _command_arg):
        """
        Initialize the ViewEntity application.

        Parameters:
        - _command_line: Command line arguments.
        - _command_arg: Command line arguments.
        """
        super(PersistentServerConnectionApplication, self).__init__()

    def handle(self, in_string):
        """
        Handle the incoming view request.

        Parameters:
        - in_string (str): The incoming JSON string containing the entity to view.

        Returns:
        - dict: A dictionary containing the response payload and status.
        """
        json_data = json.loads(in_string)
        entity = json_data.get("query", [])[0][1] if "query" in json_data else ""
        splunk_objects_manager = SplunkObjectsManager(entity)
        response = splunk_objects_manager.fetch_entities()
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
        Perform cleanup after handling the view request.
        """
        pass
