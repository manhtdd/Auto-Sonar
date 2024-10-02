1. Setup SonarQube & SonarScanner
```
docker pull sonarqube:latest
docker pull sonarsource/sonar-scanner-cli:latest
```
If successfull:
```
sonarsource/sonar-scanner-cli   latest          5eb01c509ae7   8 days ago     887MB
sonarqube                       latest          2433ac783140   2 months ago   1.07GB
```

2. Install `auto_sonar`
```
pip install -e .
```

You should be able to `import auto_sonar` now
```
$ python
Python 3.12.2 | packaged by conda-forge | (main, Feb 16 2024, 20:50:58) [GCC 12.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import auto_sonar
>>> 
```

3. Usage
An example code:
```
from auto_sonar import run_sonar

codepath = "input/test.py"
savepath = "input/test.sarif"
output = run_sonar(codepath, savepath)
print(json.dumps(output, indent=4))
```