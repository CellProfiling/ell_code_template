import numpy as np
import os
from tifffile import TiffFile
from xml.etree import ElementTree
from skimage.io import imsave


def convert_array_by_bit_depth(img_array, bit_depth):
    if img_array.dtype == np.uint8:
        if bit_depth == 8:
            return img_array
        elif bit_depth == 16:
            return np.uint16(img_array * 256)
        else:
            return np.uint32(img_array * 16777216)
    elif img_array.dtype == np.uint16:
        if bit_depth == 8:
            return np.uint8(img_array // 256)
        elif bit_depth == 16:
            return img_array
        else:
            return np.uint32(img_array * 65536)
    else:
        if bit_depth == 8:
            return np.uint8(img_array // 16777216)
        elif bit_depth == 16:
            return np.uint16(img_array // 65536)
        else:
            return img_array


def array_type_by_bit_depth(img_array, bit_depth):
    if bit_depth == 8:
        return np.uint8(img_array)
    elif bit_depth == 16:
        return np.uint16(img_array)
    else:
        return np.uint32(img_array)


def phenocycler_qptiff_extractor(config, input_path, output_path):
    config["log"].info("- Exploring directory " + input_path)
    # We iterate over all images in the current directory
    for image_file in os.listdir(input_path):
        # We expect a qptiff file with .qptiff extension
        with TiffFile(os.path.join(input_path, image_file)) as tif:
            filename_without_extension = tif.filename[0:tif.filename.index('.qptiff')]
            for page in tif.series[0].pages:
                curr_marker = ElementTree.fromstring(page.description).find('Biomarker').text
                filename_converted = filename_without_extension + '_' + curr_marker + config["image_type_extension"]
                numpy_img = page.asarray()
                if config["normalize"]:
                    numpy_img = (numpy_img - numpy_img.min()) / (numpy_img.max() - numpy_img.min())
                else:
                    numpy_img = convert_array_by_bit_depth(numpy_img, config["bit_depth"])
                imsave(os.path.join(output_path, filename_converted), array_type_by_bit_depth(numpy_img, config["bit_depth"]))
                config["log"].info("--- Image " + filename_without_extension + '_' + curr_marker + config["image_type_extension"] + ' saved')
