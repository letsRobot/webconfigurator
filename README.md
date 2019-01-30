# webconfigurator
Web server hosted on the robot for web-based configuration. Kept separate due to it's larger size and extra dependancies.

# THIS IS AN INCOMPLETE PRODUCT. IT CAN AND WILL HURT YOUR FILES. DO NOT INSTALL IF YOU DO NOT KNOW WHAT YOU ARE DOING.

## Installation
It's important that `/webconfigurator` be installed in the same directory as `/letsrobot` i.e., if LetsRobot is installed in `/home/pi/letsrobot`, then WebConfigurator needs to be installed in `/home/pi/webconfigurator`. Webconfigurator relies on your LetsRobot installation folder being called `letsrobot`. It will not work if it is set to anything else.

To install WebConfigurator, follow these steps:
1. Clone this repo: `git clone https://www.github.com/letsrobot/webconfigurator /home/pi/webconfigurator`
2. Step into the directory: `cd /home/pi/webconfigurator`
3. Install the prerequesites: `python -m pip install -r requirements.txt`
4. Add the following to your `start_robot` script:
```
cd /home/pi/webconfigurator
nohup python webconfigurator.py &> /dev/null &
```

## Configuration
(Some of these steps are planned and are not implemented yet.)

The WebConfigurator uses the same `.conf` file the rest of the LetsRobot suite uses. If the WebConfigurator cannot find the `[webconfigurator]` setting in the file, it adds the following to the bottom:
```
[webconfigurator]
enabled=True
port=80
debug=False
username=admin
password=admin
```
> `enabled=True` Tells the script whether or not it's allowed to run. Setting it to 'False' shuts down the server.

> `port=80` Tells the script which port to run the server on. Default is 80. Setting this value to 80 or 443 will make it so your web browser does not need to be told explicitly which port to run it on. If you choose another port, you will have to add `:{port}` to the end of the IP address or hostname of your robot.

> `debug=False` Enabling debug mode will slow down the page, but give more information when something goes wrong. You probably don't need to enable this unless you are a developer or a developer has asked you to.

> `username=admin` You can change this to set your username to log into the web page. It's recommended to change this from the default as soon as possible.

> `password=admin` This is the password to log into the web page. It's recommended to change this from the default as soon as possible, and to not use the same password you use to log into Let's Robot.