##  The available commands are:
##  Sf (x);   | This command sets the normal frequency to x (note that if the frequency controller is engaged this value will be overwritten)
##  sSf (x);  | This command sets the shear frequency to x (note that if the frequency controller is engaged this value will be overwritten)
##  Rf;       | This command returns the current normal frequency
##  sRf;      | This command returns the current shear frequency
##  Sa (x);   | This command sets the normal sine out amplitude to x (note that if the amplitude controller is engaged this value will be overwritten)
##  sSa (x);  | This command sets the shear sine out amplitude to x (note that if the amplitude controller is engaged this value will be overwritten)
##  Ra;       | This command returns the current normal sine out amplitude
##  sRa;      | This command returns the current shear sine out amplitude
##  Ssa (x);  | This command sets the amplitude setpoint for the normal amplitude controller to x
##  sSsa (x); | This command sets the amplitude setpoint for the shear amplitude controller to x
##  Rsa;      | This command returns the current normal amplitude setpoint for the amplitude controller
##  sRsa;     | This command returns the current shear amplitude setpoint for the amplitude controller
##  Rp;       | This command returns the current normal phase
##  sRp;      | This command returns the current shear phase
##  Ef (X);   | This command enables or disables the normal frequency controller (x = 1 enables the controller and x = 2 disables the controller)
##  sEf (X);  | This command enables or disables the shear frequency controller (x = 1 enables the controller and x = 2 disables the controller)
##  Ea (X);   | This command enables or disables the normal amplitude controller (x = 1 enables the controller and x = 2 disables the controller)
##  sEa (X);  | This command enables or disables the shear amplitude controller (x = 1 enables the controller and x = 2 disables the controller)
##  Ed (X);   | This command enables or disables the data stream (x = 1 enables the stream and x = 2 disables the stream)
##  SCe (X);  | This command sets the exponential term for the normal frequency controller
##  sSCe (X); | This command sets the exponential term for the shear frequency controller
##  SCl (X);  | This command sets the linear term for the normal frequency controller
##  sSCl (X); | This command sets the linear term for the shear frequency controller
##  SCp (X);  | This command sets both exponential and linear terms for the normal frequency controller (1 = open air, 2 = 20 cSt, 3 = 500 cSt, 4 = 10 000 cSt, 5 = 30 000 cSt)
##  sSCp (X); | This command sets both exponential and linear terms for the shear frequency controller (1 = open air, 2 = 20 cSt, 3 = 500 cSt, 4 = 10 000 cSt, 5 = 30 000 cSt)
##  SCAl (X); | This command sets the linear term for the normal amplitude controller
##  sSCAl (X);| This command sets the linear term for the shear amplitude controller
##  SCAp (X); | This command sets the linear term for the normal amplitude controller (preset 1 is most conservative and preset 5 is most agressive)
##  sSCAp (X);| This command sets the linear term for the shear amplitude controller (preset 1 is most conservative and preset 5 is most agressive)

import time
import serial
import io
from serial.tools import list_ports

def find_unique_dev_by_pidvid(pid: int, vid: int):
     found_devices = list(filter(lambda p: p.pid == pid and p.vid == vid, list_ports.comports()))
     return found_devices[0] if len(found_devices) == 1 else None



class sfa():

    def __init__(self):

        port = str(find_unique_dev_by_pidvid(0x003d,0x2341)).split(" ")[0]
        print(port)
        self.serial = serial.Serial(port, baudrate=19200,timeout=20)

    def write(self,cmd):

        #the protocol of the sfa gives no feedback if the command was correct.
        #Only when last sent command was incorrect an error message will be waiting in the buffer
       # if self.serial.in_waiting > 0:
       #      print(self.serial.read(self.serial.in_waiting).decode())

        cmd = cmd + ';'
        print(cmd)
        self.serial.write(cmd.encode())


    def write_read(self,cmd):
        self.write(cmd)

        feedback = self.serial.readline().decode()
        return feedback

    def read_line(self):
        feedback = self.serial.readline().decode()
        return feedback


    ##  Sf (x);   | This command sets the normal frequency to x (note that if the frequency controller is engaged this value will be overwritten)
    def Sf (self,x):
        self.write('Sf ' + str(x))

    ##  sSf (x);  | This command sets the shear frequency to x (note that if the frequency controller is engaged this value will be overwritten)
    def sSf (self,x):
        self.write('sSf ' + str(x))

    ##  Rf;       | This command returns the current normal frequency
    def Rf(self):
        return self.write_read("Rf").replace("normal frequency = ","")

    ##  sRf;      | This command returns the current shear frequency
    def sRf(self):
        return self.write_read("sRf").replace("shear frequency = ","")

    ##  Sa (x);   | This command sets the normal sine out amplitude to x (note that if the amplitude controller is engaged this value will be overwritten)
    def Sa (self,x):
        self.write('Sa ' + str(x))

    ##  sSa (x);  | This command sets the shear sine out amplitude to x (note that if the amplitude controller is engaged this value will be overwritten)
    def sSa (self,x):
        self.write('sSa ' + str(x))

    ##  Ra;       | This command returns the current normal sine out amplitude
    def Ra (self):
        return self.write_read("Ra").replace("normal amplitude = ","")

    ##  sRa;      | This command returns the current shear sine out amplitude
    def sRa (self):
        return self.write_read("sRa").replace("shear amplitude = ","")

    ##  Rp;       | This command returns the current normal phase
    def Rp (self):
        return self.write_read("Rp").replace("normal phase = ","")

    ##  sRp;       | This command returns the current shear phase
    def sRp (self):
        return self.write_read("sRp").replace("shear phase = ","")    

    ##  Ram;       | This command returns the current normal amplitude measured
    def Rm (self):
        return self.write_read("Rm").replace("normal measured amplitude = ","")
    
    ##  sRam;       | This command returns the current shear amplitude measured
    def sRm (self):
        return self.write_read("sRm").replace("shear measured amplitude = ","")  

    ##  Ssa (x);  | This command sets the amplitude setpoint for the normal amplitude controller to x
    def Ssa (self,x):
        self.write('Ssa ' + str(x))

    ##  sSsa (x); | This command sets the amplitude setpoint for the shear amplitude controller to x
    def aSsa (self,x):
        self.write('sSsa ' + str(x))

    ##  Rsa;      | This command returns the current normal amplitude setpoint for the amplitude controller
    def Rsa (self):
        return self.write_read("Rsa").replace("normal amplitude setpoint = ","")

    ##  sRsa;     | This command returns the current shear amplitude setpoint for the amplitude controller
    def sRsa (self):
        return self.write_read("sRsa").replace("shear amplitude setpoint = ","")
    
    ##  Rp;      | This command returns the current normal phase 
    def Rp (self):
        return self.write_read("Rp").replace("normal phase = ","")

    ##  sRp;     | This command returns the current shear phase
    def sRp (self):
        return self.write_read("sRp").replace("shear phase = ","")

    ##  Ef (X);   | This command enables or disables the normal frequency controller (x = 1 enables the controller and x = 2 disables the controller)
    def Ef (self,x):
        self.write('Ef ' + str(x))

    ##  sEf (X);  | This command enables or disables the shear frequency controller (x = 1 enables the controller and x = 2 disables the controller)
    def sEf (self,x):
        self.write('sEf ' + str(x))

    ##  Ea (X);   | This command enables or disables the normal amplitude controller (x = 1 enables the controller and x = 2 disables the controller)
    def Ea (self,x):
        self.write('Ea ' + str(x))

    ##  sEa (X);  | This command enables or disables the shear amplitude controller (x = 1 enables the controller and x = 2 disables the controller)
    def sEa (self,x):
        self.write('sEa ' + str(x))

    ##  Ed (X);   | This command enables or disables the data stream (x = 1 enables the stream and x = 2 disables the stream)
    def Ed (self,x):
        self.write('Ed ' + str(x))

    ##  SCe (X);  | This command sets the exponential term for the normal frequency controller
    def SCe (self,x):
        self.write('SCe ' + str(x))

    ##  sSCe (X); | This command sets the exponential term for the shear frequency controller
    def sSCe (self,x):
        self.write('sSCe ' + str(x))

    ##  SCl (X);  | This command sets the linear term for the normal frequency controller
    def SCl (self,x):
        self.write('SCl ' + str(x))

    ##  sSCl (X); | This command sets the linear term for the shear frequency controller
    def sSCl (self,x):
        self.write('sSCl ' + str(x))

    ##  SCp (X);  | This command sets both exponential and linear terms for the normal frequency controller (1 = open air, 2 = 20 cSt, 3 = 500 cSt, 4 = 10 000 cSt, 5 = 30 000 cSt)
    def SCp (self,x):
        return self.write_read('SCp ' + str(x))

    ##  sSCp (X); | This command sets both exponential and linear terms for the shear frequency controller (1 = open air, 2 = 20 cSt, 3 = 500 cSt, 4 = 10 000 cSt, 5 = 30 000 cSt)
    def sSCp (self,x):
        self.write_read('sSCp ' + str(x))

    ##  SCAl (X); | This command sets the linear term for the normal amplitude controller
    def SCAl (self,x):
        self.write('SCAl ' + str(x))

    ##  sSCAl (X);| This command sets the linear term for the shear amplitude controller
    def sSCAl (self,x):
        self.write('sSCAl ' + str(x))

    ##  SCAp (X); | This command sets the linear term for the normal amplitude controller (preset 1 is most conservative and preset 5 is most agressive)
    def SCAp (self,x):
        return self.write_read('SCAp ' + str(x))

    ##  sSCAp (X);| This command sets the linear term for the shear amplitude controller (preset 1 is most conservative and preset 5 is most agressive)
    def sSCAp (self,x):
        self.write_read('sSCAp ' + str(x))



if __name__ == '__main__':

    s = sfa()

    time.sleep(5)
    s.Sf(1000.02)

    print(s.Rf())
    print(s.Rf())
    print("end")

    s.serial.close()
