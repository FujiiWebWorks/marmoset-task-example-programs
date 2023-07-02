#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function
import serial
import time
import sys
import serial
sys.path.append('../PyDIO');

from wapperPyDIOBase import OneTrigger
from DllPyNIDIO import TTClassTrainDIONNUSB2TTL8DIO

def writeLX( cl, _lengthSec,_value, _sep):
    lenVal = int( _lengthSec*1000.0); # msec
    intVal = int(_value);
    #
    pwidth = int(10);
    lastVal = int(0);
    #
    cmdstr = '';
    cmdstr += str(lenVal);
    cmdstr += _sep;
    cmdstr += str(intVal);
    #
    cmdstr += _sep;
    cmdstr += str(pwidth);
    cmdstr += _sep;
    cmdstr += str(lastVal);
    # debug
    if( False ):
        cmdstr += _sep;
        cmdstr += str(5);
        cmdstr += _sep;
        cmdstr += str(intVal);
        #
        cmdstr += _sep;
        cmdstr += str(5);
        cmdstr += _sep;
        cmdstr += str(lastVal);
        pass;
    pass;
    #
    b_cmdstr = bytes(cmdstr.encode());
    ####print(b_cmdstr)
    cl.start(b_cmdstr);
    pass;

class InitDOUTUSB2TTL8DIO:
    def __init__(self,deviceName):
        self.deviceName = deviceName;
        pass;
    def begin(self):
        self.sconn = serial.Serial(self.deviceName, baudrate=128000, timeout=0.01)

        # 1. Set USB2TTL8 Data Mode to Write (digital output).
        # If the USB2TTL8 is already in Write mode, this step is not needed; but
        # setting the USB2TTL8 Data Mode at the start of the app ensures the 
        # device is always switched to the correct mode for the planned use.
        self.sconn.write(b"SET DATA_MODE WRITE\n")

        while self.sconn.readline():
            pass

        # 2a. WRITE command: Set all 8 TTL lines using a value of 0 -255.
        # In this example, TTL output is set to each possible value
        # for about 50 msec.        
        
        pass;
    def end(self):
        r = self.sconn.readline().strip()
        print("TTL Output State: %s" % r)

        # Close the USB2TTL8 serial connection
        self.sconn.close()
        pass;
    



class OneTriggerPyNNUSB2TTL8DIO(OneTrigger):
    def __init__(self,deviceName):
        super().__init__();
        self.deviceName = deviceName;
        pass;
    def __del__(self):
        del self.cl;
        pass;
    def hello(self):
        pass;
        return 'hello ' + self.cl.hello();
    def begin(self):
        initDOUT = InitDOUTUSB2TTL8DIO(self.deviceName);
        initDOUT.begin();
        initDOUT.end();
        self.cl = TTClassTrainDIONNUSB2TTL8DIO();
        print(self.cl.hello());
        self.cl.begin(self.deviceName);
        pass;
    def end(self):
        self.cl.stop();
        self.cl.end();
        pass;
    def writeA(self):
        pass;
    def writeB(self):
        pass;
    def writeDelay(self,lengthSec,value):
        _sep = ',';
        writeLX(self.cl,lengthSec, value,_sep);
        pass;
    


class OneTriggerPyRAWUSB2TTL8DIO(OneTrigger):
    def __init__(self,deviceName):
        super().__init__();
        self.deviceName = deviceName;
        pass;
    def __del__(self):
        pass;
    def hello(self):
        pass;
        return 'hello RAW serial USB2TTL8DIO ver 0.0';
    def begin(self):
        self.se = serial.Serial(self.deviceName, baudrate=128000, timeout=0.01);
        self.se.write(b"SET DATA_MODE WRITE\n")
        while self.se.readline():
            pass;
        pass;
    def end(self):
        self.se.close();
        pass;
    def writeA(self):
        pass;
    def writeB(self):
        pass;
    def writeDelay(self,lengthSec,value):
        self.se.write(b"WRITE %d 5000 0\n" % value)
        pass;

