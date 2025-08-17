import os
import json
import csv

HOTSPOTS_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'json_data')
DATA_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

json_files = os.listdir(HOTSPOTS_FOLDER)
json_files_names = [file.split('.')[0] for file in json_files]

# read csv file
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'parts_data.csv'), 'r') as file:
    reader = csv.DictReader(file)
    parts = [row for row in reader]

# update parts for each file
for file_name in json_files:
    with open(os.path.join(HOTSPOTS_FOLDER, file_name), 'r') as file:
        data = json.load(file)
        # get all linked parts of the hotspot from csv
        for hotspot in data['hotspots']:
            for part in parts:
                if part['Diagram ID'] == file_name.split('.')[0] and part['Key (Hotspot Number)'] == hotspot['id']:
                    hotspot['parts'].append(part["Part Number"])

        # write to file
        with open(os.path.join(DATA_FOLDER, file_name), 'w') as file:
            json.dump(data, file, indent=4)

        print(f"Updated {file_name}")

