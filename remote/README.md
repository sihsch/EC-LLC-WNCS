
Last updated: July 10, 2022


#  Remote Side Architecture

This document provides instructions for setting up the server-side code for a remote communication system. It outlines the steps to run the server code and explains its purpose in conjunction with the local side code. Please follow these guidelines to ensure proper functioning of the system.

## Prerequisites

Before proceeding, ensure that the following prerequisites are met:

1. **Operating System:** The server-side code is designed to run on a compatible operating system, such as Linux or Windows.

2. **Server Environment:** Make sure you have a server or a machine designated for running the server-side code. This server should have the necessary network connectivity and permissions to communicate with the remote devices.

3. **Required Software:** The server-side code relies on specific software dependencies. Ensure the following software is installed:
   - [Python](https://www.python.org/) 
   - [OpenCV ]

## Server Setup Instructions

Follow these steps to set up the server-side code on your server machine:

1. **Download:** Obtain the server-side code from the repository [link to repository](https://github.com/sihsch/EC-LLC-WNCS/archive/refs/heads/main.zip).

2. **Install Dependencies:** 

3. **Run the Server:** Launch the server-side code by executing the main scripts or using the provided command. For example: `python remote_receiver.py`.

4. **Verify Connectivity:** Ensure that the server is up and running without any errors. Check the server logs or console output for any messages indicating successful initialization.

## Usage and Interaction

Once the server-side code is running, it will be ready to accept connections and interact with the local side code. The server acts as a central hub, facilitating communication and data exchange between the remote devices and the local side.

To utilize the system effectively, follow these general guidelines:

1. **Connect Remote Devices:** Ensure that the remote devices are configured to connect to the server. Update the network settings or connection parameters on the remote devices to establish communication with the server.

2. **Local Side Configuration:** Configure the local side code, ensuring it is set to communicate with the correct server IP address or hostname, port number, and any necessary authentication credentials. Refer to the documentation or instructions provided with the local side code for specific configuration details.

3. **Run Local Side Code:** Start the local side code on the respective devices or machines. This code will establish a connection with the server and initiate communication.

4. **Monitor and Troubleshoot:** Keep an eye on the server-side logs, console output, or any provided monitoring tools to track the communication and address any potential issues. Check the documentation or troubleshooting guide for guidance on resolving common problems.

## Conclusion

By following these instructions, you should have successfully set up the server-side code for remote communication. Remember to run the server-side code first before launching the local-side code to establish proper communication channels. Should you encounter any difficulties or require further assistance, consult the documentation or reach out to the appropriate support channels.


## How to Run the Source Code

| Syntax      | Description (Remote side) |
| ----------- | ----------- |
| PID.py              | PID algorithm for smoothly tracking the line       |
| imgProcessing.py    | For extracting useful information from the image         |
| remote_receiver.py  | Receive an image from (remote_sender.py), process it, and return a control command        |
| edge1_receiver.py   | Receive semi-processed information from (edgelv1.py), finalize the processing, and return a control command       |
| edge2_receiver.py   | Receive semi-processed information from (edgelv2.py), finalize the processing, and return a control command       |
| edge3_receiver.py   | Receive semi-processed information from (edgelv3.py), finalize the processing, and return a control command       |
| adaptive_receiver.py| Receive from (adaptive_sender.py) communication       |



