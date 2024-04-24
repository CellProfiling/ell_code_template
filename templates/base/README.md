Template base
=============

This is the base template you can use as a starting point for your new script. It offers you some basic functionalities off the shelf that are easy to understand and modify according your personal preferences.



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
- If you don't want to use the file iteration functionality directed by `path_list.csv` file, just delete it.

For the configuration mechanisms you DO want to keep, modify them to suit your needs. You should always use at least the `input_path` and `output_path` parameters one way or another, so your script can be interoperable with the rest seamlessly.

Final touches:
- You might want to rename the `your_code.py` file for something more related to the functionality your code aims to provide, like `custom_clustering.py` or `calculate_csv.py`
  - You should also probably change the function `def your_function(config, input_path, output_path):` inside this file with something more memorable.
  - Remember to also change in `template.py` file the lines `import your_code` and `your_code.your_function(config, `[...]
- You might want to rename the `template.py` file for something more suitable for you, like `process.py` or `core.py`

Now you are ready to start working in your own code!



Running the code
---------------- 

**NOTE**: remember that you have to access your created virtual environment before running the code! To do so, navigate to the directory you created and activate it.
 - Example:
   - `cd /home/lab/sandbox/example`
   - `source bin/activate`

Once you have activated your virtual environment, just run the code with `python template.py` [or the name you have changed template.py with]

