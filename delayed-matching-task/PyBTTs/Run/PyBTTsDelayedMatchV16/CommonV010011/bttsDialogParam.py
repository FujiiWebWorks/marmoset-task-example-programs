from psychopy import gui, visual, core, data, event, logging, clock, colors, layout

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle, choice as randchoice
import os  # handy system and path functions
import sys  # to get file system encoding

from bttsDialog import DlgTT,relayout3,genExpInfo


def testDialog03():
    from bttsTrialDM import BTTsParamDM
    
    expName = 'bttsDialogTest'  # from the Builder filename that created this script
    
    param01 = BTTsParamDM();
    param01.Set_CurDur.value = 33.0;
    param01.Set_RewardSoundOn.value = True;
    
    bin01 = bytearray(1200);
    sz = len(param01.paramList);
    ofs = 0;
    for n in range(sz):
        szCur = param01.paramList[n].writeByteArray(bin01,ofs);
        ofs += szCur;
        print(ofs);
    
    param02 = BTTsParamDM();
    sz = len(param02.paramList);
    ofs = 0;
    for n in range(sz):
        szCur = param02.paramList[n].readByteArray(bin01,ofs);
        ofs += szCur;
        print(ofs);

    param = param02;
    sz = len(param.paramList);
    print(sz);
    for n in range( sz ):
        print(param.paramList[n]);
        val = getattr(param,param.paramList[n].vname);
        print(val);
    

    expInfo = genExpInfo(param01.paramList);
    print(expInfo);
    expInfo = genExpInfo(param.paramList);
    print(expInfo);
    """
    expInfo = {
        'participant': f"{randint(0, 999999):06.0f}",
        'session': '222',
        'param1': '001',
        'param2': '001',
        'param3': '001',
        'param4': '001',
        'param5': '001',
        'param6': '001',
    }
    """
    fixedList = ['param1'];

    # --- Show participant info dialog --
    dlg = DlgTT(dictionary=expInfo, sortKeys=False, title=expName, fixed=fixedList);

    relayout3(dlg.layout);

    dlg.show();
    if dlg.OK == False:
        #core.quit()  # user pressed cancel
        pass;
    print(expInfo);
    ##expInfo['date'] = data.getDateStr()  # add a simple timestamp
    expInfo['expName'] = expName
    ##expInfo['psychopyVersion'] = psychopyVersion
    print(expInfo);
    
    pass;

def testDialog02():
    expName = 'bttsDialogTest'  # from the Builder filename that created this script
    
    expInfo = {
        'participant': f"{randint(0, 999999):06.0f}",
        'session': '222',
        'param1': '001',
        'param2': '001',
        'param3': '001',
        'param4': '001',
        'param5': '001',
        'param6': '001',
    }
    
    fixedList = ['param1'];
    
    # --- Show participant info dialog --
    dlg = DlgTT(dictionary=expInfo, sortKeys=False, title=expName, fixed=fixedList);

    relayout3(dlg.layout);

    dlg.show();
    if dlg.OK == False:
        #core.quit()  # user pressed cancel
        pass;
    print(expInfo);
    ##expInfo['date'] = data.getDateStr()  # add a simple timestamp
    expInfo['expName'] = expName
    ##expInfo['psychopyVersion'] = psychopyVersion
    print(expInfo);
    
    pass;

def testMain():
    testDialog03();
    pass;

if __name__ == "__main__":
    testMain();

