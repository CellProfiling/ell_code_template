import numpy as np
import pandas as pd
from skimage.exposure import equalize_adapthist
from skimage.io import imsave
from skimage.filters import threshold_multiotsu
from skimage.measure import label, regionprops
from skimage.morphology import binary_erosion, binary_closing, binary_dilation
from skimage.segmentation import expand_labels


def segment_micronuclei(nuc_img, nuclei_min_diameter, micnuc_min_diameter, micnuc_max_diameter,
                        eccentricity_tolerance, solidity_tolerance, intensity_ratio,
                        nuclei_segmentation, cell_segmentation,
                        output_folder, output_prefix):

    micnuc_data = []

    nuc_filtered_img = (nuc_img - np.amin(nuc_img)) / (np.amax(nuc_img) - np.amin(nuc_img))
    nuc_filtered_img = equalize_adapthist(nuc_filtered_img, clip_limit=0.5)
    c_otsu = threshold_multiotsu(nuc_filtered_img, 5)
    nuc_filtered_img[nuc_filtered_img < c_otsu[0]] = 0
    nuc_labels = np.copy(nuc_filtered_img)

    nuc_labels = nuc_labels > 0
    nuc_labels = binary_closing(nuc_labels)
    for i in range(0, micnuc_max_diameter):
        nuc_labels = binary_erosion(nuc_labels)

    nuc_labels = label(nuc_labels)
    nuc_labels = expand_labels(nuc_labels, micnuc_max_diameter)
    #imsave("nuclei_mask.png", np.uint8(nuc_labels))

    mic_img = np.copy(nuc_filtered_img)
    mic_img = np.where(nuc_labels > 0, 0, mic_img)
    mic_img[mic_img > 0] = 1
    for i in range(0, int(micnuc_min_diameter / 2)):
        mic_img = binary_erosion(mic_img)
    for i in range(0, int(micnuc_min_diameter / 2)):
        mic_img = binary_dilation(mic_img)
    mic_labels = label(mic_img)

    for curr_micnuc in regionprops(mic_labels):
        discard = True
        if curr_micnuc.eccentricity <= eccentricity_tolerance and curr_micnuc.solidity >= solidity_tolerance:
            nuc_seg = cell_segmentation[int(curr_micnuc.centroid[0]), int(curr_micnuc.centroid[1])]
            if nuc_seg != 0:
                micnuc_intensity = 0
                nuc_masked_img = np.where(mic_labels == curr_micnuc.label, nuc_img, 0)
                nonzero_elements = nuc_masked_img[nuc_masked_img != 0]
                if nonzero_elements.size != 0:
                    micnuc_intensity = np.mean(nonzero_elements)

                nuc_intensity = 0
                nuc_masked_img = np.where(nuclei_segmentation == nuc_seg, nuc_img, 0)
                nonzero_elements = nuc_masked_img[nuc_masked_img != 0]
                if nonzero_elements.size != 0:
                    nuc_intensity = np.mean(nonzero_elements)

                if abs(1 - micnuc_intensity / nuc_intensity) <= intensity_ratio:
                    micnuc_data.append({ "id" : output_prefix,
                                         "micnuc_label": curr_micnuc.label,
                                         "nuclei_label": nuc_seg ,
                                         "area": curr_micnuc.area,
                                         "centroid_xy": str(int(curr_micnuc.centroid[1])) + ':' + str(int(curr_micnuc.centroid[0])),
                                         "eccentricity": "{:.2f}".format(curr_micnuc.eccentricity),
                                         "solidity": "{:.2f}".format(curr_micnuc.solidity),
                                         "micnuc_intensity": "{:.2f}".format(micnuc_intensity),
                                         "nuc_intensity": "{:.2f}".format(nuc_intensity),
                                         })
                    discard = False
        if discard:
            mic_labels[mic_labels == curr_micnuc.label] = 0

    if len(micnuc_data) != 0:
        imsave(f"{output_folder}/{output_prefix}micronuclei_mask.png", np.uint8(mic_labels))
        return pd.DataFrame(micnuc_data)

    return None