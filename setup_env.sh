#!/bin/bash

ENV_NAME="image_tool_env"
YML_FILE="environment.yml"

# Function to list packages in the environment
function list_packages() {
    echo "Installed packages in environment '${ENV_NAME}':"
    conda list -n $ENV_NAME
}

# Check if the environment already exists
if conda env list | grep -q "^${ENV_NAME}[[:space:]]"; then
    echo "Environment '${ENV_NAME}' already exists. Updating dependencies..."
    conda env update -n $ENV_NAME -f $YML_FILE --prune
    echo "Environment '${ENV_NAME}' has been updated."
    list_packages
else
    echo "Creating environment '${ENV_NAME}'..."
    conda env create -f $YML_FILE
    echo "Environment '${ENV_NAME}' has been created."
    list_packages
fi
