import argparse
import yaml
import os

def add_newlines_to_strings(data, max_line_length=200):
    if isinstance(data, dict):
        for key, value in data.items():
            data[key] = add_newlines_to_strings(value, max_line_length)
    elif isinstance(data, list):
        for i, item in enumerate(data):
            data[i] = add_newlines_to_strings(item, max_line_length)
    elif isinstance(data, str):
        # Replace '\\n' with a space and '\n' with a space
        data = data.replace('\\n', ' ').replace('\n', ' ')

        # Split the string into words and format with newlines
        words = data.split()
        lines = []
        current_line = []  # Store lines as a list

        for word in words:
            if len(' '.join(current_line + [word])) <= max_line_length:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]

        if current_line:
            lines.append(' '.join(current_line))

        return '\\n'.join(lines)
    return data

def main():
    parser = argparse.ArgumentParser(description="Process a YAML file and add newlines to string values.")
    parser.add_argument("input_file", help="Path to the input YAML file.")
    parser.add_argument("-o", "--output_file", help="Path to the output YAML file (default is the input file).")
    args = parser.parse_args()

    # Determine the output file path
    if args.output_file:
        output_file_path = args.output_file
    else:
        # Use the input file path with "_modified" added before the file extension
        base_path, ext = os.path.splitext(args.input_file)
        output_file_path = base_path + ext

    # Load the YAML data from the input file
    with open(args.input_file, 'r') as file:
        yaml_data = yaml.safe_load(file)

    # Add newlines to strings as per your requirements
    modified_yaml_data = add_newlines_to_strings(yaml_data)

    # Save the modified data to the output file
    with open(output_file_path, 'w') as file:
        yaml.dump(modified_yaml_data, file)  # Removed the width argument

if __name__ == "__main__":
    main()
