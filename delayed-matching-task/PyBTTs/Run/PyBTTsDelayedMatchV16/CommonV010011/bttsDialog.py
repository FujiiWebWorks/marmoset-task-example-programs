# -*- coding: utf-8 -*-

haveQt = False  # until we confirm otherwise
importOrder = ['PyQt5', 'PyQt4']

for libname in importOrder:
    try:
        exec("import {}".format(libname))
        haveQt = libname
        break
    except ImportError:
        pass

if not haveQt:
    # do the main import again not in a try...except to recreate error
    exec("import {}".format(importOrder[0]))
elif haveQt == 'PyQt5':
    from PyQt5 import QtWidgets
    from PyQt5 import QtGui
    from PyQt5.QtCore import Qt
else:
    from PyQt4 import QtGui  
    QtWidgets = QtGui  # in qt4 these were all in one package
    from PyQt4.QtCore import Qt

from psychopy import gui, visual, core, data, event, logging, clock, colors, layout

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle, choice as randchoice
import os  # handy system and path functions
import sys  # to get file system encoding

from psychopy.localization import _translate


class DlgTT(gui.DlgFromDict):
    def __init__(self, dictionary, title='', fixed=None, order=None,
        tip=None, screen=-1, sortKeys=True, copyDict=False,
        labels=None, show=False,
        sort_keys=None, copy_dict=None):
        super().__init__(dictionary, title=title, fixed=fixed, order=order,tip=tip, screen=screen, sortKeys=sortKeys, copyDict=copyDict,labels=labels, show=show,sort_keys=sort_keys, copy_dict=copy_dict);
        print(super())
        # show is false
        self.updateInfobutton = QtWidgets.QPushButton(_translate("update info"),parent=self);
        self.buttonBox.addButton(self.updateInfobutton,QtWidgets.QDialogButtonBox.ActionRole);
        self.updateInfobutton.clicked.connect(self.callbackUpdateInfo);
        #
        self.updatebutton = QtWidgets.QPushButton(_translate("update"),parent=self);
        self.buttonBox.addButton(self.updatebutton,QtWidgets.QDialogButtonBox.ActionRole);
        self.updatebutton.clicked.connect(self.callbackUpdate);
        #self.okbutton.clicked.disconnect();
        #self.okbutton.clicked.connect(self.callbackOK)
        #
        #self.okbutton.clicked.connect(self.callbackOk)
        #self.cancelbutton.clicked.connect(self.callbackCancel)        
        pass;
    def callbackUpdateInfo(self):
        print("calllbackOK");
        print(self.dictionary);
        self.updateInfoInner();
        print(self.dictionary);
    def callbackUpdate(self):
        pass;
    def updateInfoInner(self):
        for n, thisKey in enumerate(self._keys):
            if thisKey in self._labels:
                labelKey = self._labels[thisKey]
            else:
                labelKey = thisKey
            try:
                self.dictionary[thisKey] = self.inputFieldTypes[labelKey](self.data[n])
                print(thisKey);
                print(self.dictionary[thisKey]);
            except ValueError:
                self.dictionary[thisKey] = self.data[n]

def testDialog01():
    expName = 'bttsDialogTest'  # from the Builder filename that created this script
    
    expInfo = {
        'participant': f"{randint(0, 999999):06.0f}",
        'session': '001',
    }
    # --- Show participant info dialog --
    dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
    
    if dlg.OK == False:
        core.quit()  # user pressed cancel
    ##expInfo['date'] = data.getDateStr()  # add a simple timestamp
    expInfo['expName'] = expName
    ##expInfo['psychopyVersion'] = psychopyVersion

def relayout3(_lay):
    print(_lay);
    
    lst = [];
    
    sz = _lay.count();
    
    for n in range(int(sz/2)):
        lst.append( (_lay.itemAt( n * 2 + 0), _lay.itemAt( n * 2 + 1)));
    
    sz = len(lst);
    for ct in range(sz):
        cur = lst[ct];
        _lay.removeItem(cur[0]);
        _lay.removeItem(cur[1]);
    
    indexLay = 12;
    for ct in range(sz):
        cur = lst[ct];
        
        #_lay.removeItem(cur[0]);
        #_lay.removeItem(cur[1]);
        #
        y = ct % indexLay ;
        x = ct // indexLay;
        
        _lay.addWidget(cur[0].widget(), y, (x*2+0)); 
        _lay.addWidget(cur[1].widget(), y, (x*2+1)); 
        
    
    #obj01WI = _lay.itemAt(0);
    #print (ct);
    #print(type(obj01WI));
    #print(obj01WI);
    #obj01W = obj01WI.widget();
    #_lay.removeItem(obj01WI);
    #_lay.addWidget( obj01W, 0,2);

def genExpInfoHold(paramList,valueList=None):
    # paramList Object example [ValueInt]
    expInfo = dict();
    sz = len(paramList);
    for n in range(int(sz)):
        cur = paramList[n].toKeyValue();
        expInfo.update(cur);
    if valueList != None:
        sz = len(valueList);
        for n in range(int(sz)):
            cur = valueList[n].toKeyValue();
            expInfo.update(cur);
    return expInfo;
def genExpInfo(paramList,valueList=None):
    # paramList Object example [ValueInt]
    expInfo = dict();
    sz = len(paramList);
    for n in range(int(sz)):
        cur = paramList[n].toKeyValue();
        expInfo.update(cur);
    if valueList != None:
        sz = len(valueList);
        for n in range(int(sz)):
            cur = valueList[n].toKeyValue();
            expInfo.update(cur);
    return expInfo;

    
def testDialog02():
    expName = 'bttsDialogTest'  # from the Builder filename that created this script
    
    expInfo = {
        'participant': f"{randint(0, 999999):06.0f}",
        'session': '222',
        'param1': '001',
        'param2': '001',
        'param3': '001',
        'param4': '001',
        'param5': 5,
        'param6': 6,
        'param7': True,
        'param8': False,
        'param9': 9,
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

def testDialog03():
    from bttsTrialDM import BTTsParamDM
    
    param = BTTsParamDM();
    expName = 'bttsDialogTest'  # from the Builder filename that created this script
    
    expInfo = dict();
    sz = len(param.paramList);
    for n in range(int(sz)):
        cur = param.paramList[n].toKeyValue();
        expInfo.update(cur);
    print(expInfo);
    
    xexpInfo = {
        'participant': f"{randint(0, 999999):06.0f}",
        'session': '222',
        'param1': '001',
        'param2': '001',
        'param3': '001',
        'param4': '001',
        'param5': 9,
        'param6': 9,
        'param7': True,
        'param8': False,
        'param9': 9,
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
