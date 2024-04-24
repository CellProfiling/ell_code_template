Lundberg Lab template and code collection
=========================================

Here you have a collection of templates (and examples based on those) to kick-start your scripts with a simple, functional and featured base. The goal is to offer ready to use barebones script launchers with several interesting features at different levels of python programming knowledge, but also provide many examples based on those with code to perform tasks usually requested by the researchers.


Key features
------------

- **Templates with different levels of features and complexity** 
  - Several templates ready to use: base, advanced and retro-compatible.
  - Multiple configuration possibilities: basic constants, command line arguments or YAML configuration files.
  - Simple logging mechanism.
  - File iteration embedded functionality.
  - Template pipeline coordination (advanced).
- **Examples based on these templates with real functionality**
  - Readily available code to perform several requested tasks by the lab members.
  - Simple installation and usage.

 

Requirements
------------

- The code should work with any modern Python installation. For older python versions a retro template might be required/used.
- The code is script based, so you probably want to use regular plain virtual environments or an IDE like VSCode, PyCharm, etc...
- Depending on the example you download and your input data, you might need a more or less powerful system to run it.



Installation
------------

- Download all the code / clone the repository from github and save its contents in a temporary folder

If you use any Python IDE (VSCode, PyCharm, Spyder, etc...), just:
- Create a new project
- Create a virtual environment for that project
- Copy the contents of the item you want to work with from the downloaded code inside your project folder
- Install the project requirements through your IDE

If you want to install it via basic Python virtual environment:
- Install `python3`, `pip` and `virtualenv` in case you don't have them yet
- Navigate to your desired working directory
  - Example: `cd /home/lab/sandbox`
- Create a virtual environment:
  - Example: `python3 -m venv example`
- Copy the contents of the item you want to work with from the downloaded code inside your virtual environment directory
  - So for example, if you want to work with a new script from the template base, copy all the files inside `{your downloaded temporary folder}/templates/base/` to your virtual environment `/home/lab/sandbox/example/`
  - On the other hand, if you want to run the example code `otsu_explorer`, copy all the files inside `{your downloaded temporary folder}/examples/otsu_explorer/` to your virtual environment `/home/lab/sandbox/example/`
- Navigate to your virtual environment directory and activate it:
  - Example: `source bin/activate`
- Install all requirements through pip:
  - Example: `pip install -r requirements.txt`
- Profit!



Running the code
---------------- 

**NOTE**: remember that you have to access your created virtual environment before running the code! To do so, navigate to the directory you created and activate it.
 - Example:
   - `cd /home/lab/sandbox/example`
   - `source bin/activate`

Once you have activated your virtual environment, just run the code with `python {chosen_script.py}`
 - Example:
   - `python otsu_explorer.py`


Check the `README.md` file in each template/example you download, it might have additional indications that you need to follow for the code to run.

