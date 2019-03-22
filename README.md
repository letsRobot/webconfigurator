# webconfigurator
Web server hosted on the robot for web-based configuration. Kept separate due to it's larger size and extra dependancies.

## Installation
To install WebConfigurator, follow these steps:
1. Clone this repo: `git clone https://www.github.com/letsrobot/webconfigurator`
2. Install the prerequesites: `python -m pip install -r requirements.txt`

## Configuration
(Some of these steps are planned and are not implemented yet.)

This program uses its own settings file, `settings.conf`. It has a similar hierarchy to `letsrobot.conf`.

```
[configurator]
debug=true
port=8080
lr_conf_file_dir=letsrobot.conf
```
`port` is unimplemented.

> `port=8080` Tells the script which port to run the server on. Default is 8080. Setting this value to 80 or 443 will make it so your web browser does not need to be told explicitly which port to run it on. If you choose another port, you will have to add `:{port}` to the end of the IP address or hostname of your robot.

> `debug=True` Enabling debug mode will slow down the page, but give more information when something goes wrong. You probably don't need to enable this unless you are a developer or a developer has asked you to.

```
[login]
enabled=true
username=admin
password=admin
```
> `enabled=true` The login prompt can be disabled if you so choose. This is not recommended.

> `username=admin` You can change this to set your username to log into the web page. It's recommended to change this from the default as soon as possible.

> `password=admin` This is the password to log into the web page. It's recommended to change this from the default as soon as possible, and to not use the same password you use to log into Let's Robot.

```
[sixy_mode]
enabled=false
controls=true
chatroom=
robot=
robot_id=
```

> `enabled=false` Turning on sixy mode replaces the site with a single page that has a chatroom, and optional controls.

> `controls=true` Disabling controls just gives the screen a chatroom. 

> `chatroom=` You need to put your username or `global` here in order for the chat to work.

> `robot=` This is the name of your robot. You need it for sending control commands.

> `robot_id=` This is the ID of your robot. You need it for sending control commands.

## Running
you can run with the following command
```
python3 -m flask run
```

To allow remote connections (i.e., your phone or another computer), add
```
--host=0.0.0.0
```

To change the port, add
```
--port={port}
```
