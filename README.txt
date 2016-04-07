**********************************************************************************
Westermo power control for train networks setup
**********************************************************************************

Author          : Henrik Envall

Files
wsgi.py         : python bottle app
server.py       : server to handle gpio settings
views/..        : bottle templates
static/..       : static files
gpio_object.py  : gpio object to be used between server and client 

Notes
 * uwsgi + nginx setup to run wsgi.py. Server.py needs to be run manually for now.
 * python3 must be used
 * Files need to be run with user www-data
