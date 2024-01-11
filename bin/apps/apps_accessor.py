import os
import sys
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path)
from splunk_rest_client import SplunkRestApiClient
import time

class AppsAccessor(SplunkRestApiClient):
    def __init__(self):
        super().__init__()

    def get_entity_data(self):
        # Define the search query to retrieve information about installed apps
        search_query = "| rest /services/apps/local | search disabled=0 | table label title version description"

        # Specify parameters for the Splunk REST API request
        get_data = {'output_mode': 'json'}
        post_data = {
            'search': search_query,
            'earliest_time': '1',
            'latest_time': 'now',
        }

        # Specify the base URL for submitting a Splunk search job
        splunk_search_base_url = "/servicesNS/-/search/search/jobs"

        # Submit the Splunk search job
        response = self.post_splunk_data(splunk_search_base_url, get_data, None, None, post_data)

        # Check if the search job was successfully submitted
        if 'sid' not in response:
            print("Error submitting search job.")
            return

        # Extract the job ID from the response
        job_id = response['sid']
        print(f"Search job submitted. Job ID: {job_id} and response code is {response}")

        # Monitor the status of the search job until it is either DONE or FAILED
        is_job_status = ''
        while is_job_status not in ['DONE', 'FAILED']:
            time.sleep(5)
            job_status_base_url = f'/servicesNS/-/search/search/jobs/{job_id}'
            resp_job_status_data = self.post_splunk_data(job_status_base_url, get_data)
            is_job_status = resp_job_status_data['entry'][0]['content']['dispatchState']
            print("Job Errors:", resp_job_status_data.get('entry')[0]['content']['messages'])
            print(f"Current job status is {is_job_status}")

        # Retrieve the summary results of the search job
        splunk_summary_base_url = f'/servicesNS/-/search/search/jobs/{job_id}/results?count=0'
        splunk_summary_results = self.get_splunk_data(splunk_summary_base_url, params=get_data)

        # Check if there are matching apps based on the Splunk SPL query
        if splunk_summary_results:
            return splunk_summary_results['results']
        else:
            print("There are no apps that match the current Splunk SPL query")
