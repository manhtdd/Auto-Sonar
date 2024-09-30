#!/bin/bash

docker run \
    --rm \
    --user 0 \
    -v $(pwd)/cache:/opt/sonar-scanner/.sonar/cache \
    -v $(pwd)/input/test-java-one-file:/usr/src \
    sonarsource/sonar-scanner-cli \
    -X
