import os


def your_function(config, input_path, output_path):
    config["log"].info("I should do something here with file/s from " + input_path + " and put the results in " + output_path)

    data = input_path + ",data2,data3"
    with config["result_lock"]:
        with open(config["result_file"], 'a') as f:
            f.write(data + '\n')