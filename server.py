from flask import Flask, render_template, request, jsonify
import socket_worker
from threading import Thread
import os 
import time

app = Flask(__name__)

loggedin = False

forts = None

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/send', methods = ['POST'])
def handleData():
    global forts
    forts = None
    if not loggedin:
        return jsonify({'status': 'nologin', 'message': 'User not logged in.'}), 200
    data = request.get_json()
    print(data)
    
    def run_scan(data):
        global forts
        if data['type'] == 'base': 
            coords = data['coords']
            x, y = map(int, coords.split(','))  # Make sure x, y are integers
            forts = socket_worker.spiral_scan(x, y)  # Call the function
        else:
            forts = socket_worker.normal_scan()  # Add () to call the function

    Thread(target=run_scan, args=(data,), daemon=True).start()

    return jsonify({'status': 'success'}), 200




@app.route('/progress')
def progressdata():
    print(socket_worker.count)
    return jsonify({'count' : socket_worker.count if socket_worker.count > 0 else 1})


@app.route('/getdata')
def getData():
    global forts
    return render_template('forts.html', fortss = forts)


@app.route('/login', methods=['POST'])
def login():
    global loggedin
    data = request.get_json()
    print(data)
    socket_worker.validate(data)
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'status': 'error', 'message': 'Username and password are required.'}), 400
    
    try:
        if not socket_worker.initialize_socket(username, password):
            return jsonify({'status': 'loginerror', 'message': 'Login failed. Check your credentials.'}), 200
        userdata = socket_worker.getuserinfo()
        name = userdata['payload']['data']['PN']
        email = userdata['payload']['data']['E']
        loggedin = True

        return jsonify({'status': 'success', 'message': 'Login successful.', 'name': name, 'email': email}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
    
@app.route('/logstat', methods=['POST'])
def logstat():
    global loggedin
    if loggedin:
        return jsonify({'status': 'success', 'message': 'User is logged in.'}), 200
    else:
        return jsonify({'status': 'error', 'message': 'User is not logged in.'}), 200

if __name__ == '__main__':
    # if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
    #     socket_worker.initialize_socket()
    app.run(debug=True)


