import os
import random

image_dir_path = 'images/validation'  # replace with your image directory path
label_dir_path = 'labels/validation'  # replace with your label directory path

background_images = []

for filename in os.listdir(image_dir_path):
    if filename.endswith('.jpg'):  # replace with your image file extension if it's not .jpg
        # Construct the corresponding label filename
        label_filename = filename.rsplit('.', 1)[0] + '.txt'
        label_file_path = os.path.join(label_dir_path, label_filename)

        # If the corresponding label file is empty, add it to the list of background images
        if os.path.getsize(label_file_path) == 0:
            background_images.append((os.path.join(image_dir_path, filename), label_file_path))

# Compute how many images to remove
num_to_remove = int(len(background_images) * 0.8)

# Randomly select images to remove
images_to_remove = random.sample(background_images, num_to_remove)

# Remove selected images and corresponding labels
for image_path, label_path in images_to_remove:
    os.remove(image_path)
    os.remove(label_path)
