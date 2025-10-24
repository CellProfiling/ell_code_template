import numpy as np
from skimage.measure import regionprops
from skimage.segmentation import expand_labels


channels = {
    0 : "DAPI",
    1 : "mt",
    2 : "bright",
    3 : "CDT1",
    4 : "GMNN"
}

def quantify_cellcycle(config, cell_id, image_stack, otsu_stack, cell_mask, nuclei_mask):
    compiled_data = {}

    if (not np.isin(cell_id, nuclei_mask)):
        config["log"].info("  - Nuclei mask does not contain cell " + str(cell_id))
        return None
    if (not np.isin(cell_id, cell_mask)):
        config["log"].info("  - Cell mask does not contain cell " + str(cell_id))
        return None

    nuc = regionprops(np.where(nuclei_mask == cell_id, nuclei_mask, 0))[0]
    compiled_data["nuc_area"] = nuc.area
    compiled_data["nuc_centroid_xy"] = str(int(nuc.centroid[1])) + ':' + str(int(nuc.centroid[0]))
    compiled_data["nuc_eccentricity"] = "{:.2f}".format(nuc.eccentricity)
    compiled_data["nuc_solidity"] = "{:.2f}".format(nuc.solidity)

    cell = regionprops(np.where(cell_mask == cell_id, cell_mask, 0))[0]
    compiled_data["cell_area"] = cell.area
    compiled_data["cell_centroid_xy"] = str(int(cell.centroid[1])) + ':' + str(int(cell.centroid[0]))
    compiled_data["cell_eccentricity"] = "{:.2f}".format(cell.eccentricity)
    compiled_data["cell_solidity"] = "{:.2f}".format(cell.solidity)

    for img_index in range(0, len(image_stack)):
        marker = regionprops(np.where(cell_mask == int(cell_id), cell_mask, 0), image_stack[img_index][0])[0]
        compiled_data[channels[img_index] + "_otsu3"] = str(int(otsu_stack[img_index][0])) + ':' + str(int(otsu_stack[img_index][1]))
        compiled_data[channels[img_index] + "_mean"] = marker.intensity_mean
        marker_image = marker.image_intensity
        marker_image = marker_image[(marker_image != 0) & (~np.isnan(marker_image))]
        compiled_data[channels[img_index] + "_q90"] = np.quantile(marker_image, 0.9) if len(marker_image) > 0 else 0
        compiled_data[channels[img_index] + '_ratio_pixels'] = np.count_nonzero(marker_image >= otsu_stack[img_index][0]) / np.count_nonzero(marker.area)
        compiled_data[channels[img_index] + '_over_otsu'] = marker.intensity_mean - otsu_stack[img_index][0]

    return compiled_data
