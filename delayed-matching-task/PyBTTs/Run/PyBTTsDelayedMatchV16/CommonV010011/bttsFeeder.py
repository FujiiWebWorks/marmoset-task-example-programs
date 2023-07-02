# -*- coding: utf-8 -*-

import sys
import serial

#
from bttsWaitFor import BTTsWaitFor

class BTTsFeederFood:
    def __init__(self,param, envParam):
        self.param = param;
        self.envParam = envParam;
        
        #curCOM1='COM1'; # COM1
        #curCOM2='COM2'; # COM2
        #curCOM3='COM3'; # COM3
        self.comXX = None;
        #
        self.flagAllready = True;
        self.intervalSec = 1.0; # 1.0 sec;
        self.curTime = 0.0;
        self.flagFirst = True;
        self.numOfFeed = 0;
        self.countFeed = 0;
        self.flagFeed = False;
        
        
        self.waitFor = BTTsWaitFor();
        self.flagAllready = False;
        #
        self.flagFeed = False;
        pass;
    def begin(self):
        if self.envParam.fedder_device_use:
            curCOM=self.envParam.feeder_device_comport;
        else:
            curCOM=None;
        pass;
        if curCOM != None:
            self.comXX = serial.Serial(curCOM,9600);
        else:
            self.comXX = None;
        pass;
        print("BTTsFeederFood");
        print(curCOM);
    def end(self):
        if self.comXX != None:
            self.comXX.close()
        comXX = None;
        
        pass;
    
    def feed(self):
        print(self.microlCommand, file=sys.stderr);
        comXX = self.comXX;
        if self.envParam.feeder_device_drink:
            if comXX != None:
                wr = b'd1100x';
                wr = self.microlCommand;
                comXX.write(wr);
        else:
            if comXX != None:
                wr = b'A';
                comXX.write(wr);
            
    def clearFeeder(self):
        self.flagAllready = False;
        pass;
    def isAllready(self):
        return self.flagAllready;
    
    def drinkCheck(self, _microl):
        valint = int(_microl);
        if 0 <valint and valint <=999:
            ret = valint;
        else:
            ret = 33;
        pass;
        return ret;
    def initBase(self, _numOfFeed, _microl):
        self.intervalSec = 1.0; # 1.0 sec;
        self.curTime = 0.0;
        self.curTime += self.intervalSec;
        self.numOfFeed = _numOfFeed;
        self.microl = _microl;
        strMicrolCommaond = "d1"+str(self.drinkCheck( self.microl))+"x";
        self.microlCommand = strMicrolCommaond.encode();
        pass;
        
        
    def initFeeder(self, _feed, _numOfFeed, _microl):
        self.initBase(_numOfFeed, _microl);        
        self.flagAllready = True;
        self.flagFirst = True;
        self.countFeed = 0;
        self.flagFeed = False;
        self.timeStampForCounter();
        if _feed:
            self.flagFeed = True;
        else:
            self.flagFeed = False;
        pass;
    def initButtonFeeder(self,_numOfFeed, _microl):
        self.initBase(_numOfFeed, _microl);        
        self.timeStampForCounter();
        
    def timeStampForCounter(self):
        self.waitFor.stampNextFor();
    
    
    def feedForFlipLoop(self, _buttonB):
        if _buttonB:
            self.flagFeed = False;
            if self.waitFor.timerFor(self.curTime):
                self.feed(); # one
                self.curTime += self.intervalSec;
                pass;

        else:
            flagOneFeed = False;
            if self.flagFeed:
                if self.flagFirst:
                    self.flagFirst = False;
                    flagOneFeed = True;
                    pass;
                else:
                    if self.waitFor.timerFor(self.curTime):
                        flagOneFeed = True;
                        self.curTime += self.intervalSec;
                        pass;
                    else:
                        pass;
                if flagOneFeed:
                    if self.countFeed  < self.numOfFeed:
                        self.feed(); # one
                        self.countFeed += 1;
                    else:
                        self.flagFeed = False;
                        pass;
            else:
                pass;
        
    
