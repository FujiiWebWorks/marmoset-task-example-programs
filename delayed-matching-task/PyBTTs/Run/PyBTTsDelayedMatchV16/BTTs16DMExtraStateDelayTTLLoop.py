#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psychtoolbox as ptb
from psychopy import locale_setup
from psychopy import prefs

import os  # handy system and path functions
import sys  # to get file system encoding

bttsEnvPath = '../PyBTTsEnv';
sys.path.append(bttsEnvPath);
sndenvfile = bttsEnvPath + '/'+'PyBTTsSound.py'
is_file = os.path.isfile(sndenvfile)
if is_file:
    from PyBTTsSound import *
else:
    pass # パスが存在しないかファイルではない

#
from psychopy import data, visual, core
from psychopy.hardware import keyboard
from psychopy.event import Mouse;
#import psychopy.iohub as io
from psychopy.iohub import launchHubServer
from psychopy.iohub.constants import EventConstants

from psychopy import sound, gui, visual, core, data, event, logging, clock, colors, layout
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
#
import os  # handy system and path functions
import sys  # to get file system encoding
import time
import math
import signal
import gc

import win32gui
import win32con


import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle, choice as randchoice
import csv
import pyglet
import pyglet.gl as GL
from pyglet import gl


#visual.useFBO = True  # if available (try without for comparison)
import matplotlib
matplotlib.use('Qt5Agg')  # change this to control the plotting 'back end'
import pylab

#
sys.path.append('../PyDIO');
from wapperPyDIOBase import OneTrigger
sys.path.append('../PyDIONIDAQ');
from wrapperPyDIONIDAQ import NIDAQOneShotDAQ

#
sys.path.append('./CommonV010011');
from bttsTTL import BTTsTTL, BTTsTTLU3, BTTsTTLUSB2TTL8;
#
from bttsdatafile import bttsdatafile
from bttsTrial import BTTsTool,LoopFlag,BTTsMouseEvent,BTTsStateBuffer,BTTsReward
from bttsNet import BTTsNetServer,waitParamBTTsNetServ
from bttsWaitFor import BTTsWaitFor
from bttsRemoteOne import runOneDialog,runOneParamLoadBin
from bttsFeeder import BTTsFeederFood


from bttsTrialDM import BTTsTrialControlDM, BTTsParamDM,  BTTsExperimentDM,BTTsStateDM,BTTsDefineDM,BTTsPosDM,BTTsToolDM
from bttsTrialDM import BTTsControlBeepDM, BTTsPunishmentDM,BTTsRewardDM,BTTsBeepDM,BTTsCountTrialDM
from bttsTrialDM import BTTsColorDBDM, BTTsShapeDBDM

from bttsTrial import BTTsStimAttr,BTTsVisualStim,BTTsColor, BTTsShape
from bttsMouseExit import BTTsMouseExit

soundInfo = BTTsSoundInfo();

# for touch
sys.path.append('../PyBTTsTouch');
print(sys.path);

from LoadPyBTTsTouchOne import  add_double_PyBTTs
from LoadPyBTTsTouchOne import  RemoveHook_PyBTTs,InstallHookFromWindowTitlePyschopy_PyBTTs
retd = add_double_PyBTTs(1.1,2.1);
print(type(retd));
print(retd);    
#

sys.path.append('../TextGL');
from TextOpenGLObj import TextOpenGLObj

def foreground_on(hwnd, title):
    name = win32gui.GetWindowText(hwnd)
    if name.find(title) >= 0:
        #最前面ON
        #HWND_TOP
        #HWND_TOPMOST
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, 0, 0, 0, 0,  win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
        #win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
        return
def foregroundTOPMOST_on(hwnd, title):
    name = win32gui.GetWindowText(hwnd)
    if name.find(title) >= 0:
        #最前面ON
        #HWND_TOP
        #HWND_TOPMOST
        #win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, 0, 0, 0, 0,  win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
        return

def foreground_off(hwnd, title):
    name = win32gui.GetWindowText(hwnd)
    if name.find(title) >= 0:
        #最前面OFF
        win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
        return

def str2bool(s):
     return s.lower() in ["true", "t", "yes", "1"]
 
class DrawGL:
    def __init__(self, _flagDisplayInfo,_xyScreen):
        self.flagDisplayInfo = _flagDisplayInfo;
        self.xyScreen = _xyScreen;
        # unit is 'height'
        # unit is 0.5
        xs = self.xyScreen[1]  / self.xyScreen[0];
        self.yscale = 1.0;
        self.xscale = xs / 1.0;
        #
        scale = 2.0;
        self.xscale *= scale;
        self.yscale *= scale;
        pass;
 
    def DrawGLFrame(self,frame):
        if not( self.flagDisplayInfo):
            return;
        x = frame[0];
        y = frame[1];
        w = frame[2];
        h = frame[3];
        
        gl.glPushMatrix();
        gl.glScalef(self.xscale, self.yscale, 1.0);
        ##glLineWidth();
        gl.glColor3f(1.0, 1.0, 1.0);
        gl.glBegin(gl.GL_LINE_LOOP);
        gl.glVertex3f(x, y, 1);
        gl.glVertex3f(x + w, y, 1);
        gl.glVertex3f(x + w, y+h, 1);
        gl.glVertex3f(x, y+h, 1);
        gl.glEnd()
        
        gl.glPopMatrix();
    
    def DrawGLCenterFrame(self,pos, area):
        w = area[0];
        h = area[1];
        x = pos[0] - w / 2.0;
        y = pos[1] - h / 2.0;
        #
        #print("DrawGLCenterFrame");
        #print(pos);
        #print(area);
        self.DrawGLFrame([x,y,w,h])
        pass;
 
argv = sys.argv;
modeApp = -1;
flagFullScreen=False;
flagDrawMouse=True;
screenscale=100; # 100%
xscreensize=800;
yscreensize=600;
sz = len(argv);
if sz == 1:
    pass;
if 1 < sz:
    modeApp = int( argv[1] ); # -1 is param
if 2 < sz:
    flagFullScreen =  str2bool(argv[2]);
if 3 < sz:
    flagDrawMouse =  str2bool(argv[3]);
if 4 < sz:
    screenscale =  float(argv[4]);
if 5 < sz:
    xscreensize = int(argv[5]);
if 6 < sz:
    yscreensize = int(argv[6]);
    yscreensize += 1;


from bttsEnvFile import BTTsEnvFile, BTTsEnvParam, BTTsEnvHardParam

envParam = BTTsEnvParam();
env = BTTsEnvFile(envParam);
envParam.pr();

envHardParam = BTTsEnvHardParam();
envHardParam.load(env)
#envHardParam.pr();

screen_background_color = envParam.screen_background_color_rgb255;
screen_background_end_color = screen_background_color;

#winflip
holdFlipTm=None;
def winflip(win,_clock):
    global holdFlipTm;
    win.flip();
    tmpTm = _clock.getTime();
    if holdFlipTm != None:
        diffTm = tmpTm - holdFlipTm;
        if( 0.031 < diffTm ):
            print("---------------------------------------------------------------------");
            print("TIME-WinFlip-40-Over\t"+str(diffTm)+" "+str(tmpTm));
            pass;
        else:
            pass;
        pass;
    else:
        pass;
    holdFlipTm = tmpTm;
    #print("TIME-WinFlip\t"+str(tmpTm));
    pass;

#
_thisDir = os.path.dirname(os.path.abspath(__file__))
print(_thisDir);
os.chdir(_thisDir)


#oneTrigger = BTTsTTLUSB2TTL8();

print('BTTsNet 01');
bttsNet = BTTsNetServer();
if bttsNet != None:
    bttsNet.begin();

#
# pram
#if modeApp == -1:
#    pass;
#else:
#   waitParamBTTsNetServ(bttsNet,param);


# 1 --------------------------------------------------


# ----------------------------------------------------------
#

#
# sound Delay
hardsnddelay = 0.010; # soundblasterXG6 and audioLatencyMode is 0
hardsnddelay = 0.000;
doutdelay=0.050;
flagDoutDelay=False;
#
flagTTLCallOnFlip = True;

def callbackFrameLH(_port, _data, frameN):
    if _port != None :
        _port.setData(_data);

def callbackFrameLabJack(_port, volt, frameN):
    if _port != None :
        _port.write(0,volt);

def callbackFrameTT(_portA, _valA, _portB, _valB,frame):
    if _portB != None:
        _portB.write(1,_valB);
    if False and _portA != None:
        _portA.write(0,_valA);

def callbackFrameTTOneFrame(_nidaq, _oneF, _frameN):
    if _oneF.flagTTL:
        if _oneF.cmp():
            if _nidaq != None:
                _nidaq.writeAO(0,1.0);
            _oneF.flagTTL = False;
        _oneF.count();
    else:
        if _nidaq != None:
            _nidaq.writeAO(0,0.0);
        pass;

class OneFrame:
    def __init__(self):
        self.flagTTL = False;
        self.countFrame = 0;
        self.numOfFrame = 0
        self.recTime = None;
        pass;
        #
        self.flagRecVSync = False;
        self.retLabel = "None";
        self.valRecFloat32 = None;
        self.valRecFloat32CueOff = None;
        self.flagAO = False;
        self.volt = 0.0;    
        pass;
    def resetFF(self,_numOfFrame):
        self.countFrame = 0;
        self.numOfFrame = _numOfFrame;
    def cmp(self):
        return not ( self.countFrame < self.numOfFrame);
    def count(self):
        self.countFrame += 1;

"""
def callbackFrameTTOneFrame(_portA, _valA, _portB, _valB,_oneF,frame):
    #     win.callOnFlip(callbackFrameTTOneFrame, oneTriggerVSync,float(1.0), oneTrigger,int(1),oneF, frameN);

    if _oneF.flagTTL:
        if _portB != None:
            _portB.write(1,_valB);
        if False and _portA != None:
            print("callbackFrameTTOneFrame TTL _valA");
            _portA.write(0,_valA);
        pass;
        _oneF.countFrame = 0;
    else:
        if _oneF.countFrame == -1:
            pass;
        else:
            if _oneF.countFrame == 1:
                if _portB != None:
                    print("callbackFrameTTOneFrame TTL 0");
                    _portB.write(1,0);
                _oneF.countFrame = -1;
            pass;
    pass;
    if _oneF.countFrame != -1:
        _oneF.countFrame += 1;
    pass;
"""    
#

def callbackFlipOneFrameOneF(_oneF,_ttlAOut):
    if _oneF.flagTTL:
        if _oneF.flagVSync:
            if _oneF.cmp():
                _oneF.flagTTL = False;
                if _oneF.flagAO:
                    if _ttlAOut != None:
                        _ttlAOut.writeAO(0,_oneF.volt);
                    pass;
                    tmVal = logging.defaultClock.getTime();
                    if _oneF.valRecFloat32 != None:
                        _oneF.valRecFloat32.setValue(tmVal);
                    if _oneF.valRecFloat32CueOff != None:
                        if _oneF.valRecFloat32CueOff.flagSetVal:
                            # already set, is not set
                            pass;
                        else:
                            if _oneF.curRec.CueOnT_s.flagSetVal:
                                _oneF.valRecFloat32CueOff.setValue(tmVal);
                                pass;
                            else:
                                pass;
                            pass;
                    pass;
                pass;
            _oneF.count();
            pass;
        else:
            pass;
    pass;


"""
def genListStimOld(_win, stim_vertices):
    print(type(stim_vertices));
    print(stim_vertices);
    
    stimList = [];
    stimPos = (0,0);
    stimSize = (0.25, 0.25);
    image = "resource//image//"+"imgStart.png";
    
    stim0 = visual.ImageStim(_win,image, pos=stimPos,size=stimSize);
    stim0.attrName = image;
    #stim0 = visual.ShapeStim(win,pos=stimPos,size=stimSize, fillColor = 'red',  vertices = stim_vertices['triangle']);
    stim1 = visual.ShapeStim(win,pos=stimPos,size=stimSize, fillColor = 'blue', vertices = stim_vertices['rectangle']);
    stim1.attrName = "blue and rectangle";
    stim2 = visual.ShapeStim(win,pos=stimPos,size=stimSize, fillColor = 'blue',  vertices = stim_vertices['triangle']);
    stim2.attrName = "blue and triangle";
    stim3 = visual.ShapeStim(win,pos=stimPos,size=stimSize, fillColor = 'red', vertices = stim_vertices['rectangle']);
    stim3.attrName = "red and triangle";
    stimList = [stim0,stim1,stim2,stim3];
    return stimList;
def genListStimB(win, stim_vertices):
    stimPos = (0,0);
    stimSize = (0.25, 0.25);
    stim0 = visual.ShapeStim(win,pos=stimPos,size=stimSize, fillColor = 'red', vertices = stim_vertices['circle']);
    stim0.attrName = "read and circle";
    stim1 = visual.ShapeStim(win,pos=stimPos,size=stimSize, fillColor = 'blue', vertices = stim_vertices['circle']);
    stim1.attrName = "blue and circle";
    stim2 = visual.ShapeStim(win,pos=stimPos,size=stimSize, fillColor = 'blue',  vertices = stim_vertices['rectangle']);
    stim2.attrName = "blue and rectangle";
    stim3 = visual.ShapeStim(win,pos=stimPos,size=stimSize, fillColor = 'red', vertices = stim_vertices['rectangle']);
    stim3.attrName = "red and rectangle";
    stimList = [stim0,stim1,stim2,stim3];
    return stimList;
"""
"""
def genListStimC(win, listColor, listShape, colorDB, shapeDB):
    stimList = [];
    stimPos = (0,0);
    stimSize = (0.25, 0.25);
    #
    curS = None;
    curC = None;
    for snum in listShape:
        curS = shapeDB.getShape(snum);
        for cnum in listColor:
            curC = colorDB.getColor(cnum);
            stimT = visual.ShapeStim(win,pos=stimPos,size=stimSize,colorSpace='rgb255', fillColor = curC.color, vertices = curS.shapePos);
            stimT.attrName = "" + curC.cname + " " + curS.sname;
            stimList.append(stimT);
    
    pass;
    return stimList;
"""

def genStim(_win, cur):
    cur.prInfo();    
    stimPos  = cur.stimAttr.stimPos;
    stimSize = cur.stimAttr.stimSize;
    stimColur = cur.stimAttr.color.color;
    if cur.stimAttr.isImage:
        image = cur.stimAttr.stimName;
        stimT = visual.ImageStim(_win,image, pos=stimPos,size=stimSize,units='height');
    else:
        stimShape = cur.stimAttr.shape.shapePos;
        #stimT = visual.ShapeStim(win,pos=(0,0),size=(1.0,1.0),colorSpace='rgb255', fillColor = (1,1,1), vertices = stimShape ,units='height');
        stimT = visual.ShapeStim(_win,pos=stimPos,size=stimSize,colorSpace='rgb255', fillColor = stimColur, vertices = stimShape ,units='height');
        #stimT = visual.ShapeStim(win,pos=stimPos,size=stimSize,colorSpace='rgb255', fillColor = stimColur, vertices = stimShape ,units='height');
    cur.stim = stimT; 


class StimGroup:
    def __init__(self):
        self.groupName = "GroupA";
        self.stimList = [];
        pass;
def selectStimGroup(list, str ):
    retSG = list[0];
    for cur in list:
        a = cur.groupName.lower();
        b = str.lower();
        print(a);
        print(b);
        if a == b:
            retSG = cur;
            break;
    print(retSG);
    return retSG;

def genStimGroupFromList(win,_groupName, list):
    retSG = StimGroup();
    retSG.groupName = _groupName;
    for cur in list:
        genStim(win, cur);
        retSG.stimList.append(cur);
    return retSG;

def genStimListSignal(colorDB):
    stimList = [];
    stimPos = [0,0];
    stimSize = [0.25, 0.25];
    touchArea =  [0.3, 0.3];
    
    red = colorDB.getColor(3);
    green = colorDB.getColor(4);
    yellow = colorDB.getColor(2);
    
    
    resPath = "resource//image//"
    
    pnglist = [
        ( "imgStart.png", green ),
        ( "imgStartY.png", yellow ),
        ( "imgStartRed.png", red ),
        ( "imgStopBlue.png", green ),
        ( "imgStopY.png", yellow ),
        ( "imgStop.png", red )];
        
    for png in pnglist:
        vs = BTTsVisualStim();
        vs.stimAttr.isImage = True;
        vs.stimAttr.stimName = resPath + png[0];
        vs.stimAttr.color = png[1];
        vs.stimAttr.shape = None;
        vs.stimAttr.stimPos = stimPos;
        vs.stimAttr.stimSize = stimSize;
        vs.stimAttr.flagStimArea = True;
        vs.stimAttr.stimAreaSizeForTouch = touchArea;
        stimList.append(vs);
    return stimList;
     

def genStimListColorShape(listColor, listShape, colorDB, shapeDB, useArea=False):
    stimList = [];
    stimPos = [0,0];
    stimSize = [0.25, 0.25];
    touchArea =  [0.3, 0.3];
    #
    curS = None;
    curC = None;
    for snum in listShape:
        curS = shapeDB.getShape(snum);
        for cnum in listColor:
            curC = colorDB.getColor(cnum);
            vs = BTTsVisualStim();
            vs.stimAttr.stimPos = stimPos;
            vs.stimAttr.stimSize = stimSize;
            vs.stimAttr.stimName = curC.cname + "/" + curS.sname;
            vs.stimAttr.flagStimArea = useArea;
            vs.stimAttr.stimAreaSizeForTouch = touchArea;
            vs.stimAttr.color = curC;
            vs.stimAttr.shape = curS;
            stimList.append(vs);
    return stimList;

def toSecFromMSec(_tmmsec):
    return _tmmsec / 1000.0;

def recOneStimBase(exp,bname,stimS):
    exp.exp.addData(bname+"Shape",  stimS.stimAttr.stimName );
    exp.exp.addData(bname+"SizeX",  stimS.stimAttr.stimSize[0]);
    exp.exp.addData(bname+"SizeY",  stimS.stimAttr.stimSize[1]);
    exp.exp.addData(bname+"PositionX",  stimS.stimAttr.stimPos[0]);
    exp.exp.addData(bname+"PositionY",  stimS.stimAttr.stimPos[1]);
    
    if stimS.stimAttr.flagStimArea:
        windowSizeX= stimS.stimAttr.stimAreaSizeForTouch[0];
        windowSizeY= stimS.stimAttr.stimAreaSizeForTouch[1];
    else:
        windowSizeX= stimS.stimAttr.stimSize[0];
        windowSizeY= stimS.stimAttr.stimSize[1];
    exp.exp.addData(bname+"WindowSizeX",  windowSizeX);
    exp.exp.addData(bname+"WindowSizeY",  windowSizeY);


def recOneStimCue(exp,stimS):
    recOneStimBase(exp,"Cue",stimS);

def recOneStimTarget(exp,stimS):
    recOneStimBase(exp,"Target",stimS);
    
def recOneStimNonTarget(exp,stimS):
    recOneStimBase(exp,"NonTarget",stimS);

# --------------------------------------------


#for n in range(60*2):
#    win.flip()


flagPylabGraph=True;

#--------------------------------------------------------

class GraphHistVar:
    def __init__(self):
        self.win = None;
        pass;

def graphHist(graphHistVar):
    win = graphHistVar.win;
    
    deltaT01=0.0;
    deltaT02=0.0;
    deltaT = [];
    
    deltaTGraph = pylab.array(deltaT) * 1000;
    # calculate some values
    intervalsMS = pylab.array(win.frameIntervals) * 1000
    m = pylab.mean(intervalsMS)
    sd = pylab.std(intervalsMS)
    # se=sd/pylab.sqrt(len(intervalsMS)) # for CI of the mean
    
    msg = "Mean=%.1fms, s.d.=%.2f, 99%%CI(frame)=%.2f-%.2f"
    distString = msg % (m, sd, m - 2.58 * sd, m + 2.58 * sd)
    nTotal = len(intervalsMS)
    nDropped = sum(intervalsMS > (1.5 * m))
    msg = "Dropped/Frames = %i/%i = %.3f%%"
    droppedString = msg % (nDropped, nTotal, 100 * nDropped / float(nTotal))
    
    numPlt=1;
    pylab.figure(figsize=[12, 8])
    
    # plot the frameintervals
    pylab.subplot(1, 3, numPlt)
    pylab.plot(intervalsMS, '-')
    pylab.ylabel('t (ms)')
    pylab.xlabel('frame N')
    pylab.title(droppedString)
    numPlt += 1;
    
    pylab.subplot(1, 3, numPlt)
    pylab.plot(deltaTGraph, '-')
    pylab.ylabel('t (ms)')  
    pylab.xlabel('soundNum')
    pylab.title('deltaT sound')
    numPlt += 1;
    
    if True:
        pylab.subplot(1, 3, numPlt)
        pylab.hist(intervalsMS, 50, histtype='stepfilled')
        pylab.xlabel('t (ms)')
        pylab.ylabel('n frames')
        pylab.title(distString)
        numPlt += 1;
    
    pylab.tight_layout();
    
    if flagPylabGraph:
        pylab.show()


class ButtonB2:
    def __init__(self):
        self.flagOn = False;
        pass;

class RunCoreDMVar:
    def __init__(self):
        self.feeder = None;
        self.beepCtrl = None;
        self.punishment = None;
        self.reward = None;
        self.win = None;
        self.textGL = None;
        self.stimGroupA = None;
        self.msIO = None;
        self.keyIO = None;
        self.lopTr = None;
        self.lopFrame = None;
        self.oneTrigger = None;
        self.ttlAOut = None;
        self.ttlReader = None;
        self.kb = None;
        self.drawGL = None;
        self.bttsME = None;
        self.hwndPsychoPy = None;
        pass;
    


def runCoreDM(param, runCoreDMVar ):
    win = runCoreDMVar.win;

    posDM = BTTsPosDM();
    colorDB = BTTsColorDBDM();
    shapeDB = BTTsShapeDBDM();
    
    clistFix = [colorDB.white]; # color
    slistFix = [shapeDB.circle];
    listFix = genStimListColorShape(clistFix,slistFix,colorDB, shapeDB);
    stimFixGroup = genStimGroupFromList(win,"GroupFix",listFix);
    
    
    listStimGrounp = [];
    clist = [3,4,1];
    slist = [1,2,3];
    listCS = genStimListColorShape(clist,slist,colorDB, shapeDB, useArea=True);
    tmpList = genStimGroupFromList(win,"GroupA_ShapeColor",listCS);
    listStimGrounp.append(tmpList);
    clist = [3,4,1];
    slist = [4,5,6];
    listCS = genStimListColorShape(clist,slist,colorDB, shapeDB, useArea=True);
    tmpList = genStimGroupFromList(win,"GroupB_ShapeColor",listCS);
    listStimGrounp.append(tmpList);
    
    listSignal = genStimListSignal(colorDB);
    tmpList = genStimGroupFromList(win,"GroupA_image_signal",listSignal);
    listStimGrounp.append(tmpList);
    
    tmpSG = selectStimGroup(listStimGrounp,param.stimGroupName.value );
    runCoreDMVar.stimGroupA = tmpSG.stimList;
    param.stim_list_override = param.stim_list.value;
    
    
    """
    if param.modeDelayedMatch.value == 0:
        runCoreDMVar.stimGroupA = genStimGroupFromList(win,listCS);
        param.stim_list_override = param.listPosition;
        pass;
    elif param.modeDelayedMatch.value == 1:
        runCoreDMVar.stimGroupA = genStimGroupFromList(win,listCS);
        param.stim_list_override = param.listColor;
        pass;
    elif param.modeDelayedMatch.value == 2:
        runCoreDMVar.stimGroupA = genStimGroupFromList(win,listCS);
        param.stim_list_override = param.listShape;
        pass;
    elif param.modeDelayedMatch.value == 3:
        runCoreDMVar.stimGroupA = genStimGroupFromList(win,listSignal);
        param.stim_list_override = param.listSignal;
        pass;
    elif param.modeDelayedMatch.value == 4:
        runCoreDMVar.stimGroupA = genStimGroupFromList(win,listCS);
        param.stim_list_override = param.listPosition;
        pass;
    elif param.modeDelayedMatch.value == 5:
        runCoreDMVar.stimGroupA = genStimGroupFromList(win,listCS);
        param.stim_list_override = param.listColor;
        pass;
    elif param.modeDelayedMatch.value == 6:
        runCoreDMVar.stimGroupA = genStimGroupFromList(win,listCS);
        param.stim_list_override = param.listShape;
        pass;
    elif param.modeDelayedMatch.value == 7:
        runCoreDMVar.stimGroupA = genStimGroupFromList(win,listSignal);
        param.stim_list_override = param.listSignal;
        pass;
    """

    polygonLeftTop = visual.Rect(
        win=win, name='polygon',units='height', 
        width=(0.5, 0.5)[0], height=(0.5, 0.5)[1],
        ori=0.0, pos=(-0.5, 0.5), anchor='center',
        lineWidth=1.0,     colorSpace='rgb',  lineColor='white', fillColor='white',
        opacity=None, depth=0.0, interpolate=True)    
    
    fixation = BTTsVisualStim();
    fixation.copyFromLow(stimFixGroup.stimList[0]);
    fixation.stimAttr.stimName =  "fixation";
    fixation.stimAttr.stimSize = (0.1, 0.1);
    fixation.stimAttr.stimPos = posDM.phase_fixationpos;
    #fixation.stim = fixationStim;

    fixation2 = BTTsVisualStim();
    fixation2.copyFromLow(stimFixGroup.stimList[0]);
    fixation2.stimAttr.stimName =  "fixation2";
    fixation2.stimAttr.stimSize = (0.1, 0.1);
    fixation2.stimAttr.stimPos = posDM.phase_fixationpos;
    #fixation.stim = fixationStim;


    """    
    fixation2 = BTTsVisualStim();
    fixation2.stimAttr.stimName = "fixation2";
    fixation2.stimAttr.stimSize = (0.35, 0.35);
    fixation2.stimAttr.stimPos = posDM.phase_fixationpos;
    fixation2.stim = fixationStim;
    """
    
    holdCountFrame = None;
    countFrame = 0;
    
    curState = None;
    flagTrial = False;
    flagState = False;
    
    holdpxx=None;
    
    oneF = OneFrame();
    
    machineNo = 1;
    bdf = bttsdatafile(_thisDir);
    bdf.create(machineNo,"mini02DMExtra");
    
    
    #state = BTTsStateDM();
    stateBuffer = BTTsStateBuffer();
    defDM = BTTsDefineDM();
    
    curStimGroup = runCoreDMVar.stimGroupA;
    
    textGL = runCoreDMVar.textGL;
    
    countTrial = BTTsCountTrialDM();
    exp = BTTsExperimentDM(runCoreDMVar.oneTrigger);
    trc = BTTsTrialControlDM(param,countTrial,stateBuffer,runCoreDMVar.oneTrigger,runCoreDMVar.ttlAOut);
    #
    flagThread = True;
    flagStim = True;
    flagStartThread = False;
    flagStopThread = False;
    
    flagStatePr = False;
    
    trc.msIO = runCoreDMVar.msIO;
    trc.keyIO = runCoreDMVar.keyIO;
    #
    trc.beginThread();
    #
    exp.create(bdf.getFilename(), trc, param);
    exp.pr();
    
    pass;

    lopTr = runCoreDMVar.lopTr;
    lopFrame = runCoreDMVar.lopFrame;
    lopTr.init();


    btnB2 = ButtonB2() ;

    ITITimer =  BTTsWaitFor();
    ITICurrent = 0.0;
    ITICurrent += toSecFromMSec( param.Set_ITI.value );

    gl_retry_count = 0;
    holdState = None;
    thisTrial = None;
    while lopTr.isLoopFlag() :
        
        ITITimer.stampNextFor();
        curState = BTTsStateDM();
        curState.state1 = defDM.PHASE_ITI;
        curState.flagTrial = True;
        
        try:
            print("exp.getTrials().next 01");
            if exp.getTrials().flagNext:
                exp.nextEntry(); # for Save Data
            thisTrial = exp.getTrials().next( gl_retry_count != 0) ;
            win.recordFrameIntervals = True
            #if gl_retry_count == 0:
            #    pass;
            #else:
            #    gl_retry_count -= 1;
            if thisTrial == None:
                print("exp.getTrials().next 02");
                lopTr.flagLoop = False;
                break;
            pass;
            print("exp.getTrials().next end");
        except StopIteration:
            print("exp.getTrials().next StopIteration");
            lopTr.flagLoop = False;
            break;
    
        #
        if runCoreDMVar.ttlAOut != None:
            runCoreDMVar.ttlAOut.writeAO(0,0.0);
        trialComponents = [];
        #
        lopFrame.init();
        
        flagSetISI = True;
        flagStartThread = False;
        
        runCoreDMVar.reward.clearRewarded();
        runCoreDMVar.feeder.clearFeeder();
        
        runCoreDMVar.bttsME.reset(); 

        flagMouseExit = False;
        flagExitExp = False;
        
        while lopFrame.isLoopFlag():
            if trc != None:
                if trc.bttsTh != None:
                    if btnB2.flagOn:
                        if trc.bttsTh.b2:
                            pass;
                        else:
                            btnB2.flagOn = False;
                            print("btnB2.flagOff", file=sys.stderr);
                        pass;
                    else:
                        if trc.bttsTh.b2:
                            btnB2.flagOn = True;
                            numOfFood = int(param.Set_RwdNum.value);
                            microL = param.Set_RwdDrink_microl.value;
                            runCoreDMVar.feeder.initButtonFeeder(numOfFood,microL);
                            print("btnB2.flagOn", file=sys.stderr);
                            pass;
                        else:
                            pass;
                        pass;
            else:
                pass;
            
            
            flagDrawLT = False;
            if flagSetISI:
                if ITITimer.timerFor(ITICurrent):
                    flagStartThread = True;
                    flagSetISI = False;
                    pass;
                else:
                    pass;
            
            
            if bttsNet!=None:
                if (countFrame % 60) == 0:
                    param.nFrame.value = countFrame;
                    if modeApp == -1:
                        pass;
                    else:
                        pass;
                        ##bttsNet.sendToForValue(param);
                        #bttsNet.recvFromForParam(param);
                    pass;
            
            if flagStartThread:
                print('flagStartThread 01');
                flagStartThread = False;
                thisTrial.getOneTrial().beginRunOneTrial();
                #
                thisTrial.getOneTrial().curRec.retryCount.setValue(gl_retry_count);
                #
                #
                print('flagStartThread end');
            pass;
            
            if flagStopThread:
                print('flagStopThread 01');
                flagStopThread = False;
                
                flagRetry = False;
                if param.numOfMaxRetry.value == 0:
                    flagRetry = False;
                else:
                    if thisTrial.getOneTrial().correctedOneTrial:
                        flagRetry = False;
                    else:
                        flagRetry = True;
                thisTrial.getOneTrial().endRunOneTrial();
                if flagRetry:
                    if gl_retry_count < param.numOfMaxRetry.value:
                        gl_retry_count += 1;
                        exp.getTrials().nextResponse();
                    else:
                        gl_retry_count = 0;
                        pass;
                else:
                    gl_retry_count = 0;
                    #exp.exp.addData("retry",False);
                
                lopFrame.requestFlagLoopOut();
                print('flagStopThread end');
            pass;
            
            #print("lopFrame 01");
            updateExp = False;
            #
            flagChange = False;
            #
            tmpStateBuf = None;
            stateBuffer.acquire();
            tmpStateBuf = stateBuffer.moveStateBuffer();
            stateBuffer.release();
    
            if len(tmpStateBuf) != 0:
                print("curState");
                for state in tmpStateBuf:
                    if flagStatePr:
                        #state.pr();
                        pass;
                    curState = state;
                    #curState.pr();
                    flagState = True;
                    flagTrial = curState.flagTrial;
                    if flagStatePr:
                        #print(state);
                        pass;
            if flagTrial:
                pass;
            
            
            
            #print("lopFrame 02");
            if flagState:
                if curState != None:
                    flagDrawLT = True;
                    
                    if defDM.PHASE_BeforeTask == curState.state1:
                        # first set Stim
                        thisTrial.getOneTrial().setStim(thisTrial.getTH(), posDM,curStimGroup);
                        
                        #runCoreDMVar.beepCtrl.beep1.play();
                        if flagStim:
                            fixation.stimAttr.stimPos = posDM.phase_fixationpos;
                            trialComponents = [fixation];
                            #trialComponents = [];
                        else:
                            trialComponents = [];
                        pass;
                        thisTrial.getOneTrial().trialComponents = trialComponents;
                        pass;
                    elif defDM.PHASE_Sample == curState.state1:
                        if flagStim:
                            
                            """
                            stimPair = thisTrial.getTH()['stim_shape'];
                            stimPosPair = thisTrial.getTH()['stim_pos'];
                            stimCorrect = thisTrial.getTH()['stim_correctIndex'];
                            
                            stimS = BTTsVisualStim();
                            stimS.stimAttr.flagStimArea = False;
                            stimS.stim = curStimGroup[stimPair[stimCorrect]];
                            stimS.stimAttr.stimName = stimS.stim.attrName;
                            print("modeDelayedMatch.value " + str(param.modeDelayedMatch.value));
                            if param.modeDelayedMatch.value == 0:
                                stimS.stimAttr.stimPos = posDM.phase_choice_stimpos[stimPosPair[stimCorrect]];
                            else:
                                stimS.stimAttr.stimPos = posDM.phase_sample_stim1pos;
                            stimS.prInfo();
                            
                            thisTrial.getOneTrial().curRec.recOneStimCue.setValue(stimS);
                            """
                            
                            trialComponents = [thisTrial.getOneTrial().stimCue];
                            #trialComponents = [stimS];
                        else:
                            trialComponents = [];
                        pass;
                        thisTrial.getOneTrial().trialComponents = trialComponents;
                        pass;
                    elif defDM.PHASE_Delay == curState.state1:
                        if flagStim:
                            fixation2.stimAttr.stimPos = posDM.phase_fixationpos;
                            trialComponents = [fixation2];
                        else:
                            trialComponents = [];
                        pass;
                        thisTrial.getOneTrial().trialComponents = trialComponents;
                        pass;
                    elif defDM.PHASE_Choise == curState.state1:
                        if flagStim:
                            """
                            stimPair = thisTrial.getTH()['stim_shape'];
                            stimPosPair = thisTrial.getTH()['stim_pos'];
                            stimCorrect = thisTrial.getTH()['stim_correctIndex'];
                            
                            stim0 = BTTsVisualStim();
                            stim0.stimAttr.flagStimArea = True;
                            stim0.stim = curStimGroup[stimPair[0]];
                            stim0.stimAttr.stimName = stim0.stim.attrName;
                            
                            stim1 = BTTsVisualStim();
                            stim1.stimAttr.flagStimArea = True;
                            stim1.stim = curStimGroup[stimPair[1]];
                            stim1.stimAttr.stimName = stim1.stim.attrName;
                            
                            stim0.stimAttr.stimPos = posDM.phase_choice_stimpos[stimPosPair[0]];
                            stim1.stimAttr.stimPos = posDM.phase_choice_stimpos[stimPosPair[1]];
    
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
                                thisTrial.getOneTrial().curRec.recOneStimTarget.setValue(stim0);
                                thisTrial.getOneTrial().curRec.recOneStimNonTarget.setValue(stim1);
                            else:
                                thisTrial.getOneTrial().curRec.recOneStimTarget.setValue(stim1);
                                thisTrial.getOneTrial().curRec.recOneStimNonTarget.setValue(stim0);
                            """
                            trialComponents = [thisTrial.getOneTrial().stimT0,thisTrial.getOneTrial().stimT1];
                            #trialComponents = [stim0,stim1];
                        else:
                            trialComponents = [];
                        pass;
                        thisTrial.getOneTrial().trialComponents = trialComponents;
                    elif defDM.PHASE_Punishment == curState.state1:
                        trialComponents = [];
                        thisTrial.getOneTrial().trialComponents = trialComponents;
                        pass;
                    elif defDM.PHASE_PreEnd == curState.state1:
                        trialComponents = [];
                        thisTrial.getOneTrial().trialComponents = trialComponents;
                        pass;
                    elif defDM.PHASE_End == curState.state1:
                        trialComponents = [];
                        thisTrial.getOneTrial().trialComponents = trialComponents;
                        pass;
                    elif defDM.PHASE_End_Mark == curState.state1:
                        print("09 defDM.PHASE_End_Mark and flagStopThread");
                        flagStopThread = True;
                        trialComponents = [];
                        
                    else:
                        trialComponents = [];
                        pass;
                else:
                    trialComponents = [];
                    pass;
                BTTsTool.initComponents(trialComponents);
                pass; # flagState
                #
                if holdState != None:
                    if holdState.checkChange(curState):
                        holdState = curState;
                        flagChange = True;
                else:
                    holdState = curState;
                    flagChange = True;
                pass;
            
            if flagChange:
                oneF.flagTTL = True;
                oneF.resetFF(param.virticalSyncTimestampFrame.value);
                oneF.curRec = thisTrial.getOneTrial().curRec;
                (oneF.flagVSync, oneF.label, oneF.valRecFloat32,oneF.flagAO, oneF.volt) = defDM.infoLabelState_1_2(None,curState,oneF.curRec);
            if flagChange:
                if defDM.PHASE_BeforeTask == curState.state1:
                    if defDM.STATE2_TrialOnT_s == curState.state2:
                        if param.Set_StartBeepOn.value:                    
                            runCoreDMVar.beepCtrl.beep1.play();
                    pass;
                if defDM.PHASE_Choise == curState.state1:
                    if defDM.STATE2_HmReleaseT_s == curState.state2:
                        if param.Set_TargetBeepOn.value:       
                            runCoreDMVar.beepCtrl.beep2.play();
                    pass;
                elif defDM.PHASE_PrePunishment == curState.state1:
                    runCoreDMVar.reward.reward(thisTrial.getOneTrial().correctedOneTrial);
                    pass;
                elif defDM.PHASE_PreEnd == curState.state1:
                    runCoreDMVar.reward.reward(thisTrial.getOneTrial().correctedOneTrial);
                    pass;
                elif defDM.PHASE_End == curState.state1:
                    if not( runCoreDMVar.feeder.isAllready()):
                        numOfFood = int(param.Set_RwdNum.value);
                        microL = param.Set_RwdDrink_microl.value;
                        runCoreDMVar.feeder.initFeeder(thisTrial.getOneTrial().correctedOneTrial,numOfFood, microL);
                pass;
            
            if flagChange:
                flagChange = False;
    
            win.callOnFlip( callbackFlipOneFrameOneF,oneF,runCoreDMVar.ttlAOut);
            
            #print("lopFrame 03");
            for curC in trialComponents:
                curC.stim.pos = curC.stimAttr.stimPos;
                curC.stim.size = curC.stimAttr.stimSize;
                curC.stim._needUpdate = True;
                curC.stim.draw();
                if curC.stimAttr.flagStimArea:
                    pos = curC.stimAttr.stimPos;
                    area = curC.stimAttr.stimAreaSizeForTouch;
                    if param.flagTestModeDisplayInfo.value:
                        runCoreDMVar.drawGL.DrawGLCenterFrame(pos,area);
            # GL draw
            
            if textGL != None:
                tmpStr = "";
                if False:
                    tmpO = thisTrial.getOneTrial();
                    tmpStr += str(tmpO.x_pos);
                    tmpStr += " ";
                    tmpStr += str(tmpO.y_pos);
                else:
                    if curState != None:
                        tmpStr += str(curState.state1);
                        tmpStr += " ";
                        tmpStr += str(curState.state2);
                textGL.text = tmpStr;
                if param.flagTestModeDisplayInfo.value:
                    GL.glColor3f(1.0, 0.0, 1.0)
                    textGL.draw();
            
    
            if flagDrawLT:
                if( param.flagTestModeDisplayInfo.value ):
                    polygonLeftTop.draw();
    
            #
            if runCoreDMVar.ttlReader != None:
                r = runCoreDMVar.ttlReader.readOneShot();
                onerd = r.strip().decode('utf-8');
                #thisTrial.getOneTrial().inputEventTTL(ttlEvent);
                pxx = int(onerd);
                if holdpxx == None:
                    holdpxx = pxx;
                else:
                    if holdpxx != pxx:
                        print(hex(pxx));
                        holdpxx = pxx;
                        pass;
                    else:
                        pass;
            #print("lopFrame 04");
            # keyboard
            flagExitExp = False;
            flagMouseExit = False;
            ptb_keys = runCoreDMVar.kb.getKeys(waitRelease=False); # すべてのキーを受け付ける
            if len(ptb_keys):
                if 'escape' in ptb_keys:
                    print("escape key");
                    flagMouseExit = True;                   
                    flagExitExp = True;
                    pass;
                elif 'return' in ptb_keys: # returnキーが入力されたら、その試行を終了
                    lopFrame.requestFlagLoopOut();
                    flagMouseExit = True;          
                    updateExp = True;
                    pass;
                else:
                    #exp.getTrials().nextResponse();
                    #updateExp = True;
                    pass;
            #
            runCoreDMVar.feeder.feedForFlipLoop(btnB2.flagOn);
            
            if runCoreDMVar.bttsME.winflip():
                flagMouseExit = True;
                flagExitExp = True;
                pass;
            
            if countTrial.SuccessTrialNum < param.numOfTrial.value:
                pass;
            else:
                flagExitExp = True;
                pass;
            
            if flagExitExp:
                flagExitExp = False;
                win.recordFrameIntervals = False
                trc.loopOutThread();
                #tmpOneT = thisTrial.getOneTrial();
                #tmpOneT.breakWaitSecForPhase();
                trc.endThread();
                lopTr.requestFlagLoopOut();
                #lopFrame.requestFlagLoopOut();
                #
                flagStopThread = True;
                #
                updateExp = True; 
                
            #print("lopFrame 05");
            if flagState :
                flagState = False;
                updateExp = True;
            
            if updateExp:
                #同一　trialとする。
                #exp.nextEntry() # ポイント4. ExperimentHandlerの参照点をひとつ進める
                pass;
            
                
            
            if flagTrial:
                flagTrial = False;
    
            #print("lopFrame 06");
            winflip(win,stateBuffer.clock);
            nextFlip = win.getFutureFlipTime(clock='ptb');      
    
            #print("countFrame "+str(countFrame));
            countFrame += 1;
            pass;
            #print("lopFrame end");
        diffCountFrame = 0;
        if holdCountFrame != None:
            diffCountFrame = countFrame - holdCountFrame;
            holdCountFrame = countFrame;
        else:
            holdCountFrame = countFrame;
    
        #print("countFrame " + str(countFrame));
        #print("diffCountFrame " + str(diffCountFrame));
        #print("countTrial " + str(countTrial));
        #print("lopTr end");
        pass;

    win.recordFrameIntervals = False;

    for n in range(10):
        winflip(win,stateBuffer.clock);
    
    if exp.getTrials().flagNext:
        exp.nextEntry(); # for Save Data
    
    print("countFrame " + str(countFrame));
    
    print("last 01");
    trc.endThread();

    print("Last 2nd 02");
    BTTsTool.outputPsydata(exp.exp);
    
    print("Last 2nd 03");
    
    print(exp.getTrials().getResponsesTH());
    print("Last 2nd 04");

    exp.close();
    pass;
    return flagMouseExit;


def main():
    
    param = BTTsParamDM();
    param.screenscale=100;
    
    runCoreDMVar = RunCoreDMVar();
    
    lopTr = LoopFlag();
    lopFrame = LoopFlag();    
    lopTr.init();
    lopFrame.init();
    
    runCoreDMVar.lopTr = lopTr;
    runCoreDMVar.lopFrame = lopFrame;
    
    def handler(signum, frame):
        # signal SIGINT
        print("handle signum "+str(signum));
        lopFrame.requestFlagLoopOut();
        lopTr.requestFlagLoopOut();
    
    #signal.signal(signal.SIGINT, handler);
    signal.signal(signal.SIGBREAK, handler);


    def callbackgc(phase, info):
        tmpTm = logging.defaultClock.getTime();
        pass;
    
    gc.callbacks.append(callbackgc);

    oneTrigger = None;
    if oneTrigger != None:
        oneTrigger.begin();
    
    #if oneTriggerVSync != None:
    #    oneTriggerVSync.begin();
    ttlaout1Param = envHardParam.ttlaout[0];
    if ttlaout1Param.hard_ttlaout_device_use:
        if ttlaout1Param.hard_ttlaout_device_nidaq_use:
            devname = ttlaout1Param.hard_ttlaout_device_devicename;
            devmode = 1 if ttlaout1Param.hard_ttlaout_device_nidaq_ttlony else 0;
            ttlAOut = NIDAQOneShotDAQ(devname,devmode); # TTL/AnalogOut
        else:
            ttlAOut = None;
    else:
        ttlAOut = None;
        
    if ttlAOut != None:
        ttlAOut.begin();
        time.sleep(1.0);
        ttlAOut.writeAO(0,0.0);
    runCoreDMVar.ttlAOut = ttlAOut;
    
    
    #ttlReader = TTLReaderLabHacksBeta('COM3');
    ttlReader = None;
    if ttlReader != None:
        ttlReader.begin();
        print(ttlReader.hello());
    runCoreDMVar.ttlReader = ttlReader;

    # punishment reward
    beepCtrl = BTTsControlBeepDM(soundInfo);
    punishment = BTTsPunishmentDM(param,beepCtrl);
    reward = BTTsRewardDM(param,beepCtrl);
    feeder = BTTsFeederFood(param, envParam);
    
    runCoreDMVar.feeder = feeder;
    runCoreDMVar.beepCtrl = beepCtrl;
    runCoreDMVar.punishment = punishment;
    runCoreDMVar.reward = reward;

    """   
    beepCtrl.beep1.play();
    core.wait(0.8)
    for n in range(3):
        print(str(n));
        core.wait(1.0);
        beepCtrl.beep1.play();
        core.wait(1.0);
        beepCtrl.beep2.play();
        core.wait(1.0);
        beepCtrl.beep3.play();
        core.wait(1.0);
        beepCtrl.beep4.play();
    """
    if feeder != None:
        feeder.begin();
        feeder.clearFeeder();
    if reward != None:
        reward.begin();
        reward.clearRewarded();
    if punishment != None:
        punishment.begin();    
    # window

    if modeApp == -1:
        pass;
    else:
        runOneParamLoadBin(param);
    retDlg = runOneDialog( param,modeApp);

    
    #stim.setColor('Firebrick')#one of the web/X11 color names
    #stim.setColor('#FFFAF0')#an off-white
    #stim.setColor([0,90,1], colorSpace='dkl')#modulate along S-cone axis in isoluminant plane
    #stim.setColor([1,0,0], colorSpace='lms')#modulate only on the L cone
    #stim.setColor([1,1,1], colorSpace='rgb')#all guns to max
    #stim.setColor([1,0,0])#this is ambiguous - you need to specify a color spac
    
    #bgcolor = [0,0,0];
    bgcolor = screen_background_color;
    print(bgcolor);
    
    if flagFullScreen:
        wsize = [xscreensize,yscreensize];
        win = visual.Window(pos=(0,0),size=wsize,winType='pyglet',colorSpace = 'rgb255',color=bgcolor, fullscr=False,allowGUI=False, units='height')
    else:
        wsize = [1024,768];
        win = visual.Window(pos=(10,10),size=wsize,winType='pyglet',colorSpace = 'rgb255',color=bgcolor, fullscr=False, units='height')
        
    print("winType " + str(win.winType));
    print("viewScale "+str(win.viewScale) );
    
    windTitle = "PsychoPy";
    hwndPsychoPy = win32gui.FindWindow(None, windTitle);
    print(hwndPsychoPy);
    runCoreDMVar.hwndPsychoPy;

    if flagDrawMouse:
        win.mouseVisible = True;
    else:
        win.mouseVisible = False;
    win.flip();
    
    #GLtool.init_texture()
    runCoreDMVar.win = win;
    winsize = win.size.tolist();
    runCoreDMVar.drawGL = DrawGL(True, winsize);
    
    flagHookTouch = True;
    #for n in range(60*1):
    #    win.flip()
    if flagHookTouch:
        InstallHookFromWindowTitlePyschopy_PyBTTs();
    #
    
    #print(runCoreDMVar.stimGroupA );
    #for nn in runCoreDMVar.stimGroupA :
    #    nn.prInfo();
    
    textGL = TextOpenGLObj(pos=[0,0]);
    textGL.sizeOfChar = 0.04;
    textGL.setText("98765");
    runCoreDMVar.textGL = textGL;
    
    #
    ms = event.Mouse(win=win);
    ms.clickReset();
    ms.clock = core.Clock();
    ms.lastPosTime = ms.clock.getTime();

    #
    kb = keyboard.Keyboard()
    runCoreDMVar.kb = kb;
    
    msIO = None;
    keyIO = None;
    
    modeMouseIOHUB=2;
    if modeMouseIOHUB == 0:
        pass;
    elif modeMouseIOHUB == 1:
        io = launchHubServer(window=win)
        msIO = io.devices.mouse
        pass;
    elif modeMouseIOHUB == 2:
        io = launchHubServer(window=win,Mouse=dict(enable_multi_window=True))
        msIO = io.devices.mouse
        keyIO = io.devices.keyboard;
        pass;
    runCoreDMVar.msIO = msIO;
    runCoreDMVar.keyIO = keyIO;

    bttsME = BTTsMouseExit(win);
    bttsME.eventMouse = event.Mouse(win=win,visible=False);
    bttsME.reset();
    runCoreDMVar.bttsME = bttsME;


    if retDlg:
        pass;
        flagExpLoop = True;
    else:
        flagExpLoop = False;
        pass;

    expLoopCount = 0;
    while flagExpLoop:
        
        if param.flagRunOneLoopForTest.value:
            retDlg = runOneDialog( param,modeApp);
        else:
            retDlg = True;
        
        if flagDrawMouse:
            win.mouseVisible = True;
        else:
            win.mouseVisible = False;
        win.flip();
        foreground_on(hwndPsychoPy,windTitle )
        
        if retDlg:
            pass;
        else:
            flagExpLoop = False;
            pass;

        if flagExpLoop:
            ## for wait
            if msIO != None:
                msIO.clearEvents();
            if keyIO != None:
                keyIO.clearEvents();
            
            ITIFrame=6;  # 100msec
            nIntervals = param.waitBeforeRun.value * ITIFrame*10; # 6 frame * 10 * 5 = 5 sec
            prelop01 = range(int(nIntervals));
            for frameN in prelop01:
                oneFrameN = frameN % ITIFrame; #
                if( oneFrameN == 0):
                    pass;
                winflip(win,core.Clock());
                nextFlip = win.getFutureFlipTime(clock='ptb');   
            pass;
            # clear event
            if msIO != None:
                msIO.clearEvents();
            if keyIO != None:
                keyIO.clearEvents();
                
            retFlag = runCoreDM(param,runCoreDMVar);
            
            if param.flagRunOneLoopForTest.value:
                pass;
            else:
                flagMELoop = True;            
                while flagMELoop:
                    if bttsME.winflip():
                        flagMELoop = False;
                        flagExpLoop = False;
                    winflip(win,core.Clock());
            
            expLoopCount += 1;
        pass;#
    
    # RemoveHookTouch
    for n in range(60*1):
        win.flip()
    if flagHookTouch:
        RemoveHook_PyBTTs();
    for n in range(60*1):
        win.flip()
    
    print("last 05");
    # 
    if False:
        graphHistVar = GraphHistVar();
        graphHistVar.win = win;
        graphHist(graphHistVar);
    
    
    print("Last 2nd 01");
    win.close()
    
    print("last 02");
    #GLtool.end_texture()
    
    print("last 03");
    
    time.sleep(1.0);
    
    if oneTrigger != None:
        oneTrigger.end();
        del oneTrigger;
        oneTrigger = None;
        
    #if oneTriggerVSync != None:
    #    oneTriggerVSync.end();
    #    del oneTriggerVSync;
    #    oneTriggerVSync = None;
    
    if ttlAOut != None:
        ttlAOut.end();
        del ttlAOut;
        ttlAOut = None;
    
    print("last 04");

    
    if ttlReader != None:
        ttlReader.end();
        del ttlReader;
        ttlReader = None;
    
    if reward != None:
        reward.end();
    if punishment != None:
        punishment.end();
        
    if feeder != None:
        feeder.end();
    
    if bttsNet != None:
        bttsNet.end();
    
    core.quit()
    pass;

if __name__ == "__main__":
    main();


