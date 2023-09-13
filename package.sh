#!/bin/bash

# Define source directories and files
app_directory="./app"
data_directory="./data"
deploy_directory="./dist"
stranded_file="stranded.py"
stranded_shell_file="stranded.sh"
archive_name="stranded.tar"

# Ensure the deploy directory exists
mkdir -p "$deploy_directory/app"
mkdir -p "$deploy_directory/data"

# Copy files from ./app directory
cp -r "$app_directory"/* "$deploy_directory/app"

# Copy .txt and .json files from ./data directory
cp -r "$data_directory"/*.txt "$deploy_directory/data"
cp -r "$data_directory"/*.json "$deploy_directory/data"

# Copy stranded.py and stranded.sh from the current directory
cp "$stranded_file" "$deploy_directory"
cp "$stranded_shell_file" "$deploy_directory"

# Create a tar archive
tar -cf "$archive_name" "$deploy_directory"

echo "Created $archive_name archive containing the deploy directory"
