#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function
import serial
import time
import sys
sys.path.append('../PyDIO');

from wapperPyDIOBase import OneTrigger, OneShotDAQTLL
#from DllPyNIDIO import TTClassMainDIOTest02
from DllPyNIDIO import TTClassTrainDIONIDAQ
from DllPyNIDIO import TTClassTrainDIONNNIDAQ
from DllPyNIDIO import TTClassOneShotNIDAQ


def writeLXpWidth( cl, _pWidthSec, _lengthSec,_value, _sep):
    lenVal = int( _lengthSec*1000.0); # msec
    intVal = int(_value);
    #
    pwidth = int(_pWidthSec*1000.0); #msec
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

def writeLX( cl, _lengthSec,_value, _sep):
    _pWidthSec = 0.010;
    writeLXpWidth(cl, _pWidthSec, _lengthSec,_value, _sep);
    pass;



class OneTriggerPyNIDAQ(OneTrigger):
    def __init__(self,deviceName):
        super().__init__();
        self.deviceName = deviceName;
        pass;
    def __del__(self):
        pass;
    def hello(self):
        pass;
        return 'hello ' + self.cl.hello();
    def begin(self):
        self.cl = TTClassTrainDIONIDAQ();
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
    #def writeDelay(self,lengthSec,value):
    #    _sep = ',';
    #    writeLX(self.cl,lengthSec, value,_sep);
    #    pass;
    def writeDelay(self,lengthSec,value, pWidthsec=0.010):
        _sep = ',';
        writeLXpWidth(self.cl,pWidthsec,lengthSec, value,_sep);
        pass;

class OneTriggerPyNNNIDAQ(OneTrigger):
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
        self.cl = TTClassTrainDIONNNIDAQ();
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
    
    
    
class OneTriggerThreadingPyNNNIDAQ(OneTrigger):
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
        self.cl = TTClassTrainDIONNNIDAQ();
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

class NIDAQOneShotDAQ(OneShotDAQTLL):
    def __init__(self,_deviceName, _mode):
        super().__init__();
        self.deviceName = _deviceName;
        self.mode = _mode; # 0:TTL/Analog 1:TTL only
        pass;
    def __del__(self):
        pass;
    def hello(self):
        pass;
        return 'hello ' + self.cl.hello();
    def begin(self):
        self.cl = TTClassOneShotNIDAQ();
        print(self.cl.hello());
        self.cl.begin(self.deviceName, self.mode);
        pass;
    def end(self):
        self.cl.end();
        pass;
    def writeDIO(self, _data):
        self.cl.writeDIO(int(_data));
        pass;
    def writeAO(self,_ch, _data):
        self.cl.writeAO(_ch,float(_data));
        print("writeAO" + str(_data));
        pass;
    def readDIO(self):
        ret = self.cl.readDIO();
        return ret;
