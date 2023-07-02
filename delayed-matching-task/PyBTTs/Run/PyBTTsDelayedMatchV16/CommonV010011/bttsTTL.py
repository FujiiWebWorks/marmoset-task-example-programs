#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os  # handy system and path functions
import sys  # to get file system encoding

import threading
import time

try:
    from labjack import u3
except ImportError:
    import u3

from psychopy.hardware import labhackers


class BTTsTTL:
    def __init__(self):
        self.curSemaphore = threading.BoundedSemaphore(1);
        pass;
    def write(self,channel,val):
        pass;
    def begin(self):
        pass;
    def end(self):
        pass;

def runTargetTTL(that):
    that.runnable();
    pass;

class BTTsTTLDelay:
    def __init__(self,_bttsTTL, _channel):
        self.bttsTTL = _bttsTTL;
        self.channel = _channel;
        self.curThread = None;
        self.curSemaphore = None;
        self.curSemaphore = threading.BoundedSemaphore(1);
        pass;
    def writeDelay(self,_sec,_val):
        self.sec = _sec;
        self.val = _val;
        self.curThread = threading.Thread( target=runTargetTTL, args=(self,));
        self.curThread.start();
        pass;
    def runnable(self):
        self.bttsTTL.write(self.channel,self.val);
        time.sleep(self.sec);
        self.bttsTTL.write(self.channel,0);
        pass;

class BTTsTTLU3(BTTsTTL):
    # DAC0
    # 0 analog in
    # 1 analog in 
    # 2 digital in
    # 4 digital out

    #_FIOAnalog    = 0b00000011;
    #_FIODirection = 0b00010000;
    #tmpSInfo = d.configU3(FIOAnalog =_FIOAnalog , FIODirection = _FIODirection);
    #print(tmpSInfo)
    
    def __init__(self):
        super().__init__();
        #FIO4_STATE_REGISTER 
        self.RegDAC0 = 5000;
        self.RegFIO0 = 6000  # the address of line FIO0
        self.RegFIO2 = 6002  # the address of line FIO2
        self.RegFIO4 = 6004  # the address of line FIO4
        
    def begin(self):
        # IONumber: 0-7=FIO, 8-15=EIO, 16-19=CIO
        # Direction: 1 = Output, 0 = Input
        self.ports = u3.U3()
        self.ports.getFeedback(u3.BitDirWrite(IONumber = 4, Direction = 0))
        pass;
    def end(self):
        self.ports.close();
        pass;
    def write(self,channel,val):
        if channel == 0:
            volt = 0.5 * val;
            DAC0_VALUE = self.ports.voltageToDACBits(volt, dacNumber = 0, is16Bits = False)
            self.ports.getFeedback(u3.DAC0_8(DAC0_VALUE))        # Set DAC0 to xx V
        else:
            if val == 0:
                oVal = 0;
            else:
                oVal = 1;
            self.ports.writeRegister(self.RegFIO4,oVal);
        pass;
    def read(self,_channel):
        retObject = self.ports.getFeedback(u3.PortStateRead());
        retV = 0 if (( retObject[-1]['FIO'] & ( 1<< _channel ) )==0) else 1;
        return retV;


class BTTsTTLUSB2TTL8(BTTsTTL):
    def __init__(self):
        super().__init__();
        self.p_port = None;
    def begin(self):
        self.p_port = labhackers.USB2TTL8()
        pass;
    def end(self):
        pass;
    def write(self,channel,val):
        if val == 0:
            oVal = 0;
        else:
            oVal = 1;
        self.p_port.setData(val);

def mainD():
    d = u3.U3()
    d.configIO(FIOAnalog = 1) # Set FIO0 to analog
    
    d.writeRegister(5000, 3) # Set DAC0 to 3 V
    val = d.getAIN(0, 32)
    print(val);
    #3.0141140941996127    
    time.sleep(2.0);
    d.writeRegister(5000, 0) # Set DAC0 to 3 V
    val = d.getAIN(0, 32)
    print(val);
    time.sleep(2.0);
    val = d.getAIN(0, 32)
    print(val);
    pass;

def mainB():
    d = BTTsTTLU3();
    #d = BTTsTTL();
    
    d.begin();
    
    d.write(0,3);
    time.sleep(0.1);
    d.write(0,0);
    
    d.end();

def mainC():
    d = BTTsTTLU3();
    #d = BTTsTTL();
    
    d.begin();
    
    dt = BTTsTTLDelay(d,0);
    
    for vol in [0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2]:
        dt.writeDelay(0.1, vol);
        time.sleep(0.2);
    
    d.end();



def mainA():
    #FIO4_STATE_REGISTER 
    RegDAC0 = 5000;
    RegFIO0 = 6000  # the address of line FIO0
    RegFIO2 = 6002  # the address of line FIO2
    RegFIO4 = 6004  # the address of line FIO4
    
    d = u3.U3()
    # FIO 
    # 0 analog in
    # 1 analog in 
    # 2 digital in
    # 4 digital out
    
    _FIOAnalog    = 0b00000011;
    _FIODirection = 0b00010000;
    tmpSInfo = d.configU3(FIOAnalog =_FIOAnalog , FIODirection = _FIODirection);
    print(tmpSInfo)
    
    tmpS = d.getCalibrationData();
    print(tmpS);

    DAC0_VALUE = d.voltageToDACBits(1.5, dacNumber = 0, is16Bits = False)
    d.getFeedback(u3.DAC0_8(DAC0_VALUE));

    ain0bits, = d.getFeedback(u3.AIN(0));
    print(ain0bits);

    #ainValue = d.binaryToCalibratedAnalogVoltage(ain0bits, isLowVoltage = False, channelNumber = 0)
    #print(ainValue)
    
    DAC0_VALUE = d.voltageToDACBits(0.0, dacNumber = 0, is16Bits = False)
    d.getFeedback(u3.DAC0_8(DAC0_VALUE));
    ain0bits, = d.getFeedback(u3.AIN(0));
    tmpV = d.getAIN(0);
    print(ain0bits);
    print(tmpV);

    return;
    
    
    
    
    
    d.writeRegister(RegFIO2,1);
    time.sleep(0.010);
    d.writeRegister(RegFIO2,0);
    time.sleep(0.010);


    d.close();

    pass;

def mainE():
    d = BTTsTTLU3();
    #d = BTTsTTL();
    d.begin();

    print(mainE);
    print(d.ports.configU3());
    
    d.write(0,3);
    time.sleep(0.1);
    d.write(0,0);
    
    inx = d.read(4);
    print(inx);
    d.end();



if __name__ == "__main__":
    #mainA();
    #mainB();
    #mainD();
    mainE();
    
