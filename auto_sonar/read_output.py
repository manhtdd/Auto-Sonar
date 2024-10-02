import json
import logging
import os
import pandas
import requests
from requests.auth import HTTPBasicAuth

SWE_MAPPING_PATH = "."
TOKEN="sqa_0aa5afee537a0850e83e21db58acb1d119b61f1c"

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

def load_json(file_path):
    try:
        with open(file_path, 'r') as file:
            raw_string = file.read()
            data = json.loads(raw_string)
        return data
    except FileNotFoundError:
        logging.info(f"Error: File not found at path '{file_path}'")
    except Exception as e:
        logging.info(f"{file_path} {e}")
        
def sonar2cwe(cwe):
    if cwe == 'weak-cryptography':  #327
        return ['CWE-327'], ['693']
    elif cwe == 'auth':  #287
        return ['CWE-287'], ['284']
    elif cwe == 'insecure-conf':  #295
        return ['CWE-295'], ['664']
    elif cwe == 'java/path-injection':  #
        return ['CWE-74'], ['707']
    elif cwe == 'java/implicit-cast-in-compound-assignment':  #190 192 197 681
        return ['CWE-190', 'CWE-192', 'CWE-197', 'CWE-681'], ['664', '682']
    elif cwe == 'java/xss':  #79
        return ['CWE-79'], ['707']
    elif cwe == 'java/zipslip':  #29
        return ['CWE-29'], ['664']
    elif cwe == 'java/unsafe-deserialization':  #502
        return ['CWE-502'], ['284', '664']
    elif cwe.startswith('java:S'):
        df = pandas.read_csv(f'{SWE_MAPPING_PATH}/sonar_secu.csv', dtype={'cwe': str})
        df = df[df['key'] == cwe].iloc[0]
        return [f"CWE-{df['cwe']}"], [df['cwe-1000']]
    else:
        return [], ['10000']
    
def sonar_analysis(file_content:dict) -> dict:
    file_content = file_content["task"]
    if file_content['status'] == "SUCCESS":
        return {}
    
    logging.info(json.dumps(file_content, indent=4))
    if not file_content == []:
        comp = file_content['componentKey']
        file = comp.split(':')[1]
        hot_rule_id = file_content['securityCategory'] if 'securityCategory' in file_content else ''
        line = file_content['line']
        cwe, _ = sonar2cwe(hot_rule_id)

        predict = {
            'file': file,
            'line': line,
            'rule_id': hot_rule_id,
            'cwe': cwe,
            'found_by': 'code_ql'
        }
        
        return predict
    else:
        logging.error(f"Empty {file_content}")
        
    return {}

def call_ce_task_api(ce_task_url):
    # Make a GET request to the ceTaskUrl
    try:
        response = requests.get(ce_task_url, auth=HTTPBasicAuth(TOKEN, ""))
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

if __name__ == "__main__":
    file_path = "input/test-python-one-file-3rd-library"
    logging.info(file_path)
    scanner_path = f"{file_path}/scannerwork"
    logging.info(scanner_path)
    json_scanner_output = get_scanner_output(scanner_path)
    logging.info(json.dumps(json_scanner_output, indent=4))
    ce_task_url = json_scanner_output.get('ceTaskUrl')
    if ce_task_url:
        # Call the API and get the result
        api_response = call_ce_task_api(ce_task_url)
        
        # Print the API response
        if api_response:
            logging.info(json.dumps(api_response, indent=4))
    else:
        logging.info("ceTaskUrl not found in the configuration file.")
    json_output = sonar_analysis(api_response)
    logging.info(json.dumps(json_output, indent=4))