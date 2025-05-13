import numpy as np
from skimage.segmentation import expand_labels


def quantify_micronuclei(protein_img, micnuc_seg, micnuc_label,
                        micro_nuclei_expand_diameter, intensity_tolerance):

    micnuc_mask = np.copy(micnuc_seg)
    micnuc_mask[micnuc_mask != micnuc_label] = 0

    micnuc_protein_intensity = 0.0
    protein_masked = np.where(micnuc_mask > 0, protein_img, 0)
    nonzero_elements = protein_masked[protein_masked != 0]
    if nonzero_elements.size != 0:
        micnuc_protein_intensity = np.mean(nonzero_elements)

    micnuc_external_protein_intensity = 0.0
    micnuc_expanded_mask = expand_labels(micnuc_mask, micro_nuclei_expand_diameter)
    protein_masked = np.where(micnuc_expanded_mask > 0, protein_img, 0)
    protein_masked = np.where(micnuc_mask > 0, 0, protein_masked)
    nonzero_elements = protein_masked[protein_masked != 0]
    if nonzero_elements.size != 0:
        micnuc_external_protein_intensity = np.mean(nonzero_elements)

    micnuc_protein = 1 if micnuc_external_protein_intensity / micnuc_protein_intensity <= intensity_tolerance else 0

    return { "micnuc_protein_intensity" : micnuc_protein_intensity, "micnuc_external_protein_intensity" : micnuc_external_protein_intensity, "micnuc_protein" : micnuc_protein }
