#!/bin/bash

FILE_PATH=$1

# Check if the provided argument is a directory
if [ ! -d "$FILE_PATH" ]; then
    echo "ERROR: $FILE_PATH is not a valid directory."
    exit 1
fi

# Check for .java or .py files in the directory
num_java_files=$(find "$FILE_PATH" -maxdepth 1 -type f -name "*.java" | wc -l)
num_py_files=$(find "$FILE_PATH" -maxdepth 1 -type f -name "*.py" | wc -l)
total_files=$((num_java_files + num_py_files))

if [ "$total_files" -ne 1 ]; then
    echo "ERROR: There must be exactly one .java or .py file in the directory. Found $total_files."
    exit 1
fi

# If there is a .java file, check for a corresponding .class file
if [ "$num_java_files" -eq 1 ]; then
    java_file=$(find "$FILE_PATH" -maxdepth 1 -type f -name "*.java")
    class_file="${java_file%.java}.class"
    
    if [ ! -f "$class_file" ]; then
        echo "Corresponding .class file for $java_file not found."
        echo "TRY TO RUN BUILD..."
        echo "javac $java_file"
        javac $java_file
        if [ ! -f "$class_file" ]; then
            echo "ERROR: javac failed. Please check if you have JDK installed."
            exit 1
        fi
        echo "BUILD SUCCESS"
        echo
    fi
fi

echo "COMMAND:"
echo "docker run --rm --user 0 -v $(pwd)/cache:/opt/sonar-scanner/.sonar/cache -v $(pwd)/$FILE_PATH:/usr/src -e SONAR_HOST_URL="http://localhost:9000" -v $(pwd)/$FILE_PATH/scannerwork:/tmp/.scannerwork --network=host sonarsource/sonar-scanner-cli"
echo 

docker run \
    --rm \
    --user 0 \
    -v $(pwd)/sonar-cache:/opt/sonar-scanner/.sonar/cache \
    -v $(pwd)/$FILE_PATH:/usr/src \
    -e SONAR_HOST_URL="http://localhost:9000" \
    -v $(pwd)/$FILE_PATH/scannerwork:/tmp/.scannerwork \
    --network=host \
    sonarsource/sonar-scanner-cli

echo "FINISHED RUNNING"
