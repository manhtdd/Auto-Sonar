import json
import logging
import os
import requests
from requests.auth import HTTPBasicAuth
from typing import Tuple

# Setup logging to both file and console
LOGS_DIR = "logs"
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)
    
log_file_path = os.path.join(LOGS_DIR, 'logs.log')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
    handlers=[
        logging.FileHandler(log_file_path),
        logging.StreamHandler()
    ]
)

def call_sonar_api(api, token):
    logging.info(api)
    # Make a GET request to the ceTaskUrl
    try:
        response = requests.get(api, auth=HTTPBasicAuth(token, ""))
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json()  # Parse the JSON response
    except requests.exceptions.RequestException as e:
        logging.error(f"An error occurred: {e}")
        return None
    
def get_scanner_output(scanner_path:str) -> dict:
    # Create a dictionary to store the configuration
    config_data = {}
    
    # Open and read the file
    with open(f"{scanner_path}/report-task.txt", 'r') as file:
        for line in file:
            if '=' in line:
                logging.info(line)
                # Split each line at the '=' sign to separate the key and the value
                _temp = line.strip().split('=')
                key = _temp[0]
                value = '='.join(_temp[1:])
                config_data[key] = value
                
    return config_data

def main(file_path:str, sonar_url_host:str, token:str)-> Tuple[dict, dict]:
    logging.info(file_path)
    scanner_path = f"{file_path}/scannerwork"
    logging.info(scanner_path)
    
    json_scanner_output = get_scanner_output(scanner_path)
    logging.info(json.dumps(json_scanner_output, indent=4))
    
    project_key = json_scanner_output.get('projectKey')
    if project_key:
        # Call the API and get the result
        issues_api_response = call_sonar_api(f"{sonar_url_host}/api/issues/search?componentKeys={project_key}", token=token)
        logging.info(json.dumps(issues_api_response, indent=4))
        hotspots_api_response = call_sonar_api(f"{sonar_url_host}/api/hotspots/search?project={project_key}", token=token)
        logging.info(json.dumps(hotspots_api_response, indent=4))
    else:
        logging.info("projectKey not found in the configuration file.")
        return {}, {}
        
    return issues_api_response, hotspots_api_response
    
if __name__ == "__main__":
    file_path = "input/test_sonar_security"    
    issues_api_response, hotspots_api_response = main(file_path)
    logging.info(json.dumps(issues_api_response, indent=4))
    logging.info(json.dumps(hotspots_api_response, indent=4))