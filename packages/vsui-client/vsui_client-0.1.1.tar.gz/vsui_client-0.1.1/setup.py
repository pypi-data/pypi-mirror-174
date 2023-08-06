# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vsui_client']

package_data = \
{'': ['*']}

install_requires = \
['python-socketio[client]>=5.7.2,<6.0.0']

setup_kwargs = {
    'name': 'vsui-client',
    'version': '0.1.1',
    'description': 'Client module for connecting to Volume Segmantics User Inteface',
    'long_description': "# Volume Segmantics User Interface Client\n\nThis package allows a python script to connect to the volume segmantics server and update the server's information about a corresponding process. <br>\nThe task id must match the name of a process definition in the connected server. The provided methods are:\n- **set_task_id** (id : str)\n    - This should correspond to the name of this process on the server.\n- **connect** (HOST : str = 'localhost', PORT : str = '8000')\n    - Initiates a socketio session with the server.\n- **edit_element** (element_uid : str, value : Any)\n    - Target a specific display component and update its data.\n- **notify** (txt : str, type : str)\n    - send a toast to the client\n    - types:\n        - success\n        - error\n        - info\n        - warning\n    - changing the type only changes the toast colour and icon\n- **set_logging_target** (key: str)\n    - Define the component key of the task element that logs should be forwarded to.\n\n<br>\nA log component can be configured to display all messages sent to a logger using \n\n    # (if you want to get the default logger)\n    logger = logging.getLogger()\n    # add the vsui handler to your logger\n    handler = vsui_client.RequestHandler()\n\n\nNow all logging messages will be forwarded to the specified component in the web client.",
    'author': 'Matthew Pimblott',
    'author_email': 'matthew.pimblott@diamond.ac.uk',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
