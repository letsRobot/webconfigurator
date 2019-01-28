from flask import Flask, render_template, request, redirect
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    file = open('.credentials', 'r')
    username = file.readline()
    password = file.readline()
    sent_username = request.form['username']
    sent_password = request.form['password']
    if username == sent_username and password == sent_password:
        return redirect('/home')
    return 401

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/easymode', methods=['GET', 'POST'])
def easymode():
    username = request.form['username']
    robotid = request.form['robotid']
    cameraid = request.form['cameraid']
    #_type = request.form['type']
    streamkey = request.form['streamkey']

    print("%s, %s, %s, %s", username, robotid, cameraid, streamkey)
    return redirect('/home')



if __name__ == '__main__':
    app.run(debug=True)