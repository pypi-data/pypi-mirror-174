from .task_management import tasks, Task

class Client():
    '''represents one client connected through a socketio socket'''
    def __init__(self, sid : str, type : str, id : str) -> None:
        self.sid = sid # also the name of the room they are in
        self.type = type
        self.id = id
        self.task = tasks.get_by_id(id)

    def __repr__(self) -> str:
        return 'client - type: ' + self.type + ', sid: ' + self.sid + ', task: ' + self.id
    
    def deactivate_task(self):
        print(f'deactivate task {self.task}')
        if isinstance(self.task, Task):
            self.task.deactivate()

    # XXX Unused, ideally implemented but socketio doesn't like this
    #def emit_to_me(self, event : str, data : Any) -> None:
    #    '''emit an event to only this client '''
    #    socketio.emit(event, { "data" : data }, to = self.sid, namespace="/")

class ClientManager():
    '''manages the connected socketio clients'''
    def __init__(self) -> None:
        self.clients = []

    def __getitem__(self, indices) -> Client:
        return self.clients.__getitem__(indices)

    def __repr__(self) -> str:
        return self.clients.__repr__()

    def add_client(self, sid : str, type : str, id : str) -> None:
        self.clients.append(Client(sid=sid, type=type, id=id))

    def get_by_sid(self, sid : str) -> Client:
        ''' get a connected client by it's unique sid '''
        for client in self.clients:
            if client.sid == sid:
                return client

    def get_by_type(self, type : str) -> Client:
        '''returns a list of the connected clients of the specified type'''
        return [client for client in self.clients if client.type == type]

    # XXX Unused, Socketio doesn't like this
    #def emit_all_clients(self, event : str, data : Any, type : str = None) -> None:
    #    '''emit an event with attached data to all clients,
    #    optional type can be specified'''
    #    targets = []
    #    if type is None:
    #        targets = self.clients
    #    elif type == 'web' or type == 'app':
    #        targets = self.get_by_type(type)
    #    for client in targets:
    #        client.emit_to_me(event, data)

    def remove_by_sid(self, sid : str) -> None:
        for i, client in enumerate(self.clients):
            if client.sid == sid:
                print(f'disconnecting {client}')
                client.deactivate_task()
                del self.clients[i]
                break

clients = ClientManager()