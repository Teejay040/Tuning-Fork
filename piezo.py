#!/usr/bin/python
# -*- coding: utf-8 -*-

from pipython import GCSDevice
import time

class piezo():
    
    def __init__(self):
        self.pidevice = GCSDevice('E-625')
        self.pidevice.ConnectUSB("121019479")
        self.target = 'A'

    def absolute_voltage(self, voltage):
        self.pidevice.SVO(self.target, False)
        self.pidevice.SVA(self.target, voltage)

    def request_voltage(self):
        return self.pidevice.qVOL(self.target)
