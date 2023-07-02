# -*- coding: utf-8 -*-

import os  # handy system and path functions
import sys  # to get file system encoding
import time
import socket


class BTTsNetBase:
    def __init__(self, _serverPort, _clientPort):
        self.serverPort = _serverPort;
        self.clientPort = _clientPort;
        self.flagServer = False;
        self.flagBegin = False;
        self.timeOutVlaue = 60*60*24*7;
    def begin(self):
        print("BTTsNet begin 01");
        # Serverのアドレスを用意。Serverのアドレスは確認しておく必要がある。
            
        self.server_address = ('127.0.0.1', self.serverPort)
        self.client_address = ('127.0.0.1', self.clientPort)
        #self.serv_address = ('192.168.50.236', 8892)
        # ①ソケットを作成する
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
        tm = self.sock.gettimeout();
        print(tm);
        self.sock.settimeout(60*60*24*7); # 15552000:6 month sec
        tm = self.sock.gettimeout();
        print(tm);
        if self.flagServer:
            self.sock.bind(self.server_address);
            pass;
        else:
            ## self.sock.bind(self.client_address)
            pass;
        pass;
        self.flagBegin = True;
        print("BTTsNet begin end");
    def end(self):
        print('closing socket')
        self.sock.close()
        self.flagBegin = False;
        print('done')
    def isBegin(self):
        return self.flagBegin;
    def setBlocking(self,_val):
        #sock.setblocking(True) は sock.settimeout(None) と等価です
        #sock.setblocking(False) は sock.settimeout(0.0) と等価です
        if _val :
            #self.sock.settimeout(self.timeOutVlaue); # blocking
            self.sock.setblocking(1); # blocking
        else:
            #self.sock.settimeout(0.0);
            self.sock.setblocking(0);
        pass;
    def sendToBin(self, _bin1Array):
        pass;
    def recvFromBin(self,_sz):
        pass;
        return None;
    
class BTTsNetCmd(BTTsNetBase):
    def __init__(self):
        super().__init__(8890,8891); # for command;
        pass;

class BTTsNetParam(BTTsNetBase):
    def __init__(self):
        super().__init__(8892,8893); # for param;
        pass;
    def sendToForList(self,_list):
        bin01 = bytearray(1200);
        sz = len(_list);
        print(sz);
        ofs = 0;
        for n in range(sz):
            szCur = _list[n].writeByteArray(bin01,ofs);
            ofs += szCur;
            print(ofs);
        self.sendToBin(bin01);
    def sendToForValue(self,_param):
        print("sendToForValue 01");
        self.sendToForList(_param.valueList);
        print("sendToForValue end");
        pass;
    def sendToForParam(self,_param):
        self.sendToForList(_param.paramList);
    
    def recvFromForList(self,_list):
        print("recvFromForList 01");
        binLen = 1200;
        #bin01 = bytearray(binLen);
        print("recvFromForList 02");
        bin01 = self.recvFromBin(binLen);
        if bin01 != None:
            retLen = len(bin01);
        else:
            retLen = 0;
        print("recvFromForList 03 " + str(retLen));
        if retLen == binLen:
            sz = len(_list);
            ofs = 0;
            for n in range(sz):
                szCur = _list[n].readByteArray(bin01,ofs);
                ofs += szCur;
                print(ofs);
        print("recvFromForList end");
        pass;
        return retLen;
    def recvFromForParam(self,_param):
        print("recvFromForParam 01");
        self.recvFromForList(_param.paramList);
        _param.printParamList();
        print("recvFromForParam end");
    def recvFromForValue(self,_param):
        print("recvFromForValue 01");
        self.recvFromForList(_param.valueList);
        print("recvFromForValue end");

class BTTsNetClient(BTTsNetParam):
    def __init__(self):
        super().__init__();
        self.flagServer = False;
        self.cli_addr = None;
        pass;
    def sendToBin(self, _bin1Array):
        print("BTTsNetClient sendToBin 01");
        #send_len = self.sock.sendto(_bin1Array, self.cli_addr);
        send_len = self.sock.sendto(_bin1Array, self.server_address);
        print(self.server_address);
        print("BTTsNetClient sendToBin end");
    def recvFromBin(self,_sz):
        print("BTTsNetClient recvFromBin 01");
        bin01 = None;
        try:
            (bin01, self.cli_addr) = self.sock.recvfrom(_sz);
            tmpS = str(self.cli_addr);
            print("BTTsNetClient recvFromBin " + tmpS);
            if bin01 != None:
                pass;
        except Exception as e:
            en = e.args[0]
            if en == 10035:
                print("10035")
                #time.sleep(0.1)
            elif en == 11:
                print("11")
                #time.sleep(0.1)
        print("BTTsNetClient recvFromBin end");
        return bin01;


class BTTsNetServer(BTTsNetParam):
    def __init__(self):
        super().__init__();
        self.flagServer = True;
        self.cli_addr = None;
        pass;
    def sendToBin(self, _bin1Array):
        print("BTTsNetServer sendToBin 01");
        send_len = self.sock.sendto(_bin1Array, self.cli_addr);
        print(self.cli_addr);
        print("BTTsNetServer sendToBin end");
    def recvFromBin(self,_sz):
        print("BTTsNetServer recvFromBin 01");
        bin01 = None;
        try:
            (bin01, self.cli_addr) = self.sock.recvfrom(_sz);
            tmpS = str(self.cli_addr);
            print("BTTsNetServer recvFromBin " + tmpS);
            print("BTTsNetServer recvFromBin len " + str(len(bin01) ));
        except Exception as e:
            en = e.args[0]
            if en == 10035:
                print("10035")
                #time.sleep(0.1)
            elif en == 11:
                print("11")
                #time.sleep(0.1)
        print("BTTsNetServer recvFromBin end");
        return bin01;

class BTTsNetClientCmd(BTTsNetCmd):
    def __init__(self):
        super().__init__();
        self.flagServer = False;
        self.cli_addr = None;
        pass;
    def sendToBin(self, _bin1Array):
        print("BTTsNetClient sendToBin 01");
        #send_len = self.sock.sendto(_bin1Array, self.cli_addr);
        send_len = self.sock.sendto(_bin1Array, self.server_address);
        print(self.server_address);
        print("BTTsNetClient sendToBin end");
        return send_len;
    def getRecvClient(self):
        return self.cli_addr;
    def recvFromBin(self,_sz):
        print("BTTsNetClient recvFromBin 01");
        bin01 = None;
        try:
            (bin01, self.cli_addr) = self.sock.recvfrom(_sz);
            tmpS = str(self.cli_addr);
            print("BTTsNetClient recvFromBin " + tmpS);
            if bin01 != None:
                pass;
        except Exception as e:
            en = e.args[0]
            if en == 10035:
                print("10035")
                #time.sleep(0.1)
            elif en == 11:
                print("11")
                #time.sleep(0.1)
        print("BTTsNetClient recvFromBin end");
        return bin01;



"""
class BTTsNetClient(BTTsNet):
    def __init__(self):
        super().__init__();
        self.flagServer = False;
        pass;
    def sendToBin(self, _bin1Array):
        send_len = self.sock.sendto(_bin1Array, self.serv_address);
    def recvFromBin(self,_sz):
        (bin01, addr) = self.sock.recvfrom(_sz);
        print(addr);
        return bin01;
"""

def sendToForList(_list):
    bin01 = bytearray(1200);
    sz = len(_list);
    print(sz);
    ofs = 0;
    for n in range(sz):
        szCur = _list[n].writeByteArray(bin01,ofs);
        ofs += szCur;
        print(ofs);
    return bin01;

def recvFromForList(_list, binData):
    print("recvFromForList 01");
    if binData != None:
        retLen = len(binData);
    else:
        retLen = 0;
    print("recvFromForList 03 " + str(retLen));
    if True:
        sz = len(_list);
        ofs = 0;
        for n in range(sz):
            szCur = _list[n].readByteArray(binData,ofs);
            ofs += szCur;
            print(ofs);
    print("recvFromForList end");
    pass;


def waitParamBTTsNetServ(bttsNet, param ):
    if bttsNet != None:
        #bttsNet.setBlocking(True);
        bttsNet.recvFromForParam(param);
        #
        bttsNet.sendToForValue(param);
        #
        #time.sleep(param.waitBeforeRun.value);
    """
    print('BTTsNet 02');
    time.sleep(1.0);
    print('BTTsNet 03');
    if bttsNet != None:
        bttsNet.setBlocking(False);
    print('BTTsNet 04');
    time.sleep(1.0);
    print('BTTsNet 05');
    """
