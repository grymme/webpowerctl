import socket
import bottle
import os

from bottle import route, template, request, response, abort, post, get, debug, static_file

switch_dict = {1: 'TrainSwitch 2', 2: 'Vechicle switch 1', 3: 'Vechicle switch 2', 
                4: 'Vechicle switch 3', 5: 'Vechicle switch 4'}

gpio_array = [1, 2, 3, 4, 5] # GPIOs used
sock_file = "/home/pi/www/train/gpios.socket"

def send_gpio_cmd(cmd):
    status = ""
    if os.path.exists("/tmp/gpio_socket"):
        client = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        client.connect("/tmp/gpio_socket")
        status = "Ready. "
           
        try:                
            if len(cmd) > 1:
                status += "SEND: "
                client.send(cmd.encode('utf-8'))
        except Exception as e:
            status += "error " + str(e)
            client.close()
    else:
        status = "Couldn't Connect! "
    status += "Done "
    return(status)


def get_network_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.connect(('<broadcast>', 0))
    return s.getsockname()[0]

def get_gpio_status():
    gpio


@route('/')# Handle HTTP GET for the application root
def index_page():
    return template("<H1>{{message}}</H1><p><a href=\"/my_ip\">My IP</a> is a nifty thing<p>", message='Hello Train team')

@route('/my_ip')
def show_ip():
    ip = request.environ.get('REMOTE_ADDR')
    own_ip = request.environ.get('HTTP_HOST')
    return template("Your IP is <h3>{{ip}}</h3><br>Own IP is <h3>{{own_ip}}</h3>", ip=ip, own_ip=own_ip)

@route('/gpio')
def show_gpio():
    server_ip = get_network_ip()
    values = {}
    values['buttons'] = switch_dict
    values['result'] = "No button pessed"
    values['status'] = "Nothing yet "
    return template('gpio.tpl', values)
    #return ("It is working" + str(server_ip))

@post('/gpio')
def do_gpio():
    server_ip = get_network_ip()
    btn_pressed = str(request.forms.get('btn'))
    status = send_gpio_cmd("GPIO set " + btn_pressed)
    values = {}
    values['buttons'] = switch_dict
    values['result'] = "button pressed: " + btn_pressed
    values['status'] = status
    return template('gpio.tpl', values)

@route('/static/:path#.+#', name='static')
def static(path):
        return static_file(path, root='static')

debug(True)
# Run bottle internal test server when invoked directly ie: non-uxsgi mode
if __name__ == '__main__':
    bottle.run(host='0.0.0.0', port=8080)
# Run bottle in application mode. Required in order to get the application working with uWSGI!
else:
    app = application = bottle.default_app()

