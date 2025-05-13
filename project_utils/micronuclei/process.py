import datetime
import logging
import os
import pandas as pd
import numpy as np
import cv2

import micronuclei_quantification


# This is the log configuration. It will log everything to a file AND the console
logging.basicConfig(filename='log.txt', encoding='utf-8', format='%(levelname)s: %(message)s', filemode='w', level=logging.INFO)
console = logging.StreamHandler()
logging.getLogger().addHandler(console)
logger = logging.getLogger("HPA micronuclei quantification")

# This is the general configuration variable. We are going to use the special key "log" in the dictionary to use the log in our code
config = { "log": logger}

# If you want to use constants with your script, add them here
config["hpa_images_base_folder"] = 'images'
config["micro_nuclei_segmentations_base_folder"] = 'segmentations'
config["micro_nuclei_expand_diameter"] = 5
config["intensity_tolerance"] = 0.8

# Log the start time and the final configuration so you can keep track of what you did
config["log"].info('Start: ' + datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
config["log"].info('Parameters used:')
config["log"].info(config)
config["log"].info('----------')


if os.path.exists("./result.csv"):
    df = pd.read_csv('result.csv')
    df["micnuc_protein_intensity"] = 0.0
    df["micnuc_external_protein_intensity"] = 0.0
    df["micnuc_protein"] = 0
    id_list = df["id"].unique()

    curr_id = ""
    for index, row in df.iterrows():
        if curr_id != row["id"]:
            curr_id = row["id"]
            protein_img = cv2.imread(os.path.join(config["hpa_images_base_folder"], curr_id[:curr_id.index('_')], curr_id + "green.png"), -1)
            micnuc_seg = cv2.imread(os.path.join(config["micro_nuclei_segmentations_base_folder"], curr_id + "micronuclei_mask.png"), -1)
        # Micronuclei quantification
        micnuc_data_df = micronuclei_quantification.quantify_micronuclei(protein_img, micnuc_seg, row["micnuc_label"],
                    config["micro_nuclei_expand_diameter"], config["intensity_tolerance"])
        df.loc[index, "micnuc_protein_intensity"] = "{:.2f}".format(micnuc_data_df["micnuc_protein_intensity"])
        df.loc[index, "micnuc_external_protein_intensity"] = "{:.2f}".format(micnuc_data_df["micnuc_external_protein_intensity"])
        df.loc[index, "micnuc_protein"] = micnuc_data_df["micnuc_protein"]
        config["log"].info("- Saved results for " + curr_id)

    # We store the cell crops bboxes and ids for easy localization
    df.to_csv("result.csv", index=False)


config["log"].info('----------')
config["log"].info('End: ' + datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))