import datetime
import logging
import os
import pandas as pd
from skimage.io import imread

import cell_cropper


# This is the log configuration. It will log everything to a file AND the console
logging.basicConfig(filename='log.txt', encoding='utf-8', format='%(levelname)s: %(message)s', filemode='w', level=logging.INFO)
console = logging.StreamHandler()
logging.getLogger().addHandler(console)
logger = logging.getLogger("HPA cell cropper")

# This is the general configuration variable. We are going to use the special key "log" in the dictionary to use the log in our code
config = { "log": logger}

# If you want to use constants with your script, add them here
config["gray"] = True
config["crop_size"] = 1024
config["mask_cell"] = False

# Log the start time and the final configuration so you can keep track of what you did
config["log"].info('Start: ' + datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
config["log"].info('Parameters used:')
config["log"].info(config)
config["log"].info('----------')


# If we provide a "path_list.csv" file, we run our code for each pair of input/output sub-folders
if os.path.exists("./path_list.csv"):
    path_list = open("./path_list.csv", 'r')

    df = pd.DataFrame(columns=['id', 'cell', 'x1', 'y1', 'x2', 'y2'])

    for curr_set in path_list:
        if curr_set.strip() != "" and not curr_set.startswith("#"):
            curr_set_arr = curr_set.split(",")
            # We create the output folder
            os.makedirs(curr_set_arr[5].strip(), exist_ok=True)
            # We load the images as numpy arrays
            image_stack = []
            if config["gray"]:
                image_stack.append([imread(curr_set_arr[0].strip(), as_gray=True)])
                image_stack.append([imread(curr_set_arr[1].strip(), as_gray=True)])
                image_stack.append([imread(curr_set_arr[2].strip(), as_gray=True)])
                image_stack.append([imread(curr_set_arr[3].strip(), as_gray=True)])
            else:
                image_stack.append([imread(curr_set_arr[0].strip())[:, :, 0]])
                image_stack.append([imread(curr_set_arr[1].strip())[:, :, 0]])
                image_stack.append([imread(curr_set_arr[2].strip())[:, :, 2]])
                image_stack.append([imread(curr_set_arr[3].strip())[:, :, 1]])

            cell_mask = imread(curr_set_arr[4].strip(), as_gray=True)
            # Single cell crops
            cell_bbox_df = cell_cropper.generate_crops(image_stack, cell_mask, config["crop_size"], config["mask_cell"], curr_set_arr[5].strip(), curr_set_arr[6].strip())
            df = pd.concat([df, cell_bbox_df], ignore_index=True)

            config["log"].info("- Saved results for " + curr_set_arr[6].strip())

    # We store the cell crops bboxes and ids for easy localization
    df.to_csv("crop_info.csv", index=False)


config["log"].info('----------')
config["log"].info('End: ' + datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))