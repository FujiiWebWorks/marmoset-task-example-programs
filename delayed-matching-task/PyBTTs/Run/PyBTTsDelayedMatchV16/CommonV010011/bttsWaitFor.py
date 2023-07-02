#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os  # handy system and path functions
import sys  # to get file system encoding

import threading
import time

# for time
from ctypes import windll
from time import perf_counter

class BTTsWaitFor:
    def __init__(self):
        self.curThread = None;
        self.flagBreak = False;
        self.holdTime = None;
        self.nowTime = None;
        self.flagBreakeEscape = False;
        pass;
    def beginPeriod(self):
        windll.winmm.timeBeginPeriod(1)
        pass;
    def endPeriod(self):
        windll.winmm.timeEndPeriod(1)
        pass;
    def getTime(self):
        return perf_counter();
        pass;
    def sleepLoop(self, _nextTM):
        while True:
            sl_curTM = self.getTime();
            if sl_curTM < _nextTM:
                pass;
            else:
                break;
        pass;
    def sleepA(self,_sec):
        time.sleep(_sec);
        pass;
    def sleepB(self,_sec):
        if _sec == 0.0:
            return;
        lsec = 0.0016; # 1.6 msec
        if _sec < lsec:
            asec = 0.0;
        else:
            asec = _sec - lsec;
        self.beginPeriod();
        sb_hold = self.getTime();
        self.endPeriod();
        if asec != 0.0:
            self.sleepA(asec);
        self.beginPeriod();
        self.sleepLoop(sb_hold + _sec);
        self.endPeriod();
        pass;
    def waitForOldXXX(self, _sec):
        # waitFor can not use;
        self.flagBreak = False;
        flagLoop = True;
        bTime = _sec;
        #bTime = 0.001;
        self.beginPeriod();           
        self.holdTime = self.getTime();
        while flagLoop:
            self.nowTime = self.getTime();
            if _sec <= (self.nowTime - self.holdTime):
                flagLoop = False;
            if self.flagBreak:
                flagLoop = False;
            if flagLoop:
                self.sleepA(bTime);
        pass;
        self.endPeriod();
    def stampNextFor(self):
        self.beginPeriod();
        self.holdTime = self.getTime();
        self.endPeriod();
        
    def nextFor(self, _nextSec, _callback=None, _callbackArgs=None):
        ###self.nextForTypeSeep(_nextSec,_callback, _callbackArgs);
        if True:
            print("BTTsWaitFor nextFor _nextSec "+str(_nextSec));
        self.nextForTypeTimer(_nextSec,_callback, _callbackArgs);
        pass;
    def nextForTypeTimer(self, _nextSec, _callback=None, _callbackArgs=None):
        self.flagBreak = False;
        flagLoop = True;
        while(flagLoop):
            if self.timerFor( _nextSec):
                flagLoop = False;
            else:
                pass;
                self.beginPeriod();
                self.sleepA(0.001);
                self.endPeriod();
                pass;
            if self.flagBreak: 
                #print("BTTsWaitFor nextFor flagBreak " + str(self.flagBreak));
                flagLoop = False;
            if flagLoop:
                if( _callback != None ):
                    _callback(_callbackArgs);
                pass;
            pass;
        pass;

    def nextForTypeSeep(self, _nextSec, _callback=None, _callbackArgs=None):
        countNF = 0;
        self.flagBreak = False;
        flagLoop = True;
        self.beginPeriod();
        #
        #bTime = 0.001;
        bTime = 0.020;
        while flagLoop:
            self.nowTime = self.getTime();
            nextTime = self.holdTime + _nextSec;
            diffTime = nextTime-self.nowTime;
            if ( countNF % 10 ) == 0:
                #print("nextFor a lop "+str(self.nowTime) + " " + str(countNF) + " " + str(self.flagBreak));
                pass;
            countNF += 1;
            if self.nowTime >= nextTime:
                flagLoop = False;
                sTime = 0.0;
            else:
                if diffTime < bTime:
                    sTime = diffTime;
                    flagLoop = False;
                else:
                    sTime = bTime;
                    pass;
            if self.flagBreak: 
                #print("BTTsWaitFor nextFor flagBreak " + str(self.flagBreak));
                flagLoop = False;
            if flagLoop:
                if( _callback != None ):
                    _callback(_callbackArgs);
            self.sleepB(sTime);
        pass;
        self.endPeriod();
        
    def breakWait(self):
        print("BTTsWaitFor breakWait 01");
        #self.curThread.interrupt();
        self.flagBreak = True;
        print("BTTsWaitFor breakWait end");
        pass;
    def breakWaitForEscape(self):
        self.flagBreakeEscape = True;
        self.breakWait();
        pass;
    
    def timerFor(self, _nextSec):
        retB = False;
        self.beginPeriod();
        self.nowTime = self.getTime();
        nextTime = self.holdTime + _nextSec;
        if nextTime < self.nowTime:
            retB = True;
        else:
            retB = False;
        self.endPeriod();
        return retB;
        
