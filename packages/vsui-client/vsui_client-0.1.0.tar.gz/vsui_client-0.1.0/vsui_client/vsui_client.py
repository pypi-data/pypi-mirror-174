import socketio
from typing import Any
import logging
sio = socketio.Client()

task_id = None
# target log for where intercepted logs should be forwarded to
logging_target = None

def safe_emit(event, data):
    ''' emit a socketio event with exception handling '''
    try:
        sio.emit(event, data)
    except:
        pass

def connect(HOST : str = 'localhost', PORT : str = '8000') -> None:
    ''' initiate a socketio session with a server '''
    sio.connect('http://' + HOST + ':' + PORT, headers={'type':'app', 'id': task_id})
    print(f'sid is {sio.sid}')

def disconnect() -> None:
    ''' disconnect the socketio session '''
    sio.disconnect()
    print('socket disconnected')

# struct: { 'name' : 'type' }
# send a new task to be added to the server's task manager
def set_task_id(id : str) -> None:
    ''' set the id of this task '''
    global task_id
    task_id = id

def set_logging_target(key: str) -> None:
    {'element_key' : 'Logs'}

# edit one of the elements in the task, this allows data updating
def edit_element(element_uid : str, value : Any) -> None:
    ''' Edit the target display element, images must be base 64 encoded '''
    safe_emit('edit_element', {'task_id' : task_id, 'element_key' : element_uid, 'value' : value})

# mark the task as completed
def deactivate_task() -> None:
    ''' deactivate the current task '''
    safe_emit('deactivate_task', task_id)

def notify(txt : str, type : str) -> None:
    ''' send a popup to the client '''
    safe_emit('notify', {'txt':txt, 'type':type})

def logging_intercept(msg) -> None:
    ''' forward logs to the target display element '''
    if logging_target is not None:
        edit_element(logging_target['element_key'],msg)
    else:
        logging.error('No logging target set.')

# http://naoko.github.io/intercept-python-logging/
class RequestHandler(logging.Handler):
    def emit(self, record):
        ''' Intercept logs '''
        logging_intercept(record.getMessage())
