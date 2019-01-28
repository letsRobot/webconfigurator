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
Unconfigured.