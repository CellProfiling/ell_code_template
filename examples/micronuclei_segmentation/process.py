import datetime
import logging
import os
import pandas as pd
import numpy as np
import cv2

import micronuclei_segmentation


# This is the log configuration. It will log everything to a file AND the console
logging.basicConfig(filename='log.txt', encoding='utf-8', format='%(levelname)s: %(message)s', filemode='w', level=logging.INFO)
console = logging.StreamHandler()
logging.getLogger().addHandler(console)
logger = logging.getLogger("HPA micronuclei segmentation")

# This is the general configuration variable. We are going to use the special key "log" in the dictionary to use the log in our code
config = { "log": logger}

# If you want to use constants with your script, add them here
config["nuclei_min_diameter"] = 100
config["micro_nuclei_min_diameter"] = 15
config["micro_nuclei_max_diameter"] = 50
config["eccentricity_tolerance"] = 0.9
config["solidity_tolerance"] = 0.9
config["intensity_ratio_tolerance"] = 0.5

# Log the start time and the final configuration so you can keep track of what you did
config["log"].info('Start: ' + datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
config["log"].info('Parameters used:')
config["log"].info(config)
config["log"].info('----------')


# If we provide a "path_list.csv" file, we run our code for each pair of input/output sub-folders
if os.path.exists("./path_list.csv"):
    path_list = open("./path_list.csv", 'r')

    df = pd.DataFrame(columns=['id', 'micnuc_label', 'nuclei_label'])

    for curr_set in path_list:
        if curr_set.strip() != "" and not curr_set.startswith("#"):
            curr_set_arr = curr_set.split(",")
            # We create the output folder
            os.makedirs(curr_set_arr[3].strip(), exist_ok=True)
            # We load the images as numpy arrays
            img = cv2.imread(curr_set_arr[0].strip(), -1)
            nuc_seg = cv2.imread(curr_set_arr[1].strip(), -1)
            cyt_seg = cv2.imread(curr_set_arr[2].strip(), -1)

            # Micronuclei segmentation
            micnuc_seg_df = micronuclei_segmentation.segment_micronuclei(img,
                        config["nuclei_min_diameter"], config["micro_nuclei_min_diameter"], config["micro_nuclei_max_diameter"],
                        config["eccentricity_tolerance"], config["solidity_tolerance"], config["intensity_ratio_tolerance"],
                        nuc_seg, cyt_seg, curr_set_arr[3].strip(), curr_set_arr[4].strip())
            if micnuc_seg_df is not None:
                df = pd.concat([df, micnuc_seg_df], ignore_index=True)
                config["log"].info("- Saved results for " + curr_set_arr[4].strip())
            else:
                config["log"].info("- No micronuclei detected for " + curr_set_arr[4].strip())

    # We store the cell crops bboxes and ids for easy localization
    df.to_csv("result.csv", index=False)


config["log"].info('----------')
config["log"].info('End: ' + datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))