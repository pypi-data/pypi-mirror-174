import os
from pathlib import Path
from .. import definitions
from . import utils
from . import config as cfg
from .task_management import tasks
from .. import socketio
import logging

class Process():
    def __init__(self, name: str,
     directory_path: os.PathLike,
     launch_path: os.PathLike,
     launch_args: dict,
     task_schema: dict,
     settings_schema: dict,
     settings: dict) -> None:
        self.name = name
        self.directory_path = directory_path
        self.launch_path = launch_path
        self.launch_args = launch_args
        self.task_schema = task_schema
        self.settings_schema = settings_schema
        self.settings = settings
        self.namespaces_dict = {
            'settings': self.settings,
            'args': self.launch_args
        }

    def get_setting_by_id(self, id):
        try:
            return self.settings.__dict__[id]
        except KeyError:
            for key in self.settings.__dict__:
                if isinstance(self.settings.__dict__[key], dict):
                    try:
                        return self.settings.__dict__[key][id]
                    except KeyError:
                        logging.error(f'could not find ({id}) in {key}')
            logging.error(f'could not find {id} in first 2 levels')

    def set_namespace_by_id(self, id, value, namespace='settings'):
        # what namespace are we looking at
        namespace = self.namespaces_dict[namespace]
        try:
            # try on the first level to set the key we are looking for
            namespace.__dict__[id] = value
        except KeyError:
            # if it couldn't be found look one level deeper
            # XXX this logic should be greatly improved
            for key in namespace.__dict__:
                if isinstance(namespace.__dict__[key], dict):
                    try:
                        namespace.__dict__[key][id] = value
                        break
                    except KeyError:
                        logging.error(f'could not find ({id}) in {key}')
            logging.error(f'could not find {id} in first 2 levels')
            
    def export_settings(self, path):
        ''' creates a settings directory at the target path if one doesn't already exist and saves this process's settings '''
        utils.write_settings_data(self.settings, path / cfg.SETTINGSDIR /  Path(self.name+'.yaml'))

    def launch(self, task_name):
        task_root_dir = cfg.get_WORKINGDIR() / Path(task_name)
        print(f'starting new task in {task_root_dir}')
        # write the settings file for the new task
        self.export_settings(task_root_dir)
        # create the task
        tasks.create_task(
            id = task_name,
            struct = self.task_schema,
            launch_path = self.launch_path,
            launch_args = self.launch_args,
            root_path = task_root_dir
            )
            
    def __repr__(self) -> str:
        return 'Process: ' + self.name + '\n launch: ' + str(self.launch_path)# + '\n settings: ' + str(self.settings_schema)

class ProcessManager():
    def __init__(self) -> None:
        self.processes = []

    def LoadProcesses(self, path):
        ''' Search for available process definitions '''
        subfolders_with_paths = [f.path for f in os.scandir(path) if f.is_dir()]
        for process_directory in subfolders_with_paths:
            launch_path = Path(process_directory) / Path('launch.sh')
            task_schema_path = Path(process_directory) / Path('task_schema.json')
            launch_args_path = Path(process_directory) / Path('launch_args.yaml')
            settings_schema_path = Path(process_directory) / Path('settings_schema.json')
            settings_path = Path(process_directory) / Path('settings.yaml')
            # is the launch file there
            if os.path.exists(launch_path):
                # everything required is there - add a new process
                self.processes.append(Process(
                    name = os.path.basename(os.path.normpath(process_directory)),
                    directory_path = process_directory,
                    launch_path = launch_path,
                    task_schema = utils.read_json(task_schema_path),
                    launch_args = utils.get_settings_data(launch_args_path),
                    settings_schema = utils.read_json(settings_schema_path),
                    settings = utils.get_settings_data(settings_path)
                ))
                print(self.processes[-1])
            else:
                # all processes need a launch file, if one cannot be found do not add
                logging.error(f'no launch file found')

    def export_processes(self):
        ''' returns {'name': str, 'settings_schema': dict}'''
        out = []
        for process in self.processes:
            out.append({'name': process.name, 'settings_schema': process.settings_schema})
        return out
    
    def get_process_by_name(self, name):
        for process in self.processes:
            if process.name == name:
                return process
        return None
    
    def get_setting(self, process_name, setting_id):
        target_process = self.get_process_by_name(process_name)
        setting_value = target_process.get_setting_by_id(setting_id)
        return setting_value
        #socketio.emit('setting_update', {process_name: {setting_id: setting_value}})
    
    def change_setting(self, process_name: str, setting_id: str, data: dict, namespace: str = 'settings'):
        target_process = self.get_process_by_name(process_name)
        target_process.set_namespace_by_id(id=setting_id, value=data, namespace=namespace)
    
    def launch_process(self, process_name, task_name):
        ''' Take the requested process and launch it as a new task '''
        self.get_process_by_name(process_name).launch(task_name)

processes = ProcessManager()
processes.LoadProcesses(definitions.PROCESS_DIR)
