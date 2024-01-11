import json
import requests
from requests.auth import HTTPBasicAuth
import os
import sys
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path)
from config.config_accessor import ConfigAccessor

class SplunkRestApiClient:

    def __init__(self):
        """
        Initialize the SplunkRestApiClient.

        Fetches configuration values for Splunk server, port, username, and password.
        """
        super().__init__()
        self.config_accessor = ConfigAccessor()
        self.username = self.config_accessor.get_splunk_launch_conf_value("SPLUNK_USERNAME")
        self.password = self.config_accessor.get_splunk_launch_conf_value("SPLUNK_PASSWORD")

    def post_splunk_data(self, endpoint, params=None, headers=None, json=None, data=None):
        """
        Send a POST request to the Splunk REST API.

        Parameters:
        - endpoint (str): The endpoint for the POST request.
        - params (dict): Parameters to include in the request.
        - headers (dict): Headers to include in the request.
        - json: JSON data to include in the request body.
        - data: Data to include in the request body.

        Returns:
        - dict or str: Parsed JSON response or raw response content.
        """
        splunk_url = self.get_splunk_url(endpoint)
        response = requests.post(splunk_url, auth=HTTPBasicAuth(self.username, self.password), params=params, headers=headers, json=json, data=data, verify=False)
        return self.parse_response(response, endpoint)

    def get_splunk_data(self, endpoint, params=None):
        """
        Send a GET request to the Splunk REST API.

        Parameters:
        - endpoint (str): The endpoint for the GET request.
        - params (dict): Parameters to include in the request.

        Returns:
        - dict or str: Parsed JSON response or raw response content.
        """
        splunk_url = self.get_splunk_url(endpoint)
        response = requests.get(splunk_url, auth=HTTPBasicAuth(self.username, self.password), params=params, verify=False)
        return self.parse_response(response, endpoint)

    def get_splunk_url(self, endpoint):
        """
        Generate the Splunk REST API URL based on the configured server and port.

        Parameters:
        - endpoint (str): The endpoint to append to the URL.

        Returns:
        - str: The complete Splunk REST API URL.
        """
        server = self.config_accessor.get_splunk_launch_conf_value("SPLUNK_SERVER")
        port = self.config_accessor.get_splunk_launch_conf_value("SPLUNK_PORT")
        return f"https://{server}:{port}/{endpoint}"

    def parse_response(self, response, endpoint):
        """
        Parse the response from the Splunk REST API.

        Parameters:
        - response (requests.Response): The response object.
        - endpoint (str): The Splunk API endpoint.

        Returns:
        - dict or str: Parsed JSON response or raw response content.
        """
        if response.status_code in {200, 201}:
            try:
                return response.json()
            except json.decoder.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
                print("Response content:", response.text)
            return response.text
        else:
            print(f"Error accessing Splunk Endpoint {endpoint}. Status code: {response.status_code}")
            return response
