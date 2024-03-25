
Last updated: March 25, 2024

# Local-Side Architecture

This document provides instructions for setting up the local-side code for a remote communication system. It outlines the steps to run the local side code and explains its purpose in conjunction with the server-side code. Please follow these guidelines to ensure proper functioning of the system.


## Local-Side Setup Instructions

Follow these steps to set up the local-side code on your local machine:

1. **Download:** Obtain the local-side code from the repository [link to repository](https://github.com/sihsch/EC-LLC-WNCS/archive/refs/heads/main.zip).

2. **Install Dependencies:** 

3. **Run the Local-Side Code:** Launch the local-side code by executing the main script. For example: `python remote_sender.py ip {server ip address}`.

4. **Verify Connectivity:** Ensure that the local-side code can establish a connection with the server. Check the console output or logs for any messages indicating successful connection establishment.

## Usage and Interaction

Once the local-side code is running and successfully connected to the server, it can interact with the remote devices through the server-side code. The local-side code acts as a bridge between the user interface or local sensors and the remote devices.

To utilize the system effectively, follow these general guidelines:

1. **Data Exchange:** The local-side code will facilitate the transfer of data between the user interface or local sensors and the remote devices. Ensure that the necessary data is exchanged appropriately to achieve the desired results.

2. **Monitor and Troubleshoot:** Keep an eye on the local-side code's logs or console output to track the communication with the server and any potential issues. Check the documentation or troubleshooting guide for guidance on resolving common problems.

## Conclusion

By following these instructions, you should have successfully set up the local-side code for remote communication. Remember to ensure that the server-side code is running first before launching the local-side code to establish a connection. Should you encounter any difficulties or require further assistance, consult the documentation or reach out to the appropriate support channels.


## How to Run the Source Code

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


