#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from psychopy import sound,core, data, event, logging, clock
from psychopy import core, data, event, logging, clock
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)

from psychopy.iohub import launchHubServer
from psychopy.iohub.constants import EventConstants

import os  # handy system and path functions
import sys  # to get file system encoding

import threading
import time

# for time
from ctypes import windll
# タイマー精度を1msec単位にする
from time import perf_counter

sys.path.append('../PyDIO');
from wapperPyDIOBase import OneTrigger
sys.path.append('../PyDIOLabHacksBeta');
from wrapperPyDIOLabHacksBeta import OneTriggerLabHacksBeta
sys.path.append('../PyDIONIDAQ');
from wrapperPyDIONIDAQ import OneTriggerPyNIDAQ
from wrapperPyDIONIDAQ import OneTriggerPyNNNIDAQ

from bttsValue import ValueInt32, ValueFloat32, ValueFloat32Array,ValueBool8
from bttsValue import ValueRecInt32, ValueRecFloat32,ValueRecBool8
from bttsWaitFor import BTTsWaitFor

class BTTsTool:
    def __init__(self):
        pass;
    @staticmethod
    def initComponents(trialComponents):
        for stim in trialComponents:
            thisComponent = stim.stim;
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
            pass;
        pass;
    @staticmethod
    def containsComponent(trialComponents,_mEvent):
        ret = False;
        #print('BTTsTool containsComponent 01');
        for stim in trialComponents:
            thisComponent = stim.stim;
            if thisComponent.contains(_mEvent.mLastPos ):
                print('BTTsTool containsComponent 02');
                #print(thisComponent);
                ret = True;
                pass;
        #print('BTTsTool containsComponent end');
        return ret;
    @staticmethod
    def containsComponentPos(trialComponents,_pos):
        ret = False;
        print('BTTsTool containsComponentPos 01');
        for stim in trialComponents:
            thisComponent = stim.stim;
            if thisComponent.contains(_pos):
                print('BTTsTool containsComponentPos 02');
                print(thisComponent);
                ret = True;
                pass;
        print('BTTsTool containsComponentPos end');
        return ret;
    @staticmethod
    def areaIn( _cPosX, _cSizeX, _posX):
        ret = False;
        x = _posX - _cPosX;
        halfx = _cSizeX / 2.0;
        if -halfx <= x and x < halfx:
            ret = True;
        return ret;
    @staticmethod
    def containPos(_cPos, _cSize, _pos):
        flagX = BTTsTool.areaIn(_cPos[0], _cSize[0], _pos[0]);
        flagY = BTTsTool.areaIn(_cPos[1], _cSize[1], _pos[1]);
        pass;
        return flagX and flagY;
    @staticmethod
    def containsComponentPosBTTsVS(_vs,_pos):
        ret = False;
        thisComponent = _vs.stim;
        if _vs.stimAttr.flagStimArea:
            ret = BTTsTool.containPos(_vs.stimAttr.stimPos, _vs.stimAttr.stimAreaSizeForTouch,_pos);
        else:
            ret = BTTsTool.containPos(_vs.stimAttr.stimPos, _vs.stimAttr.stimSize,_pos);
            pass;
        return ret;
    @staticmethod
    def outputPsydata(_psydata):
        sortColumns=False;
        matrixOnly=False;
        delim = ',';
        #
        names = _psydata._getAllParamNames()
        names.extend(_psydata.dataNames)
        # names from the extraInfo dictionary
        names.extend(_psydata._getExtraInfo()[0])
        if len(names) < 1:
            logging.error("No data was found, so data file may not look as expected.")
        # sort names if requested
        if sortColumns:
            names.sort()
        # write a header line
        if not matrixOnly:
            for heading in names:
                print(u'%s%s' % (heading, delim))
            print('\n')

        # write the data for each entry
        for entry in _psydata.getAllEntries():
            for name in names:
                if name in entry:
                    ename = str(entry[name])
                    if ',' in ename or '\n' in ename:
                        fmt = u'"%s"%s'
                    else:
                        fmt = u'%s%s'
                    print(fmt % (entry[name], delim))
                else:
                    print(delim)
            print('\n')
        pass;
    @staticmethod
    def str2bool(s):
        return s.lower() in ["true", "t", "yes", "1"]   

class BTTsParam():
    def __init__(self):
        self.currentDirectory = "cur";
        self.filename = "filename.py";
        self.isMainFunction = False;
        self.paramButtonIn = ParamButtonIn();       
        self.screenscale=100;
        self.paramList = [];
        self.valueList = [];
        self.waitBeforeRun = ValueFloat32('waitBeforeRun',5.0);
        self.paramList.append(self.waitBeforeRun);
    def initOtherParam(self):
        self.flagRunOneLoopForTest = ValueBool8('flagRunOneLoopForTest',False);
        self.flagTestModeDisplayInfo = ValueBool8('flagTestModeDisplayInfo',False);
        self.virticalSyncTimestampFrame = ValueInt32('virticalSyncTimestampFrame',0); 
        self.paramList.append(self.flagRunOneLoopForTest);
        self.paramList.append(self.flagTestModeDisplayInfo);
        self.paramList.append(self.virticalSyncTimestampFrame);
        #
        self.paramList.append(self.paramButtonIn.flagChatteringBlockForTTL);
        self.paramList.append(self.paramButtonIn.isTTLKeyEmu);
        
        pass;
    def printValueList(self):
        for val in self.valueList:
            print(val.vname);
            print(str(val.value));
        pass;
    def printParamList(self):
        print("printParamList 01");
        for val in self.paramList:
            print(val.vname);
            print(str(val.value));
        print("printParamList end");
        pass;

class BTTsTrial:
    def __init__(self):
        pass;

class BTTsTrials:
    def __init__(self,_bttsTh, _stateBuffer, _oneTrigger):
        #self.trials = _trials;
        self.bttsTh = _bttsTh;
        self.stateBuffer = _stateBuffer;
        self.oneTrigger = _oneTrigger;
        pass;
    def create(self):
        pass;
    def getTH(self):
        return None;
    def getResponsesTH(self):
        return None;


class ParamButtonIn:
    def __init__(self):
        self.flagChatteringBlockForTTL  = ValueBool8("TTL_ChatteringBlock",True);
        self.isTTLKeyEmu = ValueBool8("TTL_KeyEmulate(ALT)",False);
        pass;

class ButtonIn():
    def __init__(self,_paramButtonIn, _keyIO,_ttlAout ):
        self.paramButtonIn = _paramButtonIn;
        self.keyIO = _keyIO;
        self.ttlAout = _ttlAout;
        self.kb_events = None;
        self.b1 = False;
        self.b2 = False;
        self.holdB1 = False;
        self.holdB2 = False;
        self.edgeB1 = False;
        self.edgeB2 = False;
        
        self.flagChatteringBlockForTTL = self.paramButtonIn.flagChatteringBlockForTTL.value;
        self.flagTTL = True;
        if self.paramButtonIn.isTTLKeyEmu.value:
            self.flagTTL = False;
        else:
            if self.ttlAout != None:
                pass;
            else:
                self.flagTTL = False;
                pass;
            pass;
    
        self.waitForForLog = BTTsWaitFor();
        self.logNum = [];
        self.logTime = [];
        pass;
    def lastLog(self):
        #for tm in self.logTime:
        #    print("buttonLog\t"+str(tm));
        #    pass;
        pass;
    def resetState(self):
        if self.flagTTL:
            pass;
        else:
            #self.keyIO.resetState();
            self.keyIO.clearEvents();
            pass;
    def updateEvent(self):
        if self.flagTTL:
            pass;
        else:
            if self.keyIO != None:
                self.kb_events = self.keyIO.getEvents();     
            pass;
        pass;
    def getButton(self):
        self.edgeB1 = False;
        self.edgeB2 = False;
        
        self.updateEvent();
        num = self.getNumOf();
        if num != 0:
            pass;
            #print("getButton " + str(num));
        for n in range(num):
            self.updateOne(n);
        pass;
        ##print((self.b1,self.b2));
        pass;
        return (self.b1,self.b2,self.edgeB1, self.edgeB2);
    def getNumOfOldFunction(self):
        ret = 1;
        if self.flagTTL:
            ret = 1;
            pass;
        else:
            if self.kb_events != None:
                ret = len(self.kb_events);
            else:
                ret = 0;
            pass;
        return ret;
    def getNumOf(self):
        ret = 0;
        if self.flagTTL:
            ret = 1;
            pass;
        else:
            if self.kb_events != None:
                ret = len(self.kb_events);
            else:
                ret = 0;
            pass;
        return ret;
    def updateOne(self, _ix):
        self.waitForForLog.beginPeriod();
        self.logTime.append(self.waitForForLog.getTime());
        self.waitForForLog.endPeriod();
        #
        if self.flagTTL:
            if self.flagChatteringBlockForTTL:
                for n in range(3):
                    btns1 = self.ttlAout.readDIO();
                    time.sleep(0.001);
                    btns2 = self.ttlAout.readDIO();
                    if btns1 == btns2:
                        break;
                btns = btns2;
            else:
                btns = self.ttlAout.readDIO();
            #
            self.b1 = True if btns & 0x01 else False;
            self.b2 = True if btns & 0x02 else False;
            if self.b1 != self.holdB1:
                self.edgeB1 = True;
            self.holdB1 = self.b1;
            pass;
            if self.b2 != self.holdB2:
                self.edgeB2 = True;
            self.holdB2 = self.b2;
        
        else:
            kb_event = self.kb_events[_ix];
            print(kb_event);
            if kb_event.key_id == 164:
                if kb_event.type == EventConstants.KEYBOARD_RELEASE:
                    self.b1 = False;
                    self.edgeB1 = True;
                    pass;
                elif kb_event.type == EventConstants.KEYBOARD_PRESS:
                    self.b1 = True;
                    self.edgeB1 = True;
                    pass;
                else:
                    pass;
            if kb_event.key_id == 165:
                if kb_event.type == EventConstants.KEYBOARD_RELEASE:
                    self.b2 = False;
                    self.edgeB2 = True;
                    pass;
                elif kb_event.type == EventConstants.KEYBOARD_PRESS:
                    self.b2 = True;
                    self.edgeB2 = True;
                    pass;
                else:
                    pass;

        pass;



def runTarget(that):
    that.runnable();
    pass;


def callbackNF(that):
    that.callbackNextFor();

class BTTsThreading():
    def __init__(self,_buttonIn,_msIO, _keyIO, _oneTrigger, _oneTriggerForThread):
        self.buttonIn = _buttonIn;
        self.msIO = _msIO;
        self.keyIO = _keyIO;
        self.oneTrigger = _oneTrigger;
        self.oneTriggerForThread = _oneTriggerForThread;
        self.waitFor = None;
        self.curThread = None;
        self.oneTrial = None;  #BTTsOneTrial
        self.trial = None;
        self.flagLoopTrial = False;
        self.b1 = False;
        self.b2 = False;
        self.edgeB1 = False;
        self.edgeB2 = False;
        pass;
    def begin(self):
        self.waitFor = BTTsWaitFor();
        self.curThread = threading.Thread( target=runTarget, args=(self,));
        self.curSemaphore = threading.BoundedSemaphore(1);
        pass;
    def end(self):
        self.curThread.join();
        if self.oneTrigger != None:
            self.oneTrigger = None;
        self.curSemaphore = None;
        self.waitFor = None;
        pass;
    def start(self):
        self.curThread.start();
        pass;
    def stop(self):
        print("BTTsThreading stop 01");
        self.flagLoopTrial = False;
        #self.waitFor.breakWait();
        self.waitFor.breakWaitForEscape();
        print("BTTsThreading stop 02");
        self.curThread.join();
        print("BTTsThreading stop 03");
        
        print("BTTsThreading stop end");
        pass;
    def initCallbackNextFor(self):
        self.countCallback = 0;
    def callbackNextFor(self):
        if (self.countCallback % 100) == 0:
            print("callbackNextFor "+str(self.countCallback));
            #tmpNowTime = self.waitFor.nowTime;
            #tmpStr = "callbackNextFor";
            #tmpStr += ",";
            #tmpStr += str(self.countCallback);
            #tmpStr += ",";
            #tmpStr += str(tmpNowTime);
            #print(tmpStr);
            pass;
        pass;
        flag = True;
        if (self.countCallback % 1) == 0:
            flag = True;
        pass;
        self.countCallback+=1;
        
        if flag and self.msIO != None:
            msEv = self.msIO.getEvents();
            sz = 0;
            if msEv:
                sz = len( msEv );
            #
            if sz != 0:
                #MouseButtonPressEventNT(experiment_id=0, session_id=0, device_id=0, event_id=198, type=32, device_time=21069.875, logged_time=21.337433599997894, time=21.337433599997894, confidence_interval=0.0, delay=0.0, filter_id=0, display_id=0, button_state=11, button_id=2, pressed_buttons=2, x_position=-0.5768518518518518, y_position=0.13055555555555556, scroll_dx=0, scroll_x=0, scroll_dy=0, scroll_y=0, modifiers=[], window_id=722744)
                ## oneMSEV = msEv[-1];
                for oneMSEV in msEv:
                    if True and (( oneMSEV.pressed_buttons & 2 )==2):
                        if oneMSEV.type == EventConstants.MOUSE_MOVE:
                            print(oneMSEV)
                            pass;
                        elif oneMSEV.type == EventConstants.MOUSE_DRAG:
                            print(oneMSEV)
                            pass;
                        elif oneMSEV.type == EventConstants.MOUSE_BUTTON_PRESS:
                            print(oneMSEV)
                            pass;
                        elif oneMSEV.type == EventConstants.MOUSE_BUTTON_RELEASE:
                            print(oneMSEV)
                            pass;
        pass;
    def runnableT01(self):
        print("runnableT01");
        lop = True;
        curTime=0.0;
        addingTime = 0.010;
        curTime += addingTime;
        self.waitFor.stampNextFor();     
        while lop:
            if self.oneTrigger != None:
                #self.oneTrigger.writeDelay(0.0, 255, pWidthsec=0.001);
                pass;
            self.waitFor.nextFor(curTime);
            curTime += addingTime;
            if self.waitFor.flagBreak:
                lop = False;
        pass;
    def runnableT01_callback(self):
        print("runnableT01");
        lop = True;
        self.initCallbackNextFor();
        curTime=0.0;
        addingTime = 0.100;
        curTime += addingTime;
        self.waitFor.stampNextFor();     
        while lop:
            if self.oneTrigger != None:
                #self.oneTrigger.writeDelay(0.0, 255, pWidthsec=0.001);
                pass;
            self.waitFor.nextFor(curTime,callbackNF,self );
            curTime += addingTime;
            if self.waitFor.flagBreak:
                lop = False;
        pass;
    def runnableT02(self):
        print("runnableT02");
        lop = True;
        curTime=0.0;
        addingTime = 0.010;
        while lop:
            if self.oneTrigger != None:
                #self.oneTrigger.writeDelay(0.0, 255, pWidthsec=0.001);
                pass;
            self.waitFor.waitFor(addingTime);
            curTime += addingTime;
            if self.waitFor.flagBreak:
                lop = False;
            pass;
    def getButton(self):
        (b1, b2, edgeB1, edgeB2) = self.buttonIn.getButton();
        self.b1 = b1;
        self.b2 = b2;
        self.edgeB1 = edgeB1;
        self.edgeB2 = edgeB2;
        return (b1,b2,edgeB1,edgeB2);
        
    def runnableTrialLoop(self):
        print("runnableTrialLoop 01");
        self.flagLoopTrial = True;
        while( self.flagLoopTrial ):
            self.curSemaphore.acquire();
            curOneTrial = self.oneTrial;
            self.oneTrial = None;
            self.curSemaphore.release();
            if( curOneTrial != None ):
                #print("runnableTrialLoop 02");
                curOneTrial.waitFor = self.waitFor;
                curOneTrial.runnable();
                self.curSemaphore.acquire();
                curOneTrial = None;
                self.curSemaphore.release();
                #print("runnableTrialLoop 03");
            else:
                (b1, b2,e1,e2) = self.getButton();
                
                self.waitFor.beginPeriod();           
                self.waitFor.sleepA(0.001);
                self.waitFor.endPeriod();
                pass;
            if self.waitFor.flagBreak:
                self.flagLoopTrial = False;
            #print("runnableTrialLoop 04");
        pass;
        print("runnableTrialLoop end");
    def runnable(self):
        self.runnableTrialLoop();
        
        #self.runnableT01();
        ######self.runnableT02();
        #self.runnableT01_callback();
        pass;

class BTTsTrialControl:
    def __init__(self,_param,_stateBuffer, _oneTrigger, _oneTriggerForThread):
        self.param = _param;
        self.stateBuffer = _stateBuffer;
        self.oneTrigger = _oneTrigger;
        self.oneTriggerForThread = _oneTriggerForThread;
        self.trials = None;
        self.msIO = None;
        self.keyIO = None;
        self.bttsTh = None;
        self.buttonIn = None;
        pass;
    def newBTTsTrials(self):
        return self.trials;
    def beginThread(self):
        self.buttonIn = ButtonIn(self.param.paramButtonIn ,self.keyIO,self.oneTriggerForThread);
        self.bttsTh = BTTsThreading(self.buttonIn,self.msIO,self.keyIO,self.oneTrigger,self.oneTriggerForThread);
        self.bttsTh.begin();
        self.bttsTh.start();
        pass;
    def endThread(self):
        print("endThread 01");
        if self.bttsTh != None:
            self.bttsTh.stop();
            print("endThread 02");
            self.bttsTh.end();
        self.bttsTh = None;
        print("endThread end");
        pass;
    def loopOutThread(self):
        print("loopOutThread 01");
        if self.bttsTh != None:
            self.bttsTh.flagLoopTrial = False;
        pass;
        print("loopOutThread end");
        pass;


class BTTsExperiment:
    def __init__(self, _oneTrigger):
        self.oneTrigger = _oneTrigger;
        pass;
    def create(self, _filename,param):
        pass;
    def pr(self):
        pass;
    def getTrials(self):
        return None;

class BTTsOneTrial():
    def __init__(self,_trials, _bttsTh, _stateBuffer, _oneTrigger):
        #super().__init__();
        self.trials = _trials;
        self.bttsTh = _bttsTh;
        self.param = None;
        self.stateBuffer = _stateBuffer;
        self.oneTrigger = _oneTrigger;
        self.pWidthsec = 0.004;
        self.trialComponents = [];
        self.flagOverrapeNextPhase = False;
        self.flagNextPhase = False;
        pass;
    def setParameter(self, _param):
        pass;
    def run(self):
        self.runnable();
        pass;
    def runnable(self):
        pass;
    def stampNextForPhase(self):
        self.curSecPhase = 0.0;
        self.bttsTh.waitFor.stampNextFor();
        pass;
    def waitSecForPhase(self, _sec,_flagRetDef=True, _callback=None, _callbackArgs=None):
        self.curSecPhase += _sec;
        self.flagOverrapeNextPhase = False;
        self.flagRet = _flagRetDef;
        self.bttsTh.waitFor.nextFor(self.curSecPhase, _callback, _callbackArgs);
        #### time.sleep(_sec);
        #### #core.wait(_sec);
        flgRet = _flagRetDef;
        if self.flagOverrapeNextPhase :
            flgRet = self.flagNextPhase;
            pass;
        else:
            pass;
        pass;
        return flgRet;
    def breakWaitSecForPhase(self):
        self.flagOverrapeNextPhase=True;
        self.flagNextPhase = False;
        if self.bttsTh != None:
            self.bttsTh.waitFor.breakWait();
        pass;
    def breakWaitSecForPhaseChoise(self):
        self.flagOverrapeNextPhase=True;
        self.flagNextPhase = True;
        if self.bttsTh != None:
            self.bttsTh.waitFor.breakWait();
        pass;
    def getFlagBreakeEscapeWaitFor(self):
        print("getFlagBreakeEscapeWaitFor" + str(self.bttsTh.waitFor.flagBreakeEscape));
        return self.bttsTh.waitFor.flagBreakeEscape;
        pass;
    def inputEventMouse(self,_curState, _trialComponents, _mEvent):
        # @override
        #print("BTTsOneTrialDM inputEventMouse 01");
        # mouse
        flag = False;
        if _mEvent.mButtons is None:
            #none
            pass;
        else:
            if _mEvent.mButtons != [0,0,0]:
                print(_mEvent.mButtons);
                print(_mEvent.mTimes);
                #print(_mEvent.mLastPos);
                #print(_mEvent.mLastPosTime);
                flag = BTTsTool.containsComponent(_trialComponents,_mEvent);
            pass;
        if flag:
            self.waitFor.breakWait();
        #print("BTTsOneTrialDM inputEventMouse end");
        pass;
        
class BTTsState:
    def __init__(self):
        self.timestamp = None;
        self.state = None;
        self.state1 = None;
        self.state2 = None;
        self.flagTrial = False;
        self.responeded = False; # state2 responded
        pass;
    def pr(self):
        tmpS = str(self.timestamp);
        tmpS += "\t";
        tmpS += str(self.state);
        tmpS += "\t";
        tmpS += str(self.state1);
        tmpS += "\t";
        tmpS += str(self.state2);
        print(tmpS);
        
class BTTsStateBuffer:
    def __init__(self):
        self.stateSemaphore = threading.BoundedSemaphore(1);
        self.stateBuffer = []; 
        self.clock = core.Clock();
        #
        self.flagPr = False;
        pass;
        self.modeOneState = True;
        pass;
    def release(self):
        if self.flagPr:
            print("BTTsStateBuffer release 01");
        self.stateSemaphore.release();
        if self.flagPr:
            print("BTTsStateBuffer release end");
        pass;
    def acquire(self):
        if self.flagPr:
            print("BTTsStateBuffer acquire 01");
        self.stateSemaphore.acquire();
        if self.flagPr:
            print("BTTsStateBuffer acquire end");
        pass;
    def appendBuffer(self,obj):
        print("appendBuffer");
        obj.pr();
        self.stateBuffer.append(obj);
        pass;
    def moveStateBuffer(self):
        retBuf = [];
        if self.modeOneState:
            sz = len(self.stateBuffer);
            if sz != 0:
                for cur in self.stateBuffer:
                    retBuf.append( cur );
                #retBuf.append ( self.stateBuffer[-1] );
                self.stateBuffer.clear();
        else:
            tmp1 = len(self.stateBuffer);
            #retBuf = self.stateBuffer;
            retBuf = self.stateBuffer.copy();
            tmp2 = len(retBuf);
            self.stateBuffer.clear();
            tmp3 = len(self.stateBuffer);
            tmp4 = len(retBuf);
            #
            tmpStr = str(tmp1);
            tmpStr += " ";
            tmpStr += str(tmp2);
            tmpStr += " ";
            tmpStr += str(tmp3);
            tmpStr += " ";
            tmpStr += str(tmp4);
            #print('moveStateBuffer ' + tmpStr);
        return retBuf;

class BTTsMouseEvent:
    def __init__(self):
        self.mButtons = None;
        self.mTimes = None;
        self.mLastPos = None;
        self.mLastPosTime = None;
        pass;
    def pr(self):
        tmpS = "";
        tmpS += str(self.mLastPos);
        tmpS += " ";
        tmpS += str(self.mButtons);
        print(tmpS);
        pass;


class LoopFlag:
    def __init__(self):
        self.flagLoop = True;
        self.flagRequestLoopOut = False;
    def isLoopFlag(self):
        if self.flagRequestLoopOut:
            self.flagRequestLoopOut = False;
            self.flagLoop = False;
        return self.flagLoop;
    def requestFlagLoopOut(self):
        self.flagRequestLoopOut = True;
        pass;
    def init(self):
        self.flagLoop = True;
        self.flagRequestLoopOut = False;
        pass;



class BTTsColor():
    def __init__(self, tColor):
        self.num = tColor[0];
        self.cname = tColor[1];
        self.color = [tColor[2],tColor[3],tColor[4]];
        pass;

class BTTsShape:
    def __init__(self,tShape):
        self.num = tShape[0];
        self.sname = tShape[1];
        self.shapePos = tShape[2];
        pass;
        
class BTTsStimAttr():
    def __init__(self):
        self.isImage = False;
        self.stimPos = [0.0, 0.0];
        self.stimSize = [0.15,0.15];
        self.stimName = "(No name stim)";
        self.flagStimArea = False;
        self.stimAreaSizeForTouch = [0.3, 0.3];
        self.color = None;
        self.shape = None;
    def copyFromLow(self, _from):
        self.isImage = _from.isImage;
        self.stimPos = _from.stimPos.copy();
        self.stimSize = _from.stimSize.copy();
        self.stimName = _from.stimName; # pointer copy
        self.flagStimArea = _from.flagStimArea;
        self.stimAreaSizeForTouch = _from.stimAreaSizeForTouch.copy();
        self.color = _from.color; # pointer copy
        self.shape = _from.shape; # pointer copy
        
        pass;

class BTTsVisualStim():
    def __init__(self):
        self.stim = None;
        self.stimAttr = BTTsStimAttr(); # new
        self.select = False; # 選択対象
        self.correct = False; # 正解
        pass;
    def copyFromLow(self, _from):
        self.stim = _from.stim; # stim is pointer 
        self.stimAttr.copyFromLow(_from.stimAttr);
        pass;
    def prInfo(self):
        tmpStr = self.stimAttr.stimName;
        tmpStr += " ";
        tmpStr += str( self.stimAttr.stimPos);
        tmpStr += " ";
        tmpStr += str(self.stimAttr.stimSize);
        tmpStr += " ";
        tmpStr += str(self.stimAttr.color);
        print(tmpStr);
        print(self.stim);
        pass;
    def prCorrect(self):
        tmpStr = str(self.select) + " / " + str(self.correct);
        print("BTTsVisualStim select/correct" + tmpStr);
        pass;


import serial
class BTTsPunishment:
    def __init__(self, _param):
        self.param = _param;
        pass;
    def begin(self):
        pass;
    def end(self):
        pass;

class BTTsReward:
    def __init__(self, _param):
        self.param = _param;
    def begin(self):
        pass;
    def end(self):
        pass;
    def clearRewarded(self):
        pass;
    def reward(self, _reward):
        pass;

"""
class BTTsFeederFood:
    def __init__(self, _param):
        self.param = _param;
        self.flagOneReward = False;
        curCOM1='COM1'; # COM1
        curCOM2='COM2'; # COM2
        curCOM3='COM3'; # COM3
        curCOM4='COM4'; # COM4
        #
        #curCOM=curCOM3;
        self.curCOM=None;
        self.comXX = None;
    def begin(self):
        if self.curCOM != None:
            self.comXX = serial.Serial(self.curCOM,9600);
    def end(self):
        if self.comXX != None:
            self.comXX.close()
            self.comXX = None;
    def clearRewarded(self):
        self.flagOneReward = False;
    def isAllreadRewarded(self):
        return self.flagOneReward;
    def reward(self, _reward):
        if self.flagOneReward:
            pass;
        else:
            if _reward:
                print("reward");
                #print('reward trail'+ str(trials.thisTrialN));
                if self.param.flag_reward_drink.value:
                    if self.comXX != None:
                        self.comXX.write(b'd1100x');
                else:
                    if self.comXX != None:
                        self.comXX.write(b'A');
            flagOneReward = True;
        pass;
"""

class BTTsTTL:
    def __init__(self):
        pass;
    def write(self,sec,val):
        pass;
class BTTsTTLU3(BTTsTTL):
    def __init__(self):
        super().__init__();
