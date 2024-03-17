from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)


@app.route('/')
def Index():
    return render_template('index.html')

@socketio.on('code_change')
def handle_code_change(data):
    code = data['code']
    emit('code_change', {'code': code}, broadcast=True)



if __name__ == '__main__':
    app.run(debug=True,use_reloder=True)
    socketio.run(app)