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
import os  # handy system and path functions
import sys  # to get file system encoding
import time
import socket
import select
import threading

from PyQt5.QtCore  import QObject

from psychopy.localization import _translate

from bttsDialog import DlgTT,relayout3,genExpInfo
from bttsNet import BTTsNetClient,BTTsNetClientCmd
from bttsEnv import BTTsEnv;
from bttsEnvDefine import BTTsEnvDefine

class BTTsRemoteOneDefine:
    def __init__(self):
        self.modeAPP_runOne = 0;
        self.modeAPP_clinet = 1;
        self.modeAPP_server = 2;
        pass;

defRemoteOneDefine = BTTsRemoteOneDefine();

class RemoteOneOldHold:
    def __init__(self):
        self.flagBegin = False;
        pass;
    def begin(self):
        # Serverのアドレスを用意。Serverのアドレスは確認しておく必要がある。
        self.serv_address = ('127.0.0.1', 8890)
        #self.serv_address = ('192.168.50.236', 8890)
        # ①ソケットを作成する
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.flagBegin = True;
    def end(self):
        print('closing socket')
        self.sock.close();
        self.flagBegin = False;
        print('done')
    def isBegin(self):
        pass;
        return self.flagBegin;
    def sendCmdAA(self, _msg):
        send_len = self.sock.sendto(_msg.encode('utf-8'), self.serv_address)

class RemoteOne:
    def __init__(self):
        self.flagBegin = False;
        self.bttsNetClient = BTTsNetClientCmd();
        pass;
    def begin(self):
        #self.serv_address = ('127.0.0.1', 8890)
        #self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.bttsNetClient.begin();
        self.flagBegin = True;
    def end(self):
        print('closing socket')
        self.sock.close();
        self.flagBegin = False;
        print('done')
    def isBegin(self):
        pass;
        return self.flagBegin;
    def sendCmdAA(self, _msg):
        bin1 = _msg.encode('utf-8');
        self.bttsNetClient.sendToBin(bin1);
    def reciveStatus(self):
        recvLen = 1200;
        bin1 = self.bttsNetClient.recvFromBin(recvLen);
        if bin1 != None:
            print(type(bin1));
            sz = len(bin1);
            print("reciveStatus size = " + str(sz));
            print(self.bttsNetClient.getRecvClient())
            if sz == recvLen:
                print("reciveStatus " + str(bin1[0]));
                print("reciveStatus " + str(bin1[1]));
            else:
                print("reciveStatus bin1 not 1200");
                pass;
        else:
            print("reciveStatus bin1 is None");
            pass;



class ROTh(QObject):
    def __init__(self):
        print(Qt);
        print(QObject);
        #Qt.QObject
        self.bttsNetClient = BTTsNetClient();
        self.dlg = None;
        self.param = None;
        self.flagRecv = False;
        pass;
    def begin(self):
        self.bttsNetClient.begin();
        self.client_thread_state = 1    # start thread in wait mode
        self.client_thread_running = True
        self.client_thread = threading.Thread(target=self._client_thread)
        self.client_thread.start()
        
        pass;
    def end(self):
        # stop acquisition
        #self.stopClient()
        # close socket
        if self.client_thread != None:
            self.client_thread_running = False
            self.client_thread.join(5.0)
            self.client_thread = None
        self.bttsNetClient.end();
        pass;
    def resetFlagRecv(self):
        self.flagRecv = False;
    def isBegin(self):
        retFlag = False;
        if self.bttsNetClient != None:
            retFlag = self.bttsNetClient.isBegin();
        else:
            retFlag = False;
        return retFlag;
    def _client_thread(self):
        ''' Client socket connection thread
        '''
        print("_client_thread 01");
        readheader = True
        requested = 24
        received = 0
        while self.client_thread_running:
            # idle mode
            if self.client_thread_state == 0: 
                time.sleep(0.2)
                self.client_thread_state = 1;
            elif self.client_thread_state == 1:
                # look for data
                rd, wr, err = select.select([self.bttsNetClient.sock],[],[self.bttsNetClient.sock], 0.05)
                if len(err) > 0:
                    # socket error
                    print("socket select error");
                    #msg.Type = RDAMessageType.DISCONNECTED
                    #self.emit(Qt.SIGNAL('clientMsg(PyQt_PyObject)'), msg)   # disconnected
                    self.client_thread_state = 0;
                elif len(rd) > 0:
                    print("select rd "+str(rd));
                    for soc in rd:
                        if soc != self.bttsNetClient.sock:
                            # other
                            pass;
                        else:
                            self.bttsNetClient.recvFromForValue(self.param);
                            print(self.bttsNetClient.cli_addr);
                            self.flagRecv = True;
                            print("recv");
                            #self.param.printValueList();
                            #print( self.dlg );
                            msg = "msg";
                            #self.dlg.emit(Qt.SIGNAL('clientMsg(PyQt_PyObject)'), msg)   # connected
                            
                    pass;
                else:
                    pass;
                pass;
            else:
                pass;
        pass;
        print("_client_thread end");

class DlgTTNet(DlgTT):
    def __init__(self, dictionary, title='', fixed=None, order=None,
        tip=None, screen=-1, sortKeys=True, copyDict=False,
        labels=None, show=False,
        sort_keys=None, copy_dict=None):
        super().__init__(dictionary, title=title, fixed=fixed, order=order,tip=tip, screen=screen, sortKeys=sortKeys, copyDict=copyDict,labels=labels, show=show,sort_keys=sort_keys, copy_dict=copy_dict);
        #
        self.ro = None;
        self.remoteParam = None;
        self.param = None;
        self.modeApp = None;
        
        self.okbutton.clicked.connect(self.callbackOk)
        self.cancelbutton.clicked.connect(self.callbackCancel)        
        pass;
    def updateButtonBox2(self):
        self.buttonBox2 = QtWidgets.QDialogButtonBox(Qt.Horizontal,parent=self)
        
        self.startButton = QtWidgets.QPushButton(_translate("start task"),parent=self);
        self.buttonBox2.addButton(self.startButton,QtWidgets.QDialogButtonBox.ActionRole);
        self.startButton.clicked.connect(self.callbackStartTask);

        self.breakButton = QtWidgets.QPushButton(_translate("break task"),parent=self);
        self.buttonBox2.addButton(self.breakButton,QtWidgets.QDialogButtonBox.ActionRole);
        self.breakButton.clicked.connect(self.callbackBreakTask);

        self.connectButton = QtWidgets.QPushButton(_translate("conn"),parent=self);
        self.buttonBox2.addButton(self.connectButton,QtWidgets.QDialogButtonBox.ActionRole);
        self.connectButton.clicked.connect(self.callbackConnect);

        self.disconnectButton = QtWidgets.QPushButton(_translate("disconn"),parent=self);
        self.buttonBox2.addButton(self.disconnectButton,QtWidgets.QDialogButtonBox.ActionRole);
        self.disconnectButton.clicked.connect(self.callbackDisconnect);
        
        self.layout.addWidget(self.buttonBox2, self.irow, 0, 1, 2);
        self.irow += 1;
        
        if self.modeApp != None:
            if self.modeApp == defRemoteOneDefine.modeAPP_runOne:
                # mode RunOne
                self.breakButton.setEnabled(False);
                self.connectButton.setEnabled(False);
                self.disconnectButton.setEnabled(False);
                self.updatebutton.setEnabled(False);
                self.updateInfobutton.setEnabled(False);
                self.startButton.setEnabled(False);
                pass;
            elif self.modeApp == defRemoteOneDefine.modeAPP_clinet:
                # mode clinet
                pass;
            elif self.modeApp == defRemoteOneDefine.modeAPP_server:
                # mode server
                self.breakButton.setEnabled(False);
                self.connectButton.setEnabled(False);
                self.disconnectButton.setEnabled(False);
                self.updatebutton.setEnabled(False);
                self.updateInfobutton.setEnabled(False);
                self.startButton.setEnabled(True);
                pass;
            else:
                pass;
        
        pass;
    def setParam(self, _param):
        self.param = _param;
        pass;
    def callbackOk(self):
        if self.modeApp != None:
            if self.modeApp == -1:
                self.updateInfoInner();
                self.updateToParamInner();
            elif self.modeApp == defRemoteOneDefine.modeAPP_runOne:
                self.updateInfoInner();
                self.updateToParamInner();
                pass;
            elif self.modeApp == defRemoteOneDefine.modeAPP_clinet:
                pass;
            elif self.modeApp == defRemoteOneDefine.modeAPP_server:
                self.disconnectNet();
                self.accept();
                pass;
            else:
                pass;
        pass;
    def callbackCancel(self):
        if self.modeApp != None:
            if self.modeApp == defRemoteOneDefine.modeAPP_runOne:
                pass;
            elif self.modeApp == defRemoteOneDefine.modeAPP_clinet:
                pass;
            elif self.modeApp == defRemoteOneDefine.modeAPP_server:
                self.disconnectNet();
                self.reject();
                pass;
            else:
                pass;
        print("callbackCancel");
        pass;
    def getParamFromParamList(self,label):
        retParam = None;
        for val in self.param.paramList:
            if val.vname != None:
                if val.vname == label:
                    retParam = val;
                    break;
        pass;
        return retParam;
    def updateToParamInner(self):
        for n, thisKey in enumerate(self._keys):
            if thisKey in self._labels:
                labelKey = self._labels[thisKey]
            else:
                labelKey = thisKey
            value = self.getParamFromParamList(labelKey);
            if value != None:
                value.setValueGUI( self.dictionary[thisKey]);
                #print(value.toKeyValue())
            pass;
    def callbackUpdateInfo(self):
        print("callbackUpdateInfo DlgTTNet");
        ######self.remoteParam.recvFromForValue(self.param);
        print(str(self.param.nFrame.value));
        self.updateInfoInner();
    def callbackUpdate(self):
        print("callbackUpdate DlgTTNet");
        self.updateInfoInner();
        self.updateToParamInner();
        if self.remoteParam != None:
            print("callbackUpdate p01");
            self.param.printParamList();
            self.remoteParam.bttsNetClient.sendToForParam(self.param);
            self.param.printParamList();
            print("callbackUpdate p02");
        
        pass;
    def callbackStartTask(self):
        if self.modeApp != None:
            if self.modeApp == defRemoteOneDefine.modeAPP_runOne:
                pass;
            elif self.modeApp == defRemoteOneDefine.modeAPP_clinet:
                pass;
            elif self.modeApp == defRemoteOneDefine.modeAPP_server:
                self.connectNet();
                time.sleep(0.3);
                pass;
            else:
                pass;
        
        print("callbackStartTask sendCmdAA 01");
        cmdStr = "run python";
        cmdStr += ",";
        cmdStr += self.param.currentDirectory;
        cmdStr += ",";
        cmdStr += self.param.filename;
        self.ro.sendCmdAA(cmdStr);
        time.sleep(1.0);
        
        for n in range(5):
            cmdStr = "get status";
            self.ro.sendCmdAA(cmdStr);
            time.sleep(0.5);
            self.ro.reciveStatus();
            time.sleep(0.5);
            
        print("callbackStartTask sendCmdAA end");
        
        #
        if self.modeApp != None:
            if self.modeApp == defRemoteOneDefine.modeAPP_runOne:
                pass;
            elif self.modeApp == defRemoteOneDefine.modeAPP_clinet:
                pass;
            elif self.modeApp == defRemoteOneDefine.modeAPP_server:
                time.sleep(15.0);
                self.updateInfoInner();
                self.updateToParamInner();
                print("callbackStartTask sendToForParam 01");
                self.remoteParam.bttsNetClient.sendToForParam(self.param);
                time.sleep(0.3);
                self.remoteParam.end();
                print("callbackStartTask sendToForParam end");
                pass;
            else:
                pass;
        
        if self.modeApp != None:
            if self.modeApp == defRemoteOneDefine.modeAPP_runOne:
                pass;
            elif self.modeApp == defRemoteOneDefine.modeAPP_clinet:
                pass;
            elif self.modeApp == defRemoteOneDefine.modeAPP_server:
                print("callbackStartTask accept()" );
                #exit(-1);
                self.accept();
                #QCoreApplication .quit()
                #exit(-1);        
                #QCoreApplication.quit()
                print("callbackStartTask accept end" );
                pass;
            else:
                pass;
        pass;
    def callbackBreakTask(self):
        print("callbackBreakTask DlgTTNet");
        cmdStr = "kill run";
        self.ro.sendCmdAA(cmdStr);
        pass;
    def callbackConnect(self):
        print("callbackConnect DlgTTNet");
        self.connectNet();
        pass;
    def connectNet(self):
        if self.ro != None:
            pass;
        else:
            self.ro = RemoteOne();
            self.ro.begin();
            self.remoteParam = ROTh();
            self.remoteParam.dlg = self;
            self.remoteParam.param =  self.param
            self.remoteParam.begin();
        pass;
        pass;
    def disconnectNet(self):
        if self.ro != None:
            if self.ro.isBegin():
                self.ro.end();
        if self.remoteParam != None:
            if self.remoteParam.isBegin():
                self.remoteParam.end();
        self.ro = None;
        self.remoteParam = None;
        
    def callbackDisconnect(self):
        print("callbackDisconnect DlgTTNet");
        self.disconnectNet();
        pass;



def remoteOne(param,modeApp):
    expName = param.filename; # from the Builder filename that created this script
    expInfo = genExpInfo(param.paramList,param.valueList);
    fixedList = [];
    
    # --- Show participant info dialog --
    dlg = DlgTTNet(dictionary=expInfo, sortKeys=False, title=expName, fixed=fixedList);
    relayout3(dlg.layout);
    dlg.modeApp = modeApp;
    dlg.updateButtonBox2();
    dlg.setParam(param);
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

def runOneParamLoadBin(param):
    env = BTTsEnv();
    bttsDefine = BTTsEnvDefine();

    oneFilename = env.homePyBTTsVarFolder + "//OneParam" + ".dat";
    
    f = open(oneFilename,'rb');
    bin01 = f.read(bttsDefine.sizeBinaryOnePacket);
    f.close();

    offsetR = 0;
    for val in param.paramList:
        print(val.vname);
        print(val.value);
        rOneLen = val.readByteArray(bin01,offsetR);
        offsetR += rOneLen;
    pass;
    
def runOneParamSaveBin(param):
    env = BTTsEnv();
    bttsDefine = BTTsEnvDefine();

    bin01 = bytearray(bttsDefine.sizeBinaryOnePacket);
    offsetW = 0;
    for val in param.paramList:
        print(val.vname);
        print(val.value);
        wOneLen = val.writeByteArray(bin01,offsetW);
        offsetW += wOneLen;
    
    oneFilename = env.homePyBTTsVarFolder + "//OneParam";
    
    f = open(oneFilename + '.dat', 'wb');
    f.write(bin01);
    f.close();
    
    pass

def runOneDialog(param,modeApp):
    retB = False;
    
    expName = param.filename; # from the Builder filename that created this script
    expInfo = genExpInfo(param.paramList,param.valueList);
    fixedList = [];
    
    # --- Show participant info dialog --
    dlg = DlgTTNet(dictionary=expInfo, sortKeys=False, title=expName, fixed=fixedList);
    relayout3(dlg.layout);
    dlg.modeApp = modeApp;
    dlg.updateButtonBox2();
    dlg.setParam(param);
    dlg.show();
    if dlg.OK == False:
        #core.quit()  # user pressed cancel
        retB = False;
        pass;
    else:
        retB = True;
        pass;
    return retB;

def runOne(param,modeApp):
    from importlib import import_module    
    import pathlib
    pass;

    runOneParamSaveBin(param);

    expName = param.filename; # from the Builder filename that created this script
    expInfo = genExpInfo(param.paramList,param.valueList);

    exp_p_file = pathlib.Path(expName);
    if param.isMainFunction:
        modulepy = import_module(exp_p_file.stem);
        modulepy.main();
        
        #mainFunction = getattr(modulepy, "main");
        #mainFunction(param);
    else:
        modulepy = import_module(exp_p_file.stem);
    pass;
        


def testMain():
    #testDialog01();
    pass;

if __name__ == "__main__":
    testMain();

