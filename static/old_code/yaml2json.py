import os
import json
import yaml

def convert_yaml_to_json(yaml_path):
    # Load YAML content
    with open(yaml_path, 'r') as yaml_file:
        yaml_data = yaml.safe_load(yaml_file)

    # Extract the file name without extension from the yaml_path
    file_name = os.path.splitext(os.path.basename(yaml_path))[0]

    # Create the JSON file path by adding the .json extension
    json_path = os.path.join(os.path.dirname(yaml_path), f"{file_name}.json")

    # Save JSON content
    with open(json_path, 'w') as json_file:
        json.dump(yaml_data, json_file, indent=4)
    return json_path

def convert_yaml_files_to_json(directory):
    # Get the absolute path of the specified directory
    directory = os.path.abspath(directory)

    # Iterate through files in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".yaml"):
            yaml_path = os.path.join(directory, filename)
            json_path = convert_yaml_to_json(yaml_path)
            print(f"Converted {yaml_path} to {json_path}")

if __name__ == "__main__":
    # Specify the absolute path of the directory containing the .yaml files
    target_directory = os.path.abspath("./data")

    # Call the function to convert YAML files to JSON
    convert_yaml_files_to_json(target_directory)
