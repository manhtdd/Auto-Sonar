# Auto Sonar

Auto Sonar is a simple Python wrapper for running SonarQube scans on your code. This package enables you to easily scan your projects for security vulnerabilities, code smells, and more using SonarQube.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Setup SonarQube & SonarScanner](#setup-sonarqube--sonarscanner)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Prerequisites

Before you start, ensure you have Docker installed on your system. You'll also need Python 3.12+ and `pip` for installing the package.

### Docker Installation
To install Docker, follow the instructions for your operating system [here](https://docs.docker.com/get-docker/).

## Setup SonarQube & SonarScanner

1. Pull the latest SonarQube and SonarScanner CLI Docker images:
   ```bash
   docker pull sonarqube:latest
   docker pull sonarsource/sonar-scanner-cli:latest
   ```

2. Verify the images have been successfully pulled:
   ```bash
   docker images
   ```

   If successful, you should see the following output:
   ```bash
   sonarsource/sonar-scanner-cli   latest          5eb01c509ae7   8 days ago     887MB
   sonarqube                       latest          2433ac783140   2 months ago   1.07GB
   ```

3. Start the SonarQube container (optional if it's not running already):
   ```bash
   docker run -d --name sonarqube -e SONAR_ES_BOOTSTRAP_CHECKS_DISABLE=true -p 9000:9000 sonarqube:latest
   ```

4. You can access the SonarQube dashboard at `http://localhost:9000`.

5. Get your SonarQube Token
   - Visit SonarQube dashboard at `http://localhost:9000`
   - You can generate new tokens at `User` > `My Account` > `Security`
   - Token type: `User Token`
   - Hit `Generate` button

## Installation
Clone this repository:
```
git clone https://github.com/manhtdd/Auto-Sonar.git auto_sonar
cd auto_sonar
```

To install the `auto_sonar` package, run:

```bash
pip install -e .
```

After installation, you should be able to import the package:

```bash
$ python
Python 3.12.2 | packaged by conda-forge | (main, Feb 16 2024, 20:50:58) [GCC 12.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import auto_sonar
>>>
```

## Usage

Here’s an example of how to use `auto_sonar` to scan a Python file:

```python
from auto_sonar import run_sonar
import json

codepath = "input/test_sonar_security/VulnerableApp.java" # Path to the code to be analyzed
savepath = "input/test_sonar_security/VulnerableApp.json" # Path where the analysis results will be saved
sonar_url_host = "http://localhost:9000"
token = "YOUR_TOKEN"
# Run SonarQube analysis
output = run_sonar(sonar_url_host, token, codepath, savepath)

# Print the output in a readable JSON format
print(json.dumps(output, indent=4))
```

### Arguments:
- `codepath`: Path to the file or directory you want to analyze.
- `savepath`: Path where the scan results will be saved (SARIF format).

### IMPORTANT:
- It is recommended to put the file (e.g. `VulnerableApp.Java`) inside a folder (e.g. `test_sonar_security`) since SonarQube's temp files will be generated inside this folder (e.g. `test_sonar_security`)