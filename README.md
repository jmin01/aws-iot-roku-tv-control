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
These commands will update your apt repository, install and start node red, install the roku python package, and clone this git repository to your home directory. Once you clone the repository, edit the TVControlScript.py script using your favorite editor (nano is a good starting point) and add the IP address of your TV and the filepath to the aws-iot-roku-tv-control folder. Once you complete these steps, you're ready to configure Node-RED to listen for IoT button clicks and control your TV!
## Configuring Node-RED
Before proceeding, I recommend adding a username and password to access the Node-RED editor. Documentation can be found [here](https://nodered.org/docs/security). Using a web browser on your laptop/desktop, type in {Raspberry Pi Hostname}.local:1880 and load the page. Enter in your credentials and you'll be taken to a page where you can create your flows. On the left panel, you'll see a palette of different objects you can add to the canvas in the middle. 

![Node-RED Palette](https://s3.amazonaws.com/jmin01-github/aws-iot-roku-tv-control/Node-RED-1.jpg)

Add the mqtt (input), exec (advanced), and 2 file (storage) nodes to the canvas and make the connections using your mouse as shown below.

![Node Flows](https://s3.amazonaws.com/jmin01-github/aws-iot-roku-tv-control/Node-RED-2.jpg)

Now, we'll start configuring all the nodes to do what we want them to do, starting with mqtt.
### MQTT Node
Double-click on the mqtt node to edit. Under topic, add "iotbutton/{DSN of IoT Button", which should look something like: ```iotbutton/G030PJ293253CPDR```. Then, click the pencil button next to Server. Within the AWS console, go to the IoT service and open up your Raspberry Pi "thing" you previously created. Click on Interact and you'll see your IoT Button endpoint under HTTPS. it should look something like this ```z92lafwp0j62d3.iot.us-east-1.amazonaws.com```. Copy that endpoint and paste it into Server in Node-Red. Type 8883 into the port field. Add a check to "Enable Secure (SSL/TLS) Connection" and type in your thing name to Client ID. At this point, your screen should look something like this (minus the text in TLS configuration).

![MQTT Config](https://s3.amazonaws.com/jmin01-github/aws-iot-roku-tv-control/Node-RED-3.jpg)

Now, press the pencil icon next to TLS configuration. Remember those certificates you saved earlier for your Raspberry Pi? You'll need them here. Upload the Certificate and Private Key you downloaded. For the CA certificate, copy the text from [here](https://www.symantec.com/content/en/us/enterprise/verisign/roots/VeriSign-Class%203-Public-Primary-Certification-Authority-G5.pem), paste it into a text file, and name the text file rootCA.pem. Upload this file within the Node-RED configuration. At this point, your screen should look something like this.

![Upload Certs](https://s3.amazonaws.com/jmin01-github/aws-iot-roku-tv-control/Node-RED-4.jpg)

Hit "Update" twice and then "Done".
### Exec Node
Double-click the exec node and paste the command to execute your python script into the "Command" field. Output when the command is complete, and add a timeout of 10 seconds. Your screen should look something like this.

![exec node](https://s3.amazonaws.com/jmin01-github/aws-iot-roku-tv-control/Node-RED-5.jpg)

Press "Done".
### File (bottom)
Double-click the file node toward at bottom of the canvas, which will be where the button click information will be stored. Make the filename ```/home/{Raspberry Pi User}/aws-iot-roku-tv-control/buttonclicktype```, substituting {Raspberry Pi User} with the username you use to log into the Raspberry Pi. Select the action to overwrite file. Then press "Done".

### File (right)
Double-click the file node on the right-hand part of the canvas, which will be your debug log. Make the filename ```/home/{Raspberry Pi User}/aws-iot-roku-tv-control/debuglog.log```. Add a newline to each payload and click "Done".

Click deploy on the top-right of the screen and you should be all set!
