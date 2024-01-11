import os
import sys
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path)
from splunk_rest_client import SplunkRestApiClient
import time
import uuid

class FieldsAccessor(SplunkRestApiClient):
    def __init__(self):
        super().__init__()

    def get_entity_data(self):
        # Generate a unique ID for the search job
        unique_id = str(uuid.uuid4())

        # Define parameters for the Splunk REST API request
        get_data = {'output_mode': 'json'}

        # Define the search query to retrieve field summary information
        search_query = 'search index=_internal | fieldsummary | fields field'

        # Specify additional parameters for submitting the search job
        post_data = {
            'id': unique_id,
            'search': search_query,
            'earliest_time': '1',
            'latest_time': 'now',
        }

        # Specify the base URL for submitting a Splunk search job
        splunk_search_base_url = "/servicesNS/-/search/search/jobs"

        # Submit the Splunk search job
        self.post_splunk_data(splunk_search_base_url, data=post_data)

        # Monitor the status of the search job until it is DONE
        is_job_completed = ''
        while is_job_completed != 'DONE':
            time.sleep(5)
            job_status_base_url = f'/servicesNS/-/search/search/jobs/{unique_id}'
            resp_job_status_data = self.post_splunk_data(job_status_base_url, params=get_data)
            is_job_completed = resp_job_status_data['entry'][0]['content']['dispatchState']
            print("Current job status is {}".format(is_job_completed))

        # Retrieve the summary results of the search job
        splunk_summary_base_url = f'/servicesNS/-/search/search/jobs/{unique_id}/results?count=0'
        splunk_summary_results = self.get_splunk_data(splunk_summary_base_url, params=get_data)

        # Check if there are matching fields based on the Splunk SPL query
        if splunk_summary_results:
            return splunk_summary_results['results']
        else:
            print("There are no fields that match the current Splunk SPL query")
