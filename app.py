import argparse
import os
import os.path
from configparser import ConfigParser
from datetime import datetime

from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)

app = Flask(__name__)

now = datetime.now()
start_time = now

local_config = ConfigParser()
local_config.read('settings.conf')
robot_config = ConfigParser()
debug_enabled = local_config.getboolean('configurator', 'debug')
port = local_config.getint('configurator', 'port')
lr_conf_file_dir = local_config.get('configurator', 'lr_conf_file_dir')

robot_config.read(lr_conf_file_dir)

sixy_enabled = local_config.getboolean('sixy_mode', 'enabled')
sixy_controls = local_config.getboolean('sixy_mode', 'controls')
chatroom = local_config.get('sixy_mode', 'chatroom')
sixy_robot = local_config.get('sixy_mode', 'robot')
sixy_robot_id = local_config.get('sixy_mode', 'robot_id')


if __name__ == "__main__":
    app.run(debug=debug_enabled, host="0.0.0.0", port=port)


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon'), 200


@app.route('/advanced')
def advanced():
    global robot_config
    return render_template('advanced.html', robot_config=robot_config), 200


@app.route('/options')
def options():
    return render_template('options.html',
                           debug=local_config.get('configurator', 'debug'),
                           port=local_config.get('configurator', 'port'),
                           lr_conf_file_dir=local_config.get(
                               'configurator', 'lr_conf_file_dir'),
                           login_enabled=local_config.getboolean(
                               'login', 'enabled'),
                           login_username=local_config.get(
                               'login', 'username'),
                           login_password=local_config.get(
                               'login', 'password'),
                           sixy_enabled=local_config.get(
                               'sixy_mode', 'enabled'),
                           sixy_controls=local_config.get(
                               'sixy_mode', 'controls'),
                           sixy_robot=local_config.get('sixy_mode', 'robot'),
                           sixy_robot_id=local_config.get(
                               'sixy_mode', 'robot_id')
                           ), 200


@app.route('/sixy')
def sixy():
    global chatroom
    global sixy_controls
    global sixy_enabled
    global sixy_robot
    global sixy_robot_id
    controls = dict(**chatroom, **sixy_controls, **sixy_enabled, **sixy_robot,
        **sixy_robot_id)
    return render_template('sixy.html', controls=controls), 200


@app.route('/')
def index():
    global start_time
    username = robot_config.get('robot', 'owner')
    robot_id = robot_config.get('robot', 'robot_id')
    camera_id = robot_config.get('robot', 'camera_id')
    robot_type = robot_config.get('robot', 'type')
    stream_key = robot_config.get('robot', 'stream_key')
    api_key = robot_config.get('robot', 'api_key')

    content = {
        "username": username,
        "robot_id": robot_id,
        "camera_id": camera_id,
        "type": robot_type,
        "stream_key": stream_key,
        "api_key": api_key,
        "now": start_time
    }
    return render_template(
        'index.html',
        **content
    ), 200


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/api/update/simple', methods=['POST'])
def simple_update():
    username = request.form['username']
    robot_id = request.form['robot_id']
    camera_id = request.form['camera_id']
    robot_type = request.form['type']
    stream_key = request.form['stream_key']
    api_key = request.form['api_key']

    os.system(
        "sed -i '/^\\[robot]/,/^\\[/{s/^owner[[:space:]]*=.*/owner=%s/}' %s" % (username, lr_conf_file_dir))
    os.system(
        "sed -i '/^\\[robot]/,/^\\[/{s/^robot_id[[:space:]]*=.*/robot_id=%s/}' %s" % (robot_id, lr_conf_file_dir))
    os.system(
        "sed -i '/^\\[robot]/,/^\\[/{s/^camera_id[[:space:]]*=.*/camera_id=%s/}' %s" % (camera_id, lr_conf_file_dir))
    os.system("sed -i '/^\\[robot]/,/^\\[/{s/^type[[:space:]]*=.*/type=%s/}' %s" % (
        robot_type, lr_conf_file_dir))
    os.system("sed -i '/^\\[robot]/,/^\\[/{s/^stream_key[[:space:]]*=.*/stream_key=%s/}' %s" % (
        stream_key, lr_conf_file_dir))
    os.system(
        "sed -i '/^\\[robot]/,/^\\[/{s/^api_key[[:space:]]*=.*/api_key=%s/}' %s" % (api_key, lr_conf_file_dir))

    return redirect('/'), 200


@app.route('/api/update/options', methods=['POST'])
def options_update():
    global debug_enabled
    global port
    global lr_conf_file_dir
    global login_enabled
    global login_password
    global login_username
    global sixy_enabled
    global sixy_controls
    global sixy_robot
    global sixy_robot_id

    debug_enabled = request.form['debug']
    port = request.form['port']
    lr_conf_file_dir = request.form['lr_conf_file_dir']
    login_enabled = request.form['login_enabled']
    login_username = request.form['login_username']
    login_password = request.form['login_password']
    sixy_enabled = request.form['sixy_enabled']
    sixy_controls = request.form['sixy_controls']
    sixy_robot = request.form['sixy_robot']
    sixy_robot_id = request.form['sixy_robot_id']

    return redirect('/options'), 200


@app.route('/api/update/advanced', methods=['POST'])
def advanced_update():
    global robot_config
    global lr_conf_file_dir
    sections = robot_config.sections()
    for section in sections:
        items = dict(robot_config.items(section))
        for item in items:
            query = str(section + " " + item)
            result = request.form[query]
            os.system("sed -i '/^\\[%s]/,/^\\[/{s/^%s[[:space:]]*=.*/%s=%s/}' %s" % (
                section, item, item, result, lr_conf_file_dir))
