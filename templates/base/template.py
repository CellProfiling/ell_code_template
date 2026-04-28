import argparse
import datetime
import logging
import os
import yaml

import your_code


# This is the log configuration. It will log everything to a file AND the console
logging.basicConfig(filename='log.txt', encoding='utf-8', format='%(levelname)s: %(message)s', filemode='w', level=logging.DEBUG)
console = logging.StreamHandler()
logging.getLogger().addHandler(console)
logger = logging.getLogger("My program")

# This is the general configuration variable. We are going to use the special key "log" in the dictionary to use the log in our code
config = { "log": logger}

# If you want to use constants with your script, add them here
config["step"] = "base"
config["threshold"] = 3
# These are example parameters in case you don't want to use the path_list.csv file. Comment this if you don't need it
config["input_directory"] = "./input"
config["output_directory"] = "./output"

# If you want to use a configuration file with your script, add it here
if os.path.exists("config.yaml"):
    with open("config.yaml", "r") as file:
        config = config | yaml.safe_load(file)

# If you want to use command line parameters with your script, add them here
argparser = argparse.ArgumentParser(description="Please input the following parameters")
argparser.add_argument("-s", "--step", help="perform that example step")
argparser.add_argument("-t", "--threshold", help="use this example threshold", default=3, type=int)
args = argparser.parse_args()
config = config | args.__dict__

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
                curr_input_path = curr_path.strip().split(",")[0]
                curr_output_path = curr_path.strip().split(",")[1]

                your_code.your_function(config, curr_input_path, curr_output_path)
# Following the input_path/output_path example, if we DON'T provide a "path_list.csv" file, we run our code once directly over the base input/output folder. Comment this if you don't need it
else:
    # We create the output folder. Comment this if you don't need it
    os.makedirs(config["output_directory"], exist_ok=True)
    for file in os.listdir(config["input_directory"]):
        your_code.your_function(config, os.path.join(config["input_directory"], file), os.path.join(config["output_directory"], file))

config["log"].info('----------')
config["log"].info('End: ' + datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))