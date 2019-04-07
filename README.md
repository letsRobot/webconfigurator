# webconfigurator
Web server hosted on the robot for web-based configuration. Kept separate due to it's larger size and extra dependancies.

## Installation
To install WebConfigurator, follow these steps:
1. Clone this repo: `git clone https://www.github.com/letsrobot/webconfigurator`
2. Install the prerequesites: `python -m pip install flask`

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
`debug` is unimplemented.
> `debug=True` Enabling debug mode will slow down the page, but give more information when something goes wrong. You probably don't need to enable this unless you are a developer or a developer has asked you to.

## Running
you can run with the following command
```
python -m flask run
```

To allow remote connections (i.e., your phone or another computer), add
```
--host=0.0.0.0
```

To change the port, add
```
--port={port}
```

Port 80 and 443 are protected by root, so to use those ports you must run with `sudo`.

If you do not want to specify a port in your web browser when you connect to the page, set the port to 80. By default, Flask sets the port to 5000.

## Auto-starting when your robot does.
You can add this to your `start_robot` file:
```
cd /home/pi/webconfigurator
sudo python -m flask --host=0.0.0.0 --port=80 &> /dev/null &
```
