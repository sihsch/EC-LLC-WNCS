
Last updated: July 10, 2023
# Edge-Computing-Enabled Low-Latency Communication for a Wireless Networked Control System

## Official implementation for the paper ["Edge-Computing-Enabled Low-Latency Communication for a Wireless Networked Control System"](https://www.mdpi.com/2399798)

<a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg"></a>  

## Description 
We implemented a testbed in which a remote server receiving camera image information from an Autonomous Mobile Robot (AMR) creates a control command for moving the AMR and sends it back to the AMR. When the camera image information is transmitted to the server that performs edge computing, frequent transmission of camera information may adversely affect the performance of the entire system by increasing the load of the network. To solve this problem, two improvements were studied.
 
1. Transmitted image information is preprocessed in AMR and only a very small amount of data is transmitted.
2. Instead of transmitting video information at regular intervals, video information is transmitted only when surprising information comes in.

(The mobile robot deployed in the testbed is manufactured by Waveshare Electronics and integrated with a Raspberry Pi 3B+.)


[Watch the video](https://youtu.be/UpQUypfKRn) Description: This video showcases the Autonomous Mobile Robot successfully following a designated path and presents the results of Improvement #2, highlighting its enhanced performance.

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
sudo raspi-config
```

1. Choose Interfacing Options -> Camera -> Yes -> Yes -> OK
2. Choose Interfacing Options -> SPI -> Yes -> OK
3. Choose Interfacing Options -> VNC -> Yes -> OK
4. Choose Interfacing Options -> I2C -> Yes -> OK
5. Choose Interfacing Options -> SERIAL -> No -> Yes -> OK

```
sudo apt update
sudo apt install fonts-wqy-zenhei
sudo pip install rpi_ws281x
```


### Step #3: Download the EC-LLC-WNCS project
Download Project from our repository [link to repo](https://github.com/sihsch/EC-LLC-WNCS/archive/refs/heads/main.zip) using command:
 
```
git clone https://github.com/sihsch/EC-LLC-WNCS

```
### Step #4: Installing the requarments for the lineFollower project 
We assume you have followed all the procedures from the biggining till here. Now we will install the necessary library to enable run our project. Navigate into the cloned repository directory using the `cd` command:

```
cd EC-LLC-WNCS\local
pip install -r requirements.txt
```

#### Step #5: How to Run the Source Code

This project consists of two main components: a server-side script (`remote_receiver.py`) and a corresponding client-side script (`remote_sender.py`). The server-side script listens for incoming connections, while the client-side script initiates a connection to the server. Both scripts are designed to work together to facilitate communication between the server and the client.

## Usage Instructions

Before running the code, please ensure that you have the IP address of the server handy. You will need this IP address to establish a connection between the server and the client.

### Server-Side Setup

1. Navigate to the server-side directory.
2. Run the server-side script using the following command:

    ```bash
    python remote_receiver.py
    ```

   This command starts the server-side script, which will begin listening for incoming connections.

### Client-Side Setup

1. Navigate to the client-side directory.
2. Run the client-side script using the following command, replacing `{server IP address}` with the actual IP address of the server:

    ```bash
    python remote_sender.py -ip {server IP address}
    ```

   This command initiates a connection to the server using the specified IP address.

Once the server and client scripts are running, they will be able to communicate with each other as intended.

## Additional Information

- Make sure that both the server and the client are connected to the same network if you are running them locally.

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


### How to run the code


## Citation
If you use this code for your research, please cite:

```
@Article{electronics12143181,
AUTHOR = {Mtowe, Daniel Poul and Kim, Dong Min},
TITLE = {Edge-Computing-Enabled Low-Latency Communication for a Wireless Networked Control System},
JOURNAL = {Electronics},
VOLUME = {12},
YEAR = {2023},
NUMBER = {14},
ARTICLE-NUMBER = {3181},
URL = {https://www.mdpi.com/2079-9292/12/14/3181},
ISSN = {2079-9292},
DOI = {10.3390/electronics12143181}
}
```

## Contact
For any inquiry please contact us at our email addresses: danielmtowe@sch.ac.kr or dmk@sch.ac.kr

