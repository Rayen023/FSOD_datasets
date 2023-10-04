import cv2
import albumentations as A
import os
import glob


image_dir = "/gpfs/scratch/rayen/YOLOv8/datasets/metatrain/images/train/"
annotation_dir = "/gpfs/scratch/rayen/YOLOv8/datasets/metatrain/labels/train/"

image_paths = sorted(glob.glob(os.path.join(image_dir, "*.jpg")))
annotation_paths = sorted(glob.glob(os.path.join(annotation_dir, "*.txt")))


transform = A.Compose([

    A.Rotate(limit=90, p=1.0), 
    A.CLAHE(p=1.0),  
    A.RandomBrightnessContrast(p=0.5),
    A.GaussNoise(var_limit=(10.0, 50.0), p=0.5),
    A.ShiftScaleRotate(shift_limit_y=0.1, scale_limit=0, rotate_limit=0, p=1.0)  # Shifting the image vertically
], bbox_params=A.BboxParams(format='yolo', label_fields=['class_labels']))

# Loop over the images and their corresponding annotations
for image_path, annotation_path in zip(image_paths, annotation_paths):
    # Read the image
    print(image_path)
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    print(annotation_path)
    # The annotation is a list of bounding boxes in the form [class, x_center, y_center, width, height]
    # where the values are normalized between 0 and 1
    with open(annotation_path, 'r') as file:
        annotations = file.read().splitlines()
        
    bboxes = []
    class_labels = []
    for ann in annotations:
        ann = ann.split(' ')
        bboxes.append(list(map(float, ann[1:])))
        class_labels.append(ann[0])
        print(bboxes)
        
    # Apply the transformation
    transformed = transform(image=image, bboxes=bboxes, class_labels=class_labels)
    transformed_image = transformed['image']
    transformed_bboxes = transformed['bboxes']
    
    extras_dir = 'extras'
    if not os.path.exists(extras_dir):
        os.makedirs(extras_dir)

    
    # Save the transformed image
    cv2.imwrite(os.path.join(extras_dir, f'transformed_{os.path.basename(image_path)}'), cv2.cvtColor(transformed_image, cv2.COLOR_RGB2BGR))
    
    # Save the transformed annotation
    with open(os.path.join(extras_dir, f'transformed_{os.path.splitext(os.path.basename(image_path))[0]}.txt'), 'w') as f:
        for bbox, label in zip(transformed_bboxes, transformed['class_labels']):
            f.write(f'{label} {" ".join(map(str, bbox))}\n')
            
    """# Loop over the transformed bounding boxes
    for bbox, label in zip(transformed_bboxes, transformed['class_labels']):
        # Convert bounding box from normalized YOLO format (center_x, center_y, width, height) to OpenCV format (x_min, y_min, x_max, y_max)
        x_min = int((bbox[0] - bbox[2] / 2) * transformed_image.shape[1])
        y_min = int((bbox[1] - bbox[3] / 2) * transformed_image.shape[0])
        x_max = int((bbox[0] + bbox[2] / 2) * transformed_image.shape[1])
        y_max = int((bbox[1] + bbox[3] / 2) * transformed_image.shape[0])
        
        # Draw the bounding box
        cv2.rectangle(transformed_image, (x_min, y_min), (x_max, y_max), (255, 0, 0), 2)
        
        # Draw the label
        cv2.putText(transformed_image, str(label), (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
        
    # Display the image
    cv2.imshow('Transformed image', cv2.cvtColor(transformed_image, cv2.COLOR_RGB2BGR))
    cv2.waitKey(0)
    cv2.destroyAllWindows()"""

