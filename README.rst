
Dang Huy Hoang - ITITIU13025
=====================
This repository includes both Ryu source code and the project code.
The code can be located at Thesis/ryu/gui folder.

It is recommended to run the controller.py on Pycharm for easy debug. The web GUI server runs on http://127.0.0.1:8000/
Some dependencies that need to be installed.

+Ryu (sudo pip install ryu)
+Flask
+gevent
+gevent-websocket 
+python-gevent, python-routes, python-webob, and python-paramiko should be installed.

Start Ryu from a terminal, there are three network applications to choose from, each application needs to run independently (terminate the ryu-manager (Ctrl-Z) and retype the command after each use).

For simple_switch and topology view: "ryu-manager --verbose --observe-links ryu.app.simple_switch ryu.app.rest_topology  ryu.app.ofctl_rest ryu.topology.switches"
For rest_firewall: "ryu-manager --verbose --observe-links ryu.app.rest_firewall"
For rest_router: "ryu-manager --verbose --observe-links ryu.app.rest_router"


The rest are for GUI

Start controller:"./ryu/ryu/gui/controller.py" (or from Pycharm) and connect to "127.0.0.1:8000". There is a authenication dialog: username:bailey password: secret. After that, there will be another
dialog to connect to the Ryu proxy server (the default is http://127.0.0.1:8080/)
