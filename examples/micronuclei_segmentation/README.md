Micronuclei segmentation
========================

This program, built upon the base template, will generate micronuclei segmentations over previously segmented (nuclei and cell) HPA-style nuclei images.  



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
  - Locate the line `config["nuclei_min_diameter"] = 100` and change the value of your minimum allowed nuclei diameter pixel size. 
  - Locate the line `config["micro_nuclei_min_diameter"] = 5` and change the value of your minimum allowed micronuclei diameter pixel size. 
  - Locate the line `config["micro_nuclei_max_diameter"] = 50` and change the value of your maximum allowed micronuclei diameter pixel size. 
  - Locate the line `config["eccentricity_tolerance"] = 0.9` and change the value of your maximum allowed eccentricity shape of the micronuclei (0 - circle, 1 - flattened ellipse). 
  - Locate the line `config["solidity_tolerance"] = 0.1` and change the value of your minimum allowed solidity shape of the micronuclei (0 - totally fragmented, 1 - totally convex hull shape). 
  - Locate the line `config["intensity_ratio_tolerance"] = 0.2` and change the value of your maximum allowed variance between the micronuclei average intensity and it's related nuclei average intensity (0 - no variance, 1 totally different)

To run micronuclei segmentation you have to gather the information about the sets of images you want to process. Micronuclei segmentation reads `path_list.csv` to locate each set of images, in the following .csv format: 

`nuclei_image,nuclei_segmentation,cytoplasm_segmentation,output_folder,output_prefix`

- `nuclei_image`: the nuclei targeting marker FOV image.
- `nuclei_segmentation`: the nuclei segmentation mask previously obtained (if you used HPACellSegmentator, this will be something like `[output_prefix]_nucleimask.png`).
- `cytoplasm_segmentation`: the cell segmentation mask previously obtained (if you used HPACellSegmentator, this will be something like `[output_prefix]_cellmask.png`).
- `output_folder`: the base folder that will contain all generated micronuclei segmentations.
- `output_prefix`: the prefix appended to all files generated per image.

All images can be relative or absolute paths, or directly URLs. You can also skip cells between runs with the special character `#` in front of the desired lines. 
Check the following `path_list.csv` content as an example:

```
#nuclei_image,nuclei_segmentation,cytoplasm_segmentation,output_folder,output_prefix
input/1128_H2_2_blue.png,input/1128_H2_2_nucleimask.png,input/1128_H2_2_cellmask.png,output,1128_H2_2_
#
input/1128_H2_2_blue.png,input/1128_H2_2_nucleimask.png,input/1128_H2_2_cellmask.png,output,1128_H2_2_
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

Micronuclei segmentation generates in the chosen output_folder the following files:
- `[output_prefix]_micronuclei_mask.png`: the segmented micronuclei mask.
- `result.csv` (in the base folder) file containing all the links between micronuclei labels / previously segmented nucleis and many other spatial information.