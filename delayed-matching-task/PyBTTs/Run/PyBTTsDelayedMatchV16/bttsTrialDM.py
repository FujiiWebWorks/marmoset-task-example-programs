#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os  # handy system and path functions
import sys  # to get file system encoding
import math
import datetime

bttsEnvPath = '../PyBTTsEnv';
sys.path.append(bttsEnvPath);
sndenvfile = bttsEnvPath + '/'+'PyBTTsSound.py'
is_file = os.path.isfile(sndenvfile)
if is_file:
    from PyBTTsSound import BTTsSoundInfo
else:
    pass # パスが存在しないかファイルではない

#from psychopy import sound,core, data, event, logging, clock
from psychopy import core, data, event, logging, clock
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)

from psychopy.iohub import launchHubServer
from psychopy.iohub.constants import EventConstants

from psychopy.tools.filetools import (openOutputFile, genDelimiter,
                                      genFilenameFromDelimiter)

from psychopy import sound
import psychtoolbox as ptb


import threading
import time

sys.path.append('./CommonV010010');

from bttsValue import ValueInt32, ValueFloat32, ValueFloat32Array,ValueInt32Array,ValueBool8
from bttsValue import ValueRecInt32, ValueRecFloat32,ValueRecBool8,ValueRecString
from bttsValue import ValueInt32Array2D
from bttsValue import ValueString

from bttsTrial import BTTsTool,LoopFlag,BTTsMouseEvent,BTTsStateBuffer
from bttsTrial import BTTsParam,BTTsTrials,BTTsTrialControl,BTTsOneTrial,BTTsExperiment,BTTsState
from bttsTrial import BTTsPunishment, BTTsReward
from bttsTrial import BTTsVisualStim,BTTsColor,BTTsShape
from bttsTrial import  ParamButtonIn;

from bttsWaitFor import BTTsWaitFor
from bttsRandom import RandomList


class RecTime:
    def __init__(self):
        self.valRecFloat32_on = None;
        self.valRecFloat32_off = None;
        #
        self.curRec = None;
        #
        self.flagRecVSync = None;
        self.label = None;
        self.valRecFloat32 = None;
        self.valRecFloat32CueOff = None;
        self.flagAO = None;
        self.volt = None;
        pass;
    def init(self):
        self.flagRecVSync = False;
        self.retLabel = "None";
        self.valueFloatTime = None;
        self.valueFloatTimeCueOff = None;
        self.flagAO = False;
        self.volt = 0.0;    

class BTTsDefineDM:
    def __init__(self):
        self.PHASE_BeforeTask = 1;
        self.PHASE_Sample = 2;
        self.PHASE_Delay = 3;
        self.PHASE_Choise = 4;
        self.PHASE_PreEnd = 5;
        self.PHASE_End = 6;
        self.PHASE_PrePunishment = 7;
        self.PHASE_Punishment = 8;
        self.PHASE_End_Mark = 9;
        self.PHASE_ITI = 10;
        pass;
        self.STATE2_TrialOnT_s = 1;
        self.STATE2_HmHoldOnT_s = 2;
        self.STATE2_HmHoldOffT_s = 3;
        pass;
        # sample
        self.STATE2_CueOnT_s = 4;
        self.STATE2_CueOffT_s = 5;
        # delay
        self.STATE2_HmHold2OnT_s = 6;
        #self.STATE2_HmHold2OffT_s = 5;
        # choise
        self.STATE2_TargetOnT_s = 7;
        self.STATE2_HmReleaseT_s = 8;
        self.STATE2_ReachTargetLimit = 9;
        self.STATE2_TargetTouchT_s = 10;
        self.STATE2_NonTargetTouchT_s = 11;
        self.STATE2_TargetHoldOff_s = 12;
        
        pass;
        self.VOL_TrialOn = 0.2;
        self.VOL_HmHoldP = 0.4;
        self.VOL_CueP = 0.6;
        self.VOL_HmHold2P = 0.8;
        self.VOL_TargetOn = 1.0;
        self.VOL_HmRelaese = 1.2;
        self.VOL_TargetTouch = 1.4;
        self.VOL_PreRwdP = 1.6;
        self.VOL_RwdP = 1.8;
        self.VOL_ErrorP = 2.0;
        self.VOL_ITI = 2.2;
        pass;
        self.errorCode0 = 0; #touch limit 
        self.errorCode1 = 1; #Break HomeButton Holding during 1st HB Hold Period
        self.errorCode2 = 2; #Break HB Holding during Cue Period 
        self.errorCode3 = 3; #Break HB Holding during 2nd HB Hold Period
        self.errorCode4 = 4; #Over time. Do not start touching HomeButton
        self.errorCode5 = 5; #Over time. Do not touch Target within the set time.
        self.errorCode7 = 7; #Miss Touch on the Non-Target.
        self.errorCode8 = 8; #Can not hold Target with the set time.
        self.errorCode100 = 100;
        pass;
        self.DataNum = "DataNum";
        self.SuccessTrialNum = "SuccessTrialNum";
        self.NonTargetTouchNum = "NonTargetTouchNum";
        self.TrialNum = "TrialNum";
        self.ErrorCode = "ErrorCode";
        self.retryCount = "retryCount"
        pass;
        self.TrialOnT_s = "TrialOnT(s)";
        self.HmHoldOnT_s = "HmHoldOnT(s)";
        self.HmHoldOffT_s = "HmHoldOffT(s)";
        self.CueOnT_s = "CueOnT(s)";
        self.CueOffT_s = "CueOffT(s)";
        self.HmHold2OnT_s = "HmHold2OnT(s)";
        self.TargetOnT_s = "TargetOnT(s)";
        self.HmReleaseT_s = "HmReleaseT(s)";
        self.TargetTouchT_s = "TargetTouchT(s)";
        self.NonTargetTouchT_s = "NonTargetTouchT(s)";
        self.TargetHoldOff_s = "TargetHoldOff(s)";
        self.PreRwdOnT_s = "PreRwdOnT(s)";
        self.RwdOnT_s = "RwdOnT_s(s)";
        self.ErrorOnT_s = "ErrorOnT(s)";
        #
        self.ITIOnT_s = "ITIOnT(s)";
        #
        self.HmHold2OffT_s = "HmHold2OffT(s)";
        
        # Dur
        self.PreHmTouchDur = "PreHmTouchDur(ms)";
        self.HmHoldDur = "HmHoldDur(ms)";
        self.CueDur = "CueDur(ms)";
        self.HmHold2Dur = "HmHold2Dur(ms)";
        self.HmReleaseDur = "HmReleaseDur(ms)";
        self.TotalHmHoldDur = "TotalHmHoldDur(ms)";
        self.ReachDur = "ReachDur(ms)";
        self.ResponseT = "ResponseT(ms)";
        self.TargetHoldDur = "TargetHoldDur(ms)";
        #
        self.spaceCol01 = "(space01)";
        self.spaceCol02 = "(space02)";
        self.spaceCol03 = "(space03)";
        self.spaceCol04 = "(space04)";
        self.spaceCol05 = "(space05)";
        self.spaceCol06 = "(space06)";
        self.spaceCol07 = "(space07)";
        self.spaceCol08 = "(space08)";
        self.spaceCol09 = "(space09)";

    def toStrState1(self,_state1):
        retLabel = "None";
        if _state1 == defDM.PHASE_BeforeTask:
            retLabel = "PHASE_BeforeTask";
        elif _state1 == defDM.PHASE_Sample:
            retLabel = "PHASE_Sample";
        elif _state1 == defDM.PHASE_Delay:
            retLabel = "PHASE_Delay";
        elif _state1 == defDM.PHASE_Choise:
            retLabel = "PHASE_Choise";
        elif _state1 == defDM.PHASE_PrePunishment:
            retLabel = "PHASE_PrePunishment";
        elif _state1 == defDM.PHASE_Punishment:
            retLabel = "PHASE_Punishment";
        elif _state1 == defDM.PHASE_PreEnd:
            retLabel = "PHASE_PreEnd";
        elif _state1 == defDM.PHASE_End:
            retLabel = "PHASE_End";
        elif _state1 == defDM.PHASE_End_Mark:
            retLabel = "PHASE_End_Mark";
        else:
            pass;
        return retLabel;
    
    def infoLabelState_1_2(self, _recTime, _stateDM, curRec):
        flagRecVSync = False;
        retLabel = "None";
        valueFloatTime = None;
        flagAO = False;
        volt = 0.0;
        print("infoLabelState_1_2");
        print(curRec);
        
        if _stateDM.state1 == self.PHASE_BeforeTask:
            if _stateDM.state2 == self.STATE2_TrialOnT_s:
                retLabel = self.TrialOnT_s;
                flagRecVSync = True;
                valueFloatTime = curRec.TrialOnT_s;
                flagAO = True;
                volt = self.VOL_TrialOn;
                pass;
            else:
                pass;
        if _stateDM.state1 == self.PHASE_Sample:
            if _stateDM.state2 == self.STATE2_CueOnT_s:
                retLabel = self.CueOnT_s;
                flagRecVSync = True;
                valueFloatTime = curRec.CueOnT_s;
                flagAO = True;
                volt = self.VOL_CueP;
                pass;
            else:
                pass;
        if _stateDM.state1 == self.PHASE_Delay:
            if _stateDM.state2 == self.STATE2_HmHold2OnT_s:
                retLabel = self.HmHold2OnT_s;
                flagRecVSync = True;
                valueFloatTime = curRec.HmHold2OnT_s;
                flagAO = True;
                volt = self.VOL_HmHold2P;
                pass;
        if _stateDM.state1 == self.PHASE_Choise:
            if _stateDM.state2 == self.STATE2_TargetOnT_s:
                retLabel = self.TargetOnT_s;
                flagRecVSync = True;
                valueFloatTime = curRec.TargetOnT_s;
                flagAO = True;
                volt = self.VOL_TargetOn;
                pass;
        elif _stateDM.state1 == self.PHASE_PreEnd:
            retLabel = self.PreRwdOnT_s;
            flagRecVSync = True;
            valueFloatTime = curRec.PreRwdOnT_s;
            flagAO = True;
            volt = self.VOL_PreRwdP;
            pass;
        elif _stateDM.state1 == self.PHASE_End:
            retLabel = self.RwdOnT_s;
            flagRecVSync = True;
            valueFloatTime = curRec.RwdOnT_s;
            flagAO = True;
            volt = self.VOL_RwdP;
            pass;
        elif _stateDM.state1 == self.PHASE_PrePunishment:
            retLabel = self.ErrorOnT_s;
            flagRecVSync = True;
            valueFloatTime = curRec.ErrorOnT_s;
            flagAO = True;
            volt = self.VOL_ErrorP;
            pass;
        elif _stateDM.state1 == self.PHASE_ITI:
            retLabel = self.ITIOnT_s;
            flagRecVSync = True;
            valueFloatTime = curRec.ITIOnT_s;
            flagAO = True;
            volt = self.VOL_ITI;
            pass;
        pass;
        return (flagRecVSync,retLabel,valueFloatTime,flagAO,volt);
    def toStrState_1_2(self, _stateDM):
        retLabel = "None";
        if _stateDM.state1 == defDM.PHASE_BeforeTask:
            if _stateDM.state2 == defDM.STATE2_HmTouchLimit:
                retLabel = "";
                pass;
            elif _stateDM.state2 == defDM.STATE2_HmHoldDur:
                pass;
            else:
                pass;
        return retLabel;

defDM = BTTsDefineDM();

class BTTsStateDM(BTTsState):
    def __init__(self):
        super().__init__();
        self.timestampCount = 0;
        self.corrected = False;
        self.selected = False;
        self.rewarded = False;
    def clearState(self):
        self.corrected = False;
        self.selected = False;
        self.rewarded = False;

    def checkChange(self, _thatState ):
        ret = False;
        if self.state != _thatState.state:
            ret = True;
        if self.state1 != _thatState.state1:
            ret = True;
        if self.state2 != _thatState.state2:
            ret = True;
        if self.responeded != _thatState.responeded:
            ret = True;
        pass;
        return ret;
    def getDataLabelTimeStamp(self):
        tmpS1 = "state.";
        tmpS1 += defDM.toStrState1(self.state1);
        tmpS1 += ".timestamp"
        return tmpS1
    def getDataLabelState1(self):
        tmpS1 = "state.";
        tmpS1 += defDM.toStrState1(self.state1);
        return tmpS1
    def timestampCurRec(self,  curRec, logging,_ttlAOut):
        (flagVSync, label, valRecFloat32,flagAO, volt) = defDM.infoLabelState_1_2(None,self, curRec);
        if flagVSync:
            pass;
        else:
            tmVal = logging.defaultClock.getTime();
            if valRecFloat32 != None:
                valRecFloat32.setValue(tmVal);
            if flagAO:
                pass;
                if _ttlAOut != None:
                    _ttlAOut.writeAO(0,volt);
                pass;
            else:
                pass;
        pass;
    
    def timestampOnFlipCur(self,exp, win, cur):
        #print("timestampOnFlipCur 01 timestampCount " + str(self.timestampCount));
        label01 = cur.getDataLabelTimeStamp();
        label02 = cur.getDataLabelState1();
        #print(exp.exp.thisEntry);
        exp.exp.timestampOnFlip(win,label01);
        exp.getTrials().th_trials.addData(label02, cur.state1);
        self.timestampCount += 1;
        #
        #print(exp.exp.thisEntry);
        #print("timestampOnFlipCur end");
        pass;
    def timestampOnFlipForChange(self,exp, win, curState):
        if self.checkChange(curState):
            self.timestampOnFlipCur(exp,win,curState);
        pass;
    def timestampOnFlip(self,exp, win):
        self.timestampOnFlipCur(exp,win,self);
        pass;
    def prDM(self):
        print("prDM " + str(self.selected) + " " + str(self.corrected));

    
class BTTsColorDBDM():
    def __init__(self):
        self.datas =  [
            ( 1 ,  'blue',    0,    0,    255 ),
            ( 2,   'yellow',    255,    255,    0),
            ( 3,   'red',    255,    0,    0),
            ( 4,   'green',    0,    128,    0),
            ( 5,   'white',    255,    255,    255),
            ( 6,   'light gray',    191,    191,    191),
            ( 7,   'dark gray',    127,    127,    127),
            ( 8,   'black',    0,    0,    0),
            (10,    'olive',    128,    128,    0 ),
            (11,    'fuchsia',  255,    0,    255 ),
            (12,    'aqua',    0,    255,    255 ),
            (13,    'lime',    0,    255,    0 ),
            (14,    'purple',    128,    0,    128 ),
            (15,    'navy',    0,    0,    128 ),
            (16,    'teal',    0,    128,    128 ),
            (17,    'maroon',    128,    0,    0 ),
            (20,    "white2",    255,    255,    255 ),
            (21,    "gray01",    239,    239,    239 ),
            (22,    "gray02",    223,    223,    223 ),
            (23,    "gray03",    207,    207,    207 ),
            (24,    "gray04",    191,    191,    191 ),
            (25,    "gray05",    175,    175,    175 ),
            (26,    "gray06",    159,    159,    159 ),
            (27,    "gray07",    143,    143,    143 ),
            (28,    "gray08",    127,    127,    127 ),
            (29,    "gray09",    111,    111,    111 ),
            (30,    "gray10",    95,    95,    95 ),
            (31,    "gray11",    79,    79,    79 ),
            (32,    "gray12",    63,    63,    63 ),
            (33,    "gray13",    47,    47,    47 ),
            (34,    "gray14",    31,    31,    31 ),
            (35,    "gray15",    15,    15,    15 ),
            (36,    "Black2",    0,    0,    0 )
           ];
        self.blue = 1;
        self.yellow = 2;
        self.red = 3;
        self.green = 4;
        self.white = 5;
        self.lightgray = 6;
        self.darkgray = 7;
        self.black = 8;
        self.olive = 10;
        self.fuchsia = 11;
        self.aqua = 12;
        self.lime = 13;
        self.purple = 14;
        self.navy = 15;
        self.teal = 16;
        self.maroon = 17;
        self.white2 = 20;
        self.gray01 = 21;
        self.gray02 = 22;
        self.gray03 = 23;
        self.gray04 = 24;
        self.gray05 = 25;
        self.gray06 = 26;
        self.gray07 = 27;
        self.gray08 = 28;
        self.gray09 = 29;
        self.gray10 = 30;
        self.gray11 = 31;
        self.gray12 = 32;
        self.gray13 = 33;
        self.gray14 = 34;
        self.gray15 = 35;
        self.Black2 = 36;
        pass;
    def getMaxNum(self):
        return 36; # bloack
    def getMinNum(self):
        return 1;
    def search(self, _num):
        cur = None;
        for dat in self.datas:
            if dat[0] == _num:
                cur = dat;
                break;
        pass;
        return cur;
    def getColor(self, _num):
        cur = self.search(_num);
        if cur != None:
            pass;
        else:
            cur = self.search(20);
        retColor = BTTsColor(cur);
        return retColor;



class BTTsShapeDBDM:
    def __init__(self):
        self.stim_verticesDB = [ # 三角形と四角形の座標
            (1,'circle',BTTsShapeDBDM.genPosCircle() ),
            (2,'rectangle' , [(-0.5, -0.5), (0.5, -0.5), (0.5, 0.5), (-0.5, 0.5)] ),
            (3,'Cross' , BTTsShapeDBDM.genPosCross() ),
            #(4,'triangle' , [(-0.5, 0), (0, 0.5), (0.5,0)] )
            (4,'triangle' , BTTsShapeDBDM.genPosTriangle(False) ),
            (5,'Inverted triangle' , BTTsShapeDBDM.genPosTriangle(True) ),
            (6,'Star' , BTTsShapeDBDM.genPosStar() )
            ];
        #Circle（丸）、Rectangle（四角）、Cross（十字）、Triangle（三角）、Inverted triangle（逆三角形）、Star（星）
        #
        #Rectangle
        self.circle = 1;
        self.rectangle = 3;
        self.Cross = 3;
        self.triangle = 4;
        self.Invertedtriangle = 5;
        self.Star = 6;
        pass;
    
    @staticmethod
    def genPosPolygonN(num, baseAngle):
        r = 0.5;
        
        bAngle = math.radians(baseAngle);
        posList = [];
        for n in range(num):
            ms = n * 360 / num;
            x = math.cos(bAngle + math.radians(ms));
            y = math.sin(bAngle + math.radians(ms));
            t = (x*r,y*r);
            posList.append( t );
        return posList;
    
    @staticmethod
    def genPosCircle():
        baseAngle = 90.0;
        return BTTsShapeDBDM.genPosPolygonN(90,baseAngle);
    @staticmethod
    def genPosTriangle( _inv):
        if _inv :
            baseAngle = -90;
        else:
            baseAngle = 90.0;
        return BTTsShapeDBDM.genPosPolygonN(3, baseAngle);
    
    @staticmethod
    def crossPoint(l0a, l0b, l1a, l1b):
        pass;
        x1 = l0a[0];
        y1 = l0a[1];
        x2 = l0b[0];
        y2 = l0b[1];
    
        x3 = l1a[0];
        y3 = l1a[1];
        x4 = l1b[0];
        y4 = l1b[1];
    
        a1 = (y2-y1)/(x2-x1)
        a3 = (y4-y3)/(x4-x3)

        x = (a1*x1 - y1- a3*x3 +y3)/(a1-a3)
        y = (y2-y1)/(x2-x1)*(x-x1) +y1
    
        return (x,y);   
    
    @staticmethod
    def genPosStar():
        baseAngle = 90;
        tmpList = BTTsShapeDBDM.genPosPolygonN(5, baseAngle);

        a = BTTsShapeDBDM.crossPoint( tmpList[0],tmpList[3], tmpList[1],tmpList[4] );
        b = BTTsShapeDBDM.crossPoint( tmpList[0],tmpList[3], tmpList[4],tmpList[2] );
        c = BTTsShapeDBDM.crossPoint( tmpList[3],tmpList[1], tmpList[4],tmpList[2] );
        d = BTTsShapeDBDM.crossPoint( tmpList[2],tmpList[0], tmpList[3],tmpList[1] );
        e = BTTsShapeDBDM.crossPoint( tmpList[2],tmpList[0], tmpList[1],tmpList[4] );
        
        retList = [];
        
        if False:
            retList.append(tmpList[0]);
            retList.append(tmpList[3]);
            retList.append(tmpList[1]);
            retList.append(tmpList[4]);
            retList.append(tmpList[2]);
        else:
            retList.append(tmpList[0]);
            retList.append(a);
            retList.append(tmpList[4]);
            retList.append(b);
            retList.append(tmpList[3]);
            retList.append(c);
            retList.append(tmpList[2]);
            retList.append(d);
            retList.append(tmpList[1]);
            retList.append(e);
            
        
        return retList;
    @staticmethod
    def genPosCross():
        posList = [];
        a = 0.125;
        b = 0.5;
        t = (a,b);
        posList.append( t );
        t = (a,a);
        posList.append( t );
        t = (b,a);
        posList.append( t );

        t = (b,-a);
        posList.append( t );
        t = (a,-a);
        posList.append( t );
        t = (a,-b);
        posList.append( t );

        t = (-a,-b);
        posList.append( t );
        t = (-a,-a);
        posList.append( t );
        t = (-b,-a);
        posList.append( t );

        t = (-b,a);
        posList.append( t );
        t = (-a,a);
        posList.append( t );
        t = (-a,b);
        posList.append( t );

        
        return posList;
    
    def getMaxNum(self):
        return 3; # bloack
    def getMinNum(self):
        return 1;
    def search(self, _num):
        cur = None;
        for dat in self.stim_verticesDB:
            if dat[0] == _num:
                cur = dat;
                break;
        pass;
        return cur;
    def getShape(self, _num):
        cur = self.search(_num);
        if cur != None:
            pass;
        else:
            cur = self.search(1);
        retColor = BTTsShape(cur);
        return retColor;


class CListShapeColor:
    def __init__(self, _clistLabel,_listShape,_listColor ):
        self.clistLabel = _clistLabel;
        self.listShape = _listShape;
        self.listColor = _listColor;
        #BTTsColorDBDM
        pass;
    

class BTTsParamDM(BTTsParam):
    def __init__(self):
        super().__init__();
        #
        self.isMainFunction = True;     
        #
        #self.paramButtonIn.flagChatteringBlockForTTL = True;
        #self.paramButtonIn.isTTLKeyEmu = True;
        
        self.recList = [];
        #self.phaseSampleTime = 0.100;
        self.phaseSampleTime = 4.00;
        self.phase_choice_stimpos = 2; # position target
        
        self.listColor = [[0,1],[3,4],[6,7]];
        self.listShape = [[0,3],[1,4],[2,5]];
        #
        self.listColor = [[0,1,2],[3,4,5],[6,7,8]];
        self.listShape = [[0,3,6],[1,4,7],[2,5,8]];
        #
        self.listPosition = [[0,1,2,3,4,5,6,7,8]];
        self.listPosition = [[0,1,2]];
        
        self.listSignal = [[0,1,2],[4,5,6]];  # 形の一致
        self.listSignal = [[0,3],[1,4],[2,5]];  # 色の一致
        
        self.initParam();
        self.initValue();
        self.initRecList();
        #
        self.initOtherParam();
        
        pass;
    def initParam(self):
        self.modeDelayedMatch = ValueInt32('modeDelayedMatch',1); 
        self.paramList.append(self.modeDelayedMatch);
        self.modeOption = ValueInt32('modeOption', 0);
        self.paramList.append(self.modeOption);
        #
        self.numOfTrial = ValueInt32('numOfTrial',20); 
        self.numOfSuffle = ValueInt32('numOfSuffle',2); 
        self.numOfMaxRetry = ValueInt32('numOfMaxRetry',0); 
        self.paramList.append(self.numOfTrial);
        self.paramList.append(self.numOfSuffle);
        self.paramList.append(self.numOfMaxRetry);
        #
        #
        self.Set_ITI = ValueFloat32('Set_ITI', 2000.0);
        self.paramList.append(self.Set_ITI);
        # before
        #self.Set_HmInputLimit = ValueFloat32('Set_HmInputLimit', 2.0, x1000=True);
        self.Set_HmTouchLimit = ValueFloat32('Set_HmTouchLimit', 2000.0);
        self.Set_HmHoldDur = ValueFloat32('Set_HmHoldDur', 1000.0);
        #self.paramList.append(self.Set_HmInputLimit);
        self.paramList.append(self.Set_HmTouchLimit);
        self.paramList.append(self.Set_HmHoldDur);
        #
        self.Set_CueDur = ValueFloat32('Set_CueDur', 2000.0);
        self.Set_HmHold2Dur = ValueFloat32('Set_HmHold2Dur', 1000.0);
        self.paramList.append(self.Set_CueDur);
        self.paramList.append(self.Set_HmHold2Dur);
        # choise Set_HmReleaseLmit
        self.Set_HmReleaseLimit = ValueFloat32('Set_HmReleaseLimit', 2000.0);
        self.Set_ReachTargetLimit = ValueFloat32('Set_ReachTargetLimit', 2000.0);
        self.Set_TargetHoldDur = ValueFloat32('Set_TargetHoldDur', 2000.0);
        self.paramList.append(self.Set_HmReleaseLimit);
        self.paramList.append(self.Set_ReachTargetLimit);
        self.paramList.append(self.Set_TargetHoldDur);
        # end/reward
        self.Set_PreRwdDur_ms = ValueFloat32('Set_PreRwdDur_ms', 2000.0);
        self.Set_RwdDur_ms = ValueFloat32('Set_RwdDur_ms', 2000.0);
        self.Set_ErrorDur_ms = ValueFloat32('Set_ErrorDur_ms', 2000.0);
        self.paramList.append(self.Set_PreRwdDur_ms);
        self.paramList.append(self.Set_RwdDur_ms);
        self.paramList.append(self.Set_ErrorDur_ms);
        #
        self.delayUseList = ValueBool8('delayUseList',False);
        self.delayTimeMSec = ValueFloat32Array('delayTimeMSec',[500,750,1000,2000]);
        self.paramList.append(self.delayUseList);
        self.paramList.append(self.delayTimeMSec);
        #
        self.Set_RewardSoundOn = ValueBool8('Set_RewardSoundOn',True);
        self.Set_PunishmentSoundOn = ValueBool8('Set_PunishmentSoundOn',True);
        self.Set_StartBeepOn = ValueBool8('Set_Beep_Start',True);
        self.Set_TargetBeepOn = ValueBool8('Set_Beep_Target',True);
        self.Set_RwdNum = ValueInt32('Set_RwdNum', 1);
        self.Set_RwdDrink_microl = ValueFloat32('Set_RwdDrink_microl', 33.0);
        self.paramList.append(self.Set_RewardSoundOn);
        self.paramList.append(self.Set_PunishmentSoundOn);
        self.paramList.append(self.Set_StartBeepOn);
        self.paramList.append(self.Set_TargetBeepOn);
        self.paramList.append(self.Set_RwdNum);
        self.paramList.append(self.Set_RwdDrink_microl);
        
        #self.clistLabel = ValueString("clistGroupName","groupA");        
        #self.cListShape = ValueInt32Array("cListShape",[1,2,3]);
        #self.cListColor = ValueInt32Array("cListColor",[1,2,3]);
        #self.paramList.append(self.clistLabel);
        #self.paramList.append(self.cListShape);
        #self.paramList.append(self.cListColor);
        #self.stim_list = ValueInt32Array('stim_list',[0,1,2]);
        #self.paramList.append(self.stim_list);
        self.stimGroupName = ValueString("stimGroupName","GroupA_ShapeColor");  
        self.stim_list = ValueInt32Array2D('stim_list',[[0,1,2],[3,4,5],[6,7,8]]);
        self.paramList.append(self.stimGroupName);
        self.paramList.append(self.stim_list);
        
        self.HmRetry = ValueBool8('HmRetry',False);
        self.paramList.append(self.HmRetry);
        self.HmErrorSound = ValueBool8('HmErrorSound',True);
        self.paramList.append(self.HmErrorSound);

        self.UsePunishment = ValueBool8('UsePunishment',True);
        self.paramList.append(self.UsePunishment);
        
        
    def initValue(self):
        self.nFrame = ValueInt32('nFrame', 0);
        # dont useself.valueList.append(self.nFrame);
        pass;
        
    def initRecList(self):
        self.recList.append(self.Set_HmTouchLimit);
        self.recList.append(self.Set_HmHoldDur);
        self.recList.append(self.Set_CueDur);
        self.recList.append(self.Set_HmHold2Dur);
        self.recList.append(self.Set_HmReleaseLimit);
        self.recList.append(self.Set_ReachTargetLimit);
        self.recList.append(self.Set_TargetHoldDur);
        #
        self.recList.append(self.Set_PreRwdDur_ms);
        self.recList.append(self.Set_RwdDur_ms);
        self.recList.append(self.Set_ErrorDur_ms);
        self.recList.append(self.Set_ITI);
        self.recList.append(self.Set_RwdDrink_microl);
        self.recList.append(self.Set_RwdNum);
        #
        pass;

class BTTsCountTrialDM():
    def __init__(self):
        self.DataNum = 0;
        self.SuccessTrialNum = 0;
        self.NonTargetTouchNum = 0;
        self.TrialNum = 0;
        pass;
    def count(self,_select, _correct):
        self.DataNum += 1;
        if _select:
            if _correct:
                self.SuccessTrialNum += 1;
            else:
                self.NonTargetTouchNum += 1;
        else:
            pass;
        self.TrialNum = self.SuccessTrialNum + self.NonTargetTouchNum;

class BTTsTrialDM():
    def __init__(self):
        super().__init__();
        self.th_trial = None;
        self.oneTrial = None;
        pass;
    def getTH(self):
        pass;
        return self.th_trial;
    def getOneTrial(self):
        return self.oneTrial;


class BTTsTrialsDM(BTTsTrials):
    def __init__(self,_param,_countTrial,_bttsTh, _stateBuffer, _oneTrigger):
        super().__init__( _bttsTh,_stateBuffer,_oneTrigger);
        self.param = _param;
        self.countTrial = _countTrial;
        self.th_trials = None;
        self.flagNext = False;
        self.hold_tr = None;
        self.randomForDelay = RandomList();
        self.ramdomForTarget = RandomList();
        pass;
    def genCorrectSTIM(self, _LockFirst, _lockIndex):
        pairList = [];
        #stims = [0,1,2,3];
        stims = self.param.stim_list_override;
        ##
        ## stims = [[0,1,2],[3,4,5],[6,7,8]]
        #stims = self.param.listColor;

        if _LockFirst:
            for slist in stims:
                # slist [0,1,2]
                sz = len(slist);
                if _lockIndex < sz:
                    ix = _lockIndex;
                else:
                    ix = 0;
                a = slist[ix];
                for b in slist:
                    if a == b:
                        pass;
                    else:
                        pairList.append([a,b]);
        else:
            for slist in stims:
                # slist [0,1,2]
                for a in slist:
                    for b in slist:
                        if a == b:
                            pass;
                        else:
                            pairList.append([a,b]);
            pass;

        print(pairList);
        
        if _LockFirst:
            stim_correctIndex = [0];
        else:
            stim_correctIndex = [0,1];
        
        """       
        conditonDict_Stim = {
            'stim_pos' : [[0,1],[1,0]],
            'stim_shape' : pairList,
            'stim_correctIndex' : [0,1]
        }
        """
        conditonDict_Stim = {
            'stim_pos' : [[0,1],[1,0]],
            'stim_shape' : pairList,
            'stim_correctIndex' : stim_correctIndex
        }
        return conditonDict_Stim;
    def genCorrectPos(self, _LockPos, _pos):
        pairList = [];
        #stims = [0,1,2,3];
        stims = self.param.stim_list_override;


        for slist in stims:
            for a in slist:
                pairList.append([a,a]);
        print(pairList);
        
        if _LockPos:
            if _pos == 0:
                stim_correctIndex = [0,0];
            else:
                stim_correctIndex = [1,1];
            
            stim_pos_list =  [[0,1]];
        else:
            stim_pos_list =  [[0,1],[1,0]];
            stim_correctIndex = [0,1];

        """
        conditonDict_Stim_Pos = {
            'stim_pos' : [[0,1],[1,0]],
            'stim_shape' : pairList,
            'stim_correctIndex' : [0,1]
        }
        """
        conditonDict_Stim_Pos = {
            'stim_pos' : stim_pos_list,
            'stim_shape' : pairList,
            'stim_correctIndex' : stim_correctIndex
        }
        
        return conditonDict_Stim_Pos;
    def create(self):
        self.flagPr = False;
        # _param
        _numShuffle = self.param.numOfSuffle.value;
        _numOfMaxRetry = self.param.numOfMaxRetry.value;
        #
        # rand
        self.randomForDelay.setListValue(self.param.delayTimeMSec.value);
        self.randomForDelay.init();
        #
        modePotion = self.param.modeOption.value;
        if self.param.modeDelayedMatch.value == 0:
            conditionsDict =  self.genCorrectPos(False,modePotion);
        elif self.param.modeDelayedMatch.value == 1:
            conditionsDict =  self.genCorrectSTIM(False,modePotion);
        elif self.param.modeDelayedMatch.value == 2:
            conditionsDict =  self.genCorrectSTIM(False,modePotion);
        elif self.param.modeDelayedMatch.value == 3:
            conditionsDict =  self.genCorrectSTIM(False,modePotion);
        elif self.param.modeDelayedMatch.value == 4:
            conditionsDict =  self.genCorrectPos(True,modePotion);
        elif self.param.modeDelayedMatch.value == 5:
            conditionsDict =  self.genCorrectSTIM(True,modePotion);
        elif self.param.modeDelayedMatch.value == 6:
            conditionsDict =  self.genCorrectSTIM(True,modePotion);
        elif self.param.modeDelayedMatch.value == 7:
            conditionsDict =  self.genCorrectSTIM(True,modePotion);
        else:
            conditionsDict =  self.genCorrectPos(False,modePotion);
        pass;
        
        self.conditions = data.createFactorialTrialList(conditionsDict);
        print(self.conditions);
        
        if self.flagPr:
            print("_numShuffle " + str(_numShuffle)); 
        if self.flagPr:
            print("conditions");
            print(self.conditions);
        
        #method: ‘random’, ‘sequential’, or ‘fullRandom’ # n
        _methedForCondition = 'sequential';
        _methedForCondition = 'random'; # not fullRamdom
        self.th_trials = data.TrialHandler(self.conditions, _numShuffle,method=_methedForCondition) ;
        
        print(self.th_trials.sequenceIndices );
        self.th_responses = data.TrialHandler([], 100);
        #
        pass;
    def next(self,_retry):
        print("BTTsTrialsDM  next");
        tr = None;
        try:
            if _retry:
                #self.hold_tr; same
                pass;
            else:
                self.hold_tr = self.th_trials.next();
            print("holdTrial");
            print(self.hold_tr );
            if self.hold_tr  != None:
                self.flagNext = True;
                tr = BTTsTrialDM();
                tr.th_trial = self.hold_tr;
                tr.oneTrial = BTTsOneTrialDM(self, self.bttsTh, self.stateBuffer, self.oneTrigger);
                tr.oneTrial.setOneTrial(self.param,None);
                tr.oneTrial.setValueRamdom(_retry);
                print("BTTsTrialsDM next");
                print(tr.oneTrial);
            else:
                tr = None;
        except StopIteration:
            lopTr = False;
            print('except StopIteration for lopTr');
        return tr;
    def nextResponse(self):
        ## responses.next() # ポイント3. responsesについては、addDataをする前に手動でnext()
        self.th_responses.next();
        #print("BTTsTrialsDM nextResponse");
        pass;
    
    def getTH(self):
        return self.th_trials;
    def getResponsesTH(self):
        return self.th_responses;
    

class BTTsTrialControlDM(BTTsTrialControl):
    def __init__(self,_param,_countTrial,_stateBuffer, _oneTrigger, _oneTriggerForThread):
        super().__init__(_param,_stateBuffer,_oneTrigger,_oneTriggerForThread);
        self.countTrial = _countTrial;
        pass;
    def newBTTsTrials(self):
        print("newBTTsTrials");
        print(type(self.param));
        print(self.param);
        self.trials = BTTsTrialsDM(self.param,self.countTrial, self.bttsTh, self.stateBuffer, self.oneTrigger);
        return self.trials;

#def runTarget(that):
#    that.runnable();
#    pass;

def callbackNFDM(that):
    that.callbackPhase();

class RecOneStimBase:
    def __init__(self,bname):
        self.b_Shape = ValueRecString(bname+"Shape");
        self.b_color_number = ValueRecInt32(bname+"ColorNum");
        self.b_color_name = ValueRecString(bname+"ColorName");
        self.b_shape_number = ValueRecInt32(bname+"ShapeNum");
        self.b_shape_name = ValueRecString(bname+"ShapeName");
        self.b_SizeX = ValueRecFloat32(bname+"SizeX");
        self.b_SizeY = ValueRecFloat32(bname+"SizeY");
        self.b_PositionX = ValueRecFloat32(bname+"PositionX");
        self.b_PositionY = ValueRecFloat32(bname+"PositionY");
        self.b_WindowSizeX = ValueRecFloat32(bname+"WindowSizeX");
        self.b_WindowSizeY = ValueRecFloat32(bname+"WindowSizeY");
    def addList(self, recList):
        recList.append(self.b_Shape);
        recList.append(self.b_color_number);
        recList.append(self.b_color_name);
        recList.append(self.b_shape_number);
        recList.append(self.b_shape_name);
        recList.append(self.b_SizeX);
        recList.append(self.b_SizeY);
        recList.append(self.b_PositionX);
        recList.append(self.b_PositionY);
        recList.append(self.b_WindowSizeX);
        recList.append(self.b_WindowSizeY);
        pass;
    def setValue(self, stimS):
        self.b_Shape.setValue(stimS.stimAttr.stimName );
        self.b_color_number.setValue(stimS.stimAttr.color.num);
        self.b_color_name.setValue(stimS.stimAttr.color.cname);
        if stimS.stimAttr.shape !=None:
            self.b_shape_number.setValue(stimS.stimAttr.shape.num);
            self.b_shape_name.setValue(stimS.stimAttr.shape.sname);
        else:
            #self.b_shape_number.setValue(stimS.stimAttr.shape.num);
            #self.b_shape_number.setValue(stimS.stimAttr.shape.num);
            # not set
            pass;
        self.b_SizeX.setValue(stimS.stimAttr.stimSize[0]);
        self.b_SizeY.setValue(stimS.stimAttr.stimSize[1]);
        self.b_PositionX.setValue(stimS.stimAttr.stimPos[0]);
        self.b_PositionY.setValue(stimS.stimAttr.stimPos[1]);
        
        if stimS.stimAttr.flagStimArea:
            windowSizeX= stimS.stimAttr.stimAreaSizeForTouch[0];
            windowSizeY= stimS.stimAttr.stimAreaSizeForTouch[1];
        else:
            windowSizeX= stimS.stimAttr.stimSize[0];
            windowSizeY= stimS.stimAttr.stimSize[1];
        self.b_WindowSizeX.setValue(windowSizeX);
        self.b_WindowSizeY.setValue(windowSizeY);

class RecOneStimCue(RecOneStimBase):
    def __init__(self):
        super().__init__("Cue");
        pass;
class RecOneStimTarget(RecOneStimBase):
    def __init__(self):
        super().__init__("Target");
        pass;
class RecOneStimNonTarget(RecOneStimBase):
    def __init__(self):
        super().__init__("NonTarget");
        pass;


class BTTsRecOneTrialDM:
    def __init__(self):
        self.recList01 = [];
        self.recList02 = [];
        
        self.spaceCol01 = ValueRecString(defDM.spaceCol01);
        self.spaceCol01.setValue("");
        self.spaceCol02 = ValueRecString(defDM.spaceCol02);
        self.spaceCol02.setValue("");
        self.spaceCol03 = ValueRecString(defDM.spaceCol03);
        self.spaceCol03.setValue("");
        self.spaceCol04 = ValueRecString(defDM.spaceCol04);
        self.spaceCol04.setValue("");
        self.spaceCol05 = ValueRecString(defDM.spaceCol05);
        self.spaceCol05.setValue("");
        self.spaceCol06 = ValueRecString(defDM.spaceCol06);
        self.spaceCol06.setValue("");
        self.spaceCol07 = ValueRecString(defDM.spaceCol07);
        self.spaceCol07.setValue("");
        
        #
        self.DataNum = ValueRecInt32(defDM.DataNum);
        self.SuccessTrialNum = ValueRecInt32(defDM.SuccessTrialNum);
        self.NonTargetTouchNum = ValueRecInt32(defDM.NonTargetTouchNum);
        self.TrialNum = ValueRecInt32(defDM.TrialNum);
        self.errorcode = ValueRecInt32(defDM.ErrorCode);
        self.retryCount = ValueRecInt32(defDM.retryCount);
        
        self.recList01.append(self.DataNum);
        self.recList01.append(self.SuccessTrialNum);
        self.recList01.append(self.NonTargetTouchNum);
        self.recList01.append(self.TrialNum);
        self.recList01.append(self.errorcode);
        self.recList01.append(self.retryCount);
        self.recList01.append(self.spaceCol01);
        #
        self.TrialOnT_s = ValueRecFloat32(defDM.TrialOnT_s);
        self.HmHoldOnT_s = ValueRecFloat32(defDM.HmHoldOnT_s);
        self.HmHoldOffT_s = ValueRecFloat32(defDM.HmHoldOffT_s);
        # sample
        self.CueOnT_s = ValueRecFloat32(defDM.CueOnT_s);
        self.CueOffT_s = ValueRecFloat32(defDM.CueOffT_s);
        # delay
        self.HmHold2OnT_s = ValueRecFloat32(defDM.HmHold2OnT_s);
        self.HmHold2OffT_s = ValueRecFloat32(defDM.HmHold2OffT_s);
        # choice
        self.TargetOnT_s = ValueRecFloat32(defDM.TargetOnT_s);
        self.HmReleaseT_s = ValueRecFloat32(defDM.HmReleaseT_s);
        self.TargetTouchT_s = ValueRecFloat32(defDM.TargetTouchT_s);
        self.NonTargetTouchT_s = ValueRecFloat32(defDM.NonTargetTouchT_s);
        self.TargetHoldOff_s = ValueRecFloat32(defDM.TargetHoldOff_s);
        #self.HmHold2OffT_s = ValueRecFloat32(defDM.HmHold2OffT_s);
        
        self.PreRwdOnT_s = ValueRecFloat32(defDM.PreRwdOnT_s);
        self.RwdOnT_s = ValueRecFloat32(defDM.RwdOnT_s);
        self.ErrorOnT_s = ValueRecFloat32(defDM.ErrorOnT_s);
        self.ITIOnT_s = ValueRecFloat32(defDM.ITIOnT_s);
        
        self.recList01.append(self.TrialOnT_s);
        self.recList01.append(self.HmHoldOnT_s);
        self.recList01.append(self.HmHoldOffT_s);
        self.recList01.append(self.CueOnT_s);
        self.recList01.append(self.CueOffT_s);
        self.recList01.append(self.HmHold2OnT_s);
        self.recList01.append(self.HmHold2OffT_s);
        self.recList01.append(self.TargetOnT_s);
        self.recList01.append(self.HmReleaseT_s);
        self.recList01.append(self.TargetTouchT_s);
        self.recList01.append(self.NonTargetTouchT_s);
        self.recList01.append(self.TargetHoldOff_s);
        
        self.recList01.append(self.PreRwdOnT_s);
        self.recList01.append(self.RwdOnT_s);
        self.recList01.append(self.ErrorOnT_s);
        self.recList01.append(self.ITIOnT_s);
        #
        self.recList01.append(self.spaceCol02);
        #
        self.PreHmTouchDur_ms = ValueRecFloat32(defDM.PreHmTouchDur);
        self.HmHoldDur_ms = ValueRecFloat32(defDM.HmHoldDur);
        self.CueDur_ms = ValueRecFloat32(defDM.CueDur);
        self.HmHold2Dur_ms = ValueRecFloat32(defDM.HmHold2Dur);
        self.HmReleaseDur_ms = ValueRecFloat32(defDM.HmReleaseDur);
        self.TotalHmHoldDur_ms = ValueRecFloat32(defDM.TotalHmHoldDur);
        self.ReachDur_ms = ValueRecFloat32(defDM.ReachDur);
        self.ResponseT_ms = ValueRecFloat32(defDM.ResponseT);
        self.TargetHoldDur_ms = ValueRecFloat32(defDM.TargetHoldDur);
        
        self.recList01.append(self.PreHmTouchDur_ms);
        self.recList01.append(self.HmHoldDur_ms);
        self.recList01.append(self.CueDur_ms);
        self.recList01.append(self.HmHold2Dur_ms);
        self.recList01.append(self.HmReleaseDur_ms);
        self.recList01.append(self.TotalHmHoldDur_ms);
        self.recList01.append(self.ResponseT_ms);
        self.recList01.append(self.TargetHoldDur_ms);
        #
        self.Corrected = ValueRecBool8("Corrected");
        self.recList01.append(self.Corrected);
        self.recList01.append(self.spaceCol03);
        
        # corrected
        self.recOneStimCue = RecOneStimCue();
        self.recOneStimTarget = RecOneStimTarget();
        self.recOneStimNonTarget = RecOneStimNonTarget();
        
        
        self.recOneStimCue.addList(self.recList02);
        self.recList02.append(self.spaceCol05);
        self.recOneStimTarget.addList(self.recList02);
        self.recList02.append(self.spaceCol06);
        self.recOneStimNonTarget.addList(self.recList02);
        self.recList02.append(self.spaceCol07);
        
        self.TouchPositionX = ValueRecFloat32("TouchPositionX");
        self.TouchPositionY = ValueRecFloat32("TouchPositionY");
        self.recList02.append(self.TouchPositionX);
        self.recList02.append(self.TouchPositionY);
        self.recDate = ValueRecString("recDate");
        self.recList02.append(self.recDate);
        pass;
    def updateCountTrial(self,_countTrial):
        self.DataNum.setValue(_countTrial.DataNum );
        self.SuccessTrialNum.setValue(_countTrial.SuccessTrialNum );
        self.NonTargetTouchNum.setValue(_countTrial.NonTargetTouchNum );
        self.TrialNum.setValue(_countTrial.TrialNum );
        pass;
    
    def toCalcDiffRecValue(self, _recVal_a, _recVal_b):
        retVal = None;
        pass; # sec to msec
        b1 =  _recVal_a.flagSetVal;
        b2 =  _recVal_b.flagSetVal;
        if b1 and b2 :
            retVal = (_recVal_a.getValue() - _recVal_b.getValue()) * 1000.0; 
            pass;
        else:
            pass;
        return retVal;
    def updateCalcData(self):
        self.PreHmTouchDur_ms.setValue( self.toCalcDiffRecValue(self.HmHoldOnT_s , self.TrialOnT_s ));
        self.HmHoldDur_ms.setValue( self.toCalcDiffRecValue(self.HmHoldOffT_s , self.HmHoldOnT_s ));
        self.CueDur_ms.setValue( self.toCalcDiffRecValue(self.CueOffT_s , self.CueOnT_s ));
        self.HmHold2Dur_ms.setValue( self.toCalcDiffRecValue(self.HmHold2OffT_s , self.HmHold2OnT_s ));
        self.HmReleaseDur_ms.setValue( self.toCalcDiffRecValue(self.HmReleaseT_s , self.TargetOnT_s ));
        self.TotalHmHoldDur_ms.setValue( self.toCalcDiffRecValue(self.HmReleaseT_s , self.HmHoldOnT_s ));
        self.ReachDur_ms.setValue( self.toCalcDiffRecValue(self.TargetTouchT_s , self.HmReleaseT_s ));
        self.ResponseT_ms.setValue( self.toCalcDiffRecValue(self.TargetTouchT_s , self.TargetOnT_s ));
        self.TargetHoldDur_ms.setValue( self.toCalcDiffRecValue(self.TargetHoldOff_s , self.TargetTouchT_s ));
    def updateDate(self):
        t_delta = datetime.timedelta(hours=9)
        JST = datetime.timezone(t_delta, 'JST')
        now = datetime.datetime.now(JST)        
        d = now.strftime('%Y/%m/%d %H:%M:%S');
        self.recDate.setValue(d);
        
        pass;
        pass;




class BTTsOneTrialDM(BTTsOneTrial):
    def __init__(self,_trials, _bttsTh,_stateBuffer, _oneTrigger):
        super().__init__(_trials,_bttsTh,_stateBuffer, _oneTrigger);
        # 
        #self.buttonIn = ButtonIn(self.trials.param,self.bttsTh.keyIO,self.bttsTh.oneTriggerForThread);
        self.curComp = [];
        # 
        self.flagPr = True;
        #
        # info
        self.flagRBMouse = False;
        self.x_pos = 0.0;
        self.y_pos = 0.0;
        self.mouseBtnPress = False;
        #
        self.curState = None;
        pass;
        self.correctedOneTrial = False;
        self.selectedOneTrial = False;
        self.curRec = None;
        #
        self.stimCue = None;
        self.stimT0 = None;
        self.stimT1 = None;
        #
        self.prePunishmentTimeMSec = 50.0;
        pass;
    def setOneTrial(self, _param, _thatTrial):
        self.param = _param;
        
        self.thatTrial = _thatTrial;
        pass;
    def setValueRamdom(self, _isRetry):
        # リトライの場合は設定しないようにする。
        # ramdomList
        if self.param.delayUseList.value :
            self.param.Set_HmHold2Dur.value = self.trials.randomForDelay.getValue() ;
            pass;
        else:
            pass;
        #
        if _isRetry:
            pass;
        else:
            self.trials.randomForDelay.nextIndex();
            pass;
        
        pass;
    def beginRunOneTrial(self):
        print('BTTsOneTrialDM::beginRunOneTrial 01');
        num = 0;
        self.curState = None;
        #
        self.curRec = BTTsRecOneTrialDM(); # New
        #
        self.bttsTh.curSemaphore.acquire();
        self.bttsTh.oneTrial = self;
        self.bttsTh.curSemaphore.release();
        #
        print('BTTsOneTrialDM::beginRunOneTrial end');
        pass;
    def endRunOneTrial(self):
        print('BTTsOneTrialDM::endRunOneTrial 01');
        self.trials.countTrial.count(self.selectedOneTrial,self.correctedOneTrial);
        
        if self.curRec != None:
            self.curRec.updateCountTrial(self.trials.countTrial);
            self.curRec.updateCalcData();
            self.curRec.updateDate();
            
            # recList 02
            for aRec in self.curRec.recList01:
                self.trials.getTH().addData(aRec.vname,aRec.getValue());
            # recList Param
            for aRec in self.param.recList:
                self.trials.getTH().addData(aRec.vname,aRec.value);
            self.trials.getTH().addData(self.curRec.spaceCol04.vname,self.curRec.spaceCol04.getValue());
            # recList 02
            for aRec in self.curRec.recList02:
                self.trials.getTH().addData(aRec.vname,aRec.getValue());
                
        print('BTTsOneTrialDM::endRunOneTrial end');
        #
        self.curRec = None;
        pass;
    def setStimCue(self,stimS, tHandle,posDM ,curStimGroup):
        #stimPair = self.trials.getTH()['stim_shape'];
        #stimPosPair = self.trials.getTH()['stim_pos'];
        #stimCorrect = self.trials.getTH()['stim_correctIndex'];
        
        stimPair = tHandle['stim_shape'];
        stimPosPair = tHandle['stim_pos'];
        stimCorrect = tHandle['stim_correctIndex'];
                            
        vs = curStimGroup[stimPair[stimCorrect]]
        stimS.copyFromLow(vs);
        stimS.stimAttr.flagStimArea = False;
        if self.param.modeDelayedMatch.value == 0 or self.param.modeDelayedMatch.value == 4 :
            defStimPos = posDM.phase_choice_stimposList[self.param.phase_choice_stimpos];
            stimS.stimAttr.stimPos = defStimPos[stimPosPair[stimCorrect]];
        else:
            stimS.stimAttr.stimPos = posDM.phase_sample_stim1pos;
        pass;
        self.curRec.recOneStimCue.setValue(stimS);
    
    
    def setStimTarget(self,stim0,stim1, tHandle,posDM ,curStimGroup):
        #stimPair = self.trials.getTH()['stim_shape'];
        #stimPosPair = self.trials.getTH()['stim_pos'];
        #stimCorrect = self.trials.getTH()['stim_correctIndex'];
        
        stimPair = tHandle['stim_shape'];
        stimPosPair = tHandle['stim_pos'];
        stimCorrect = tHandle['stim_correctIndex'];
                            
        vs0 = curStimGroup[stimPair[0]];
        stim0.copyFromLow(vs0);
        stim0.stimAttr.flagStimArea = True;
        
        vs1 = curStimGroup[stimPair[1]];
        stim1.copyFromLow(vs1);
        stim1.stimAttr.flagStimArea = True;
                            
        defStimPos = posDM.phase_choice_stimposList[self.param.phase_choice_stimpos];
        stim0.stimAttr.stimPos = defStimPos[stimPosPair[0]];
        stim1.stimAttr.stimPos = defStimPos[stimPosPair[1]];

        if stimCorrect == 0:
            stim0.select = True;
            stim1.select = True;
            stim0.correct = True;
            stim1.correct = False;
        else:
            stim0.select = True;
            stim1.select = True;
            stim0.correct = False;
            stim1.correct = True;
        
        if stimCorrect == 0:
            self.curRec.recOneStimTarget.setValue(stim0);
            self.curRec.recOneStimNonTarget.setValue(stim1);
        else:
            self.curRec.recOneStimTarget.setValue(stim1);
            self.curRec.recOneStimNonTarget.setValue(stim0);
            
        pass;
            
    def setStim(self,tHandle, posDM,curStimGroup):
        self.stimCue = BTTsVisualStim();
        self.setStimCue(self.stimCue,tHandle, posDM,curStimGroup);
        self.stimT0 = BTTsVisualStim();
        self.stimT1 = BTTsVisualStim();
        self.setStimTarget(self.stimT0,self.stimT1,tHandle,posDM,curStimGroup);
    
    def toMouseInfo(self,oneMSEV):
        self.x_pos = oneMSEV.x_position;
        self.y_pos = oneMSEV.y_position;
        if self.curState != None:
            self.curState.pr();
        print(oneMSEV)
        if self.curState != None:
            self.curState.pr();
        scale = 100.0 / self.param.screenscale;
        scale = 1.0;
        pos = (self.x_pos * scale, self.y_pos * scale);
        #print(scale);
        #print(pos);
        curSec = self.stateBuffer.clock.getTime();
        return (curSec,pos,scale) ;
    def callbackPhase(self):
        # btn
        btnResponeded = False;
        #(b1, b2) = self.bttsTh.buttonIn.getButton();
        (b1, b2, edgeb1, edgeb2) = self.bttsTh.getButton();
        
        #if self.bttsTh.oneTriggerForThread != None:
        if edgeb1 and self.curState != None:
            if self.curState.state1 == defDM.PHASE_BeforeTask:
                if self.curState.state2 == defDM.STATE2_TrialOnT_s:
                    if b1 :
                        btnResponeded = True;
                        self.breakWaitSecForPhaseChoise();
                    else:
                        pass;
                if self.curState.state2 == defDM.STATE2_HmHoldOnT_s:
                    if b1:
                        pass;
                    else:
                        btnResponeded = True;
                        self.breakWaitSecForPhase();
            elif self.curState.state1 == defDM.PHASE_Sample:
                if b1 :
                    pass;
                else:
                    btnResponeded = True;
                    self.breakWaitSecForPhase();
                pass;
            elif self.curState.state1 == defDM.PHASE_Delay:
                if b1 :
                    pass;
                else:
                    btnResponeded = True;
                    self.breakWaitSecForPhase();
                pass;
            elif self.curState.state1 == defDM.PHASE_Choise:
                if self.curState.state2 == defDM.STATE2_TargetOnT_s:
                    if b1 :
                        pass;
                    else:
                        btnResponeded = True;
                        self.breakWaitSecForPhaseChoise();
                        pass;
            else:
                pass;
            pass;
                
        
        sz = len(self.curComp);
        if sz != 0:
            #print(self.curComp);
            pass;
        pass;
        ##self.bttsTh.callbackNextFor();
        
        msResponeded = False;
        if self.bttsTh.msIO != None:
            msEv = self.bttsTh.msIO.getEvents();
            sz = 0;
            if msEv:
                sz = len( msEv );
            if sz != 0:
                pass;
                #MouseButtonPressEventNT(experiment_id=0, session_id=0, device_id=0, event_id=198, type=32, device_time=21069.875, logged_time=21.337433599997894, time=21.337433599997894, confidence_interval=0.0, delay=0.0, filter_id=0, display_id=0, button_state=11, button_id=2, pressed_buttons=2, x_position=-0.5768518518518518, y_position=0.13055555555555556, scroll_dx=0, scroll_x=0, scroll_dy=0, scroll_y=0, modifiers=[], window_id=722744)
                #MouseButtonPressEventNT(experiment_id=0, session_id=0, device_id=0, event_id=138, type=32, device_time=3141.515, logged_time=13.91373220000014, time=13.91373220000014, confidence_interval=0.0, delay=0.0, filter_id=0, display_id=0, button_state=11, button_id=2, pressed_buttons=2, x_position=-0.42407407407407405, y_position=0.12314814814814815, scroll_dx=0, scroll_x=0, scroll_dy=0, scroll_y=0, modifiers=[], window_id=1706312)
                pass;
                ## oneMSEV = msEv[-1];
                for oneMSEV in msEv:
                    if True and (( oneMSEV.button_id)==2):
                        if oneMSEV.type == EventConstants.MOUSE_MOVE:
                            #print(oneMSEV)
                            pass;
                        elif oneMSEV.type == EventConstants.MOUSE_DRAG:
                            #print(oneMSEV)
                            pass;
                        elif oneMSEV.type == EventConstants.MOUSE_BUTTON_PRESS:
                            self.mouseBtnPress = True;
                            (curSec,pos,scale) = self.toMouseInfo(oneMSEV);

                            print("MOUSE_BUTTON_PRESS 01");
                            flagCheck = False;
                            if self.curState != None:
                                if self.curState.state1 == defDM.PHASE_Choise:
                                    if self.curState.state2 == defDM.STATE2_TargetOnT_s:
                                        flagCheck = False;
                                    elif self.curState.state2 == defDM.STATE2_HmReleaseT_s:
                                        pass;
                                    elif self.curState.state2 == defDM.STATE2_ReachTargetLimit:
                                        #flagCheck = not( self.curState.responeded);
                                        flagCheck = True;
                                    elif self.curState.state2 == defDM.STATE2_TargetTouchT_s:
                                        flagCheck = False; # not( self.curState.responeded);
                                    else:
                                        pass;
                                    pass;
                            if flagCheck:
                                if self.trialComponents != None:
                                    sz=len(self.trialComponents);
                                    if sz != 0:
                                        theSelected = False;
                                        theCorrected = False;
                                        for compStim in self.trialComponents:
                                            #compStim.prCorrect();
                                            #compStim.prInfo();
                                            if BTTsTool.containsComponentPosBTTsVS(compStim,pos):
                                                theSelected = True;
                                                if compStim.correct:
                                                    theCorrected = True;
                                                    self.curRec.TouchPositionX.setValue(pos[0]);
                                                    self.curRec.TouchPositionY.setValue(pos[1]);
                                                else:
                                                    pass;
                                        pass;
                                        if theSelected:
                                            self.selectedOneTrial = True;
                                            if self.curState != None:
                                                self.curState.selected = True;
                                            if theCorrected:
                                                if self.curState != None:
                                                    self.curState.corrected = True;
                                                #self.curRec.TargetTouchT_s.setValue(curSec);
                                                pass;
                                            else:
                                                #self.curRec.NonTargetTouchT_s.setValue(curSec);
                                                pass;
                                        if self.curState != None:
                                            print("curState");
                                            self.curState.pr();
                                            self.curState.prDM();
                                                    
                                        if theSelected:
                                            msResponeded = True;
                                        if theCorrected:
                                            if self.bttsTh.oneTrigger != None:
                                                print("Trigger On");
                                                #self.bttsTh.oneTrigger.write(1,255);
                                            else:
                                                pass;
                                            #if self.bttsTh.oneTriggerForThread != None:
                                            #    volt = BTTsToolDM.getVoltage(self.curState);
                                            #    #self.bttsTh.oneTriggerForThread.write(0,volt);
                                            #    #
                                            pass;
                                        if theSelected:
                                            if theCorrected:
                                                self.breakWaitSecForPhaseChoise();
                                            else:
                                                self.breakWaitSecForPhaseChoise();
                                                #self.breakWaitSecForPhaseChoise();
                                        #print(self.trialComponents);
                            pass;
                            print("MOUSE_BUTTON_PRESS end");

                        elif oneMSEV.type == EventConstants.MOUSE_BUTTON_RELEASE:
                            self.mouseBtnPress = False;
                            (curSec,pos,scale) = self.toMouseInfo(oneMSEV);

                            print("MOUSE_BUTTON_RELEASE 01");
                            flagCheck = False;
                            if self.curState != None:
                                if self.curState.state1 == defDM.PHASE_Choise:
                                    if self.curState.state2 == defDM.STATE2_TargetOnT_s:
                                        flagCheck = False;
                                    elif self.curState.state2 == defDM.STATE2_HmReleaseT_s:
                                        flagCheck = False;
                                    elif self.curState.state2 == defDM.STATE2_ReachTargetLimit:
                                        flagCheck = False;
                                    elif self.curState.state2 == defDM.STATE2_TargetTouchT_s:
                                        #flagCheck = not( self.curState.responeded);
                                        flagCheck = True;
                                    else:
                                        pass;
                                    pass;
                            print("MOUSE_BUTTON_RELEASE 02 "+str(flagCheck));
                            if flagCheck:
                                if self.trialComponents != None:
                                    sz=len(self.trialComponents);
                                    if sz != 0:
                                        theSelected = False;
                                        theCorrected = False;
                                        for compStim in self.trialComponents:
                                            #compStim.prCorrect();
                                            #compStim.prInfo();
                                            if BTTsTool.containsComponentPosBTTsVS(compStim,pos):
                                                theSelected = True;
                                                if compStim.correct:
                                                    theCorrected = True;
                                                else:
                                                    pass;
                                        pass;
                                        if theSelected:
                                            if self.curState != None:
                                                self.curState.responeded = True;
                                        
                                        if theCorrected:
                                            if self.curState != None:
                                                self.curState.corrected = True;
                                                self.curState.selected = True;
                                        print("MOUSE_BUTTON_RELEASE 03 "+str(theSelected)+" "+str(theCorrected));
                                        if theSelected:
                                            if theCorrected:
                                                self.breakWaitSecForPhase();
                                            else:
                                                self.breakWaitSecForPhase();
                                                #self.breakWaitSecForPhaseChoise();
                                        print("MOUSE_BUTTON_RELEASE 04");
                                        #print(self.trialComponents);                            
                            print("MOUSE_BUTTON_RELEASE end");
                            pass;
        
        pass;
        
    #def run(self):
    #    self.runnable(self,"thName");
    #    pass;
    
    def writeAO(self, ch, volt):
        if self.bttsTh.oneTriggerForThread != None:
            self.bttsTh.oneTriggerForThread.writeAO(ch,volt);
        pass;
    def toSecFromMSec(self, _mSec):
        return _mSec / 1000.0;
    
    def phaseBeforeTask_HmTouchLimit(self):
        if self.flagPr:
            print('BTTsOneTrialDM phaseBeforeTask_HmTouchLimit 01');
        #if self.oneTrigger != None:
        #    self.oneTrigger.writeDelay(0,255,pWidthsec=self.pWidthsec);
        curSt = BTTsStateDM();
        curSt.timestamp = self.stateBuffer.clock.getTime();
        curSt.state1 = defDM.PHASE_BeforeTask;
        curSt.state2 = defDM.STATE2_TrialOnT_s;
        curSt.flagTrial = True;
        curSt.timestampCurRec(self.curRec,logging,self.bttsTh.oneTriggerForThread);
        self.curState = curSt;
        self.stateBuffer.acquire();
        self.stateBuffer.appendBuffer(curSt);
        self.stateBuffer.release();
        #
        if self.flagPr:
            print('BTTsOneTrialDM phaseBeforeTask_HmTouchLimit 02');
        retP = self.waitSecForPhase(self.toSecFromMSec(self.param.Set_HmTouchLimit.value ),False,callbackNFDM,self );
        if self.flagPr:
            print('BTTsOneTrialDM phaseBeforeTask_HmTouchLimit end');
        if retP:
            volt = defDM.VOL_HmHoldP;
            self.writeAO(0,volt);
            self.curRec.HmHoldOnT_s.setValue(logging.defaultClock.getTime());
            pass;
        else:
            self.curRec.errorcode.setValue(defDM.errorCode0);
            pass;
        return retP;
    def phaseBeforeTask_HmHoldDur(self):
        if self.flagPr:
            print('BTTsOneTrialDM phaseBeforeTask_HmHoldDur 01');
        #if self.oneTrigger != None:
        #    self.oneTrigger.writeDelay(0,255,pWidthsec=self.pWidthsec);
        curSt = BTTsStateDM();
        curSt.timestamp = self.stateBuffer.clock.getTime();
        curSt.state1 = defDM.PHASE_BeforeTask;
        curSt.state2 = defDM.STATE2_HmHoldOnT_s;
        curSt.flagTrial = True;
        curSt.timestampCurRec(self.curRec,logging,self.bttsTh.oneTriggerForThread);
        self.curState = curSt;
        self.stateBuffer.acquire();
        self.stateBuffer.appendBuffer(curSt);
        self.stateBuffer.release();
        #
        if self.flagPr:
            print('BTTsOneTrialDM phaseBeforeTask_HmHoldDur 02');
        retP = self.waitSecForPhase(self.toSecFromMSec(self.param.Set_HmHoldDur.value ) ,True, callbackNFDM,self );
        if self.getFlagBreakeEscapeWaitFor():
            retP = False;
        else:
            if retP:
                pass;
            else:
               
                self.curRec.HmHoldOffT_s.setValue(logging.defaultClock.getTime());
                self.curRec.errorcode.setValue( defDM.errorCode1 );
                pass;
        if self.flagPr:
            print('BTTsOneTrialDM phaseBeforeTask_HmHoldDur end ' + str(retP));
        return retP;
    def phaseSample(self):
        if self.flagPr:
            print('BTTsOneTrialDM phaseSample 01');
        #if self.oneTrigger != None:
        #    self.oneTrigger.writeDelay(0,255,pWidthsec=self.pWidthsec);
        curSt = BTTsStateDM();
        curSt.timestamp = self.stateBuffer.clock.getTime();
        curSt.state1 = defDM.PHASE_Sample;
        curSt.state2 = defDM.STATE2_CueOnT_s;
        curSt.timestampCurRec(self.curRec,logging,self.bttsTh.oneTriggerForThread);
        self.curState = curSt;
        self.stateBuffer.acquire();
        self.stateBuffer.appendBuffer(curSt);
        self.stateBuffer.release();
        #
        if self.flagPr:
            print('BTTsOneTrialDM phaseSample 02');
        retP = self.waitSecForPhase(self.toSecFromMSec(self.param.Set_CueDur.value) ,True,callbackNFDM,self  );
        if self.flagPr:
            print('BTTsOneTrialDM phaseSample end');
        if self.getFlagBreakeEscapeWaitFor():
            retP = False;
        else:
            if retP:
                pass;
            else:
                self.curRec.CueOffT_s.setValue(logging.defaultClock.getTime());
                self.curRec.errorcode.setValue(defDM.errorCode2);
        return retP;
    def phaseDelay(self):
        if self.flagPr:
            print('BTTsOneTrialDM phaseDelay 01');
        #if self.oneTrigger != None:
        #    self.oneTrigger.writeDelay(0,255,pWidthsec=self.pWidthsec);
        curSt = BTTsStateDM();
        curSt.timestamp = self.stateBuffer.clock.getTime();
        curSt.state1 = defDM.PHASE_Delay;
        curSt.state2 = defDM.STATE2_HmHold2OnT_s;
        curSt.timestampCurRec(self.curRec,logging,self.bttsTh.oneTriggerForThread);
        self.curState = curSt;
        self.stateBuffer.acquire();
        self.stateBuffer.appendBuffer(curSt);
        self.stateBuffer.release();
        if self.flagPr:
            print('BTTsOneTrialDM phaseDelay 02');
        retP = self.waitSecForPhase(self.toSecFromMSec(self.param.Set_HmHold2Dur.value ),True,callbackNFDM,self );
        if self.flagPr:
            print('BTTsOneTrialDM phaseDelay end');
        if self.getFlagBreakeEscapeWaitFor():
            retP = False;
        else:
            if retP:
                pass;
            else:
                self.curRec.HmHold2OffT_s.setValue(logging.defaultClock.getTime());
                self.curRec.errorcode.setValue(defDM.errorCode3);
        return retP;
    def pahseChoice_Set_HmReleaseLimit(self):
        if self.flagPr:
            print('BTTsOneTrialDM pahseChoice_Set_HmReleaseLmit 01');
        #if self.oneTrigger != None:
        #    self.oneTrigger.writeDelay(0,255,pWidthsec=self.pWidthsec);
        curSt = BTTsStateDM();
        curSt.timestamp = self.stateBuffer.clock.getTime();  
        curSt.state1 = defDM.PHASE_Choise;
        curSt.state2 = defDM.STATE2_TargetOnT_s; 
        curSt.timestampCurRec(self.curRec,logging,self.bttsTh.oneTriggerForThread);
        self.curState = curSt;
        self.stateBuffer.acquire();
        self.stateBuffer.appendBuffer(curSt);
        self.stateBuffer.release();
        if self.flagPr:
            print('BTTsOneTrialDM pahseChoice_Set_HmReleaseLimit 02');
        retP = self.waitSecForPhase(self.toSecFromMSec(self.param.Set_HmReleaseLimit.value),False,callbackNFDM,self );
        if self.flagPr:
            print('BTTsOneTrialDM pahseChoice_Set_HmReleaseLimit 03');
        print("pahseChoice_Set_HmReleaseLimit");
        self.curState.pr();
        self.curState.prDM();
        
        if self.flagPr:
            print('BTTsOneTrialDM phaseBeforeTask_HmTouchLimit end');
        if self.getFlagBreakeEscapeWaitFor():
            retP = False;
        else:
            if retP:
                volt = defDM.VOL_HmRelaese;
                self.writeAO(0,volt);
                self.curRec.HmReleaseT_s.setValue(logging.defaultClock.getTime());
                pass;
            else:
                self.curRec.errorcode.setValue(defDM.errorCode4);
                pass;
        print("pahseChoice_Set_HmReleaseLimit end "+str(retP) );
        return retP;
    def pahseChoice_Set_ReachTargetLimit(self):
        if self.flagPr:
            print('BTTsOneTrialDM pahseChoice_Set_HmReleaseLmit 01');
        #if self.oneTrigger != None:
        #    self.oneTrigger.writeDelay(0,255,pWidthsec=self.pWidthsec);
        curSt = BTTsStateDM();
        curSt.timestamp = self.stateBuffer.clock.getTime();
        curSt.state1 = defDM.PHASE_Choise;
        curSt.state2 = defDM.STATE2_ReachTargetLimit;
        self.curState = curSt;
        curSt.timestampCurRec(self.curRec,logging,self.bttsTh.oneTriggerForThread);
        self.stateBuffer.acquire();
        self.stateBuffer.appendBuffer(curSt);
        self.stateBuffer.release();
        if self.flagPr:
            print('BTTsOneTrialDM pahseChoice_Set_HmReleaseLimit 02');
        retP = self.waitSecForPhase(self.toSecFromMSec(self.param.Set_ReachTargetLimit.value) ,False,callbackNFDM,self );
        if self.flagPr:
            print('BTTsOneTrialDM pahseChoice_Set_HmReleaseLimit 03');
        #print("pahseChoice_Set_HmReleaseLimit");
        #self.curState.pr();
        #self.curState.prDM();
        """
        if self.curState.selected:
            # correct を 離したら、エラー
            # 他を選んだら直ぐにエラー
            if self.curState.corrected:
                retP = True;
            else:
                print("errorCode7");
                self.curRec.errorcode.setValue(defDM.errorCode7);
                retP = False;
        else:
            retP = not retP;
            if not retP:
                self.curRec.errorcode.setValue(defDM.errorCode5);
                
        print("pahseChoice_Set_HmReleaseLimit end "+str(retP) );
        """
        if self.getFlagBreakeEscapeWaitFor():
            retP = False;
        else:
            if retP:
                if self.curState.selected:
                    if self.curState.corrected:
                        volt = defDM.VOL_TargetTouch;
                        self.writeAO(0,volt);
                        self.curRec.TargetTouchT_s.setValue( logging.defaultClock.getTime());                 
                        retP = True;
                    else:
                        self.curRec.NonTargetTouchT_s.setValue( logging.defaultClock.getTime());                 
                        self.curRec.errorcode.setValue(defDM.errorCode7);
                        retP = False;
                    pass;
            else:
                self.curRec.errorcode.setValue(defDM.errorCode5);
                pass;
        return retP;
    def pahseChoice_TargetHoldDur(self):
        if self.flagPr:
            print('BTTsOneTrialDM pahseChoice_TargetHoldDur 01');
        #if self.oneTrigger != None:
        #    self.oneTrigger.writeDelay(0,255,pWidthsec=self.pWidthsec);
        curSt = BTTsStateDM();
        curSt.timestamp = self.stateBuffer.clock.getTime();
        curSt.state1 = defDM.PHASE_Choise;
        curSt.state2 = defDM.STATE2_TargetTouchT_s;
        curSt.timestampCurRec(self.curRec,logging,self.bttsTh.oneTriggerForThread);
        self.curState = curSt;
        self.stateBuffer.acquire();
        self.stateBuffer.appendBuffer(curSt);
        self.stateBuffer.release();
        if self.flagPr:
            print('BTTsOneTrialDM pahseChoice_TargetHoldDur 02');
        retP = self.waitSecForPhase(self.toSecFromMSec(self.param.Set_TargetHoldDur.value) ,True,callbackNFDM,self );
        if self.flagPr:
            print('BTTsOneTrialDM pahseChoice_TargetHoldDur 03');
        if retP:
            print("Corrected");
            self.curRec.Corrected.setValue(True);
            #self.correctedOneTrial = True;
            self.correctedOneTrial = True;
            self.curRec.errorcode.setValue(defDM.errorCode100);
            #
            self.curState.rewarded = True;
        else:
            print("errorCode8");
            self.curRec.TargetHoldOff_s.setValue(logging.defaultClock.getTime());
            self.curRec.errorcode.setValue(defDM.errorCode8);
            
        if self.getFlagBreakeEscapeWaitFor():
            retP = False;
        else:
            if self.curState.selected:
                if self.curState.corrected:
                    pass;
                else:
                    pass;
        print("pahseChoice_TargetHoldDur end "+str(retP) );
        return retP;
    def phasePreEnd(self):
        if self.flagPr:
            print('BTTsOneTrialDM phaseEnd 01');
        #if self.oneTrigger != None:
        #    self.oneTrigger.writeDelay(0,255,pWidthsec=self.pWidthsec);
        curSt = BTTsStateDM();
        curSt.timestamp = self.stateBuffer.clock.getTime();
        curSt.state1 = defDM.PHASE_PreEnd;
        curSt.timestampCurRec(self.curRec,logging,self.bttsTh.oneTriggerForThread);
        self.curState = curSt;
        self.stateBuffer.acquire();
        self.stateBuffer.appendBuffer(curSt);
        self.stateBuffer.release();
        if self.flagPr:
            print('BTTsOneTrialDM phaseEnd 02');
        retP = self.waitSecForPhase(self.toSecFromMSec(self.param.Set_PreRwdDur_ms.value),True,callbackNFDM,self );
        if self.flagPr:
            print('BTTsOneTrialDM phaseEnd end');
        if self.getFlagBreakeEscapeWaitFor():
            retP = False;
        else:
            pass;
        return retP;
    def phaseEnd(self):
        if self.flagPr:
            print('BTTsOneTrialDM phaseEnd 01');
        #if self.oneTrigger != None:
        #    self.oneTrigger.writeDelay(0,255,pWidthsec=self.pWidthsec);
        curSt = BTTsStateDM();
        curSt.timestamp = self.stateBuffer.clock.getTime();
        curSt.state1 = defDM.PHASE_End;
        curSt.timestampCurRec(self.curRec,logging,self.bttsTh.oneTriggerForThread);
        self.curState = curSt;
        self.stateBuffer.acquire();
        self.stateBuffer.appendBuffer(curSt);
        self.stateBuffer.release();
        if self.flagPr:
            print('BTTsOneTrialDM phaseEnd 02');
        retP = self.waitSecForPhase(self.toSecFromMSec(self.param.Set_RwdDur_ms.value),True,callbackNFDM,self );
        if self.flagPr:
            print('BTTsOneTrialDM phaseEnd end');
        if self.getFlagBreakeEscapeWaitFor():
            retP = False;
        else:
            pass;
        return retP;
    def phasePrePunishment(self):
        if self.flagPr:
            print('BTTsOneTrialDM phasePunishment 01');
        #if self.oneTrigger != None:
        #    self.oneTrigger.writeDelay(0,255,pWidthsec=self.pWidthsec);
        curSt = BTTsStateDM();
        curSt.timestamp = self.stateBuffer.clock.getTime();
        curSt.state1 = defDM.PHASE_PrePunishment;
        curSt.timestampCurRec(self.curRec,logging,self.bttsTh.oneTriggerForThread);
        self.curState = curSt;
        self.stateBuffer.acquire();
        self.stateBuffer.appendBuffer(curSt);
        self.stateBuffer.release();
        #
        timeMSec = self.prePunishmentTimeMSec;
        if self.flagPr:
            print('BTTsOneTrialDM pahseEnd 02');
        retP = self.waitSecForPhase(self.toSecFromMSec(timeMSec),True,callbackNFDM,self );
        if self.flagPr:
            print('BTTsOneTrialDM pahseEnd end');
        if self.getFlagBreakeEscapeWaitFor():
            retP = False;
        else:
            pass;
        return retP;   
    def phasePunishment(self):
        if self.flagPr:
            print('BTTsOneTrialDM phasePunishment 01');
        #if self.oneTrigger != None:
        #    self.oneTrigger.writeDelay(0,255,pWidthsec=self.pWidthsec);
        curSt = BTTsStateDM();
        curSt.timestamp = self.stateBuffer.clock.getTime();
        curSt.state1 = defDM.PHASE_Punishment;
        curSt.timestampCurRec(self.curRec,logging,self.bttsTh.oneTriggerForThread);
        self.curState = curSt;
        self.stateBuffer.acquire();
        self.stateBuffer.appendBuffer(curSt);
        self.stateBuffer.release();
        
        if self.param.Set_ErrorDur_ms.value < self.prePunishmentTimeMSec:
            timeMSec = 50.0;
        else:
            timeMSec = self.param.Set_ErrorDur_ms.value - self.prePunishmentTimeMSec;
        if self.flagPr:
            print('BTTsOneTrialDM pahseEnd 02');
        retP = self.waitSecForPhase(self.toSecFromMSec(timeMSec),True,callbackNFDM,self );
        if self.flagPr:
            print('BTTsOneTrialDM pahseEnd end');
        if self.getFlagBreakeEscapeWaitFor():
            retP = False;
        else:
            pass;
        return retP;
    def phaseEnd_Mark(self):
        if self.flagPr:
            print('BTTsOneTrialDM phaseEnd_Mark 01');
        #if self.oneTrigger != None:
        #    self.oneTrigger.writeDelay(0,255,pWidthsec=self.pWidthsec);
        curSt = BTTsStateDM();
        curSt.timestamp = self.stateBuffer.clock.getTime();
        curSt.state1 = defDM.PHASE_End_Mark;
        curSt.timestampCurRec(self.curRec,logging,self.bttsTh.oneTriggerForThread);
        self.curState = curSt;
        self.stateBuffer.acquire();
        self.stateBuffer.appendBuffer(curSt);
        self.stateBuffer.release();
        retP = True;
        if self.flagPr:
            print('BTTsOneTrialDM phaseEnd_Mark end');
        if self.getFlagBreakeEscapeWaitFor():
            retP = False;
        else:
            pass;
        return retP;
    def isRetry(self):
        return False;
    
    def runnable(self):
        _thName = "BTTsOneTrialDM runnable";
        print(_thName + " 01");
        retPhase = False;
        lopRetry = True;
        while lopRetry:
            self.bttsTh.initCallbackNextFor();
            self.bttsTh.buttonIn.resetState();
            
            lopHmRetry = True;
            while lopHmRetry:
                print(_thName + " 02");
                self.stampNextForPhase();
                print(_thName + " 03");
                retPhase = self.phaseBeforeTask_HmTouchLimit();
                if self.getFlagBreakeEscapeWaitFor():
                    print("getFlagBreakeEscapeWaitFor 01 True");
                    lopHmRetry = False;
                    retPhase = False;
                    pass;
                print(_thName + " 04");
                if( retPhase ):
                    self.stampNextForPhase();
                    print(_thName + " 05");
                    retPhase = self.phaseBeforeTask_HmHoldDur();
                    print(_thName + " 06");
                    if self.getFlagBreakeEscapeWaitFor():
                        print("getFlagBreakeEscapeWaitFor 02 True");
                        lopHmRetry = False;
                        retPhase = False;
                        pass;
                if ( retPhase ):
                    lopHmRetry = False;
                else:
                    if self.param.HmRetry.value:
                        pass;
                    else:
                        lopHmRetry = False;
                        pass;
                pass;
            print(_thName + " 07");
            if( retPhase ):
                self.stampNextForPhase();
                retPhase = self.phaseSample();
                if( retPhase ):
                    self.stampNextForPhase();
                    retPhase = self.phaseDelay();
                    if( retPhase ):                 
                        self.stampNextForPhase();
                        retPhase = self.pahseChoice_Set_HmReleaseLimit();
                        if( retPhase ):
                            self.stampNextForPhase();
                            retPhase = self.pahseChoice_Set_ReachTargetLimit();
                            if( retPhase ):
                                self.stampNextForPhase();
                                retPhase = self.pahseChoice_TargetHoldDur();
            print(_thName + " 08");
                                
            #lopRetry = self.isRetry(); DontUse
            lopRetry = False;
        pass;
        if self.getFlagBreakeEscapeWaitFor():
            pass;
        else:
            if (retPhase):
                self.stampNextForPhase();
                retPhase = self.phasePreEnd();
                if (retPhase):
                    self.stampNextForPhase();
                    retPhase = self.phaseEnd();
                pass;
            else:
                self.stampNextForPhase();
                retPhase = self.phasePrePunishment();
                if self.param.UsePunishment.value:
                    if (retPhase):
                        self.stampNextForPhase();
                        retPhase = self.phasePunishment();
                else:
                    pass;
                pass;
        self.stampNextForPhase();
        self.phaseEnd_Mark();
        self.bttsTh.buttonIn.lastLog();
        print(_thName + " end");    
    def runnableNEWBUG(self):
        self.bttsTh.initCallbackNextFor();
        self.bttsTh.buttonIn.resetState();
        
        paramHmErrorSound = self.param.HmErrorSound.value;
        paramHmRetry =self.param.HmRetry.value;
        paramUsePunishment = self.param.UsePunishment.value;
        
        retPhase = False;
        lopRetry = True;
        while lopRetry:
            flagPhasePreEnd = False;
            flagPhaseEnd = False;
            flagPhasePrePushment = True;
            flagPhasePushment = True;
            
            flagErrorHm    = False;
            flagErrorChoice = False;
            flagESCBreak = False;
            
            lopHmRetry = True;
            while lopHmRetry:
                self.stampNextForPhase();
                retPhase = self.phaseBeforeTask_HmTouchLimit();
                if self.getFlagBreakeEscapeWaitFor():
                    flagESCBreak = True;
                else:
                    if retPhase:
                        pass;
                    else:
                        if paramHmErrorSound:
                            flagPhasePrePushment = True;
                        else:
                            pass; # to EndMark
                print("runnable AAA 01" );
                if( not(flagESCBreak) and retPhase ):
                    self.stampNextForPhase();
                    retPhase = self.phaseBeforeTask_HmHoldDur();
                    if self.getFlagBreakeEscapeWaitFor():
                        flagESCBreak = True;
                        pass;
                    else:
                        if retPhase:
                            pass;
                        else:
                            flagErrorHm = True;                         
                        pass;
                if( not(flagESCBreak) and retPhase ):
                    self.stampNextForPhase();
                    retPhase = self.phaseSample();
                    if self.getFlagBreakeEscapeWaitFor():
                        flagESCBreak = True;
                        pass;
                    else:
                        if retPhase:
                            pass;
                        else:
                            flagErrorHm = True;                         
                        pass;
                if( not(flagESCBreak) and retPhase ):
                    self.stampNextForPhase();
                    retPhase = self.phaseDelay();
                    if self.getFlagBreakeEscapeWaitFor():
                        flagESCBreak = True;
                        pass;
                    else:
                        if retPhase:
                            pass;
                        else:
                            flagErrorHm = True;                         
                        pass;
                #
                if flagESCBreak:
                    lopHmRetry = False;
                    retPhase = False;
                    pass;
                else:
                    if retPhase:
                        lopHmRetry = False;
                    else:
                        if flagErrorHm:
                            if paramHmRetry:
                                # retry
                                retPhase = False;
                                pass;
                            else:
                                lopHmRetry = False;
                                if paramHmErrorSound:
                                    flagPhasePrePushment = True;
                                    flagPhasePushment = True;
                                else:
                                    pass; # to EndMark
                    
            if flagESCBreak:
                flagsecondLoop = False;
            else:
                if retPhase:
                    flagsecondLoop = True;
                else:
                    flagsecondLoop = False;
            while flagsecondLoop:
                if( retPhase ):
                    self.stampNextForPhase();
                    retPhase = self.pahseChoice_Set_HmReleaseLimit();
                    if self.getFlagBreakeEscapeWaitFor():
                        flagESCBreak = True;
                    else:
                        if retPhase:
                            pass;
                        else:
                            flagErrorChoice = True;

                if( not(flagESCBreak) and retPhase ):
                    self.stampNextForPhase();
                    retPhase = self.pahseChoice_Set_ReachTargetLimit();
                    if self.getFlagBreakeEscapeWaitFor():
                        flagESCBreak = True;
                    else:
                        if retPhase:
                            pass;
                        else:
                            flagErrorChoice = True;
                if( not(flagESCBreak) and retPhase ):
                    self.stampNextForPhase();
                    retPhase = self.pahseChoice_TargetHoldDur();
                    if self.getFlagBreakeEscapeWaitFor():
                        flagESCBreak = True;
                    else:
                        if retPhase:
                            pass;
                        else:
                            flagErrorChoice = True;

                if flagESCBreak:
                    retPhase = False;
                    flagsecondLoop = False;
                else:
                    if retPhase:
                        flagsecondLoop = False;
                        pass;
                    else:
                        flagsecondLoop = False;
                        if flagErrorChoice:
                            if paramHmErrorSound:
                                flagPhasePrePushment = True;
                                flagPhasePushment = True;
                            else:
                                pass;
                            if paramUsePunishment:
                                flagPhasePrePushment = True;
                                flagPhasePushment = True;
                    
            if self.getFlagBreakeEscapeWaitFor():
                pass;
            else:
                if (retPhase):
                    flagPhasePreEnd = True;
                    flagPhaseEnd = True;
                else:
                    pass;
                flagPhasePrePushment = True;
                flagPhasePushment = True;

                if flagPhasePreEnd:
                    if (retPhase):
                        self.stampNextForPhase();
                        retPhase = self.phasePreEnd();
                        if self.getFlagBreakeEscapeWaitFor():
                            flagESCBreak = True;
                            pass;
                if flagPhaseEnd:
                    if( not(flagESCBreak) and retPhase ):
                        self.stampNextForPhase();
                        retPhase = self.phaseEnd();
                        if self.getFlagBreakeEscapeWaitFor():
                            flagESCBreak = True;
                            pass;
                if flagPhasePrePushment:
                    if( not(flagESCBreak) and not(retPhase) ):
                        self.stampNextForPhase();
                        retPhase = self.phasePrePunishment();
                        if self.getFlagBreakeEscapeWaitFor():
                            flagESCBreak = True;
                            pass;
                if flagPhasePushment:
                    if( not(flagESCBreak) and not(retPhase) ):
                        self.stampNextForPhase();
                        retPhase = self.phasePunishment();
                pass;
        self.stampNextForPhase();
        self.phaseEnd_Mark();
        self.bttsTh.buttonIn.lastLog();
        pass;
    def inputEventMouse(self,_curState,_trialComponents, _mEvent):
        # @override
        #print("BTTsOneTrialDM inputEventMouse 01");
        # mouse
        flag = False;
        if _curState == None:
            return;
        else:
            if defDM.PHASE_Choise == _curState.state1:
                flagCheck = True;
            else:
                flagCheck = False;
            
            if flagCheck:
                if _mEvent.mButtons is None:
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
            else:
                pass;
            #print("BTTsOneTrialDM inputEventMouse end");
        pass;        


class ExExperimentHandler(data.ExperimentHandler):
    def __init__(self,_name, _dataFileName):
        super().__init__(_name, _dataFileName);
        pass;
    def prEx(self):
        sortColumns=False;
        matrixOnly=False;
        delim = ',';
        
        names = self._getAllParamNames()
        names.extend(self.dataNames)
        # names from the extraInfo dictionary
        names.extend(self._getExtraInfo()[0])
        if len(names) < 1:
            logging.error("No data was found, so data file may not look as expected.")
        # sort names if requested
        if sortColumns:
            names.sort()
        # write a header line        sortColumns=False;

        if not matrixOnly:
            for heading in names:
                print(u'%s%s' % (heading, delim))
            print('\n')

        # write the data for each entry
        for entry in self.getAllEntries():
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
    
    def saveAsWideTextEx(self,
                           fileName,
                           delim='auto',
                           matrixOnly=False,
                           appendFile=None,
                           encoding='utf-8-sig',
                           fileCollisionMethod='rename',
                           sortColumns=False):
            """Saves a long, wide-format text file, with one line representing
            the attributes and data for a single trial. Suitable for analysis
            in R and SPSS.
            If `appendFile=True` then the data will be added to the bottom of
            an existing file. Otherwise, if the file exists already it will
            be kept and a new file will be created with a slightly different
            name. If you want to overwrite the old file, pass 'overwrite'
            to ``fileCollisionMethod``.
            If `matrixOnly=True` then the file will not contain a header row,
            which can be handy if you want to append data to an existing file
            of the same format.
            :Parameters:
                fileName:
                    if extension is not specified, '.csv' will be appended if
                    the delimiter is ',', else '.tsv' will be appended.
                    Can include path info.
                delim:
                    allows the user to use a delimiter other than the default
                    tab ("," is popular with file extension ".csv")
                matrixOnly:
                    outputs the data with no header row.
                appendFile:
                    will add this output to the end of the specified file if
                    it already exists.
                encoding:
                    The encoding to use when saving a the file.
                    Defaults to `utf-8-sig`.
                fileCollisionMethod:
                    Collision method passed to
                    :func:`~psychopy.tools.fileerrortools.handleFileCollision`
                sortColumns:
                    will sort columns alphabetically by header name if True
            """
            print("saveAsWideTextEx");
            # set default delimiter if none given
            delimOptions = {
                    'comma': ",",
                    'semicolon': ";",
                    'tab': "\t"
                }
            if delim == 'auto':
                delim = genDelimiter(fileName)
            elif delim in delimOptions:
                delim = delimOptions[delim]
    
            if appendFile is None:
                appendFile = self.appendFiles
    
            # create the file or send to stdout
            fileName = genFilenameFromDelimiter(fileName, delim)
            f = openOutputFile(fileName, append=appendFile,
                               fileCollisionMethod=fileCollisionMethod,
                               encoding=encoding)
    
            names = self._getAllParamNames()
            names.extend(self.dataNames)
            # names from the extraInfo dictionary
            names.extend(self._getExtraInfo()[0])
            if len(names) < 1:
                logging.error("No data was found, so data file may not look as expected.")
            # sort names if requested
            if sortColumns:
                names.sort()
            # write a header line
            if not matrixOnly:
                for heading in names:
                    f.write(u'%s%s' % (heading, delim))
                f.write('\n')
    
            # write the data for each entry
            for entry in self.getAllEntries():
                print(type(entry));
                print(entry);
                
                tmpV = entry.get('errorcode'); # dict 

                flagWr = True;                
                if tmpV != None:
                    if tmpV < 1:
                        flagWr = False;
                        pass;
                    else:
                        flagWr = True;
                        pass;
                else:
                    flagWr = False;
                if flagWr :
                    for name in names:
                        if name in entry:
                            ename = str(entry[name])
                            if ',' in ename or '\n' in ename:
                                fmt = u'"%s"%s'
                            else:
                                fmt = u'%s%s'
                            f.write(fmt % (entry[name], delim))
                        else:
                            f.write(delim)
                    f.write('\n')
            if f != sys.stdout:
                f.close()
            logging.info('saved data to %r' % f.name)    
    
    

class BTTsExperimentDM(BTTsExperiment):
    def __init__(self,_oneTrigger):
        super().__init__(_oneTrigger);
        self.exp = None;
        self.filename = None;
        pass;
    def create(self, _filename,trc,param):
        self.filename = _filename;
        # experiment
        #self.exp = ExExperimentHandler(_name='testExpDM', _dataFileName=_filename);
        self.exp = data.ExperimentHandler(name='testExpDM', dataFileName=_filename);
        #self.exp = ExExperimentHandler(_name='testExpDM', _dataFileName=self.filename);
        
        #self.exp.saveAsPickle
        # trials
        self.trials = trc.newBTTsTrials();
        self.trials.create();
        cur = self.trials;
        print("BTTsExperimentDM create trials");
        #print(type(cur));
        #print(cur);
        
        # loop
        self.exp.addLoop(self.trials.getResponsesTH()) 
        self.exp.addLoop(self.trials.getTH())
        pass;
    def close(self):
        if self.exp != None:
            if isinstance(self.exp, ExExperimentHandler):
                self.exp.saveAsWideTextEx("expDM",delim='comma');
                print("close saveAsWideTextEx");
            self.exp.close();
        pass;
    
    def nextEntry(self):
        print("BTTsExperimentDM nextEntry 01");
        self.exp.nextEntry();
        print("BTTsExperimentDM nextEntry end");
        pass;
    def pr(self):
        if False:
            print(self.exp);
            print(self.trials.th_trials);
            print(self.trials.__repr__());
        pass;
    def getTrials(self):
        return self.trials;


class BTTsPosDM:
    def __init__(self):
        self.phase_fixationpos = (0,0);
        self.phase_sample_stim1pos = (0,0);
        self.phase_delay_fixationpos = (0,0);
        self.phase_choice_stimposList = [
            [[-0.3, 0.0],[ 0.3, 0.0]],
            [[ 0.0,-0.3],[ 0.0, 0.3]],
            [[-0.3,-0.3],[ 0.3, 0.3]],
            [[-0.3, 0.3],[ 0.3,-0.3]]
            ];

class BTTsToolDM:
    def __init__(self):
        pass;
    @staticmethod
    def getVoltage(bttsState ):
        retVol = 0.0;
        if defDM.PHASE_BeforeTask == bttsState.state1:
            retVol = defDM.VOL_TrialOn;
        elif defDM.PHASE_Sample == bttsState.state1:
            retVol = defDM.VOL_CueP;
        elif defDM.PHASE_Delay == bttsState.state1:
            retVol = defDM.VOL_HmHold2P;
        elif defDM.PHASE_Choise == bttsState.state1:
            retVol = defDM.VOL_TargetOn;
        elif defDM.PHASE_PreEnd == bttsState.state1:
            retVol = defDM.VOL_PreRwdP;
        elif defDM.PHASE_End == bttsState.state1:
            retVol = defDM.VOL_RwdP;
        elif defDM.PHASE_PrePunishment == bttsState.state1:
            retVol = defDM.VOL_ErrorP;
            pass;
        else:
            pass;
        return retVol;

class BTTsBeepDM:
    def __init__(self, soundInfo, _beep):
        self.soundFile = 'A';
        self.soundSecs = 0.2;
        self.soundStereo=True;
        self.soundHamming=True
        self.soundInfo = soundInfo;
        if _beep == 1:
            self.soundFile = 'C';
            self.soundSecs = 0.3;
        elif _beep == 2:
            self.soundFile = 'D';
            self.soundSecs = 0.3;
            self.psychopySound = sound.Sound(self.soundFile, secs = self.soundSecs, sampleRate=soundInfo.sound_sampleRate,stereo = self.soundStereo , hamming = self.soundHamming)
        elif _beep == 3:
            self.soundFile = 'E';
            self.soundSecs = 0.3;
            self.psychopySound = sound.Sound(self.soundFile, secs = self.soundSecs, sampleRate=soundInfo.sound_sampleRate,stereo = self.soundStereo , hamming = self.soundHamming)
        elif _beep == 4:
            self.soundFile = 'F';
            self.soundSecs = 1.0;
            self.psychopySound = sound.Sound(self.soundFile, secs = self.soundSecs, sampleRate=soundInfo.sound_sampleRate,stereo = self.soundStereo , hamming = self.soundHamming)
        else:
            self.soundFile = 'G';
            self.soundSecs = 0.2;
            self.psychopySound = sound.Sound(self.soundFile, secs = self.soundSecs, sampleRate=soundInfo.sound_sampleRate,stereo = self.soundStereo , hamming = self.soundHamming)
        pass;
        self.psychopySound = sound.Sound(self.soundFile, secs = self.soundSecs, sampleRate=self.soundInfo.sound_sampleRate,stereo = self.soundStereo , hamming = self.soundHamming)
    
    def play(self):
        now = ptb.GetSecs()
        #self.psychopySound.setSound(self.soundFile, secs=self.soundSecs,  hamming=self.soundHamming );
        #self.psychopySound.play(when=now+self.soundInfo.hardsnddelay);
        #self.psychopySound.play(when=now);
        if self.soundInfo.useReload:
            self.psychopySound = sound.Sound(self.soundFile, secs = self.soundSecs, sampleRate=self.soundInfo.sound_sampleRate,stereo = self.soundStereo , hamming = self.soundHamming)
            pass;
        else:
            pass;
        print("beeo play " + self.soundFile);
        self.psychopySound.play();
        pass;
    def stop(self):
        self.psychopySound.stop();
        pass
    
class BTTsControlBeepDM:
    def __init__(self,soundInfo):
        self.soundInfo = soundInfo;
        self.beep1 = BTTsBeepDM(self.soundInfo,1);
        self.beep2 = BTTsBeepDM(self.soundInfo,2);
        self.beep3 = BTTsBeepDM(self.soundInfo,3);
        self.beep4 = BTTsBeepDM(self.soundInfo,4);
        pass;


class BTTsPunishmentDM(BTTsPunishment):
    def __init__(self, _param, _beepControl):
        super().__init__(_param);
        self.beepControl = _beepControl;
        pass;
class BTTsRewardDM(BTTsReward):
    def __init__(self,_param, _beepControl):
        super().__init__(_param);
        self.beepControl = _beepControl;
        pass;
    def clearRewarded(self):
        pass;
    def reward(self, _reward):
        if _reward:
            pass;
            if self.param.Set_RewardSoundOn.value:
                self.beepControl.beep3.play();
        else:
            if self.param.Set_PunishmentSoundOn.value:
                self.beepControl.beep4.play();
            pass;
        pass;

def testMain2():
    param = BTTsParamDM();
    trials = BTTsTrialsDM(param);
    trials.create();
    print(trials.th_trials);
    pass;

def testMain1():
    stateBuffer = BTTsStateBuffer();
    #defDM = BTTsDefineDM();
    oTrig =None;
    oneTriggerThread =None;
    
    param = BTTsParamDM();
    
    countTrial = BTTsCountTrialDM();
    trc = BTTsTrialControlDM(param,countTrial,stateBuffer,oTrig,oneTriggerThread);
    trials = trc.newBTTsTrials();
    
    # create
    trials.create();
    print(trials.th_trials);
    
    countTrial = 0;
    lopTr = True;
    while lopTr:
        try:
            trial = trials.next();
            if trial == None:
                lopTr = False;
        except StopIteration:
            lopTr = False;
            print("lopTr01 " + str(lopTr));
            print("except StopIteration for lopTr " + str(lopTr));
        print("lopTr02 " + str(lopTr));
        if lopTr:
            stim_col = trial.getTH()['stim_color']
            stim_shape = trial.getTH()['stim_shape'];
            print(trial.getTH());
            countTrial += 1;
    pass;
    print('end of task');
    print("countTrial " + str(countTrial));
    pass;
    core.quit()
    pass;
    
    
def testMain3():
    stateBuffer = BTTsStateBuffer();
    #defDM = BTTsDefineDM();
    oTrig =None;
    oneTriggerThread =None;
    
    param = BTTsParamDM();
    #param.numOfTrial.setValue(1);
    #param.modeDelayedMatch.setValue(0);
    
    countTrial = BTTsCountTrialDM();
    exp = BTTsExperimentDM(oTrig);
    trc = BTTsTrialControlDM(param,countTrial,stateBuffer,oTrig,oneTriggerThread);
    
    trc.msIO = None;
    trc.keyIO = None;
    #
    trc.beginThread();
    #
    exp.create("data/testMain3", trc, param);

    print(exp.getTrials().th_trials);
    print("testMain3 __");
    
    countTrial = 0;
    lopTr = True;
    while lopTr:
        try:
            thisTrial = exp.getTrials().next(False);
            if thisTrial == None:
                lopTr = False;
        except StopIteration:
            lopTr = False;
            #print("lopTr01 " + str(lopTr));
            print("except StopIteration for lopTr " + str(lopTr));
        print("lopTr02 " + str(lopTr));
        if lopTr:
            
            stimPair = thisTrial.getTH()['stim_shape'];
            stimPosPair = thisTrial.getTH()['stim_pos'];
            stim_correctIndex = thisTrial.getTH()['stim_correctIndex'];

            print("countTrial" + str(countTrial));
            print(stimPair)
            print(stimPosPair)
            print(stim_correctIndex)
            #
            
            countTrial += 1;
    pass;
    print('end of task');
    print("countTrial " + str(countTrial));
    pass;
    print(exp.getTrials().getResponsesTH());
    pass;
    trc.endThread();
    
    print(type(exp.exp));
    BTTsTool.outputPsydata(exp.exp);
    
    
    core.quit()
    pass;
    
def testMainSound1():
    soundInfo = BTTsSoundInfo();
    
    param = BTTsParamDM();
    
    beepCtrl = BTTsControlBeepDM(soundInfo);
    feeder = BTTsFeederFood(param);
    punishment = BTTsPunishmentDM(param,beepCtrl);
    reward = BTTsRewardDM(param,beepCtrl,feeder);

    beepCtrl.beep1.play();
    core.wait(0.8)
    for n in range(5):
        print(str(n));
        core.wait(1.0);
        beepCtrl.beep1.play();
        core.wait(1.0);
        beepCtrl.beep2.play();
        core.wait(1.0);
        beepCtrl.beep3.play();
        core.wait(1.0);
        beepCtrl.beep4.play();

    pass;
def testMain():
    testMain3();
    #testMainSound1();
    pass;

def testParam():
    p1 = BTTsParamDM();
    p1.printParamList();
    
    pass;


if __name__ == "__main__":
    testParam();

