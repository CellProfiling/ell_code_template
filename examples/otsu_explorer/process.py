import datetime
import logging
import os

import otsu_explorer


# This is the log configuration. It will log everything to a file AND the console
logging.basicConfig(filename='log.txt', encoding='utf-8', format='%(levelname)s: %(message)s', filemode='w', level=logging.INFO)
console = logging.StreamHandler()
logging.getLogger().addHandler(console)
logger = logging.getLogger("Otsu explorer")

# This is the general configuration variable. We are going to use the special key "log" in the dictionary to use the log in our code
config = { "log": logger}

# If you want to use constants with your script, add them here
config["input_directory"] = "./input"
config["output_directory"] = "./output"

# Log the start time and the final configuration so you can keep track of what you did
config["log"].info('Start: ' + datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
config["log"].info('Parameters used:')
config["log"].info(config)
config["log"].info('----------')


# If we provide a "path_list.csv" file, we run our code for each pair of input/output sub-folders
if os.path.exists("./path_list.csv"):
    with open("./path_list.csv", 'r') as path_list:
        for curr_path in path_list:
            if curr_path.strip() != "" and not curr_path.startswith("#"):
                curr_input_path = os.path.join(config["input_directory"], curr_path.strip().split(",")[0])
                curr_output_path = os.path.join(config["output_directory"], curr_path.strip().split(",")[1])
                os.makedirs(curr_output_path, exist_ok=True)

                otsu_explorer.otsu_explorer(config, curr_input_path, curr_output_path)
# If we DON'T provide a "path_list.csv" file, we run our code once directly over the base input/output folder
else:
    os.makedirs(config["output_directory"], exist_ok=True)
    otsu_explorer.otsu_explorer(config, config["input_directory"], config["output_directory"])

config["log"].info('----------')
config["log"].info('End: ' + datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
