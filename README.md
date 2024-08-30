# Ischemic Stroke Lesion Segmentation [ufpr-uav2]

This repository contains the necessary steps to run the "ufpr-uav2" algorithm. This code was submitted to the ISLES'24 [challenge](https://isles-24.grand-challenge.org).

## Instructions

1. **Clone this repository.**

2. **Install nnU-Netv2.**
  Install the framework using these [guidelines](https://github.com/MIC-DKFZ/nnUNet/blob/master/documentation/installation_instructions.md), following step 2.ii.

3. **Download our model.**
  [Here](https://drive.google.com/file/d/1L72vfeI8wDWkbs33dle_OlasBHE__ZcG/view?usp=sharing).
  
4. **This structure is required for the algorithm to function:** 

    ```plaintext
    isles24-docker-template/
    ├── nnUNet/
    ├── test/
    │   ├── input/
    │   │   ├── images/
    │   │   │   ├── preprocessed-CT-angiography/
    │   │   │   │   └── xxx.mha
    │   └── output/  # This will be created by OUR script
    └── (... other files ...)
    ```

4. **Test the algorithm** 
  Run `./test_run.sh`. This script will predict the images located in `test/input/images/preprocessed-CT-angiography`, saving the results in `test/output/`.
