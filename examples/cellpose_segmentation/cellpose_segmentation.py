import numpy as np
from skimage.io import imsave


# Code to generate the segmentation
def segment(model_nuc, model_cyto, nuclei_img, cito_img, nuc_diameter, cell_diameter, output_folder, output_prefix):
    channels = [0, 0]
    nuclei_masks, flows, styles = model_nuc.eval(
        nuclei_img,
        channels=channels,
        diameter=nuc_diameter,
    )
    imsave(output_folder + "/" + output_prefix + "nuclei_mask.png", nuclei_masks)

    if cito_img is not None:
        cell_masks, flows, styles = model_cyto.eval(
            cito_img,
            channels=channels,
            diameter=cell_diameter,
        )
        imsave(output_folder + "/" + output_prefix + "cell_mask.png", cell_masks)
