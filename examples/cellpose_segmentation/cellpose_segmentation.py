import numpy as np
from skimage.exposure import rescale_intensity, equalize_adapthist
from skimage.io import imsave
from scipy import ndimage as ndi
from skimage.morphology import erosion
from skimage.segmentation import join_segmentations, watershed, relabel_sequential


def sharpen(image):
    pl, ph = np.percentile(image, (0.1, 99.9))
    img_rescale = rescale_intensity(image, in_range=(pl, ph))
    return img_rescale


def adaptive_hist(image):
    q10 = np.percentile(image, 10.0)
    image[image < q10] = q10
    return image
    img_adapteq = equalize_adapthist(image)
    return img_adapteq


def solve_conflict_watershed(cyto_img, nuc_img):
    distance = ndi.distance_transform_edt(cyto_img)
    wl = watershed(-distance, np.where(cyto_img > 0, nuc_img, 0), mask=cyto_img)
    return wl


def solve_conflict_expand(to_fix_img, expanded_img):
    to_fix_img = np.where(to_fix_img != 0, expanded_img, 0)
    return to_fix_img


def merge_segmentations(seg_nuclei, seg_cyto1, seg_cyto2, nuc_diameter):
    merged_masks = None
    seg_nuc = np.zeros_like(seg_nuclei)
    for label in np.unique(seg_nuclei):
        if label != 0:
            nuc_temp = np.zeros_like(seg_nuclei)
            nuc_temp = np.where(seg_nuclei == label, seg_nuclei, 0)
            for i in range(int(nuc_diameter / 10)):
                nuc_temp = erosion(nuc_temp)
            seg_nuc = np.where(nuc_temp != 0, nuc_temp, seg_nuc)

    conflicting_seg1_1cytNnuc = {}
    conflicting_seg1_nuc_list = set()
    merged_cyto1_masks, seg1_ms2n, seg1_ms2c = join_segmentations(seg_nuc, seg_cyto1, return_mapping=True)

    seg1_cyt2shape = {}
    seg1_nuc2shape = {}
    seg1_cyt2nuc = {}
    seg1_nuc2cyt = {}
    for label in seg1_ms2c.in_values:
        if label != 0:
            if seg1_ms2c[label] != 0:
                if seg1_ms2c[label] not in seg1_cyt2shape:
                    seg1_cyt2shape[seg1_ms2c[label]] = set()
                    seg1_cyt2nuc[seg1_ms2c[label]] = set()
                if label not in seg1_cyt2shape[seg1_ms2c[label]]: seg1_cyt2shape[seg1_ms2c[label]].add(label)
                if seg1_ms2n[label] != 0 and seg1_ms2n[label] not in seg1_cyt2nuc[seg1_ms2c[label]]:
                    seg1_cyt2nuc[seg1_ms2c[label]].add(seg1_ms2n[label])
            else:
                merged_cyto1_masks[merged_cyto1_masks == label] = 0
    for label in seg1_ms2n.in_values:
        if label != 0 and seg1_ms2n[label] != 0:
            if seg1_ms2n[label] not in seg1_nuc2shape:
                seg1_nuc2shape[seg1_ms2n[label]] = set()
                seg1_nuc2cyt[seg1_ms2n[label]] = set()
            if label not in seg1_nuc2shape[seg1_ms2n[label]]: seg1_nuc2shape[seg1_ms2n[label]].add(label)
            if seg1_ms2c[label] != 0 and seg1_ms2c[label] not in  seg1_nuc2cyt[seg1_ms2n[label]]:
                seg1_nuc2cyt[seg1_ms2n[label]].add(seg1_ms2c[label])

    for cyt in seg1_cyt2nuc:
        if len(seg1_cyt2nuc[cyt]) == 0:
            for shape_label in seg1_cyt2shape[cyt]:
                merged_cyto1_masks[merged_cyto1_masks == shape_label] = 0
            del seg1_cyt2shape[cyt]
        else:
            if len(seg1_cyt2nuc[cyt]) > 1:
                conflicting_seg1_1cytNnuc[cyt] = seg1_cyt2nuc[cyt]
                for curr_conf_nuc in seg1_cyt2nuc[cyt]:
                    conflicting_seg1_nuc_list.add(curr_conf_nuc)

            current_shape = seg1_cyt2shape[cyt].copy().pop()
            for shape_label in seg1_cyt2shape[cyt]:
                merged_cyto1_masks[merged_cyto1_masks == shape_label] = current_shape
            seg1_cyt2shape[cyt] = current_shape

    if seg_cyto2 is not None:
        conflicting_seg2_1cytNnuc = {}
        conflicting_seg2_nuc_list = set()
        merged_cyto2_masks, seg2_ms2n, seg2_ms2c = join_segmentations(seg_nuc, seg_cyto2, return_mapping=True)

        seg2_cyt2shape = {}
        seg2_nuc2shape = {}
        seg2_cyt2nuc = {}
        seg2_nuc2cyt = {}
        for label in seg2_ms2c.in_values:
            if label != 0:
                if seg2_ms2c[label] != 0:
                    if seg2_ms2c[label] not in seg2_cyt2shape:
                        seg2_cyt2shape[seg2_ms2c[label]] = set()
                        seg2_cyt2nuc[seg2_ms2c[label]] = set()
                    if label not in seg2_cyt2shape[seg2_ms2c[label]]: seg2_cyt2shape[seg2_ms2c[label]].add(label)
                    if seg2_ms2n[label] != 0 and seg2_ms2n[label] not in seg2_cyt2nuc[seg2_ms2c[label]]:
                        seg2_cyt2nuc[seg2_ms2c[label]].add(seg2_ms2n[label])
                else:
                    merged_cyto2_masks[merged_cyto2_masks == label] = 0
        for label in seg2_ms2n.in_values:
            if label != 0 and seg2_ms2n[label] != 0:
                if seg2_ms2n[label] not in seg2_nuc2shape:
                    seg2_nuc2shape[seg2_ms2n[label]] = set()
                    seg2_nuc2cyt[seg2_ms2n[label]] = set()
                if label not in seg2_nuc2shape[seg2_ms2n[label]]: seg2_nuc2shape[seg2_ms2n[label]].add(label)
                if seg2_ms2c[label] != 0 and seg2_ms2c[label] not in  seg2_nuc2cyt[seg2_ms2n[label]]:
                    seg2_nuc2cyt[seg2_ms2n[label]].add(seg2_ms2c[label])

        for cyt in seg2_cyt2nuc:
            if len(seg2_cyt2nuc[cyt]) == 0:
                for shape_label in seg2_cyt2shape[cyt]:
                    merged_cyto2_masks[merged_cyto2_masks == shape_label] = 0
                del seg2_cyt2shape[cyt]
            else:
                if len(seg2_cyt2nuc[cyt]) > 1:
                    conflicting_seg2_1cytNnuc[cyt] = seg2_cyt2nuc[cyt]
                    for curr_conf_nuc in seg2_cyt2nuc[cyt]:
                        conflicting_seg2_nuc_list.add(curr_conf_nuc)
                current_shape = seg2_cyt2shape[cyt].copy().pop()
                for shape_label in seg2_cyt2shape[cyt]:
                    merged_cyto2_masks[merged_cyto2_masks == shape_label] = current_shape
                seg2_cyt2shape[cyt] = current_shape

        merged_masks, segm_ms2seg1, segm_ms2seg2 = join_segmentations(merged_cyto1_masks, merged_cyto2_masks, return_mapping=True)

        merged_shape2final = {}
        merged_shape_conflicting2cyt1 = {}
        merged_shape_conflicting2cyt2 = {}

        for label in segm_ms2seg1.in_values:
            if segm_ms2seg1[label] != 0 and seg1_ms2c[segm_ms2seg1[label]] != 0:
                if segm_ms2seg2[label] != 0 and seg2_ms2c[segm_ms2seg2[label]] != 0:
                    seg1_shape = segm_ms2seg1[label]
                    seg2_shape = segm_ms2seg2[label]
                    seg_cyt1_final = 0
                    seg_cyt2_final = 0
                    for seg1_cyt in seg1_cyt2shape:
                        if seg1_cyt2shape[seg1_cyt] == seg1_shape:
                            if seg1_cyt in conflicting_seg1_1cytNnuc:
                                merged_shape_conflicting2cyt1[label] = seg1_cyt
                            else:
                                seg_cyt1_final = seg1_cyt
                            break
                    for seg2_cyt in seg2_cyt2shape:
                        if seg2_cyt2shape[seg2_cyt] == seg2_shape:
                            if seg2_cyt in conflicting_seg2_1cytNnuc:
                                merged_shape_conflicting2cyt2[label] = seg2_cyt
                            else:
                                seg_cyt2_final = seg2_cyt
                            break
                    if seg_cyt1_final != 0:
                        merged_shape2final[label] = seg1_cyt2nuc[seg_cyt1_final].copy().pop() * 1000
                        if label in merged_shape_conflicting2cyt2:
                            del merged_shape_conflicting2cyt2[label]
                    elif seg_cyt2_final != 0:
                        merged_shape2final[label] = seg2_cyt2nuc[seg_cyt2_final].copy().pop() * 1000
                        if label in merged_shape_conflicting2cyt1:
                            del merged_shape_conflicting2cyt1[label]
                else:
                    seg1_shape = segm_ms2seg1[label]
                    for seg1_cyt in seg1_cyt2shape:
                        if seg1_cyt2shape[seg1_cyt] == seg1_shape:
                            if seg1_cyt not in conflicting_seg1_1cytNnuc:
                                merged_shape2final[label] = seg1_cyt2nuc[seg1_cyt].copy().pop() * 1000
                            else:
                                merged_shape_conflicting2cyt1[label] = seg1_cyt
            elif segm_ms2seg2[label] != 0 and seg2_ms2c[segm_ms2seg2[label]] != 0:
                seg2_shape = segm_ms2seg2[label]
                for seg2_cyt in seg2_cyt2shape:
                    if seg2_cyt2shape[seg2_cyt] == seg2_shape:
                        if seg2_cyt not in conflicting_seg2_1cytNnuc:
                            merged_shape2final[label] = seg2_cyt2nuc[seg2_cyt].copy().pop() * 1000
                        else:
                            merged_shape_conflicting2cyt2[label] = seg2_cyt

        merged_masks_simple = np.zeros_like(merged_masks)
        for shape in merged_shape2final:
            merged_masks_simple = np.where(merged_masks == shape, merged_shape2final[shape], merged_masks_simple)

        for label in segm_ms2seg1.in_values:
            if label in merged_shape_conflicting2cyt1:
                if label in merged_shape_conflicting2cyt2:
                    # 3 body problem
                    print("3 body problem")
                else:
                    seg1_cyt = merged_shape_conflicting2cyt1[label]
                    affected_shapes = set()
                    affected_nuclei = set()
                    for seg1_nuc in conflicting_seg1_1cytNnuc[seg1_cyt]:
                        affected_nuclei.add(seg1_nuc)
                    for curr_shape in segm_ms2seg1.in_values:
                        if segm_ms2seg1[curr_shape] == seg1_cyt2shape[seg1_cyt]:
                            affected_shapes.add(curr_shape)
                    if len(affected_shapes) > 0:
                        cyto_img = np.zeros_like(merged_masks)
                        for shape_label in affected_shapes:
                            cyto_img = np.where(merged_masks == shape_label, shape_label, cyto_img)
                            if shape_label in merged_shape_conflicting2cyt1:
                                del merged_shape_conflicting2cyt1[shape_label]
                        nuc_img = np.zeros_like(merged_masks)
                        for nuc_label in affected_nuclei:
                            nuc_img = np.where(seg_nuc == nuc_label, seg_nuc, nuc_img)
                        wl = solve_conflict_watershed(cyto_img, nuc_img)
                        for curr_shape in affected_shapes:
                            if curr_shape in merged_shape2final:
                                wl = np.where(merged_masks_simple == merged_shape2final[curr_shape], 0, wl)
                        merged_masks_simple = np.where(wl != 0, wl * 1000, merged_masks_simple)
            elif label in merged_shape_conflicting2cyt2:
                seg2_cyt = merged_shape_conflicting2cyt2[label]
                affected_shapes = set()
                affected_nuclei = set()
                for seg2_nuc in conflicting_seg2_1cytNnuc[seg2_cyt]:
                    affected_nuclei.add(seg2_nuc)
                for curr_shape in segm_ms2seg2.in_values:
                    if segm_ms2seg2[curr_shape] == seg2_cyt2shape[seg2_cyt]:
                        affected_shapes.add(curr_shape)
                if len(affected_shapes) > 0:
                    cyto_img = np.zeros_like(merged_masks)
                    for shape_label in affected_shapes:
                        cyto_img = np.where(merged_masks == shape_label, shape_label, cyto_img)
                        if shape_label in merged_shape_conflicting2cyt2:
                            del merged_shape_conflicting2cyt2[shape_label]
                    nuc_img = np.zeros_like(merged_masks)
                    for nuc_label in affected_nuclei:
                        nuc_img = np.where(seg_nuc == nuc_label, seg_nuc, nuc_img)
                    wl = solve_conflict_watershed(cyto_img, nuc_img)
                    for curr_shape in affected_shapes:
                        if curr_shape in merged_shape2final:
                            wl = np.where(merged_masks_simple == merged_shape2final[curr_shape], 0, wl)
                    merged_masks_simple = np.where(wl != 0, wl * 1000, merged_masks_simple)

        merged_masks = merged_masks_simple
    else:
        merged_masks = merged_cyto1_masks

        fixed_nuclei = set()
        fixed_shapes = set()
        for seg1_conf_nuc in conflicting_seg1_nuc_list:
            if seg1_conf_nuc not in fixed_nuclei:
                affected_shapes = set()
                affected_nuclei = set()
                for seg1_conf_cyt in conflicting_seg1_1cytNnuc:
                    if seg1_conf_nuc in conflicting_seg1_1cytNnuc[seg1_conf_cyt]:
                        for curr_nuc in conflicting_seg1_1cytNnuc[seg1_conf_cyt]:
                            affected_nuclei.add(curr_nuc)
                            for extra_cyt in seg1_nuc2cyt[curr_nuc]:
                                affected_shapes.add(seg1_cyt2shape[extra_cyt])
                        for curr_shape in seg1_ms2c.in_values:
                            if seg1_ms2c[curr_shape] == seg1_cyt2shape[seg1_conf_cyt]:
                                affected_shapes.add(curr_shape)
                cyto_img = np.zeros_like(merged_masks)
                for shape_label in affected_shapes:
                    cyto_img = np.where(merged_masks == shape_label, shape_label, cyto_img)
                nuc_img = np.zeros_like(merged_masks)
                for nuc_label in affected_nuclei:
                    nuc_img = np.where(seg_nuc == nuc_label, seg_nuc, nuc_img)
                wl = solve_conflict_watershed(cyto_img, nuc_img)
                merged_masks = np.where(wl != 0, wl * 1000, merged_masks)
                fixed_nuclei.update(affected_nuclei)
                fixed_shapes.update(affected_shapes)

    return relabel_sequential(merged_masks)[0]


# Code to generate the segmentation
def segment(model_nuc, model_cyto, nuclei_img, cyto_img1, cyto_img2, nuc_diameter, cell_diameter, output_folder, output_prefix):
    channels = [1, 0]
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
            cell_masks = merge_segmentations(nuclei_masks, cyto1_masks, cyto2_masks, nuc_diameter)
        else:
            # We merge the nuclei and cytoplasm segmentations
            cell_masks = merge_segmentations(nuclei_masks, cyto1_masks, None, nuc_diameter)

        imsave(output_folder + "/" + output_prefix + "cell_mask.png", cell_masks)