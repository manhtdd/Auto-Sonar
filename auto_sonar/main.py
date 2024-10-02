import os
import logging
import json
from typing import Optional
from .api import main as read_analyze
from .setup_project import main as setup_project
import subprocess

SONAR_HOST_URL = "http://localhost:9000"

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

def check_directory(path):
    if not os.path.isdir(path):
        logging.error(f"ERROR: {path} is not a valid directory.")
        return False
    return True

def check_sonar_properties(path):
    sonar_properties = os.path.join(path, 'sonar-project.properties')
    if not os.path.isfile(sonar_properties):
        logging.info(f"sonar-project.properties file not found in {path}.")
        logging.info("Creating sonar-project.properties")
        setup_project(path)
        if not os.path.isfile(sonar_properties):
            logging.error("FAILED TO GENERATE sonar-project.properties")
            return False
    return True

def check_file_count(path):
    num_java_files = count_files(path, ".java")
    num_py_files = count_files(path, ".py")
    total_files = num_java_files + num_py_files

    if total_files != 1:
        logging.error(f"ERROR: There must be exactly one .java or .py file in the directory. Found {total_files}.")
        return -1, -1

    return num_java_files, num_py_files

def check_java_class_file(path):
    java_file = next(f for f in os.listdir(path) if f.endswith(".java"))
    class_file = os.path.splitext(java_file)[0] + ".class"

    if not os.path.isfile(os.path.join(path, class_file)):
        logging.info(f"Corresponding .class file for {java_file} not found.")
        logging.info("TRY TO RUN BUILD...")
        logging.info(f"javac {java_file}")
        subprocess.run(["javac", os.path.join(path, java_file)])
        if not os.path.isfile(os.path.join(path, class_file)):
            logging.error("ERROR: javac failed. Please check if you have JDK installed.")
            return False
        logging.info("BUILD SUCCESS")
    return True

def check_sonar_accessibility():
    logging.info(f"Checking if {SONAR_HOST_URL} is accessible...")
    result = subprocess.run(["curl", "--output", "/dev/null", "--silent", "--head", "--fail", SONAR_HOST_URL])

    if result.returncode != 0:
        logging.error(f"ERROR: {SONAR_HOST_URL} is not accessible. Please ensure that the SonarQube server is running.")
        logging.error("Try running this command:\n\tdocker run -d --name sonarqube -e SONAR_ES_BOOTSTRAP_CHECKS_DISABLE=true -p 9000:9000 sonarqube:latest")
        logging.error("Or if your sonarqube container already exists:\n\tdocker container start sonarqube")
        return False
    else:
        logging.info(f"SonarQube server is accessible at {SONAR_HOST_URL}.")

    return True
        
def run_sonar_scanner(path):
    logging.info(f"COMMAND:\n\tdocker run --rm --user 0 -v {os.getcwd()}/{path}:/usr/src -e SONAR_HOST_URL=\"{SONAR_HOST_URL}\" "
          f"-v {os.getcwd()}/{path}/scannerwork:/tmp/.scannerwork --network=host sonarsource/sonar-scanner-cli")
    
    subprocess.run([
        "docker", "run", "--rm", "--user", "0",
        "-v", f"{os.getcwd()}/{path}:/usr/src",
        "-e", f"SONAR_HOST_URL={SONAR_HOST_URL}",
        "-v", f"{os.getcwd()}/{path}/scannerwork:/tmp/.scannerwork",
        "--network=host",
        "sonarsource/sonar-scanner-cli"
    ])

    logging.info("FINISHED RUNNING")

def count_files(path, extension):
    return len([f for f in os.listdir(path) if f.endswith(extension)])

def run_sonar(codepath: str, savepath: Optional[str] = None) -> None:
    logging.info(codepath)
    logging.info(savepath)
    
    dir_path = os.path.dirname(codepath)
    logging.info(dir_path)
    file_name = os.path.basename(codepath)
    logging.info(file_name)
    
    if not check_directory(dir_path):
        return {}
    
    if not check_sonar_properties(dir_path):
        return {}
    
    num_java_files, num_py_files = check_file_count(dir_path)
    if num_java_files == -1 and num_py_files == 1:
        return {}
    
    if num_java_files == 1:
        if not check_java_class_file(dir_path):
            return {}
        
    if not check_sonar_accessibility():
        return {}
    
    run_sonar_scanner(dir_path)
    
    issues_api_response, hotspots_api_response = read_analyze(os.path.dirname(savepath))
    
    output = {
        "issues": issues_api_response,
        "hotspots": hotspots_api_response
    }
    
    with open(savepath, 'w') as json_file:
        json.dump(output, json_file, indent=4)
        
    if not os.path.exists(savepath):
        logging.error(f"The file '{savepath}' does not exist.")

if __name__ == "__main__":
    codepath = "input/test_sonar_security/VulnerableApp.java"
    savepath = "input/test_sonar_security/VulnerableApp.json"
    # codepath = "input/Main.java"
    # savepath = "input/main.json"
    output = run_sonar(codepath, savepath)
    logging.info(json.dumps(output, indent=4))