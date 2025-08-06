import argparse
import concurrent.futures
import datetime
import logging
import threading
import os
import yaml

import your_code


# This method calls your code per worker. config dict is passed so you can have access to all configuration data
def assign_files_to_worker(config, curr_list):
    for curr_path in curr_list:
        if curr_path.strip() != "" and not curr_path.startswith("#"):
            curr_input_path = curr_path.strip().split(",")[0]
            curr_output_path = curr_path.strip().split(",")[1]
            your_code.your_function(config, curr_input_path, curr_output_path)


# This is the log configuration. It will log everything to a file AND the console
logging.basicConfig(filename='log.txt', encoding='utf-8', format='%(levelname)s: %(message)s', filemode='w', level=logging.DEBUG)
console = logging.StreamHandler()
logging.getLogger().addHandler(console)
logger = logging.getLogger("My program")

# This is the general configuration variable. We are going to use the special key "log" in the dictionary to use the log in our code
config = { "log": logger}

# If you want to use constants with your script, add them here
config["workers"] = 2
config["result_file"] = "result.csv"
config["step"] = "base"
config["threshold"] = 3

# If you want to use a configuration file with your script, add it here
with open("config.yaml", "r") as file:
    config = config | yaml.safe_load(file)

# If you want to use command line parameters with your script, add them here
argparser = argparse.ArgumentParser(description="Please input the following parameters")
argparser.add_argument("-w", "--workers", help="use this number of parallel workers", default=2, type=int)
argparser.add_argument("-r", "--result_file", help="use file as resulting data compilation result", default="result.csv")
argparser.add_argument("-s", "--step", help="perform that example step")
argparser.add_argument("-t", "--threshold", help="use this example threshold", default=3, type=int)
args = argparser.parse_args()
config = config | args.__dict__

# Log the start time and the final configuration so you can keep track of what you did
config["log"].info('Start: ' + datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
config["log"].info('Parameters used:')
config["log"].info(config)
config["log"].info('----------')

# We create a thread lock to safely concurrent-write to result file
config["result_lock"] = threading.Lock()

if os.path.exists("./path_list.csv"):
    path_list = open("./path_list.csv", 'r').readlines()

    # We split evenly the lines in path_list amongs the desired workers
    list_shares = []
    for i in range(config["workers"]):
        curr_list = []
        for j in range(len(path_list)):
            if j % config["workers"] == i:
                curr_list.append(path_list[j].strip())
        list_shares.append(curr_list)

    # We create a thread per worker and assign the split lists t
    with concurrent.futures.ThreadPoolExecutor(max_workers=config["workers"]) as executor:
        for w in range(config["workers"]):
            executor.submit(assign_files_to_worker, config, list_shares[w])


config["log"].info('----------')
config["log"].info('End: ' + datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))