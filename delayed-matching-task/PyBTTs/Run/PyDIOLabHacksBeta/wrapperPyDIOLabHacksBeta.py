#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function
import serial
import time
import sys
sys.path.append('../PyDIO');

from wapperPyDIOBase import OneTrigger,TTLReader

def writeLX( _conn, _lengthSec,_value):
    intVal = int(_value);
    lenVal = int( _lengthSec*1000.0*1000.0);
    cmdstr = '';
    cmdstr += 'WRITE';
    cmdstr += ' ';
    cmdstr += str(intVal);
    cmdstr += ' ';
    cmdstr += str(lenVal);
    cmdstr += ' ';
    cmdstr += '0'; # repeart zero
    cmdstr += '\n';
    #WRITE 0 5000 0\n
    b_cmdstr = bytes(cmdstr.encode());
    print(b_cmdstr)
    _conn.write(b_cmdstr);



class OneTriggerLabHacksBeta(OneTrigger):
    def __init__(self,deviceName):
        super().__init__();
        self.deviceName = deviceName;
        pass;
    def __del__(self):
        pass;
    def hello(self):
        pass;
        return 'hello OneTriggerLabHacksBeta';
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
    def writeA(self):
        pass;
    def writeB(self):
        pass;
    def writeDelay(self,lengthSec,value):
        writeLX(self.sconn,lengthSec, value);
        pass;
    
class TTLReaderLabHacksBeta(TTLReader):
    def __init__(self,deviceName):
        super().__init__();
        self.deviceName = deviceName;
        pass;
    def __del__(self):
        pass;
    def hello(self):
        pass;
        return 'hello TTLReaderLabHacksBeta';
    def begin(self):
        self.sconn = serial.Serial(self.deviceName, baudrate=128000, timeout=0.01)
        self.sconn.write(b"SET DATA_MODE READ\n")
        while self.sconn.readline():
            pass
        pass;
    def readOneShot(self):
        self.sconn.write(b"READ\n")
        retRL = self.sconn.readline();
        pass;
        return retRL;
    def end(self):
        r = self.sconn.readline().strip()
        #print("TTL Output State: %s" % r)
        # Close the USB2TTL8 serial connection
        self.sconn.close()
        pass;
