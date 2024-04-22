import numpy as np
import os
from skimage.filters import threshold_multiotsu
from skimage.io import imsave, imread


def generate_otsu(config, data, classes, output_filename_prefix):
    config["log"].info("----- Otsu classes " + str(classes))
    # We calculate the Otsu thresholds for the required classes
    c_otsu = threshold_multiotsu(data, classes)
    config["log"].info("----- Otsu thresholds " + str(c_otsu))
    # We expand the threshold list with 0 bottom
    bins = np.insert(c_otsu, 0, 0.0)
    # We re-create the image based on classes
    regions = np.digitize(data, bins=bins)
    # We convert back the classes to the thresholded pixel values
    regions = np.reshape(np.array([bins[x - 1] for x in np.ravel(regions)]), (len(data), len(data[0])))
    # We save the image as jpg 8bit-depth for quick browsing
    imsave(output_filename_prefix + '_otsu_' + str(classes) + '.png', np.uint8(regions * 255))


def otsu_explorer(config, input_path, output_path):
    config["log"].info("- Exploring directory " + input_path)
    # We iterate over all images in the current directory
    for image_file in os.listdir(input_path):
        config["log"].info("--- Exploring file " + image_file)
        # We generate the output filename prefix
        output_filename_prefix = os.path.join(output_path, image_file[:-4])
        # We read the image as a numpy array
        data = imread(os.path.join(input_path, image_file))
        # We normalize the image
        data = (data - data.min()) / (data.max() - data.min())
        # We run several otsu threshols and save the images in low quality just to explore how they look
        generate_otsu(config, data, 3, output_filename_prefix)
        generate_otsu(config, data, 4, output_filename_prefix)
        generate_otsu(config, data, 5, output_filename_prefix)