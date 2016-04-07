import socket
import os
import gpio_object
import wiringpi

class gpio():
    """
    GPIO settings
    """
    def __init__(self, size):
        self.gpio = gpio_object.gpio_object(size)
        self.size = size

    def get_str(self):
        return (self.gpio.get_str())

    def set_str(self, cmd):
        return (self.gpio.set_str(cmd))

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

    gpio = gpio(5)

    if os.path.exists("/tmp/gpio_socket"):
        os.remove("/tmp/gpio_socket")

    print("Opening socket...")
    backlog = 5
    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server.bind("/tmp/gpio_socket")
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
