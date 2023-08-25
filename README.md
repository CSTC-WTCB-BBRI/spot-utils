# spot-utils

This repository aims at developping a Web Interface to control and interact with Boston Dynamic's Spot.

## Getting Started

This project is meant to be run on linux machines.

If running on a docker container, refer to [this document](./ops/README.md). Otherwise, keep reading!

### Environment Variables

This project's python scripts use environment variables. These are stored within the `.env` file at the root of this project's directory.

Create a new `.env` file and paste the following inside it (values are placeholders):

```bash
BOSDYN_CLIENT_ADMIN_USERNAME=admin_user 
BOSDYN_CLIENT_ADMIN_PASSWORD=admin_password
BOSDYN_CLIENT_USERNAME=user
BOSDYN_CLIENT_PASSWORD=password
ROBOT_IP=WW.XX.YY.ZZ
ROBOT_USERNAME=SPOT_CORE_USERNAME
ROBOT_SSH_PORT=XX
SPOT_SLAM_PORT=YY
ROBOT_SPOT_UTILS_ROOT_DIR=/home/SPOT_CORE_USERNAME/src/spot-utils
ROBOT_LIBUVC_THETA_SAMPLE_ROOT_DIR=/home/SPOT_CORE_USERNAME/src/libuvc-theta-sample
SELF_IP=ZZ.YY.XX.WW
ROBOT_ESTOP_TIMEOUT_SEC=5
BOSDYN_CLIENT_LOGGING_VERBOSE=True
GUID=GUID
SECRET=SECRET
DEV_MODE=True
```

To get the value of SELF_IP (this value might change over time), run:
```bash
python3 -m bosdyn.client $ROBOT_IP self-ip
# The IP address of the computer used to talk to the robot is: 192.168.80.100
```

### Development Payload

This project's python scripts use payload credentials registered with the robot to authenticate on Spot.

Follow [this](https://dev.bostondynamics.com/docs/python/daq_tutorial/daq1) to learn how to setup a new payload on Spot.

Save the GUID and SECRET values to the .env file at the root of this project's repository.

**NOTE: At [BuildWise](https://www.buildwise.be/en/), there already is a "Dev Payload" payload registered on Spot. Ask for the GUID and SECRET values**

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

### Setup the needed services

Refer to the [Services](##services) section.

### Start Web Server

cd to the root of the project's directory and run:
```bash
python manage.py runserver
```

## Access Development Web Application

First, run the server. Then, follow [this](http://127.0.0.1:8000) link.

## API Endpoints

First, run the server. Then, follow [this](http://127.0.0.1:8000/api/) link..

## Services

### SpotCameras Image Service

For retrieving Spot's built-in cameras' live video feeds, this project uses the ```ImageClient``` default service. This service is available by default on any Spot robot.

For retrieving Spot's other cameras' live video feeds, this project uses a service called ```spot-cameras-image-service```.

Some USB camera devices are not available by default as a ```/dev/video*``` device. If this is the case for your USB camera, refer to the [RicohTheta Image Service](###ricoh-theta-z1) section.

This service was developped for this project and does not exist on the factory version of Spot.

First, create a ```.dockerenv``` file (refer to the [Development Payload](###development-payload) section for the values of GUID and SECRET):
```bash
IMAGE_SERVICE_NAME=spot-cameras-image-service
AUTHORITY='robot-web-cam'
SERVICE_TYPE='bosdyn.api.ImageService'
CAMERA_PORT=5000
GUID=GUID
SECRET=SECRET
ROBOT_IP=192.168.50.3
SELF_IP=192.168.50.5
```

Then, create a ```.env``` file (the video device number should be 0 if you have no other usb camera connected to the Spot CORE):
```bash
ORIG_VIDEO_DEV=/dev/video0
```

To enable it, there is a few required steps:
* Clone this project on the SPOT CORE:
```bash
# Change directory to match the ROBOT_SPOT_UTILS_ROOT_DIR environment variable
git clone https://github.com/CSTC-WTCB-BBRI/spot-utils.git
```
* Build the docker image:
```bash
cd $ROBOT_SPOT_UTILS_ROOT_DIR/spot-services/SpotCameras
docker build -t spot_cameras_image_service .
```
**NOTE**: depending on the specifications of your Spot CORE, you might need to [build the image for an ARM64 architecture](https://dev.bostondynamics.com/docs/python/daq_tutorial/daq4#recreate-docker-images-for-arm64-architecture).
* If your camera is a RICOH THETA, make sure to follow the steps described in the [RicohTheta Image Service](###ricoh-theta-z1) section.
* Add the Spot CORE user to the video and plugdev groups:
```bash
sudo usermod -aG plugdev,video spot
```

## Tests

All test files are located inside the /tests/ folder.

### Execute All Tests

cd to the root of the project's directory and run:
```bash
python manage.py test tests
```

## Examples

### RICOH THETA Z1

First, plug the RICOH THETA Z1 USB camera to the Spot CORE.

Making this camera available on the Spot CORE requires a few adaptations. Connect the Spot CORE to internet and access its terminal, then run:
```bash
# Various dependencies
sudo apt install -y cmake libusb-1.0-0-dev libjpeg-dev
# GStreamer packages
sudo apt install -y libgstreamer1.0-0 \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-bad \
    gstreamer1.0-plugins-ugly \
    gstreamer1.0-libav \
    gstreamer1.0-doc \
    gstreamer1.0-tools \
    gstreamer1.0-x \
    gstreamer1.0-alsa \
    gstreamer1.0-gl \
    gstreamer1.0-gtk3 \
    gstreamer1.0-qt5 \
    gstreamer1.0-pulseaudio \
    libgstreamer-plugins-base1.0-dev

# cd to wherever you want to build source code
# for example:
mkdir ~/src
cd ~/src

# Install libuvc-theta
git clone https://github.com/ricohapi/libuvc-theta.git
mkdir libuvc-theta/build
cd libuvc-theta/build
cmake ..
make
sudo make install
cd ../..

# Install libuvc-theta-sample
git clone https://github.com/ricohapi/libuvc-theta-sample.git
cd libuvc-theta-sample/gst
make
sudo /sbin/ldconfig -v
cd ../..

# Install v4l2loopback
git clone https://github.com/umlaeute/v4l2loopback.git
cd v4l2loopback
make
sudo make install
sudo depmod -a
```

Now, you can run:
```bash
# This will load the v4l2loopback module to the kernel, but you will need to execute this command each time you restart the robot...
sudo modprobe v4l2loopback
# This will make sure the v4l2loopback module is automatically loaded to the kernel on boot
sudo vim /etc/modules
# Add a line with "v4l2loopback" at the end of the file
# Save and quit
# On the next boot, the module will be available
```

You should then see a new ```/dev/video0``` device.

Right now, this is a "Dummy Device" and it can't access the RICOH THETA Z1 camera. This project has scripts to automatically set this up, you don't have to do anything!

Should you want to set it up yourself though, just execute this:
```bash
# make sure the camera is plugged and in "live stream" mode
# cd to wherever you cloned the libuvc-theta-sample repository
./libuvc-theta-sample/gst/gst_loopback
```