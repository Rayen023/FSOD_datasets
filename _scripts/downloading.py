import os
import urllib.request
import zipfile
from pycocotools.coco import COCO
import numpy as np

# Download COCO 2017 dataset
os.makedirs('coco', exist_ok=True)
url_train = 'http://images.cocodataset.org/zips/train2017.zip'
url_val = 'http://images.cocodataset.org/zips/val2017.zip'
url_annotation = 'http://images.cocodataset.org/annotations/annotations_trainval2017.zip'

urllib.request.urlretrieve(url_train, 'coco/train2017.zip')
urllib.request.urlretrieve(url_val, 'coco/val2017.zip')
urllib.request.urlretrieve(url_annotation, 'coco/annotations.zip')

# Unzip the dataset
with zipfile.ZipFile('coco/train2017.zip', 'r') as zip_ref:
    zip_ref.extractall('coco/')
with zipfile.ZipFile('coco/val2017.zip', 'r') as zip_ref:
    zip_ref.extractall('coco/')
with zipfile.ZipFile('coco/annotations.zip', 'r') as zip_ref:
    zip_ref.extractall('coco/')

# Load COCO annotations
coco = COCO('coco/annotations/instances_train2017.json')

# Initialize the 10-shot set
tenshot_set = {}

# Loop over all categories
for cat in coco.loadCats(coco.getCatIds()):
    cat_id = cat['id']
    cat_name = cat['name']

    # Get all image ids for this category
    img_ids = coco.getImgIds(catIds=cat_id)
    
    # Check if there are at least 10 images
    if len(img_ids) >= 10:
        # Randomly select 10 images
        selected_img_ids = np.random.choice(img_ids, 10, replace=False)
        
        # Get the annotations for these images
        annotations = [coco.loadAnns(coco.getAnnIds(imgIds=img_id, catIds=cat_id)) for img_id in selected_img_ids]
        
        # Store in the 10-shot set
        tenshot_set[cat_name] = {
            "image_ids": selected_img_ids.tolist(),
            "annotations": annotations,
        }

# Print the 10-shot set
print(tenshot_set)
