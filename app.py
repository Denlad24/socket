from flask import Flask, render_template
from flask.ext.socketio import SocketIO
import json

app = Flask(__name__)
socketio = SocketIO(app)

@app.route("/")
def index():
  return render_template('index.html',)

@socketio.on('send_message')
def handle_source(json_data):

if __name__ == "__main__":
app.run(threaded=True, port=5000)