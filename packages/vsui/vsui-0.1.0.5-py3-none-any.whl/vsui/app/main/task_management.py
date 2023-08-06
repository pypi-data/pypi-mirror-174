import logging
from os import PathLike
from typing import Union, Any
from .. import socketio
import subprocess
from . import utils

class TaskElement():
    '''Represents one type of data to be displayed, keys should be unique identifiers.'''
    def __init__(self, key: str, task_id: str) -> None:
        super(TaskElement, self).__init__()
        self.key = key
        self.task_id = task_id

    @property
    def type() -> None:
        return 'TaskElement'

    def __repr__(self) -> str:
        return str(type(self))

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, TaskElement):
            return self.key == __o.key

class Progress(TaskElement):
    '''Signifies a Progress Bar.'''
    def __init__(self, key: str, task_id: str) -> None:
        super().__init__(key, task_id)
        # {'current' : x, 'max' : x}
        self.data = {"current": 0, "max": 1}

    @property
    def component(self) -> str:
        return 'ProgressElement'

    def struct(self) -> dict:
        return {"key": self.key, "component": self.component}

    def set(self, value: dict) -> None:
        ''' set data to a new dictionary '''
        self.data = value
        self.update()

    def update(self) -> None:
        socketio.emit('progress_data_update', {self.task_id: {self.key: self.data}})

class Chart(TaskElement):
    ''' Signifies a plot on a 2D graph.'''
    def __init__(self, key: str, task_id: str, label_x: str = '', label_y: str = '') -> None:
        super().__init__(key, task_id)
        self.labels = {"label_x": label_x, "label_y": label_y}
        self.data = {"x": [], "y": []}

    @property
    def component(self) -> str:
        return 'ChartElement'

    def struct(self) -> dict:
        return {"key": self.key, "component": self.component, "labels": self.labels}

    def set(self, value: dict) -> None:
        self.data = value
        self.update()
    
    def update(self) -> None:
        socketio.emit('chart_data_update', {self.task_id: {self.key: self.data}})


class Log(TaskElement):
    '''Signifies a console log - style scrolling output / text data'''
    def __init__(self, key: str, task_id: str) -> None:
        super().__init__(key, task_id)
        self.data = []

    @property
    def component(self) -> str:
        return 'LogElement'

    def struct(self) -> dict:
        return {"key": self.key, "component": self.component}

    # XXX should be append, but doesn't play well with structure of other elements
    def set(self, value: str) -> None:
        ''' adds a log or list of logs to the end of the log '''
        if isinstance(value, list):
            self.data = self.data + value
        elif isinstance(value, str):
            self.data.append(value)
        self.update()

    def update(self) -> None:
        socketio.emit('log_data_update', {self.task_id: {self.key: self.data}})

class Gallery(TaskElement):
    '''Signifies an image gallery '''
    def __init__(self, key: str, task_id: str) -> None:
        super().__init__(key, task_id)
        # list of base64 encoded images
        self.data = []
        self.reference = []

    @property
    def component(self) -> str:
        return 'GalleryElement'

    def struct(self) -> dict:
        return {"key": self.key, "component": self.component}

    # XXX should be append, but doesn't play well with structure of other elements
    def set(self, value: str) -> None:
        ''' appends the new image to the gallery '''
        print('setting image')
        if "data" in value:
            print('data images')
            self.add_data(value["data"])
        elif "reference" in value:
            print('reference images')
            self.add_reference(value["reference"])

    def add_reference(self, value) -> None:
        self.reference.append(value)
        self.update()

    def add_data(self, value) -> None:
        self.data.append(value)
        self.update()

    def update(self) -> None:
        socketio.emit('gallery_data_update', {self.task_id: {self.key: self.data}})
        socketio.emit('gallery_reference_update', {self.task_id: {self.key: self.reference}})

class Task():
    '''Represents one running process, id is a unique identifier for this task,
    mainly a list of task elements that compose the UI required by this process'''
    def __init__(self, id: str,
    struct: dict,
    launch_path: PathLike,
    launch_args: dict,
    root_path: PathLike) -> None:
        print(launch_args)
        self.id = id
        elements = []
        self.active = True
        for k, type in struct.items():
            if type == 'progress':
                elements.append(Progress(key=k, task_id=id))
            elif type == 'chart':
                elements.append(Chart(key=k, task_id=id))
            elif type == 'log':
                elements.append(Log(key=k, task_id=id))
            elif type == 'gallery':
                elements.append(Gallery(key=k, task_id=id))
            else:
                pass
        self.elements = elements
        self.root_path = root_path
        print(f'launch args: {launch_args}')
        print([launch_path, "-id", id, "--rootpath", root_path] + utils.parse_args(launch_args))
        self.process = subprocess.Popen([launch_path, "-id", id, "--rootpath", root_path] + utils.parse_args(launch_args))

    def get_by_key(self, key: str) -> TaskElement:
        for element in self.elements:
            if element.key == key:
                return element
        return None

    def struct(self) -> dict:
        ''' returns the task's structure as a dictionary '''
        return {"id": self.id, "struct": [el.struct() for el in self.elements], "active": self.active}

    def update_component(self, key: str) -> None:
        target_element = self.get_by_key(key)
        target_element.update()

    def end(self) -> None:
        self.process.terminate()
        self.process.wait()
        self.active = False

    def deactivate(self) -> None:
        self.active = False
        

    def __repr__(self) -> str:
        return 'id: ' + self.id + 'struct: ' + " ".join(str(x) for x in self.elements)

class TaskManager():
    ''' Manages the Tasks, manages the history of all the tasks that have been run this session,
     has a list of tasks and tasks can be retrieved through indexing '''
    def __init__(self) -> None:
        self.tasks = []

    def __getitem__(self, indices):
        return self.tasks.__getitem__(indices)

    def __repr__(self) -> Any:
        return self.tasks.__repr__()

    def create_task(self, id: str, struct: str, launch_path: PathLike, launch_args: dict, root_path: PathLike) -> None:
        ''' append a new task to the end or override an existing task if the id matches '''
        if self.get_by_id(id) is not None:
            # task id's should be unique, do not add if there is already a task with this id
            logging.error(f'a task with id: {id} already exists')
        else: 
            self.tasks.append(Task(
                id = id,
                struct = struct,
                launch_path = launch_path,
                launch_args = launch_args,
                root_path = root_path
            ))
            socketio.emit('server_added_task', id)
            # update clients about task state
            socketio.emit('tasks', self.struct())
    
    def end_task(self, id: str) -> None:
        '''close the process associated with a task.'''
        self.get_by_id(id).end()
        socketio.emit('tasks', self.struct())

    def deactivate_task(self, id: str) -> None:
        self.get_by_id(id).deactivate()
        socketio.emit('tasks', self.struct())

    def get_task_index(self, id : str) -> int:
        for i, task in enumerate(self.tasks):
            if task.id == id:
                return i

    def get_by_id(self, id) -> Union[Task, None]:
        for task in self.tasks:
            if task.id == id:
                return task
        return None
    
    def struct(self) -> list:
        ''' return a list of all the task dictionaries, representing the state of the entire system,
        in the structure required by the frontend to flow through the props in the vue components'''
        data = [task.struct() for task in self.tasks]
        return data

    def export(self) -> list:
        for task in self.tasks:
            for component in task:
                component.export()

    def write_element(self, task_id: str, element_key: str, new_value: str) -> None:
        ''' Located the specified element by using its key an the id of the Task it is part of,
        then calls its set with the new value.'''
        target_task = self.get_by_id(task_id)
        if target_task is None:
            print('target task does not exist')
            return None
        target_element = target_task.get_by_key(element_key)
        if target_element is None:
            print('target element does not exits')
            return None
        target_element.set(new_value)

    def update_component(self, task_id: str, key: str) -> None:
        ''' cause a targeted component to fire its update method '''
        target_task = self.get_by_id(task_id)
        if target_task is not None:
            target_task.update_component(key)

tasks = TaskManager()
