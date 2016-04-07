import socket
import bottle
import os
import gpio_object

from bottle import route, template, request, response, abort, post, get, debug, static_file

switch_array = [[0, 'TrainSwitch 2', True], [1, 'Vechicle switch 1', True], [2, 'Vechicle switch 2', True], [3, 'Vechicle switch 3', True], [4, 'Vechicle switch 4', True]]

gpio_array = [1, 2, 3, 4, 5] # GPIOs used
sock_file = "/tmp/gpio_socket"

gp_obj = gpio_object.gpio_object(5)

def send_gpio_cmd(cmd):
    status = ""
    if os.path.exists(sock_file):        
        client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        client.connect(sock_file)
        status = "Ready. "          
        try:                
            if len(cmd) > 1:
                status += "SEND: " + cmd
                client.send(cmd.encode('utf-8'))
                response = client.recv(1024)
        except Exception as e:
            status += "error " + str(e)
        client.close()
    else:
        status = "Couldn't Connect! "    
    return(status, response.decode('utf-8'))

def get_gpio_status():
    status = True
    try:
        client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        client.connect(sock_file)
        client.send("GPIO_GET".encode('utf-8'))
        dgram = client.recv(1024)
        client.close()
        gp_obj.set_str(dgram.decode('utf-8'))
        response = gp_obj.get_str()
    except:
        status = False
        client.close()
        response = "Error"
    return status, response

def set_gpio(gpio_string):
    status = True
    send_str = "GPIO_SET, "+gpio_string
    try:
        client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        client.connect(sock_file)
        client.send(send_str.encode('utf-8'))
        dgram = client.recv(1024)
        client.close()
        gp_obj.set_str(gpio_string)
    except:
        status = False
        client.close()
        dgram = "Error".encode('utf-8')
    return status, dgram.decode('utf-8')


def get_network_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.connect(('<broadcast>', 0))
    name =  s.getsockname()[0]
    s.close()
    return name

@route('/')# Handle HTTP GET for the application root
def index_page():
    return template('index.tpl', message='Hello Train team')

@route('/my_ip')
def show_ip():
    ip = request.environ.get('REMOTE_ADDR')
    own_ip = request.environ.get('HTTP_HOST')
    return template("Your IP is <h3>{{ip}}</h3><br>Own IP is <h3>{{own_ip}}</h3>", ip=ip, own_ip=own_ip)

@route('/gpio')
def show_gpio():
    server_ip = get_network_ip()
    status, resp = get_gpio_status()

    gpio_state = resp.split(', ')
    values = {}
    values['buttons'] = switch_array
    values['result'] = "No data sent"
    values['status'] = "Ready"
    values['gpio'] = gpio_state
    return template('gpio.tpl', values)
    #return ("It is working" + str(server_ip))

@post('/gpio')
def do_gpio():
    server_ip = get_network_ip()
    chk_0 = str(request.forms.get('powerbutton[0]') == "True")
    chk_1 = str(request.forms.get('powerbutton[1]') == "True")
    chk_2 = str(request.forms.get('powerbutton[2]') == "True")
    chk_3 = str(request.forms.get('powerbutton[3]') == "True")
    chk_4 = str(request.forms.get('powerbutton[4]') == "True")
    gpio_state = []
    gpio_state.append(chk_0)
    gpio_state.append(chk_1)
    gpio_state.append(chk_2)
    gpio_state.append(chk_3)
    gpio_state.append(chk_4)
    gpio_set_string = chk_0 +', '+ chk_1 +', '+ chk_2 +', '+ chk_3 +', '+ chk_4
    print("GPIO set string: " + gpio_set_string)
    status, resp1 = set_gpio(gpio_set_string)
    if status == True:
        status, resp2 = get_gpio_status()
        print("get_gpio_status() ", status, end =", resp :")
        print(resp2)
        gpio_state = resp2.split(', ')
        print(resp2, gpio_state)
    else:
        status = False
        resp2 = 'Failed to get GPIO status'
   
    print(gpio_state, len(gpio_state))
    values = {}
    values['buttons'] = switch_array
    values['result'] = "button pressed: " + chk_0 +', '+ chk_1 +', '+ chk_2 +', '+ chk_3 +', '+ chk_4 
    values['status'] = str(status)
    values['gpio'] = gpio_state
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

