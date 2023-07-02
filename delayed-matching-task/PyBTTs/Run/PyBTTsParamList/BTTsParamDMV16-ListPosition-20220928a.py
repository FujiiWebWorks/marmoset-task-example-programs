#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

folderName = "PyBTTsDelayedMatchV16";
sys.path.append("../"+folderName);
sys.path.append("../"+folderName+"/CommonV010011");

from bttsRemoteOne import remoteOne,runOne,runOneParamSaveBin,runOneParamLoadBin
from bttsDialog import DlgTT,relayout3,genExpInfo
from bttsTrialDM import BTTsParamDM

def main01(args):
    modeApp = 0;
    sz = len(args);
    if sz == 1:
        pass;
    else:
        modeApp = int( args[1] );
    
    curParam = BTTsParamDM();
    curParam.currentDirectory = folderName;
    curParam.filename = "BTTs16DMExtraStateDelayTTLLoop.py";
    #
    curParam.waitBeforeRun.setValue(5);
    curParam.Set_HmHold2Dur.setValue(2000.0);
    #
    curParam.modeDelayedMatch.setValue(0); # 0:ポジション  1:形/色 
    curParam.modeOption.setValue(0);
    curParam.stim_list.setValue([[0,1,2,3,4,5,6,7,8]]); # listPosition

    if modeApp == 0:
        runOne(curParam,modeApp);
        pass;
    elif modeApp == 1:
        pass;
    elif modeApp == 2:
        remoteOne(curParam,modeApp);
        pass;
    else:
        pass;


def testParam():
    from bttsNet import sendToForList, recvFromForList
    import struct
    import binascii
    import ctypes
    
    p01 = BTTsParamDM();
    p01.delayTimeMSec.setValue([999,888,77.0]);
    
    bin01 = sendToForList(p01.paramList);
    
    p02 = BTTsParamDM();
    recvFromForList(p02.paramList,bin01);
    p02.printParamList();

def testParamSave():

    p01 = BTTsParamDM();
    p01.printParamList();

    runOneParamSaveBin(p01);

    p02 = BTTsParamDM();
    runOneParamLoadBin(p02);
    p02.printParamList();

def testParamDlg():
    
    p01 = BTTsParamDM();
    p01.currentDirectory = folderName;
    p01.filename = "BTTs16DMExtraStateDelayTTLLoop.py";
    p01.printParamList();
    remoteOne(p01,-1);
    p01.printParamList();
    
    pass;

if __name__ == "__main__":
    argv = sys.argv
    #testParamDlg();
    #testParam();
    #testParamSave();
    main01(argv);
