#!/bin/bash

FILE_PATH=$1


echo "COMMAND:"
echo "docker run --rm --user 0 -v $(pwd)/cache:/opt/sonar-scanner/.sonar/cache -v $(pwd)/$FILE_PATH:/usr/src -e SONAR_HOST_URL="http://localhost:9000" -v $(pwd)/$FILE_PATH/scannerwork:/tmp/.scannerwork --network=host sonarsource/sonar-scanner-cli"
echo 

docker run \
    --rm \
    --user 0 \
    -v $(pwd)/cache:/opt/sonar-scanner/.sonar/cache \
    -v $(pwd)/$FILE_PATH:/usr/src \
    -e SONAR_HOST_URL="http://localhost:9000" \
    -v $(pwd)/$FILE_PATH/scannerwork:/tmp/.scannerwork \
    --network=host \
    sonarsource/sonar-scanner-cli

echo "FINISHED RUNNING"
