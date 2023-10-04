import os
import urllib.request
import zipfile
import shutil
import json
from pycocotools.coco import COCO
import numpy as np

# Load COCO annotations
coco = COCO('coco/annotations/instances_train2017.json')

# Initialize the 10-shot set and new annotations dictionary
tenshot_set = {}
new_annotations = {"images": [], "annotations": [], "categories": coco.dataset['categories']}

# Loop over all categories
for cat in coco.loadCats(coco.getCatIds()):
    cat_id = cat['id']
    cat_name = cat['name']

    # Get all annotations for this category
    ann_ids = coco.getAnnIds(catIds=cat_id)
    anns = coco.loadAnns(ann_ids)

    # Filter images to those that contain exactly one object of the current category
    missing = ['backpack', 'handbag', 'snowboard', 'sports ball', 'baseball bat', 'baseball glove', 'tennis racket', 'wine glass', 'cup', 'fork', 'spoon', 'mouse', 'toaster','book', 'hair drier']
    if cat_name in missing : 
        img_ids = [ann['image_id'] for ann in anns if len(coco.getAnnIds(imgIds=ann['image_id'])) == 1]
        bonus_ids = [ann['image_id'] for ann in anns if len(coco.getAnnIds(imgIds=ann['image_id'])) == 2][:11-len(img_ids)]
        print(f'Warning: "{cat_name}" has {len(img_ids)} images, so added {len(bonus_ids)}')
        img_ids.extend(bonus_ids)
    else:
        img_ids = [ann['image_id'] for ann in anns if len(coco.getAnnIds(imgIds=ann['image_id'])) == 1]


    # Check if there are at least 10 images
    if len(img_ids) >= 10:
        # Randomly select 10 images
        selected_img_ids = np.random.choice(img_ids, 10, replace=False)

        # Get the annotations and image info for these images
        selected_annotations = []
        for img_id in selected_img_ids:
            ann_ids = coco.getAnnIds(imgIds=img_id, catIds=cat_id)
            anns = coco.loadAnns(ann_ids)
            selected_annotations.extend(anns)
            new_annotations["annotations"].extend(anns)
            

            # Get image information and copy the image to a new folder
            img_infos = coco.loadImgs([img_id])
            if img_infos:
                img_info = img_infos[0]
                new_annotations["images"].append(img_info)
                source_img_path = os.path.join('coco/train2017', img_info['file_name'])
                target_img_path = os.path.join('coco/tenshot', img_info['file_name'])
                shutil.copyfile(source_img_path, target_img_path)
            else:
                print(f"Warning: No image information found for image ID {img_id}. This image will be skipped.")

        # Store in the 10-shot set
        tenshot_set[cat_name] = {
            "image_ids": selected_img_ids.tolist(),
            "annotations": selected_annotations,
        }
        print(f'Finished processing category "{cat_name}", number of images: {len(tenshot_set[cat_name]["image_ids"])}')
        
availabel_cats = list(tenshot_set.keys())
# cats not in availabel_cats
print([cat['name'] for cat in coco.loadCats(coco.getCatIds()) if cat['name'] not in availabel_cats])        
        
        
# Save new annotations to a JSON file
with open('coco/tenshot/annotations.json', 'w') as f:
    json.dump(new_annotations, f)

