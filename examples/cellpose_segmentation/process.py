import datetime
import logging
import os
from skimage.io import imread
import cellpose_segmentation
from cellpose import models


# This is the log configuration. It will log everything to a file AND the console
logging.basicConfig(filename='log.txt', encoding='utf-8', format='%(levelname)s: %(message)s', filemode='w', level=logging.INFO)
console = logging.StreamHandler()
logging.getLogger().addHandler(console)
logger = logging.getLogger("Cellpose segmentation")

# This is the general configuration variable. We are going to use the special key "log" in the dictionary to use the log in our code
config = { "log": logger}

# If you want to use constants with your script, add them here
config["nuclei_only"] = False
config["nuc_diameter"] = 80
config["cyto_diameter"] = 240

# Log the start time and the final configuration so you can keep track of what you did
config["log"].info('Start: ' + datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
config["log"].info('Parameters used:')
config["log"].info(config)
config["log"].info('----------')


# We load the model
model_nuc = models.CellposeModel(gpu=False, model_type='nuclei')
model_cyto = models.CellposeModel(gpu=False, model_type='cyto3')

# If we provide a "path_list.csv" file, we run our code for each pair of input/output sub-folders
if os.path.exists("./path_list.csv"):
    path_list = open("./path_list.csv", 'r')

    for curr_set in path_list:
        if curr_set.strip() != "" and not curr_set.startswith("#"):
            curr_set_arr = curr_set.split(",")
            # We create the output folder
            os.makedirs(curr_set_arr[3].strip(), exist_ok=True)
            # We load the images as numpy arrays
            nuclei_img = imread(curr_set_arr[0].strip(), as_gray=True)
            cyto_img1 = None
            cyto_img2 = None
            if not config["nuclei_only"]:
                cyto_img1 = imread(curr_set_arr[1].strip(), as_gray=True)
                if curr_set_arr[2].strip() != "":
                    cyto_img2 = imread(curr_set_arr[2].strip(), as_gray=True)

            # Single cell crops
            cell_bbox_df = cellpose_segmentation.segment(model_nuc, model_cyto, nuclei_img, cyto_img1, cyto_img2, config["nuc_diameter"], config["cyto_diameter"], curr_set_arr[3].strip(), curr_set_arr[4].strip())

            config["log"].info("- Saved results for " + curr_set_arr[4].strip())


config["log"].info('----------')
config["log"].info('End: ' + datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
