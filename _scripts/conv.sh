#!/bin/bash

# Specify the directory containing the BMP images
IMAGE_DIR="images"

# Loop through each BMP file in the directory
for file in "$IMAGE_DIR"/*.bmp; do
  # Extract the file name without the extension
  filename=$(basename "$file" .bmp)

  # Convert BMP to JPG using ImageMagick's `convert` command
  convert "$file" "$IMAGE_DIR/$filename.jpg"

  # Optional: Remove the original BMP file
  # Uncomment the line below to delete the BMP file after conversion
  rm "$file"

  echo "Converted $filename.bmp to $filename.jpg"
done

