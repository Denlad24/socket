from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import sys

sys.path.append(
    "C:/Users\Denis\Documents/5 курс\Инженерия информационных систем\socketio\Flask-SocketIO-master\example")
import model

async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
# thread = None
# thread_lock = Lock()


# def background_thread():
#     """Example of how to send server generated events to clients."""
#     count = 0
#     while True:
#         socketio.sleep(10)
#         count += 1
#         socketio.emit('my_response',
#                       {'data': 'Server generated event', 'count': count},
#                       namespace='/test')


@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)


@socketio.on('my_broadcast_event', namespace='/test')
def test_broadcast_message(message):
    note = message['data2']
    id = message['data']
    model.save_note(id, note)
    rez = model.get_note(id)
    emit('my_response',
         {'data': rez, 'id': id},
         broadcast=True)


@socketio.on('my_delete_2', namespace="/test")
def delete_note2(message):
    id = message["data"]
    model.delete_note(id)
    emit('my_delete_response_2', {'data': id}, broadcast=True)


@socketio.on('my_delete_note', namespace='/test')
def delete_note(message):
    id = message["data"]
    mes1 = 'Заметка удалена'
    mes2 = 'Заметки с таким id нет'
    try:
        model.delete_note(id)
        emit('my_delete_response', {'data': mes1}, broadcast=True)
        emit('my_delete_response_2', {'data': id}, broadcast=True)
    except KeyError:
        print('Заметки с таким id нет')
        emit('my_delete_response', {'data': mes2}, broadcast=True)


@app.route("/view", methods=["POST"])
def get_note():
    id = request.form["id"]
    rez = model.get_note(id)
    return render_template('view_one.html', v=rez, flag=0)


@app.route("/view_all", methods=["POST"])
def get_notes():
    rez = model.get_notes()
    return render_template('view_all.html', v=rez)


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected', request.sid)


if __name__ == '__main__':
    socketio.run(threaded=True, port=5000)
