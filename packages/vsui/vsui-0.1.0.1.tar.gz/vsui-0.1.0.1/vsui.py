from app import create_app, socketio

HOST = 'localhost'
PORT = 8000
application = create_app(debug=True)

if __name__ == '__main__':
    socketio.run(application, host=HOST, port=PORT)