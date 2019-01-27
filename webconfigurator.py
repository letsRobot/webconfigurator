from flask import Flask, render_template, request, redirect
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/easymode')
def easymode():
    username = request.form['username']
    robotid = request.form['robotid']
    cameraid = request.form['cameraid']
    #_type = request.form['type']
    streamkey = request.form['streamkey']

    print("%s, %s, %s, %s", username, robotid, cameraid, streamkey)
    return redirect('/')



if __name__ == '__main__':
    app.run()