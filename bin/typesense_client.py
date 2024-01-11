import os
import sys
lib_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),"..","lib")
sys.path.append(lib_path)
import typesense
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path)
from config.config_accessor import ConfigAccessor

class TypesenseClient:
    # Class variable to store the Typesense client
    _instance = None

    def __new__(cls):
        """
        Create a new instance of TypesenseClient only if it doesn't exist.

        Returns:
        - TypesenseClient: The instance of the TypesenseClient.
        """
        if not cls._instance:
            cls._instance = super(TypesenseClient, cls).__new__(cls)
            cls._instance.typesense_client = cls._create_typesense_client()
        return cls._instance

    @staticmethod
    def _create_typesense_client():
        """
        Create and configure a Typesense client based on configuration values.

        Returns:
        - typesense.Client: The configured Typesense client.
        """
        config_accessor = ConfigAccessor()
        return typesense.Client({
            'nodes': [{
                'host': config_accessor.get_splunk_launch_conf_value("TYPESENSE_SERVER"),
                'port': config_accessor.get_splunk_launch_conf_value("TYPESENSE_PORT"),
                'protocol': config_accessor.get_splunk_launch_conf_value("TYPESENSE_PROTOCOL")
            }],
            'api_key': config_accessor.get_splunk_launch_conf_value("TYPESENSE_API_KEY"),
            'connection_timeout_seconds': 2
        })

    def get_typesense_client(self):
        """
        Get the Typesense client.

        Returns:
        - typesense.Client: The Typesense client.
        """
        return self.typesense_client
