import os.path
import argparse
import os

from configparser import ConfigParser
from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

local_config = ConfigParser()
local_config.read('settings.conf')
robot_config = ConfigParser()

debug_enabled = None
port = None
lr_conf_file_dir = None

login_enabled = None
login_username = None
login_password = None

sixy_enabled = None
sixy_controls = None
sixy_robot = None
sixy_robot_id = None

def setup():
    global debug_enabled
    global port
    global lr_conf_file_dir
    global login_enabled
    global login_username
    global login_password
    global sixy_enabled
    global sixy_controls
    global sixy_robot
    global sixy_robot_id

    debug_enabled = local_config.getboolean('configurator', 'debug')
    port = local_config.getint('configurator', 'port')
    lr_conf_file_dir = local_config.get('configurator', 'lr_conf_file_dir')
    login_enabled = local_config.getboolean('login', 'enabled')
    login_username = local_config.get('login', 'username')
    login_password = local_config.get('login', 'password')

    robot_config.read(lr_conf_file_dir)

@app.route('/update/simple', methods=['POST'])
def simple_update():
    username = request.form['username']
    robot_id = request.form['robot_id']
    camera_id = request.form['camera_id']
    robot_type = request.form['type']
    stream_key = request.form['stream_key']
    api_key = request.form['api_key']

    os.system("sed -i '/^\\[robot]/,/^\\[/{s/^owner[[:space:]]*=.*/owner=%s/}' %s" % (username, lr_conf_file_dir))
    os.system("sed -i '/^\\[robot]/,/^\\[/{s/^robot_id[[:space:]]*=.*/robot_id=%s/}' %s" % (robot_id, lr_conf_file_dir))
    os.system("sed -i '/^\\[robot]/,/^\\[/{s/^camera_id[[:space:]]*=.*/camera_id=%s/}' %s" % (camera_id, lr_conf_file_dir))
    os.system("sed -i '/^\\[robot]/,/^\\[/{s/^type[[:space:]]*=.*/type=%s/}' %s" % (robot_type, lr_conf_file_dir))
    os.system("sed -i '/^\\[robot]/,/^\\[/{s/^stream_key[[:space:]]*=.*/stream_key=%s/}' %s" % (stream_key, lr_conf_file_dir))
    os.system("sed -i '/^\\[robot]/,/^\\[/{s/^api_key[[:space:]]*=.*/api_key=%s/}' %s" % (api_key, lr_conf_file_dir))

    return redirect('/')
    

@app.route('/')
def index():
    return render_template(
        'index.html', 
        username="username",
        robot_id="robot_id",
        camera_id="camera_id",
        type="type",
        stream_key="stream_key",
        api_key="api_key")

if __name__ == "__main__":
    setup()
    app.run(debug=debug_enabled, host="0.0.0.0", port=port)
