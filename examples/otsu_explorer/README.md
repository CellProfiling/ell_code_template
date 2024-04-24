Otsu explorer
=============

This program, built upon the base template, will generate otsu thresholded images for 3, 4 and 5 bins/intervals from your original images. I will work with grayscale single channel images in PNG or JPG format. 



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
  - Locate the line `config["input_path"] = "./input"` and change the path value with your desired input directory. This directory should contain all your images OR all the subfolders present in `path_list.csv` (see below). 
  - Locate the line `config["output_path"] = "./output"` and change the path value with your desired output directory. This directory will contain the resulting generated images OR the resulting subfolders stated `path_list.csv` (see below). OBS: it will be created if it does not exists
- You can copy all your images in the stated input folder OR use a detailed `path_list.csv` listing:
  - If you want to copy all your images in the input folder, just delete the `path_list.csv` file. OBS: don't choose an output folder inside the stated input folder if you are going this way! 
  - If you want to use a detailed `path_list.csv` listing:
    - Create the desired subfolder structure in your input folder: one subfolder for every line in `path_list.csv` file.
    - Copy the associated images in each created subfolder.
    - Write a line in `path_list.csv` for each subolder, with the input subfolder first and the output subfolder after a comma ","
    - You can comment any of the lines with the character "#"
  


Running the code
---------------- 

**NOTE**: remember that you have to access your created virtual environment before running the code! To do so, navigate to the directory you created and activate it.
 - Example:
   - `cd /home/lab/sandbox/example`
   - `source bin/activate`

Once you have activated your virtual environment and modified all the desired parameters (see section **Setup**, just run the code with `python process.py`. OBS: you have to run the `process.py` file, which will on its turn call the rest of the code.

