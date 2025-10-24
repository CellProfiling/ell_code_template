import datetime
import logging
import os
import pandas as pd
from skimage.filters import threshold_multiotsu

import cellcycle_quantification
import image_utils


# This is the log configuration. It will log everything to a file AND the console
logging.basicConfig(filename='log.txt', encoding='utf-8', format='%(levelname)s: %(message)s', filemode='w', level=logging.INFO)
console = logging.StreamHandler()
logging.getLogger().addHandler(console)
logger = logging.getLogger("Cellcycle dataset quantification")

# This is the general configuration variable. We are going to use the special key "log" in the dictionary to use the log in our code
config = { "log": logger}

# If you want to use constants with your script, add them here
config["images_base_folder"] = '/data/temp/max_proj'
config["segmentations_base_folder"] = '/data/temp/cellcycle/segs'

# Log the start time and the final configuration so you can keep track of what you did
config["log"].info('Start: ' + datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
config["log"].info('Parameters used:')
config["log"].info(config)
config["log"].info('----------')


if os.path.exists("./crop_info.csv"):
    df_crop = pd.read_csv("./crop_info.csv")

    df_result = pd.DataFrame(columns=['id', 'cell', 'x1', 'y1', 'x2', 'y2'])
    index = 0

    for base_image_FOV in df_crop["id"].unique():
        config["log"].info("- Now quantifying FOV " + base_image_FOV)
        image_stack = []
        image_stack.append([image_utils.read_grayscale_image(os.path.join(config["images_base_folder"], base_image_FOV + "DAPI_MAX.tif"), minmax_norm=True)])
        image_stack.append([image_utils.read_grayscale_image(os.path.join(config["images_base_folder"], base_image_FOV + "mt_MAX.tif"), minmax_norm=True)])
        image_stack.append([image_utils.read_grayscale_image(os.path.join(config["images_base_folder"], base_image_FOV + "bright_MAX.tif"), minmax_norm=True)])
        image_stack.append([image_utils.read_grayscale_image(os.path.join(config["images_base_folder"], base_image_FOV + "CDT1_MAX.tif"), minmax_norm=True)])
        image_stack.append([image_utils.read_grayscale_image(os.path.join(config["images_base_folder"], base_image_FOV + "GMNN_MAX.tif"), minmax_norm=True)])

        otsu_stack = []
        otsu_stack.append(threshold_multiotsu(image_stack[0][0], 3))
        otsu_stack.append(threshold_multiotsu(image_stack[1][0], 3))
        otsu_stack.append(threshold_multiotsu(image_stack[2][0], 3))
        otsu_stack.append(threshold_multiotsu(image_stack[3][0], 3))
        otsu_stack.append(threshold_multiotsu(image_stack[4][0], 3))

        cell_mask = image_utils.read_grayscale_image(os.path.join(config["segmentations_base_folder"], base_image_FOV + "cell_mask.png"))
        nuclei_mask = image_utils.read_grayscale_image(os.path.join(config["segmentations_base_folder"], base_image_FOV + "nuclei_mask.png"))

        df_filtered = df_crop[df_crop["id"] == base_image_FOV]
        for curr_cell in df_filtered["cell"]:
            cellcycle_data = cellcycle_quantification.quantify_cellcycle(config, curr_cell, image_stack, otsu_stack, cell_mask, nuclei_mask)
            if (cellcycle_data):
                df_result.loc[index, "id"] = base_image_FOV
                df_result.loc[index, "cell"] = curr_cell
                df_result.loc[index, "x1"] = df_filtered.loc[df_filtered['cell'] == curr_cell, "x1"].values[0]
                df_result.loc[index, "y1"] = df_filtered.loc[df_filtered['cell'] == curr_cell, "y1"].values[0]
                df_result.loc[index, "x2"] = df_filtered.loc[df_filtered['cell'] == curr_cell, "x2"].values[0]
                df_result.loc[index, "y2"] = df_filtered.loc[df_filtered['cell'] == curr_cell, "y2"].values[0]
                df_result.loc[index, "nuc_area"] = cellcycle_data["nuc_area"]
                df_result.loc[index, "nuc_centroid_xy"] = cellcycle_data["nuc_centroid_xy"]
                df_result.loc[index, "nuc_eccentricity"] = cellcycle_data["nuc_eccentricity"]
                df_result.loc[index, "nuc_solidity"] = cellcycle_data["nuc_solidity"]
                df_result.loc[index, "cell_area"] = cellcycle_data["cell_area"]
                df_result.loc[index, "cell_centroid_xy"] = cellcycle_data["cell_centroid_xy"]
                df_result.loc[index, "cell_eccentricity"] = cellcycle_data["cell_eccentricity"]
                df_result.loc[index, "cell_solidity"] = cellcycle_data["cell_solidity"]
                df_result.loc[index, "DAPI_otsu3"] = cellcycle_data["DAPI_otsu3"]
                df_result.loc[index, "DAPI_mean"] = cellcycle_data["DAPI_mean"]
                df_result.loc[index, "DAPI_q90"] = cellcycle_data["DAPI_q90"]
                df_result.loc[index, "DAPI_ratio_pixels"] = cellcycle_data["DAPI_ratio_pixels"]
                df_result.loc[index, "DAPI_over_otsu"] = cellcycle_data["DAPI_over_otsu"]
                df_result.loc[index, "mt_otsu3"] = cellcycle_data["mt_otsu3"]
                df_result.loc[index, "mt_mean"] = cellcycle_data["mt_mean"]
                df_result.loc[index, "mt_q90"] = cellcycle_data["mt_q90"]
                df_result.loc[index, "mt_ratio_pixels"] = cellcycle_data["mt_ratio_pixels"]
                df_result.loc[index, "mt_over_otsu"] = cellcycle_data["mt_over_otsu"]
                df_result.loc[index, "bright_otsu3"] = cellcycle_data["bright_otsu3"]
                df_result.loc[index, "bright_mean"] = cellcycle_data["bright_mean"]
                df_result.loc[index, "bright_q90"] = cellcycle_data["bright_q90"]
                df_result.loc[index, "bright_ratio_pixels"] = cellcycle_data["bright_ratio_pixels"]
                df_result.loc[index, "bright_over_otsu"] = cellcycle_data["bright_over_otsu"]
                df_result.loc[index, "CDT1_otsu3"] = cellcycle_data["CDT1_otsu3"]
                df_result.loc[index, "CDT1_mean"] = cellcycle_data["CDT1_mean"]
                df_result.loc[index, "CDT1_q90"] = cellcycle_data["CDT1_q90"]
                df_result.loc[index, "CDT1_ratio_pixels"] = cellcycle_data["CDT1_ratio_pixels"]
                df_result.loc[index, "CDT1_over_otsu"] = cellcycle_data["CDT1_over_otsu"]
                df_result.loc[index, "GMNN_otsu3"] = cellcycle_data["GMNN_otsu3"]
                df_result.loc[index, "GMNN_mean"] = cellcycle_data["GMNN_mean"]
                df_result.loc[index, "GMNN_q90"] = cellcycle_data["GMNN_q90"]
                df_result.loc[index, "GMNN_ratio_pixels"] = cellcycle_data["GMNN_ratio_pixels"]
                df_result.loc[index, "GMNN_over_otsu"] = cellcycle_data["GMNN_over_otsu"]
                config["log"].info("  - Saved results for " + base_image_FOV + " - " + str(curr_cell))
                index = index + 1

    df_result.to_csv("result.csv", index=False)


config["log"].info('----------')
config["log"].info('End: ' + datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
