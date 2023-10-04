#!/bin/bash

# Specify the directory containing the TXT files
TXT_DIR="annotations"

# Specify the directory containing the corresponding images
IMAGE_DIR="images"

# Loop through each TXT file in the directory
for file in "$TXT_DIR"/*_anno.txt; do
  # Extract the file name without the '_anno' suffix
  filename=$(basename "$file" _anno.txt)

  # Generate the corresponding image file name without the '_anno' suffix
  image_filename="${filename}.jpg"

  # Check if the corresponding image file exists
  echo "$IMAGE_DIR/$image_filename"
  if [ -f "$IMAGE_DIR/$image_filename" ]; then
    # Generate the new file name by removing the '_anno' suffix
    new_filename="${filename}.txt"

    # Rename the file
    mv "$file" "$new_filename"

    echo "Renamed $file to $new_filename"
  else
    # Remove the TXT file if the corresponding image file does not exist
    rm "$file"

    echo "Deleted $file (No corresponding image)"
  fi
done

