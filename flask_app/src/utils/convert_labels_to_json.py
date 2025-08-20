import os
import json


def create_labels_list():
    """
    Creates a list of labels from classes.txt file and returns it
    """
    labels_list = []

    if not os.path.exists("data/classes.txt"):
        raise FileNotFoundError("Unable to create labels list, file classes.txt not found. Please make sure it exists in the data folder.")
    
    with open("data/classes.txt", "r") as f:
        lines = f.readlines()
        for line in lines:
            labels_list.append(line.strip())

    return labels_list




def create_hotspots(labelPath, labels_list):
    hotspots = []
    with open(labelPath, "r") as f:
        lines = f.readlines()
        for line in lines:
            class_id = line.split(" ")[0]
            x_center = line.split(" ")[1]
            y_center = line.split(" ")[2]

            hotspot = {
                'id': labels_list[int(class_id)].split("h")[1],
                'label': labels_list[int(class_id)].split("h")[1],
                'position': {
                    'x': x_center,
                    'y': y_center
                },
                'parts': []
            }

            hotspots.append(hotspot)

    return hotspots


def write_json_file(image_obj):
    file_path = os.path.join("data/json_data", image_obj['diagram_id'] + ".json")
    with open(file_path, "w") as f:
        json.dump(image_obj, f, indent=4)




def main():
    labels_list = create_labels_list()

    # Fetch images paths from data/test-images folder
    images = os.listdir("data/test-images")
    if len(images) == 0:
        raise FileNotFoundError("Unable to create json, no images found in data/test-images folder. Please make sure it exists and contains images.")


    # Create hotspots json object
    for img in images:
        label = img.split(".")[0] + ".txt"
        labelPath = os.path.join("data/labels", label)

        image_obj = {
            'diagram_id': img.split(".")[0],
            'image_filename': img,
            'make': 'ferrari',
        }

        hotspots = create_hotspots(labelPath, labels_list)
        image_obj['hotspots'] = hotspots

        write_json_file(image_obj)



if __name__ == "__main__":
    main()




