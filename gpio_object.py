import ast

class tcol:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class gpio_object:
    """
    GPIO object to be passed between server and client
    """
    def __init__(self, num_gpios):
       self.size = num_gpios
       self.gpio = []
       # Set all gpios to active
       for x in range(self.size):
           self.gpio.append(True)

    def get(self):
        return (self.gpio)

    def get_str(self):
        gpio_str = ""
        print("gpio_obj get_str in :" + str(self.gpio))
        for res in self.gpio:
            gpio_str += str(res) + ', '
            print(res)
        print("gpio_obj get_str out :" + gpio_str)
        return (gpio_str)

    def set(self, gpio_list):
        status = True
        for x in range(self.size):
            try:
                self.gpio[x] = gpio_list[x]
            except:
                status = False
        return (status)

    def set_str(self, gpio_str):
        status = True
        print("gpio_obj set_str :" + gpio_str)
        gpio_list = gpio_str.split(', ')
        for x in range(self.size):
            try:
                self.gpio[x] = bool(gpio_list[x] == "True")
                print(self.gpio_list[x] + '! ', end="")
                print(self.gpio[x])
            except:
                status = False
        return (status)

def test_ok():
    print("[" + tcol.OKGREEN + "OK" + tcol.ENDC + "]")

def test_fail():
    print("[" + tcol.FAIL + "Fail" + tcol.ENDC + "]")

if __name__ == '__main__':
    print("GPIO object test")
    test_str1 = 'False, True, False'
    test_str2 = 'True, False'
    
    gp_obj = gpio_object(3)
    print("Init&get test\t\t\t\t", end="")
    if gp_obj.get() == [True, True, True]:
        test_ok()
    else:
        test_fail()

    print("Set_str test\t\t\t\t", end="")
    status = gp_obj.set_str(test_str1)
    if gp_obj.get() == [False, True, False]:
         test_ok()
    else:
        test_fail()

    print("Get_str test\t\t\t\t", end="")
    res = gp_obj.get_str()
    if res == '[False, True, False]':
         test_ok()
    else:        
        test_fail()
        print(res)


        
