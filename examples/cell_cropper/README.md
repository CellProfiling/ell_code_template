Cell cropper
============

This program, built upon the base template, will generate the cell crops from previously segmented HPA-style images. The code it's embedded in HPACellSegmentator, but this version can help you crop the images later on and/or other kind of similar image types. 



Requirements
------------

Please read the overall `README.md` file to understand the structure principles of this code. 



Installation
------------

- Install the code following the steps indicated in the overall `README.md` file, just remember to use all the contents of this directory as you working code.



Setup
-----

The code expects you to perform certain steps to run with your data:

- Edit and modify `process.py` file:
  - Locate the line `config["gray"] = True` and change the value to `False` if your markers are in RGB for any reason. 
  - Locate the line `config["crop_size"] = 1024` and change the value to your desired crop size. 
  - Locate the line `config["mask_cell"] = False` and change the value to `True` if you want to additionally generate all the cell crops masked by the cells boundaries.

To run HPA cell cropper you have to gather the information about the sets of images you want to process. HPA cell cropper reads `path_list.csv` to locate each set of images, in the following .csv format: 

`r_image,y_image,b_image,g_image,segmentation_mask,crop_folder,output_prefix`

- `r_image`: the microtubules targeting marker FOV image. 
- `y_image`: the ER targeting marker FOV image.
- `b_image`: the nuclei targeting marker FOV image.
- `g_image`: the protein targeting marker FOV image (only needed if you want to generate the cell crops).
- `segmentation_mask`: the cell segmentation mask previously obtained (if you used HPACellSegmentator, this will be something like `[output_prefix]_cellmask.png`).
- `crop_folder`: the base folder that will contain all generated crops.
- `output_prefix`: the prefix appended to all files generated per cell.

All images can be relative or absolute paths, or directly URLs. You can also skip cells between runs with the special character `#` in front of the desired lines. 
Check the following `path_list.csv` content as an example:

```
#r_image,y_image,b_image,g_image,segmentation_mask,crop_folder,output_prefix
images/CACO-2_2047_C3_6_red.png,images/CACO-2_2047_C3_6_yellow.png,images/CACO-2_2047_C3_6_blue.png,images/CACO-2_2047_C3_6_green.png,segmentation/CACO-2_2047_C3_6_cellmask.png,output,CACO-2_2047_C3_6_
#images/CACO-2_2047_C3_7_red.png,images/CACO-2_2047_C3_7_yellow.png,images/CACO-2_2047_C3_7_blue.png,images/CACO-2_2047_C3_7_green.png,segmentation/CACO-2_2047_C3_7_cellmask.png,output,CACO-2_2047_C3_7_
images/U-215MG792_H7_2_red.png,images/U-215MG792_H7_2_yellow.png,images/U-215MG792_H7_2_blue.png,images/U-215MG792_H7_2_green.png,segmentation/U-215MG792_H7_2_cellmask.png,output,U-215MG792_H7_2_
```
  


Running the code
---------------- 

**NOTE**: remember that you have to access your created virtual environment before running the code! To do so, navigate to the directory you created and activate it.
 - Example:
   - `cd /home/lab/sandbox/example`
   - `source bin/activate`

Once you have activated your virtual environment and modified all the desired parameters (see section **Setup**, just run the code with `python process.py`. OBS: you have to run the `process.py` file, which will on its turn call the rest of the code.



Output
------ 

Cell cropper generates in the chosen crop_folder the following files:
- `[output_prefix]_cell[X]_crop_[red|yellow|blue|green].png`: a cropped cell from the FOV.
- `[output_prefix]_cell[X]_crop_masked_[red|yellow|blue|green].png`: a cropped and masked cell from the FOV (if the mask_cell option was selected).
- Additionally, a `crop_info.csv` file will be created containing all generated cell crops bboxes for convenience.