Cellpose segmentation
=====================

This program, built upon the base template, wraps and runs the Cellpose segmentation model in a convenient way. It can run nuclei, nuclei + cytoplasm or nuclei + 2 x cytoplasm [combined] segmentation over grayscale images. 



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
  - Locate the line `config["nuclei_only"] = False` and change the value to `True` if you want to only perform the nuclei segmentation.
  - Locate the line `config["nuc_diameter"] = 80` and change the value to the average nuclei diameter (in pixels) of your images to be segmented. 
  - Locate the line `config["cyto_diameter"] = 240` and change the value to the average cell diameter (in pixels) of your images to be segmented. 

To run Cellpose segmentation you have to gather the information about the sets of images you want to process. Cellpose segmentation reads `path_list.csv` to locate each set of images, in the following .csv format: 

`nuclei_image,cyto_image1,cyto_image2,output_folder,output_prefix`

- `nuclei_image`: the nuclei targeting marker FOV image.
- `cyto_image1`: the cytoplasm targeting marker FOV image. It can be microtubuli, ER, etc... Leave it blank if you want to segment only the nuclei.
- `cyto_image2`: the cytoplasm targeting marker FOV image. It can be microtubuli, ER, etc... Leave it blank if you want to segment only the nuclei or use 1 single cytoplasm marker.
- `output_folder`: the base folder that will contain all generated segmentations.
- `output_prefix`: the prefix appended to all files generated per cell.

All images can be relative or absolute paths, or directly URLs. You can also skip cells between runs with the special character `#` in front of the desired lines. 
Check the following `path_list.csv` content as an example:

```
#nuclei_image,cyto_image,output_folder,output_prefix
input/nuc1.tif,input/mt1.tif,,output,example1_
#input/nuc2.tif,input/mt2.tif,,output,example2_
input/nuc3.tif,input/mt3.tif,,output,example3_
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

Cellpose segmentation generates in the chosen output_folder the following files:
- `[output_prefix]_nuclei_mask.png`: a labeled image with the cellpose nuclei segmentation.
- `[output_prefix]_cyto1_mask.png`: a labeled image with the cellpose cyto1 marker segmentation.
- `[output_prefix]_cyto2_mask.png`: a labeled image with the cellpose cyto2 marker segmentation.
- `[output_prefix]_cell_mask.png`: a labeled image with the final cell segmentation produced with the custom merging algorithm. (This is probably the one you want) 
- Additionally, a `crop_info.csv` file will be created containing all generated cell crops bboxes for convenience.