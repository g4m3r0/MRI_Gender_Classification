import nibabel as nib
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import glob
import os

# Define your input and output directories.
input_dir = "E:\\MRI_Dataset\\ds003592-download\\**\\*T1w.nii.gz"
output_dir = "E:\\MRI_Dataset\\T1w_MRI_Brain_Slices\\images\\"

# Get a list of all .nii.gz files in the input directory.
nifti_files = glob.glob(input_dir, recursive=True)

# Loop through all .nii.gz files.
for nifti_file in nifti_files:

    # Get the subject identifier from the file name.
    # This assumes file names are in the format 'sub-01_ses-1_T1w.nii.gz'.
    identifier = os.path.basename(nifti_file).split('_')[0] # e.g. sub-01
    subject_number = identifier.split('-')[1] # e.g. 01

    # Load the .nii.gz file.
    img = nib.load(nifti_file)

    # Image orientation differs e.g. due to use of different scanners so we need to reorient the image
    img = nib.as_closest_canonical(img)

    # Get the image data array.
    data = img.get_fdata()
    #data = nib.as_closest_canonical(img)

    # Loop through all slices along a specified axis.
    # Here we use axis=2, which corresponds to coronal slices.
    slice_axis = 2
    for i in range(data.shape[slice_axis]):
        # Get a slice at the ith position along the specified axis.
        slice = data.take(i, axis=slice_axis)

        # Normalize the slice to 0-255
        slice = ((slice - slice.min()) / (slice.max() - slice.min()) * 255.9).astype(np.uint8)

        # Create an image from the slice.
        image = Image.fromarray(slice)

        # Skip some images
        if i < 140 or i > 200:
            continue

        # Only take every other image
        if i % 2 == 0:
            continue

        # Define the output path for the slice image.
        output_path = os.path.join(output_dir, f"{identifier}_slice_{i}.png")

        # Save the slice as an image.
        plt.imsave(output_path, slice, cmap='gray')