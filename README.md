Host SonarQube

```
docker run -d --name sonarqube -e SONAR_ES_BOOTSTRAP_CHECKS_DISABLE=true -p 9000:9000 sonarqube:latest
```

Setup `sonar-project.properties`

```
sonar.projectKey=my:project
sonar.projectName=My project
sonar.projectVersion=1.0
sonar.sources=Main.java
sonar.java.binaries=Main.class
sonar.sourceEncoding=UTF-8
sonar.token=sqa_0aa5afee537a0850e83e21db58acb1d119b61f1c
sonar.scm.disabled=true
```