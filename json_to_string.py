import json

def print_json_as_oneline_string(file_path):
    """
    Reads a JSON file, converts it into a compact single-line JSON string, and prints it.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Convert JSON object to a one-line JSON string
        json_str = json.dumps(data, separators=(',', ':'))

        print(json_str)
        return json_str

    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
    except json.JSONDecodeError:
        print("Error: The file is not a valid JSON.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

print_json_as_oneline_string("credentials.json")