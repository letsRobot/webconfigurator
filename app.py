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
                               'configurator', 'lr_conf_file_dir')
                           ), 200


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


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html', e=e), 500


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

    debug_enabled = request.form['debug']
    port = request.form['port']
    lr_conf_file_dir = request.form['lr_conf_file_dir']

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

    return redirect('/advanced'), 200
