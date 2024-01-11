from splunk.persistconn.application import PersistentServerConnectionApplication
import os
import sys
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path)
import json
from manager.splunkobjects_manager import SplunkObjectsManager

class UpdateEntity(PersistentServerConnectionApplication):
    def __init__(self, _command_line, _command_arg):
        """
        Initialize the UpdateEntity application.

        Parameters:
        - _command_line: Command line arguments.
        - _command_arg: Command line arguments.
        """
        super(PersistentServerConnectionApplication, self).__init__()

    def handle(self, in_string):
        """
        Handle the incoming update request.

        Parameters:
        - in_string (str): The incoming JSON string containing the entity to update.

        Returns:
        - dict: A dictionary containing the response payload and status.
        """
        json_data = json.loads(in_string)
        entity = json_data.get("query", [])[0][1] if "query" in json_data else ""
        splunk_objects_manager = SplunkObjectsManager(entity)
        splunk_objects_manager.publish_entities()
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
