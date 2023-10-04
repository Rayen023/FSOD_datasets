

# Specify the prefix of the files to copy
prefix=${1}


# Copy the first 10 files from the image and labels directory that start with the prefix
for file in $(ls images/train/${prefix}* | head -10); do cp "${file}" extras/; done
for file in $(ls labels/train/${prefix}* | head -10); do cp "${file}" extras/; done
