from flask import Flask, jsonify, render_template
from flask.json import load
from flask_restful import Resource, Api, marshal_with
from flask_socketio import SocketIO, emit, send
from threading import Thread
import time
from pymongo import MongoClient
import socketio,os,json
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()
#Call the Flask framework and create a secret Key
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!' 
socketio = SocketIO(app,cors_allowed_origins='*')
CORS(app)
thread = None
clients = 0
_host = os.getenv("mongohost")
_port = int(os.getenv("mongoport"))
_client = MongoClient(_host,_port)
_db = _client["frontend"]


def ini_socket():
    global clients, thread,status 
    thread = None


@app.route('/api/socket')
def index():
    print('Route socket init')
    global thread
    if thread is None:
        thread = Thread(target=ini_socket)
        print('Creating Thread')
        thread.start()
    return ('{"ok":"success"}')

@socketio.on('connect')
def test_connect():
    global clients
    clients += 1
    print('Client connected test')
    

@socketio.on('start')
def start():
    status = True
    coll = _db["pricedata"]
    while (status == True):
        change_stream = _db["pricedata"].watch()
        document = next(change_stream)
        doc = document['fullDocument']
        doc.pop("_id")
        doc1 = json.dumps(doc)
        emit('frontend',doc1)

        
@socketio.on('disconnect')
def test_discoonect():
    global clients, status
    status = False
    clients -= 1
    print('Client Disconnected')

if __name__ == '__main__':
    print('Starting WebService')
    socketio.run(app,host='localhost',port=9200)