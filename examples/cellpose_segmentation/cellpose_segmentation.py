import numpy as np
from skimage.exposure import rescale_intensity, equalize_adapthist
from skimage.io import imsave
from scipy import ndimage as ndi
from skimage.segmentation import join_segmentations, watershed, relabel_sequential, expand_labels


def sharpen(image):
    p2, p98 = np.percentile(image, (2, 98))
    img_rescale = rescale_intensity(image, in_range=(p2, p98))
    return img_rescale


def adaptive_hist(image):
    img_adapteq = equalize_adapthist(image)
    return img_adapteq


def solve_conflict_watershed(cyto_img, nuc_img):
    distance = ndi.distance_transform_edt(cyto_img)
    wl = watershed(-distance, np.where(cyto_img > 0, nuc_img, 0), mask=cyto_img)
    return wl


def solve_conflict_expand(to_fix_img, expanded_img):
    to_fix_img = np.where(to_fix_img != 0, expanded_img, 0)
    return to_fix_img


def merge_segmentations(seg_nuc, seg_cyto1, seg_cyto2):
    merged_masks = None

    conflicting_cyt12nuc = {}
    conflicting_nuc12cyt = {}
    merged_cyto1_masks, mc12n, mc12c = join_segmentations(seg_nuc, seg_cyto1, return_mapping=True)

    cyt12shape = {}
    nuc12shape = {}
    cyt12nuc = {}
    for label in mc12c.in_values:
        if label != 0:
            if mc12c[label] != 0:
                if mc12c[label] not in cyt12shape:
                    cyt12shape[mc12c[label]] = []
                    cyt12nuc[mc12c[label]] = []
                if label not in cyt12shape[mc12c[label]]: cyt12shape[mc12c[label]].append(label)
                if mc12n[label] != 0 and mc12n[label] not in cyt12nuc[mc12c[label]]:
                    cyt12nuc[mc12c[label]].append(mc12n[label])
                    if mc12n[label] not in nuc12shape:
                        nuc12shape[mc12n[label]] = []
                    nuc12shape[mc12n[label]].append(label)
            else:
                merged_cyto1_masks[merged_cyto1_masks == label] = 0

    for label in cyt12nuc:
        if len(cyt12nuc[label]) == 0:
            for cell_label in cyt12shape[label]:
                merged_cyto1_masks[merged_cyto1_masks == cell_label] = 0
        else:
            if len(cyt12nuc[label]) > 1:
                conflicting_cyt12nuc[label] = cyt12nuc[label]
                for curr_conf_nuc in cyt12nuc[label]:
                    conflicting_nuc12cyt[curr_conf_nuc] = label
            current_shape = cyt12shape[label][0]
            for cell_label in cyt12shape[label]:
                merged_cyto1_masks[merged_cyto1_masks == cell_label] = current_shape

    if seg_cyto2 is not None:
        conflicting_cyt22nuc = {}
        conflicting_nuc22cyt = {}
        merged_cyto2_masks, mc22n, mc22c = join_segmentations(seg_nuc, seg_cyto2, return_mapping=True)

        cyt22shape = {}
        nuc22shape = {}
        cyt22nuc = {}
        for label in mc22c.in_values:
            if label != 0:
                if mc22c[label] != 0:
                    if mc22c[label] not in cyt22shape:
                        cyt22shape[mc22c[label]] = []
                        cyt22nuc[mc22c[label]] = []
                    if label not in cyt22shape[mc22c[label]]: cyt22shape[mc22c[label]].append(label)
                    if mc22n[label] != 0 and mc22n[label] not in cyt22nuc[mc22c[label]]:
                        cyt22nuc[mc22c[label]].append(mc22n[label])
                        if mc22n[label] not in nuc22shape:
                            nuc22shape[mc22n[label]] = []
                        nuc22shape[mc22n[label]].append(label)
                else:
                    merged_cyto2_masks[merged_cyto2_masks == label] = 0

        for label in cyt22nuc:
            if len(cyt22nuc[label]) == 0:
                for cell_label in cyt22shape[label]:
                    merged_cyto2_masks[merged_cyto2_masks == cell_label] = 0
            else:
                if len(cyt22nuc[label]) > 1:
                    conflicting_cyt22nuc[label] = cyt22nuc[label]
                    for curr_conf_nuc in cyt22nuc[label]:
                        conflicting_nuc22cyt[curr_conf_nuc] = label
                current_shape = cyt22shape[label][0]
                for cell_label in cyt22shape[label]:
                    merged_cyto2_masks[merged_cyto2_masks == cell_label] = current_shape


        merged_masks, m2c1, m2c2 = join_segmentations(merged_cyto1_masks, merged_cyto2_masks, return_mapping=True)

        fixed_nuclei = []
        fixed_shapes = []
        for conf_nuc1 in conflicting_nuc12cyt:
            if conf_nuc1 not in fixed_nuclei:
                if conf_nuc1 in conflicting_nuc22cyt or conf_nuc1 not in nuc22shape:
                    affected_shapes = []
                    affected_nuclei = []
                    for conf_cyt1 in conflicting_cyt12nuc:
                        if conf_nuc1 in conflicting_cyt12nuc[conf_cyt1]:
                            for curr_nuc in conflicting_cyt12nuc[conf_cyt1]:
                                affected_nuclei.append(curr_nuc)
                            for curr_shape in m2c1.in_values:
                                if m2c1[curr_shape] == cyt12shape[conf_cyt1][0]:
                                    affected_shapes.append(curr_shape)
                    for conf_cyt2 in conflicting_cyt22nuc:
                        if conf_nuc1 in conflicting_cyt22nuc[conf_cyt2]:
                            for curr_shape in m2c2.in_values:
                                if m2c2[curr_shape] == cyt22shape[conf_cyt2][0]:
                                    affected_shapes.append(curr_shape)
                    cyto_img = np.zeros_like(merged_masks)
                    for shape_label in affected_shapes:
                        cyto_img = np.where(merged_masks == shape_label, shape_label, cyto_img)
                    nuc_img = np.zeros_like(merged_masks)
                    for nuc_label in affected_nuclei:
                        nuc_img = np.where(seg_nuc == nuc_label, seg_nuc, nuc_img)
                    wl = solve_conflict_watershed(cyto_img, nuc_img)
                    merged_masks = np.where(wl != 0, wl * 1000, merged_masks)
                    fixed_nuclei.extend(affected_nuclei)
                    fixed_shapes.extend(affected_shapes)
                else:
                    reference_shapes = []
                    to_fix_shapes = []
                    affected_nuclei = []
                    for conf_cyt1 in conflicting_cyt12nuc:
                        if conf_nuc1 in conflicting_cyt12nuc[conf_cyt1]:
                            for curr_nuc in conflicting_cyt12nuc[conf_cyt1]:
                                affected_nuclei.append(curr_nuc)
                            for curr_shape in m2c1.in_values:
                                if m2c1[curr_shape] == cyt12shape[conf_cyt1][0]:
                                    to_fix_shapes.append(curr_shape)
                    for conf_nuc2 in affected_nuclei:
                        for conf_cyt2 in cyt22nuc:
                            if conf_nuc2 in cyt22nuc[conf_cyt2]:
                                for curr_shape in m2c2.in_values:
                                    if m2c2[curr_shape] == cyt22shape[conf_cyt2][0]:
                                        reference_shapes.append(curr_shape)
                    to_fix_img = np.zeros_like(merged_masks)
                    expand_img = np.zeros_like(merged_masks)
                    for shape_label in to_fix_shapes:
                        to_fix_img = np.where(merged_masks == shape_label, merged_masks, to_fix_img)
                    for shape_label in reference_shapes:
                        expand_img = np.where(merged_masks == shape_label, cyt22nuc[m2c2[shape_label]][0], expand_img)
                        to_fix_img = np.where(merged_masks == shape_label, merged_masks, to_fix_img)
                    expand_img = expand_labels(expand_img, 540)
                    el = solve_conflict_expand(to_fix_img, expand_img)
                    merged_masks = np.where(el != 0, el * 1000, merged_masks)
                    fixed_nuclei.extend(affected_nuclei)
                    fixed_shapes.extend(to_fix_shapes)
                    fixed_shapes.extend(reference_shapes)

        for conf_nuc2 in conflicting_nuc22cyt:
            if conf_nuc2 not in fixed_nuclei:
                if conf_nuc2 not in nuc12shape:
                    affected_shapes = []
                    affected_nuclei = []
                    for conf_cyt2 in conflicting_cyt22nuc:
                        if conf_nuc2 in conflicting_cyt22nuc[conf_cyt2]:
                            for curr_nuc in conflicting_cyt22nuc[conf_cyt2]:
                                affected_nuclei.append(curr_nuc)
                            for curr_shape in m2c2.in_values:
                                if m2c2[curr_shape] == cyt22shape[conf_cyt2][0]:
                                    affected_shapes.append(curr_shape)
                    cyto_img = np.zeros_like(merged_masks)
                    for shape_label in affected_shapes:
                        cyto_img = np.where(merged_masks == shape_label, shape_label, cyto_img)
                    nuc_img = np.zeros_like(merged_masks)
                    for nuc_label in affected_nuclei:
                        nuc_img = np.where(seg_nuc == nuc_label, seg_nuc, nuc_img)
                    wl = solve_conflict_watershed(cyto_img, nuc_img)
                    merged_masks = np.where(wl != 0, wl * 1000, merged_masks)
                    fixed_nuclei.extend(affected_nuclei)
                    fixed_shapes.extend(affected_shapes)
                elif conf_nuc2 not in conflicting_nuc12cyt:
                    reference_shapes = []
                    to_fix_shapes = []
                    affected_nuclei = []
                    for conf_cyt2 in conflicting_cyt22nuc:
                        if conf_nuc2 in conflicting_cyt22nuc[conf_cyt2]:
                            for curr_nuc in conflicting_cyt22nuc[conf_cyt2]:
                                affected_nuclei.append(curr_nuc)
                            for curr_shape in m2c2.in_values:
                                if m2c2[curr_shape] == cyt22shape[conf_cyt2][0]:
                                    to_fix_shapes.append(curr_shape)
                    for conf_nuc1 in affected_nuclei:
                        for conf_cyt1 in cyt12nuc:
                            if conf_nuc1 in cyt12nuc[conf_cyt1]:
                                for curr_shape in m2c1.in_values:
                                    if m2c1[curr_shape] == cyt12shape[conf_cyt1][0]:
                                        reference_shapes.append(curr_shape)
                    to_fix_img = np.zeros_like(merged_masks)
                    expand_img = np.zeros_like(merged_masks)
                    for shape_label in to_fix_shapes:
                        to_fix_img = np.where(merged_masks == shape_label, merged_masks, to_fix_img)
                    for shape_label in reference_shapes:
                        expand_img = np.where(merged_masks == shape_label, cyt12nuc[m2c1[shape_label]][0], expand_img)
                        to_fix_img = np.where(merged_masks == shape_label, merged_masks, to_fix_img)
                    expand_img = expand_labels(expand_img, 540)
                    el = solve_conflict_expand(to_fix_img, expand_img)
                    merged_masks = np.where(el != 0, el * 1000, merged_masks)
                    fixed_nuclei.extend(affected_nuclei)
                    fixed_shapes.extend(to_fix_shapes)
                    fixed_shapes.extend(reference_shapes)

        for label in m2c1.in_values:
            if m2c1[label] != 0 and mc12c[m2c1[label]] != 0 and label not in fixed_shapes:
                current_cyto1 = mc12c[m2c1[label]]
                current_set = cyt12nuc[current_cyto1].copy()
                if 0 in current_set:
                    current_set.remove(0)
                if len(current_set) == 0:
                    merged_masks[merged_masks == label] = (cyt12shape[current_cyto1][0] + 200) * 10000
                else:
                    merged_masks[merged_masks == label] = current_set[0] * 10000
            if m2c2[label] != 0 and mc22c[m2c2[label]] != 0:
                current_cyto2 = mc22c[m2c2[label]]
                current_set = cyt22nuc[current_cyto2].copy()
                if 0 in current_set:
                    current_set.remove(0)
                if len(current_set) == 0:
                    merged_masks[merged_masks == label] = (cyt22shape[current_cyto2][0] + 400) * 10000
                else:
                    merged_masks[merged_masks == label] = current_set[0] * 10000
    else:
        merged_masks = merged_cyto1_masks

        fixed_nuclei = []
        fixed_shapes = []
        for conf_nuc1 in conflicting_nuc12cyt:
            if conf_nuc1 not in fixed_nuclei:
                affected_shapes = []
                affected_nuclei = []
                for conf_cyt1 in conflicting_cyt12nuc:
                    if conf_nuc1 in conflicting_cyt12nuc[conf_cyt1]:
                        for curr_nuc in conflicting_cyt12nuc[conf_cyt1]:
                            affected_nuclei.append(curr_nuc)
                        for curr_shape in mc12c.in_values:
                            if mc12c[curr_shape] == cyt12shape[conf_cyt1][0]:
                                affected_shapes.append(curr_shape)
                cyto_img = np.zeros_like(merged_masks)
                for shape_label in affected_shapes:
                    cyto_img = np.where(merged_masks == shape_label, shape_label, cyto_img)
                nuc_img = np.zeros_like(merged_masks)
                for nuc_label in affected_nuclei:
                    nuc_img = np.where(seg_nuc == nuc_label, seg_nuc, nuc_img)
                wl = solve_conflict_watershed(cyto_img, nuc_img)
                merged_masks = np.where(wl != 0, wl * 1000, merged_masks)
                fixed_nuclei.extend(affected_nuclei)
                fixed_shapes.extend(affected_shapes)

    return relabel_sequential(merged_masks)[0]


# Code to generate the segmentation
def segment(model_nuc, model_cyto, nuclei_img, cyto_img1, cyto_img2, nuc_diameter, cell_diameter, output_folder, output_prefix):
    channels = [1, 2]
    # We segment the nuclei using cellpose default nuclei model
    nuclei_masks, flows, styles = model_nuc.eval(
        np.stack([nuclei_img, np.zeros_like(nuclei_img)]),
        channels=channels,
        diameter=nuc_diameter,
    )
    imsave(output_folder + "/" + output_prefix + "nuclei_mask.png", nuclei_masks)

    channels = [1, 2]
    if cyto_img1 is not None:
        cell_masks = None

        # We segment the 1st cytoplasm marker using cellpose default cyto3 model
        cyto1_masks, flows, styles = model_cyto.eval(
            np.stack([sharpen(adaptive_hist(cyto_img1)), nuclei_masks]),
            channels=channels,
            diameter=cell_diameter,
            flow_threshold=0.8,
            cellprob_threshold=-0.4
        )
        imsave(output_folder + "/" + output_prefix + "cyto1_mask.png", cyto1_masks)

        if cyto_img2 is not None:
            # In case we are using 2 cytoplasm markers
            # We segment the 2nd cytoplasm marker using cellpose default cyto3 model
            cyto2_masks, flows, styles = model_cyto.eval(
                np.stack([sharpen(adaptive_hist(cyto_img2)), nuclei_masks]),
                channels=channels,
                diameter=cell_diameter,
                flow_threshold=0.8,
                cellprob_threshold=-0.4
            )
            imsave(output_folder + "/" + output_prefix + "cyto2_mask.png", cyto2_masks)

            # We merge the nuclei and 2 cytoplasm segmentations
            cell_masks = merge_segmentations(nuclei_masks, cyto1_masks, cyto2_masks) #cyto2_masks)
        else:
            # We merge the nuclei and cytoplasm segmentations
            cell_masks = merge_segmentations(nuclei_masks, cyto1_masks, None)

        imsave(output_folder + "/" + output_prefix + "cell_mask.png", cell_masks)