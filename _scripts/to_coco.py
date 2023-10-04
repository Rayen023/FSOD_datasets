from globox import AnnotationSet
import os
import json

with open("to_remove","r") as f:
    lines = f.readlines()
    
for line in lines:
    line = line.strip()
    txt_file_path = line
    image_file_path = line.replace("labels","images").replace("txt","jpg")
    
    if os.path.exists(txt_file_path):
        os.remove(txt_file_path)
    
    if os.path.exists(image_file_path):
        os.remove(image_file_path)


yolo = AnnotationSet.from_yolo_v5(
    folder="/gpfs/scratch/rayen/YOLOv8/datasets/wood/labels/val/",
    image_folder="/gpfs/scratch/rayen/YOLOv8/datasets/wood/images/val/"
)


yolo.show_stats()

yolo.save_coco("labels.json", auto_ids = True)

data = json.load(open("labels.json"))

map_categories = {
    'knot_with_crack': 0,
    'Live_Knot' : 1,
    'Dead_Knot' : 2,
    'Crack' : 3
    }

#invert the map
map_categories = {v: k for k, v in map_categories.items()}

for cat in data["categories"]:
    print(cat['name'])
    print(map_categories[0])
    cat['name'] = map_categories[int(cat['name'])]

with open("labels.json", "w") as f:
    json.dump(data, f, indent=4)
    
data = json.load(open("labels.json"))

print(data["categories"])