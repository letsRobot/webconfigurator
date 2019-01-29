import os.path
import argparse
import sys

from configparser import ConfigParser
from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

logged_in = False
'''
robot_config = ConfigParser()

try:
    robot_config.readfile(open('../letsrobot/letsrobot.conf'))
except IOError:
    print("unable to read letsrobot.conf, please check that you have copied letsrobot.sample.conf to letsrobot.conf and modified it.")
    sys.exit()
except:
    print("error in letsrobot.conf:", sys.exc_info()[0])
    sys.exit()

# robot
owner = robot_config.get('robot', 'owner')
robot_id = robot_config.get('robot', 'robot_id')
camera_id = robot_config.get('robot', 'camera_id')
'''

@app.route('/')
def index():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    global logged_in
    error = None
    if request.method == 'POST':
#        if request.form['username'] != robot_config.get('webconfigurator', 'username') or request.form['password'] != robot_config.get('webconfigurator', 'password'):
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid credentials. Please try again.'
        else:
            logged_in = True
            return redirect(url_for('home'))
    return render_template('login.html', error=error)


@app.route('/home')
def home():
    global logged_in
    if logged_in:
        return render_template('index.html')
    return redirect('/')


@app.route('/easymode', methods=['GET', 'POST'])
def easymode():
    username = request.form['username']
    robotid = request.form['robotid']
    cameraid = request.form['cameraid']
    #_type = request.form['type']
    streamkey = request.form['streamkey']

    #
    # Print is a placeholder for when letsrobot.conf actually gets modified.
    # I'd also like to populate with values from letsrobot.conf when the page
    # is loaded.
    #
    print("{}, {}, {}, {}".format(username, robotid, cameraid, streamkey))

    return redirect('/home')

@app.route('/advancedmode', methods=['GET', 'POST'])
def advancedmode():
    return render_template('advanced.html')

if __name__ == '__main__':
#    if robot_config.get('webconfigurator', 'enabled') == True:
#        app.run(debug=robot_config.get('webconfigurator', 'debug'), port=robot_config.get('webconfigurator', 'port'))
    app.run(debug=True, port=80)
