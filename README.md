
Last updated: July 10, 2023
# Edge Computing enabled Low-Latency Communication for Wireless Networked Control System

<a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg"></a>  

## Official implementation for the paper ["Edge Computing enabled Low-Latency Communication for Wireless Networked Control System"]

## Description 

<div style="text-align: justify;">
This study introduces a novel strategy for achieving enhanced low-latency control performance in Wireless Networked Control Systems (WNCS) via the integration of edge computing. Traditional networked control systems necessitate the receipt of raw data from distant sensors to enable the controller to generate an appropriate control command, a process that often results in substantial periodic communication traffic and resultant performance degradation in certain applications. To mitigate this, we suggest the use of edge computing to preprocess raw data, distill critical features, and subsequently transmit them. Moreover, we present an adaptive scheme aimed at curtailing regularly occurring data traffic by adaptively altering periodic data transmission based on necessity. This is achieved by abstaining from data transmission when a comparative analysis of previously transmitted and newly generated data indicates no significant update. 


 
 The effectiveness of our proposed strategy is empirically validated through experiments conducted on a remote control system testbed using a mobile robot that navigates the road by utilizing camera information. The remote vehicle follows a predetermined route while being operated by a server that processes camera data from the vehicle and sends appropriate control commands. Connectivity is maintained via a wireless network, which transmits the state of the actuator (in this case, the remote vehicle) and allows the server to issue control commands. The system under consideration comprises two main components: the remote vehicle and the server. The vehicle provides sensor data concerning its environment to the server, which processes this information and makes decisions in real-time. These decisions are then transmitted back to the vehicle through the wireless channel, enabling it to execute assigned tasks. The ongoing communication keeps the remote control system operational. (The mobile robot deployed in the testbed is manufactured by Waveshare Electronics and integrated with a Raspberry Pi 3B+.)
</div>



## Implementation setup on the remote vehicle
The Raspberry Pi is moving towards a 64-bit operating system. Within a year or so, the 32-bit OS will be fully replaced by the faster 64-bit version.

### Step #1: Installation of Raspberry Pi OS
1. Dowmload and install the Raspberry Pi Imager into your computer 
2. Run the Raspberry Pi Imager in your computer
3. Pluge in the sd card that you want to write the OS on
4. Select the operating system that you want to install
4. Select your sd card 
5. Click write to write the OS into your sd card


### Step #2: Enable Interfaces for AlphaBot2

More detalits about the Alphabot2 can be obtainet on the [Link here](https://www.waveshare.com/wiki/AlphaBot2)

Type the following command in terminal.

```
$ sudo raspi-config
```

1. Choose Interfacing Options -> Camera -> Yes -> Yes -> OK
2. Choose Interfacing Options -> SPI -> Yes -> OK
3. Choose Interfacing Options -> VNC -> Yes -> OK
4. Choose Interfacing Options -> I2C -> Yes -> OK
5. Choose Interfacing Options -> SERIAL -> No -> Yes -> OK

```
$ sudo apt update
$ sudo apt install fonts-wqy-zenhei
$ sudo pip install rpi_ws281x
```

### Step #3: Virtual Environments on the Raspberry Pi

In the hidden file .profile, set the value for VIRTUALENVWRAPPER_PYTHON

```
sudo nano ~/.profile
```

At the bottom of the file, type in the following line:
```
VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3.X
```

Save and exit nano. Now run .profile by typing:
```
source ~/.profile
```

Now install virtualenv and virtualenvwrapper

```
sudo pip3 install virtualenv
sudo pip3 install virtualenvwrapper
```

edit the .profile file again to set 1) the variable WORKON_HOME to the path of the directory .virtualenvs which contains our virtual environments and 2) make known the location of the shell file, virualenvwrapper.sh

```
sudo nano ~/.profile
```

Type the following two lines at the bottom:

```
export WORKON_HOME=$HOME/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh
```

Save and exit nano. Run .profile by typing:

```
source ~/.profile
```

The command mkvirtualenv can now be used to create python virtual environments as shown below

```
mkvirtualenv whatever -p /usr/bin/python3.X
```
VEs are stored in the hidden directory .virtualenvs located at your home path (~). The directory “whatever” is a subdirectory of .virtualenvs

To activate the VE “whatever” in any Terminal window enter:

```
source ~/.profile
workon whatever
```

Your prompt now begins with (whatever). This means you are now working in the VE named “whatever”. All packages installed using pip3 (when the whatever VE is active) are placed in the site-packages directory located at:
~/.virtualenvs/whatever/lib/python3.X/site-packages

### Step #4 Install OpenCV 4.5.5 on Raspberry Pi 3 or 4 (Building from source)
This article helps you install OpenCV 4.5.5 on Raspberry Pi 3 or 4 with a 64-bit operation system.

The difference is if you build from source, then you can enable or disable some functionalities, for example, you can build OpenCV with opencv_contrib module, Or
you can build OpenCV with Deep-Learning-Inference-Engine-backend, Or CUDA, Or Qt, Or with GStreamer, Or with tesseract-ocr and many other configurations which you
can change or enable/disable. But if you do not need the extra functionality, then you can directly install the pre-built library and use it.

Assumptions
* You already own Raspberry Pi 3 or 4 with a 64-bit operation system installed.

### Version check.
Before installing OpenCV 4.5 on your Raspberry 64-bit OS, you should first check your version. Run the command $uname -a$ and verify your version.
You also need to check your C++ compiler version with the command $gcc -v$. It must also be an aarch64-linux-gnu version.

```
$ uname -a
$ gcc -v
```

#### Step #1: Expand filesystem on your Raspberry Pi
OpenCV needs a lot of memory to compile. The latest versions want to see a minimum of 6.5 GB of memory before building. But swap space is limited to 2048 MByte by default. To exceed this 2048 MByte limit, you need to increase this maximum in the /sbin/dphys-swapfile. 

```
# edit the swap configuration by changing CONF_MAXSWAP as shown below
# CONF_MAXSWAP = 4096 
$ sudo nano /sbin/dphys-swapfile
$ sudo nano /etc/dphys-swapfile
# reboot
$ sudo reboot
```

#### Step #2: Installation script
we created an installation script that executes all commands at once. It starts with the installation of the dependencies and ends with the ldconfig.
```
wget https://github.com/sihsch/EC-LLC-WNCS/OpenCV-4-5-5.sh
sudo chmod 755 ./OpenCV-4-5-5.sh
./OpenCV-4-5-5.sh
```

#### Step #3: Resizing dphys-swap 
That is resetting the swap space back to its original 100 Mbyte. Flash memory can only write a limited number of cycles. In the end, it will wear your SD card out. It is therefore wise to keep memory swapping to a minimum. Besides, it also slows down your application.

```
$ sudo nano /etc/dphys-swapfile
set CONF_SWAPSIZE=100 with the Nano text editor

$ cd ~
$ rm opencv.zip
$ rm opencv_contrib.zip
$ sudo reboot
```

If you have installed OpenCV in a virtual environment, you need to make a symbolic link to the library. Without this link, OpenCV will not be found by python and the import fails. You can skip these steps if you have installed OpenCV without a virtual environment.


```

$ cd ~/.virtualenvs/cv450/lib/python3.9/site-packages
$ ln -s /usr/local/lib/python3.9/site-packages/cv2/python-3.9/cv2.cpython-39m-arm-linux-gnueabihf.so
$ cd ~
```

### Step #5: Download the EC-LLC-WNCS project
Download Project from our repository [link to repo](https://github.com/sihsch/EC-LLC-WNCS/archive/refs/heads/main.zip) using command:
 
```
git clone https://github.com/sihsch/EC-LLC-WNCS

```
### Step #6: Installing the requarments for the lineFollower project 
We assume you have followed all the procedures from the biggining till here. Now we will install the necessary library to enable run our project

```
pip install -r requirements.txt
```

#### Step #7: How to Run the Source Code

| Syntax      | Description (Local side) |
| ----------- | ----------- |
|AlphaBot2.py       | contain the functionality to move the AlphaBot       |
|full_local.py     | All the computation is performed by the mobile robot        |
|full_local_display.py | All the computation is performed at the mobile robot, and this will display what the mobile robot camera sees       |
|remote_sender.py  | offloads all the computation to the server      |
|edgelv1.py        | Pre-process the image before offloading it to the server       |
|edgelv2.py        | Pre-process the image before offloading it to the server       |
|edgelv3.py        | Pre-process the image before offloading it to the server       |
|adaptive_sender.py| The mobile robot offloads the information to the server only when a threshold is violated         |



| Syntax      | Description (Remote side) |
| ----------- | ----------- |
| PID.py              | PID algorithm for smoothly tracking the line       |
| imgProcessing.py    | For extracting useful information from the image         |
| remote_receiver.py  | Receive an image from (remote_sender.py), process it, and return a control command        |
| edge1_receiver.py   | Receive semi-processed information from (edgelv1.py), finalize the processing, and return a control command       |
| edge2_receiver.py   | Receive semi-processed information from (edgelv2.py), finalize the processing, and return a control command       |
| edge3_receiver.py   | Receive semi-processed information from (edgelv3.py), finalize the processing, and return a control command       |
| adaptive_receiver.py| Receive from (adaptive_sender.py) communication       |

## Citation
If you use this code for your research, please cite:

```
The paper is currently under review
```

## Contact
For any inquiry please contact us at our email addresses: danielmtowe@sch.ac.kr or dmk@sch.ac.kr

