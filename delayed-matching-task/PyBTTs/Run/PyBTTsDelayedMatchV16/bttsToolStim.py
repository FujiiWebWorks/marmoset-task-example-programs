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
import signal
import gc

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle, choice as randchoice
import csv
import pyglet
import pyglet.gl as GL
from pyglet import gl

visual.useFBO = True  # if available (try without for comparison)
import matplotlib
matplotlib.use('Qt5Agg')  # change this to control the plotting 'back end'
import pylab

#example
# from bttsToolStim import WinFlip, callbackFrameTTOneFrame, OneFrame

class WinFlip():
    def __init__(self,_win, _clock):
        self.win = _win;
        self.clock = _clock;
        self.holdFlipTm=None;
    def flip(self):
        self.win.flip();
        tmpTm = self.clock.getTime();
        if self.holdFlipTm != None:
            diffTm = tmpTm - self.holdFlipTm;
            if( 0.040 < diffTm ):
                print("TIME-WinFlip-40-Over\t"+str(diffTm)+" "+str(tmpTm));
                pass;
            else:
                pass;
            pass;
        else:
            pass;
        self.holdFlipTm = tmpTm;
        #print("TIME-WinFlip\t"+str(tmpTm));
        pass;

def callbackFrameTTOneFrame(_portA, _valA, _portB, _valB,_oneF,frame):
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

class OneFrame:
    def __init__(self):
        self.flagTTL = False;
        self.countFrame = -1;
        pass;


