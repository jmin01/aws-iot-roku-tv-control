# Controlling a Roku TV using the AWS IoT Button and a Raspberry Pi
This repository explains how to set up a Raspberry Pi to listen to AWS IoT Button clicks using the node-Red software and execute commands to a Roku smart TV using a Python script.
## Adding IoT Button and Raspberry Pi as IoT devices in the AWS Console
Follow the instructions that came with your IoT button to register the button as a device in the IoT Device Management service. For your Raspberry Pi, create/register a new device, filling out the appropriate fields to identify the device. Then, generate and download the appropriate certificates. You'll need these later to connect to the IoT button topic.
## Installing packages and setting up Node-RED 
SSH into your Raspberry Pi and execute the following commands, one line at a time.
```sh
sudo apt-get update
bash <(curl -sL https://raw.githubusercontent.com/node-red/raspbian-deb-package/master/resources/update-nodejs-and-nodered)
node-red-start
sudo systemctl enable nodered.service
pip install roku
cd ~
git clone https://github.com/jmin01/aws-iot-roku-tv-control/
sudo chmod 700 ~/aws-iot-roku-tv-control/TVControlScript.py
```
These commands will update your apt repository, install and start node red, install the roku python package, and clone this git repository to your home directory. Once you complete these steps, you're ready to configure Node-RED to listen for IoT button clicks and control your TV!
## Configuring Node-RED

