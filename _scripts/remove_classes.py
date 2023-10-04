import os

dir_path = "/gpfs/scratch/rayen/YOLOv8/datasets/pt-fs-surface/labels/validation/" # path to the directory containing your files

# Define a mapping dictionary
mapping = {'1': '0', '2': '1', '4': '2'}

for filename in os.listdir(dir_path):
    if filename.endswith('.txt'):  # assuming your annotation files are text files
        file_path = os.path.join(dir_path, filename)

        # Read the file into memory
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Filter out the lines that start with '0', '3', or '5'
        modified_lines = [line for line in lines if not line.startswith(('0', '3', '5'))]

        # Apply the mapping
        modified_lines = [mapping.get(line[0], line[0]) + line[1:] if line else line for line in modified_lines]

        # Write the modified data back to the file
        with open(file_path, 'w') as file:
            file.writelines(modified_lines)
