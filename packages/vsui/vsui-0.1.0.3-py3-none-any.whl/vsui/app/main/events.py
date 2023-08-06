from flask import request
import os
from .. import socketio
from .task_management import tasks
from .client_management import Client, clients
from .processes import processes
from .utils import explore
from . import config as cfg

@socketio.on('connect')
def connect():
    sid = request.sid
    type = request.headers.get('type')
    id = request.headers.get('id')
    if type is None:
        print('Client Type is None')
        return None
    if id is None:
        print('client did not provide an id')
    clients.add_client(sid, type, id)
    print(f'{type} client connected with sid {sid}')
    print(f'clients: {clients}')
    # export the available processes this session can run
    socketio.emit('available_processes', processes.export_processes())
    # export the current structure of the tasks
    exp_tasks = tasks.struct()
    socketio.emit('tasks', exp_tasks)

@socketio.on('disconnect')
def app_disconnect():
    sid = request.sid
    clients.remove_by_sid(sid)
    print(f'disconnected')
    print(f'clients: {clients}')

@socketio.on('notify')
def notify(data):
    ''' pass on the toast '''
    socketio.emit('toast', data)

@socketio.on('launch_process')
def launch_new_task(data):
    # data {'process_id': str, 'task_id': str}
    processes.launch_process(data['process_id'], data['task_id'])

@socketio.on('deactivate_task')
def deactivate_task(id):
    print(f'deactivating task {id}')
    tasks.deactivate_task(id)

@socketio.on('request_is_task_id_unique')
def check_task_id_unique(id):
    if tasks.get_by_id(id) is None:
        return True
    else:
        return False

@socketio.on('edit_element')
def edit_element(data):
    ''' overwrite an element's data, targeted by the id of the parent task and the element's unique key'''
    tasks.write_element(data['task_id'],data['element_key'],data['value'])

@socketio.on('request_update')
def request_update(data):
    ''' handle a request for a component's data to be updated '''
    tasks.update_component(data['task_id'], data['key'])

@socketio.on('request_setting')
def request_setting(data):
    ''' handle a request for a setting's default value to be populated'''
    return processes.get_setting(data['process_id'], data['setting_id'])

@socketio.on('setting_change')
def setting_change(data):
    processes.change_setting(data['process_id'], data['setting_id'], data['data'], data['namespace'])

# both of these do the same, only the events emitted are different so the web knows to append to history or not
@socketio.on('request_directory_contents')
def explore_directory(path):
    error, contents = explore(path)
    return {'path': path, 'status': error, 'contents': contents}

@socketio.on('request_filetype')
def check_filetype(path):
    if os.path.isdir(path):
        return 'dir'
    else:
        return 'file'

@socketio.on('web_working_dir')
def change_working_dir(path):
    cfg.set_WORKINGDIR(path)

@socketio.on('request_working_dir')
def get_working_dir():
    return cfg.get_WORKINGDIR()
