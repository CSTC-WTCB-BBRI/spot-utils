# spot-utils

This repository aims at developping a Web Interface to control and interact with Boston Dynamic's Spot.

## Getting Started

This project is meant to be run on linux machines.

### ASDF

First, make sure ASDF is installed on your system.

Then, execute the following command to install the project's specific python version:

```bash
asdf install
```

### Python Virtual Environment

Before creating a virtual environment for this project, you need to install and setup two pip packages:

```bash
pip install virtualenv virtualenvwrapper
```

|   Package             |   Description     |
|   ---                 |   ---             |
|   virtualenv          |   [A tool for creating isolated virtual python environments](https://pypi.org/project/virtualenv/)    |
|   virtualenvwrapper   |   [virtualenvwrapper is a set of extensions to Ian Bicking’s virtualenv tool](https://pypi.org/project/virtualenvwrapper/)    |

Once both packages are installed, you will need to add the following lines to your ```~/.bashrc``` (or the equivalent for your current shell):

```bash
#PYTHON VENV
export WORKON_HOME=~/.virtualenvs
. $(asdf where python)/bin/virtualenvwrapper.sh
```

Now, update your shell and ASDF:

```bash
source ~/.bashrc # reload the .bashrc configurations
# NOTE: don't forget to adapt ~/.bashrc to whatever you actually use!
asdf reshim # reload asdf tools
```

This is almost done! Execute the following command to create a vitual environment for this project:

```bash
mkvirtualenv -a $(pwd) spotUtils
```

From now on, you can access this project's folder and activate its virtual environment by running this simple command:

```bash
workon pythonFullStackTemplate
```

To exit the virtual environment, simply run: 
```bash
deactivate
```

### Python Dependencies

To install this project's Python dependencies to your newly created virtual environment, run:

```bash
pip install -r requirements.txt
```

|   Package             |   Description     |
|   ---                 |   ---             |
|   Django              |   [Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design](https://pypi.org/project/Django/)    |
|   djangorestframework |   [Awesome web-browsable Web APIs](https://pypi.org/project/djangorestframework/)    |