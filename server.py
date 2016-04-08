import socket
import pwd
import grp
import os
import gpio_object
import wiringpi

class gpio():
    """
    GPIO settings
    GPIOs from 0 to SIZE-1 are set to outputs HIGH initially.
    """
    def __init__(self, size):
        self.gpio = gpio_object.gpio_object(size)
        self.size = size
        # Initialize
        wiringpi.wiringPiSetup()
        # Set as output HIGH
        for port in range(self.size):
            wiringpi.pinMode(port, 1)
            wiringpi.digitalWrite(port, 1)
        # wiringpi.pullUpDnControl(pin_or_port_num, 2)

    def __del__(self):
        # Clean up GPIO states. Set ports to LOW and input
        for port in range(self.size):
            wiringpi.digitalWrite(port, 0)
            wiringpi.pinMode(port, 0)

    def get_str(self):
        return (self.gpio.get_str())

    def set_str(self, cmd):
        result = self.gpio.set_str(cmd)
        list = self.gpio.get()
        # Set GPIOs
        port = 0
        for state in list:
            if state:
                wiringpi.digitalWrite(port, 1)
            else:
                wiringpi.digitalWrite(port, 0)
            port += 1
        return (result)

def handle_cmd(socket, cmd, gpio):
    cmd_array = cmd.split(', ')
    if cmd_array[0] == "GPIO_GET":
        response = gpio.get_str()
        print("server get in : ", cmd)
        print("server get out: ", response)
        socket.send(response.encode('utf-8'))
    elif cmd_array[0] == "GPIO_SET":
        gpio.set_str(cmd[cmd.find(',')+2:])
        response = gpio.get_str()
        print("server set in : ", cmd)
        print("server set out: ", response)
        socket.send(response.encode('utf-8'))
    else:
        response = "ERROR"
        socket.send(response.encode('utf-8'))

if __name__ == '__main__':
    sock_file = '/tmp/gpio_socket'
    gpio = gpio(5)
    if os.path.exists(sock_file):
        os.remove(sock_file)

    print("Opening socket...")
    backlog = 5
    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server.bind(sock_file)
    # Set socket permissions to www-data user/group
    uid = pwd.getpwnam("www-data").pw_uid
    gid = grp.getgrnam("www-data").gr_gid
    os.chown(sock_file, uid, gid) 

    server.listen(backlog)
    print("Listening...")
    try:
        while True:
            client, address = server.accept()
            datagram = client.recv(1024)
            if not datagram:
                break
            else:
                cmd = datagram.decode('utf-8')
                print("-" * 20)
                print(cmd)
                if "DONE" == cmd:
                    break
                handle_cmd(client, cmd, gpio)
                client.close()
    except KeyboardInterrupt as k:
        print("CTRL + C \n")

    print("-" * 20)
    print("Shutting down...")
    server.close()
    os.remove("/tmp/gpio_socket")
    print("Done")
