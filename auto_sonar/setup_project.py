import sys
import os
import logging

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

TOKEN="sqa_0aa5afee537a0850e83e21db58acb1d119b61f1c"
PYTHON_VERSION = 3.8
SONAR_PROJECT_PROPERTIES_TEMPLATE = '''sonar.projectKey=my:{}
sonar.projectName={}
sonar.projectVersion=1.0
sonar.sources={}
sonar.sourceEncoding=UTF-8
sonar.token={}
sonar.scm.disabled=true
'''

def dump_to_text_file(file_path: str, data: str, additional_data: str = None, read_after: bool = False):
    """
    Writes data to a text file, appends additional data if provided,
    and reads the content if specified.

    Args:
        file_path (str): The path to the text file.
        data (str): The data to write to the file.
        additional_data (str, optional): Additional data to append to the file. Defaults to None.
        read_after (bool, optional): Whether to read and print the content after writing. Defaults to False.
    """
    # Writing data to the file
    with open(file_path, 'w') as file:
        file.write(data)
        logging.info(f"Data written to {file_path}")

        # Append additional data if provided
        if additional_data:
            file.write(additional_data)
            logging.info("Additional data appended.")

    # Read the content of the file if specified
    if read_after:
        with open(file_path, 'r') as file:
            content = file.read()
            logging.info(f"Content of {file_path}:")
            logging.info(content)

def main(file_path: str):
    # Log the start of the main function
    logging.info("Starting the check for .py and .java files in: %s", file_path)

    # Check if the provided path is a directory
    if not os.path.isdir(file_path):
        logging.error("ERROR: %s is not a valid directory.", file_path)
        return
    
    # Initialize counters for found files
    num_py_files = 0
    num_java_files = 0
    src_file_name = ""

    # Iterate over files in the given directory
    for filename in os.listdir(file_path):
        if filename.endswith('.py'):
            num_py_files += 1
            src_file_name = filename
            logging.info("Found Python file: %s", filename)
        elif filename.endswith('.java'):
            num_java_files += 1
            src_file_name = filename
            logging.info("Found Java file: %s", filename)

    if num_py_files == 0 and num_java_files == 0:
        logging.error("No .py or .java files found in the directory.")
        return
    else:
        logging.info("Total Python files found: %d", num_py_files)
        logging.info("Total Java files found: %d", num_java_files)
        
    if num_java_files == 1:
        src_file_name_without_extention = src_file_name.split('.')[0]
        sonar_proj_prop_txt = SONAR_PROJECT_PROPERTIES_TEMPLATE + f"sonar.java.binaries={src_file_name_without_extention}.class"
        logging.info(sonar_proj_prop_txt)
    elif num_py_files == 1:
        sonar_proj_prop_txt = SONAR_PROJECT_PROPERTIES_TEMPLATE + f"sonar.python.version={PYTHON_VERSION}\n"
        logging.info(sonar_proj_prop_txt)
    sonar_proj_prop_txt = sonar_proj_prop_txt.format(file_path.replace('/', '_'), file_path.replace('/', '_'), src_file_name, TOKEN)
    logging.info(sonar_proj_prop_txt)
    
    dump_to_text_file(file_path=f"{file_path}/sonar-project.properties", data=sonar_proj_prop_txt)
    
if __name__ == "__main__":
    if len(sys.argv) != 2:
        logging.error("ERROR: This script requires exactly one argument.")
        sys.exit(1)
    
    # Retrieve the argument (which is the shell variable passed)
    shell_variable = sys.argv[1]
    logging.info(f"Received shell variable: {shell_variable}")
    
    main(shell_variable)
