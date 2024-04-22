import datetime
import logging
import os

import phenocycler_qptiff_extractor


# This is the log configuration. It will log everything to a file AND the console
logging.basicConfig(filename='log.txt', encoding='utf-8', format='%(levelname)s: %(message)s', filemode='w', level=logging.INFO)
console = logging.StreamHandler()
logging.getLogger().addHandler(console)
logger = logging.getLogger("Phenocycler qptiff extractor")

# This is the general configuration variable. We are going to use the special key "log" in the dictionary to use the log in our code
config = { "log": logger}

# If you want to use constants with your script, add them here
config["input_path"] = "./input"
config["output_path"] = "./output"

config["bit_depth"] = 16
config["image_type_extension"] = ".png"
config["normalize"] = False

# Log the start time and the final configuration so you can keep track of what you did
config["log"].info('Start: ' + datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
config["log"].info('Parameters used:')
config["log"].info(config)
config["log"].info('----------')


# We create the output folder
os.makedirs(config["output_path"], exist_ok=True)
# If we provide a "path_list.csv" file, we run our code for each pair of input/output sub-folders
if os.path.exists("./path_list.csv"):
    path_list = open("./path_list.csv", 'r')
    for curr_path in path_list:
        if curr_path.strip() != "" and not curr_path.startswith("#"):
            curr_input_path = config["input_path"] + "/" + curr_path.strip().split(",")[0]
            curr_output_path = config["output_path"] + "/" + curr_path.strip().split(",")[1]
            os.makedirs(curr_output_path, exist_ok=True)

            phenocycler_qptiff_extractor.phenocycler_qptiff_extractor(config, curr_input_path, curr_output_path)
# If we DON'T provide a "path_list.csv" file, we run our code once directly over the base input/output folder
else:
    phenocycler_qptiff_extractor.phenocycler_qptiff_extractor(config, config["input_path"], config["output_path"])

config["log"].info('----------')
config["log"].info('End: ' + datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))