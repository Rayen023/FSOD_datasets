from globox import AnnotationSet

import os
import json


file_path = "images/train/instances_train2017.json"

coco_ans = AnnotationSet.from_coco(file_path=file_path)

coco_ans.show_stats()


id_to_label = {
    #0: 'pitted_surface',
    0: 'rolled-in_scale',
    1: 'scratches',
    #1: 'crazing',
    2: 'inclusion',
    #2: 'patches'
    }

label_to_id = {v: k for k, v in id_to_label.items()}

#save the mapping dictionary
with open("labels.json", "w") as f:
    json.dump(label_to_id, f, indent=4)

#load the mapping dictionary
with open("labels.json", "r") as f:
    label_to_id = json.load(f)

print(type(label_to_id))
print(label_to_id)

# YOLOv5
coco_ans.save_yolo_v5(
    save_dir="labels/train/", 
    label_to_id=label_to_id,
)


