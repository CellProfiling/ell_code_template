import argparse
import concurrent.futures
import datetime
import logging
import multiprocessing
import os
import yaml
from tqdm import tqdm

import your_code


# This wrapper calls your code for a single file. It also initializes a logger for
# the worker process since logging.Logger cannot be pickled across processes.
def _run_file(config, input_path, output_path):
    if config.get("log") is None:
        logging.basicConfig(filename=config.get("log_file", "log.txt"), encoding='utf-8',
                            format='%(levelname)s: %(message)s', filemode='a', level=logging.DEBUG)
        config["log"] = logging.getLogger("worker")
    your_code.your_function(config, input_path, output_path)


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
# These are example parameters in case you don't want to use the path_list.csv file. Comment this if you don't need it
config["input_directory"] = "./input"
config["output_directory"] = "./output"

# If you want to use a configuration file with your script, add it here
if os.path.exists("config.yaml"):
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

# We write the result file header once before the workers start
with open(config["result_file"], 'w') as f:
    f.write(your_code.RESULT_HEADERS + '\n')

if os.path.exists("./path_list.csv"):
    with open("./path_list.csv", 'r') as f:
        path_list = f.readlines()

    # Parse valid entries from path_list
    path_entries = []
    for line in path_list:
        if line.strip() != "" and not line.startswith("#"):
            path_entries.append((line.strip().split(",")[0], line.strip().split(",")[1]))

    # Strip non-picklable objects from config and set up a process-safe lock
    manager = multiprocessing.Manager()
    worker_config = {k: v for k, v in config.items() if k != "log"}
    worker_config["result_lock"] = manager.Lock()
    worker_config["log_file"] = "log.txt"

    # Submit one future per file and track progress with tqdm
    with concurrent.futures.ProcessPoolExecutor(max_workers=config["workers"]) as executor:
        futures = [executor.submit(_run_file, worker_config, inp, out) for inp, out in path_entries]
        for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures)):
            future.result()
# Following the input_path/output_path example, if we DON'T provide a "path_list.csv" file, we run our code once directly over the base input/output folder. Comment this if you don't need it
else:
    # We create the output folder. Comment this if you don't need it
    os.makedirs(config["output_directory"], exist_ok=True)
    for file in os.listdir(config["input_directory"]):
        your_code.your_function(config, os.path.join(config["input_directory"], file), os.path.join(config["output_directory"], file))


config["log"].info('----------')
config["log"].info('End: ' + datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
