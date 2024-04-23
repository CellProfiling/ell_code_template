Phenocycler qptiff extractor
============================

This program, built upon the base template, will extract each marker image from the Phenocycler qptiff file. 



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
  - Locate the line `config["input_path"] = "./input"` and change the path value with your desired input directory. This directory should contain the qptiff file. 
  - Locate the line `config["output_path"] = "./output"` and change the path value with your desired output directory. This directory will contain the resulting marker images. OBS: it will be created if it does not exists
  - Locate the line `config["bit_depth"] = 8` and change the integer value with the desired bit-depth of the resulting marker images. OBS: 8, 16 or 32 are the normal expected values.  
  - Locate the line `config["image_type_extension"] = ".png"` and change the value with the desired image format/extension of the resulting marker images. OBS: ".png", ".jpg" or ".tif" are the usual expected values. 
  - Locate the line `config["normalize"] = false` and change the value with if you want to apply a min-max normalization to the resulting marker images.
- Copy your Phenocycler qptiff file in your stated input folder. OBS: The file must end with ".qptiff" extension. 



Running the code
---------------- 

**NOTE**: remember that you have to access your created virtual environment before running the code! To do so, navigate to the directory you created and activate it.
 - Example:
   - `cd /home/lab/sandbox/example`
   - `source bin/activate`

Once you have activated your virtual environment and modified all the desired parameters (see section **Setup**, just run the code with `python process.py`

