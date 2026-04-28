Template advanced
=================

This is the advanced template you can use as a starting point for your new script. Beyond the basic functionalities of the base template, it offers:
- Multi-CPU parallelisation using separate processes; this is specially indicated for CPU-intensive tasks like image processing or heavy computation.
- Progress bar showing how many files have been processed out of the total.
- Process-safe compiled CSV result with automatic header written before the workers start.



Requirements
------------

Please read the overall `README.md` file to understand the structure principles of this template. 



Installation
------------

- Install the code following the steps indicated in the overall `README.md` file, just remember to use all the contents of this directory as you working code.



Extend the template
-------------------

Although the template works from scratch, it does not much without your code and modifications. 

Let's start with the `template.py` file:
- Find the line `logger = logging.getLogger("My program")` and change the "My program" value for something short and related to your project.
- You might want to remove unused configuration mechanisms: 
  - If you don't want to use constants, remove the section under the comment `# If you want to use constants with your script, add them here`
  - If you don't want to use YAML config file, remove the section under the comment `# If you want to use a configuration file with your script, add it here`
  - If you don't want to use command line arguments, remove the section under the comment `# If you want to use command line parameters with your script, add them here`
- The file iteration functionality directed by `path_list.csv` file makes things far more easy to run and bookkeep later on, so it's not optional in this template
- Note that the YAML configuration file (`config.yaml`) is optional: if the file is not present the script will simply skip it and use the constants and command line arguments instead.

For the configuration mechanisms you want to add, just put them in the proper place highlighted above. 

Final touches:
- You might want to rename the `your_code.py` file for something more related to the functionality your code aims to provide, like `custom_clustering.py` or `calculate_csv.py`
  - You should also probably change the function `def your_function(config, input_path, output_path):` inside this file with something more memorable.
  - Remember to also change in `template.py` file the lines `import your_code` and `your_code.your_function(config, `[...]
- Open `your_code.py` and update the `RESULT_HEADERS` constant at the top to match the columns your function will write to the result CSV. The header is written automatically before the workers start, so you only need to define it once there.
- You can control how many CPU cores are used via the `workers` constant, the `workers` key in `config.yaml`, or the `-w` command line argument.
- You might want to rename the `template.py` file for something more suitable for you, like `process.py` or `core.py`

Now you are ready to start working in your own code!



Running the code
---------------- 

**NOTE**: remember that you have to access your created virtual environment before running the code! To do so, navigate to the directory you created and activate it.
 - Example:
   - `cd /home/lab/sandbox/example`
   - `source bin/activate`

Once you have activated your virtual environment, just run the code with `python template.py` [or the name you have changed template.py with]

