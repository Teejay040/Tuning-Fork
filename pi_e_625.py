#!/usr/bin/python
# -*- coding: utf-8 -*-

from pipython import GCSDevice
from threading import Thread
import threading
import time

class pi_e_625():
    
    def __init__(self):

        self.pidevice = GCSDevice('E-625')
        # Serial number to connect to can be read on device!
        self.pidevice.ConnectUSB("121019479")

#        Or use the dialog and you will read "E-816USB SN 121019479" 
#        self.pidevice.InterfaceSetupDlg(key='sample')

        self.stopMutex = threading.Lock()
        self._stop = True

        self.target = 'A'

        print("???")

    def servoloop(self,closed=False):
        
        self.pidevice.SVO(self.target,closed)


    def relative_voltage(self,voltage):

        self.pidevice.SVO(self.target,False)
        self.pidevice.SVR(self.target,voltage)

        
    def absolute_voltage(self,voltage):

        self.pidevice.SVO(self.target,False)
        self.pidevice.SVA(self.target,voltage)

    def request_voltage(self):

        return self.pidevice.qVOL(self.target)

    def thread_for_voltage(self,start,end,step,waittime):

        v = start

        while v < end:
            with self.stopMutex:
                if self._stop:
                    break
            self.absolute_voltage(v)
        
            v = v + step
            time.sleep(waittime)

        self.stop()

    def stop(self):
        # Must protect self._stop with a mutex because a secondary thread 
        # might try to access it at the same time.
        print("*")
        with self.stopMutex:
            if not self._stop:
                self._stop = True
                        
        
    def for_voltage(self,start,end,step,waittime):
        # Must protect self._stop with a mutex because a secondary thread 
        # might try to access it at the same time.
        # if a thread is already running do not start a second one!!!
        with self.stopMutex:
            if self._stop:
                self._stop = False
                ok_to_start = True
            else:
                ok_to_start = False

        if ok_to_start:                        

            self.for_task = Thread(target = self.thread_for_voltage, args =(start,end,step,waittime,))
    
            self.for_task.start()




if __name__ == '__main__':

    try:
        print("***")
        pd = pi_e_625()
        time.sleep(10)
        print(pd.request_voltage())
        pd.absolute_voltage(0.)
        time.sleep(1)
        print(pd.request_voltage())

        pd.for_voltage(0,1,1,1)

        door = True
        while door:
            with pd.stopMutex:
                door = not pd._stop
                time.sleep(.5)
            print(pd.request_voltage())
    finally:
        try:
            pd.stop()
        except:
            pass
        print("done")
