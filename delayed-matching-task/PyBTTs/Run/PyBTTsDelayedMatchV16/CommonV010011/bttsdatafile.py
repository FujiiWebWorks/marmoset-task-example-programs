# -*- coding: utf-8 -*-

import os  # handy system and path functions
import sys  # to get file system encoding

#from psychopy import sound, gui, visual, core, data, event, logging, clock, colors, layout
from psychopy import core, data, event, logging, clock

class bttsdatafile:
    def __init__(self, curDir):
        self.curDir = curDir;
        self.filename = None;
        pass;

    def create(self,_machineNo, _expName):
        _dateStr = data.getDateStr();
        #self.filename = "mini01_exp_results";
        self.filename = self.curDir + os.sep + u'data/%s_%s_%s' % (str(_machineNo), _expName, _dateStr)
        pass;
    def getFilename(self):
        return self.filename;

def testMain():
    
    _thisDir = os.path.dirname(os.path.abspath(__file__))
    print(_thisDir);
    os.chdir(_thisDir)
    
    bdf = bttsdatafile(_thisDir);
    bdf.create(1,"expTest");
    print(bdf.getFilename());


if __name__ == "__main__":
    testMain();
