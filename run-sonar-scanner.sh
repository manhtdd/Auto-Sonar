#!/bin/bash

docker run \
    --rm \
    --user 0 \
    -v $(pwd)/cache:/opt/sonar-scanner/.sonar/cache \
    -v $(pwd)/input/test-java-one-file:/usr/src \
    -e SONAR_HOST_URL="http://localhost:9000" \
    -v $(pwd)/scannerwork:/tmp/.scannerwork \
    --network=host \
    sonarsource/sonar-scanner-cli
