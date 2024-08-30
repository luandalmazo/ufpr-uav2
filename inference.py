from pathlib import Path
from glob import glob
import SimpleITK as sitk
import os 
import subprocess
import random 

def run():
    INPUT_PATH = Path("/input")
    OUTPUT_PATH = Path("/output")
    
    ''' dict with original uid and new uid so we can track the images'''
    uid = {}
    
    ''' reads the image'''
    input_dir = f"{INPUT_PATH}/images/preprocessed-CT-angiography"
    output_dir = f"{OUTPUT_PATH}/images/stroke-lesion-segmentation"

    ''' find the model zip'''
    zip_dir = "./best-901.zip"
    
    predict_infarct(input_dir, output_dir, zip_dir, uid)

    return 0

def install_pretrained_model(zip_file_path):
    """
    Installs a pretrained nnU-Net model from a ZIP file.

    Args:
        zip_file_path (str): The path to the ZIP file containing the pretrained model.
    """
    command = ['nnUNetv2_install_pretrained_model_from_zip', zip_file_path]

    try:
        subprocess.run(command, check=True)
        print("Pretrained model installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred during installation: {e}")

def convert_nifti_to_mha(NIFTI_DIR, uid_mapping):
    """
    Converts an NIfTI file to MHA format.

    Args:
        NIFTI_DIR (str): Path to the .nii file.

    """

    # Get all .nii files in the directory
    nii_files = [f for f in os.listdir(NIFTI_DIR) if f.endswith('.nii.gz')]

    for nii_file in nii_files:
        image = sitk.ReadImage(f"{NIFTI_DIR}/{nii_file}")
        OUTPUT_DIR = NIFTI_DIR

        # Create the output filename traking the original uid
        mha_filename = os.path.join(OUTPUT_DIR, f"{uid_mapping[int(nii_file.split('.')[0])]}.mha")
        
        # Write the image as NIfTI
        sitk.WriteImage(image, mha_filename)

        # Print the filename of the converted file
        print(f"Converted {nii_file} to {mha_filename}")

    print(f"Converted.")

def predict_infarct(DIR, OUTPUT_DIR, ZIP_DIR, uid):
        
    """
    Args:
        DIR (str): The directory containing the input data.
        OUTPUT_DIR (str): The directory that will contain the prediction
        ZIP_DIR (str)> The directory where is the best model
    """


    """
    Before we need to install the model if it is not already installed.
    """

    install_pretrained_model(ZIP_DIR)

    """
    Now, we need to convert all mha images to nifti
    """

    # Get only the mha ids 
    original_files = [f for f in os.listdir(DIR) if f.endswith('.mha')]
    uid_mapping = {}    
    
    NEW_DIR = "/opt/app/"

    # Get all .mha files in the directory
    for mha_file in original_files:
        image = sitk.ReadImage(f"{DIR}/{mha_file}")

        # Create the output filename
        random_id = random.randint(7000, 9000)
        uid_mapping[random_id] = mha_file.split('.')[0]
        nifti_filename = os.path.join(NEW_DIR, f"{random_id}_0000.nii.gz")
        
        sitk.WriteImage(image, nifti_filename)

    print(f"Converted.")

    # Construct the nnUNetv2_predict command
    command = [
        'nnUNetv2_predict',
        '-i', NEW_DIR ,    # Input directory
        '-o', '/output/images/stroke-lesion-segmentation', # Output directory
        '-d', '901',         # Dataset ID
        '-c', '3d_lowres',  # Configuration 
        '--disable_progress_bar',
        '--disable_tta',
        '-num_parts', '2',
        '-part_id', '0'
    ]

    # Run the command
    try:
        subprocess.run(command, check=True)
        print("Prediction completed successfully.")

        # Now we need to run the second part of the prediction
        command = [
            'nnUNetv2_predict',
            '-i', NEW_DIR ,    # Input directory
            '-o', '/output/images/stroke-lesion-segmentation', # Output directory
            '-d', '901',         # Dataset ID
            '-c', '3d_lowres',  # Configuration 
            '--disable_progress_bar',
            '--disable_tta',
            '-num_parts', '2 ',
            '-part_id', '1'
        ]
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred during prediction: {e}")

    ''' convert the output to mha (nii.gz > mha)'''
    convert_nifti_to_mha(OUTPUT_DIR, uid_mapping)

if __name__ == "__main__":
    raise SystemExit(run())

