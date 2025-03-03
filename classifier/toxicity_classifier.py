import ../files
import json

def main():
    json_files = files.JSON_FILES

    for i in range(len(json_files)):
        file_name = json_files[i]['file_name']

        with open(file_name, 'r') as f:
            file = json.load(f)
