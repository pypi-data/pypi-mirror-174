import os
from pathlib import Path
from .. import socketio

WORKINGDIR = os.path.expanduser('~')
def set_WORKINGDIR(value):
    global WORKINGDIR
    print(f'setting working dir to {value}')
    socketio.emit('server_working_dir', value)
    WORKINGDIR = value

def get_WORKINGDIR():
    return WORKINGDIR

SETTINGSDIR = Path('settings')