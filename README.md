# spot-utils

This repository aims at developping a Web Interface to control and interact with Boston Dynamic's Spot.

## Getting Started

This project is meant to be run on linux machines.

If running on a docker container, see the [Getting Started (Docker)](##getting-started-(docker)) section.

### Environment Variables

This project's python scripts use environment variables. These are stored within a ```/api/scripts/.env```.

Create the .env file and paste the following inside it (values are placeholders):

```bash
BOSDYN_CLIENT_USERNAME=user 
BOSDYN_CLIENT_PASSWORD=password
ROBOT_IP=192.168.80.3
SELF_IP=192.168.80.100
ROBOT_ESTOP_TIMEOUT_SEC=5
BOSDYN_CLIENT_LOGGING_VERBOSE=True
WEBCAM_PORT=5000
GUID=GUID
SECRET=SECRET
```

### Development Payload

This project's python scripts use payload credentials registered with the robot to authenticate on Spot.

Follow [this](https://dev.bostondynamics.com/docs/python/daq_tutorial/daq1) to learn how to setup a new payload on Spot.

Save the CRED_FILE to the root of this project's repository.

**NOTE: At [BuildWise](https://www.buildwise.be/en/), there already is a "Dev Payload" payload registered on Spot. Ask for the CRED_FILE**

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

The [Pillow](https://pillow.readthedocs.io/en/stable/installation.html#building-on-macos) python package has pre-requisites. If you are on Ubuntu, execute the following command:

```bash
sudo apt-get install libtiff5-dev libjpeg8-dev libopenjp2-7-dev zlib1g-dev \
    libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python3-tk \
    libharfbuzz-dev libfribidi-dev libxcb1-dev
```

To install this project's Python dependencies to your newly created virtual environment, run:

```bash
pip install -r requirements.txt
```

|   Package             |   Description     |
|   ---                 |   ---             |
|   Django              |   [Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design](https://pypi.org/project/Django/)    |
|   djangorestframework |   [Awesome web-browsable Web APIs](https://pypi.org/project/djangorestframework/)    |
|   bosdyn-client       |   [The bosdyn-client wheel contains client interfaces for interacting with the Boston Dynamics Spot API. The client interfaces implement the Remote Procedure Calls (RPCs) defined in the bosdyn-api wheel](https://pypi.org/project/bosdyn-client/)    |
|   bosdyn-mission      |   [The bosdyn-mission wheel contains client interfaces and helper functionality for managing missions, which are part of the Boston Dynamics Spot API](https://pypi.org/project/bosdyn-mission/)    |
|   bosdyn-choreography-client  |   [The bosdyn-choreography-client wheel contains client interfaces for interacting with the Boston Dynamics Choreography API](https://pypi.org/project/bosdyn-choreography-client/)    |
|   Pillow  |   [Pillow is the friendly PIL fork by Alex Clark and Contributors. PIL is the Python Imaging Library by Fredrik Lundh and Contributors](https://pypi.org/project/Pillow/)    |
|   six  |   [Six is a Python 2 and 3 compatibility library](https://pypi.org/project/six/)    |
|   pyqt5  |   [Qt is set of cross-platform C++ libraries that implement high-level APIs for accessing many aspects of modern desktop and mobile systems](https://pypi.org/project/PyQt5/)    |
|   python-dotenv  |   [Python-dotenv reads key-value pairs from a .env file and can set them as environment variables](https://pypi.org/project/python-dotenv/)    |

### Set Up Database

to set the database, cd to the root of the project's directory and run:

```bash
python manage.py migrate
```

### Create Django Superuser

cd to the root of the project's directory and run:
```bash
python manage.py createsuperuser
```

### Start Web Server

cd to the root of the project's directory and run:
```bash
python manage.py runserver
```
## Getting Started (Docker)

### Environment Variables

This project's python scripts use environment variables. These are stored within a ```/api/scripts/.env```.

Create the .env file and paste the following inside it (values are placeholders):

```bash
BOSDYN_CLIENT_USERNAME=user 
BOSDYN_CLIENT_PASSWORD=password
ROBOT_IP=192.168.80.3
SELF_IP=192.168.80.100
ROBOT_ESTOP_TIMEOUT_SEC=5
BOSDYN_CLIENT_LOGGING_VERBOSE=True
WEBCAM_PORT=5000
GUID=GUID
SECRET=SECRET
```

### Development Payload

This project's python scripts use payload credentials registered with the robot to authenticate on Spot.

Follow [this](https://dev.bostondynamics.com/docs/python/daq_tutorial/daq1) to learn how to setup a new payload on Spot.

Save the GUID and SECRET to the .env file you created at the previous step.

**NOTE: At [BuildWise](https://www.buildwise.be/en/), there already is a "Dev Payload" payload registered on Spot. Ask for the CRED_FILE**

### Start Dockerized Web Server

cd to the root of the project's directory and run:
```bash
docker compose up build -d
```

### Stop Dockerized Web Server

```bash
docker compose down
```

## Access Development Web Application

First, run the server. Then, follow [this](http://127.0.0.1:8000) link (local dev server) or [this](http://127.0.0.1:80) link (dockerized dev server) to access the web application.

## API Endpoints

```TEMPORARY SECTION```

First, run the server. Then, follow [this](http://127.0.0.1:8000/api/) link (local dev server) or [this](http://127.0.0.1:80/api) link (dockerized dev server) to get all public api routes.

## Tests

All test files are located inside the /tests/ folder.

<!-- ### Dependencies

Some tests rely on [this](https://github.com/TheoPierne/spot-server-js) repository.

cd to /api/scripts and clone it:
```bash
git clone https://github.com/TheoPierne/spot-server-js.git
``` -->

### Execute All Tests

cd to the root of the project's directory and run:
```bash
python manage.py test tests
```
