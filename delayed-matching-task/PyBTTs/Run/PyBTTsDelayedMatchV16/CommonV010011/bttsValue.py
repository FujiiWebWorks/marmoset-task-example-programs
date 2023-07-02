# -*- coding: utf-8 -*-

#from socket import *
#from select import *
import struct
import binascii
import ctypes

#from bttsValue import ValueInt32, ValueFloat32, ValueFloat32Array,ValueBool8
#from bttsValue import ValueRecInt32, ValueRecFloat32,ValueRecBool8

def separateXstr(result,s):
    stack = []
    print(s);
    for i, ch in enumerate(s):
        if ch == '[':
            stack.append(i)
        elif ch == ']':
            tmpA = s[stack.pop():i + 1];
            result.append(tmpA)

def separateYstr(result,s):
    stack = []
    print(s);
    for i, ch in enumerate(s):
        if ch == '[':
            stack.append(i)
        elif ch == ']':
            tmpA = s[stack.pop()+1:i];
            result.append(tmpA)


class ValueBase:
    def __init__(self):
        self.vname = None;
        pass;
    def overwriteByte1Array(self,_b1array, _offset, _bx, _blen):
        for n in range(_blen):
            _b1array[_offset + n ] = _bx[n];
        pass;
    def writeByteArray(self, _barray, _offset):
        retLen = 0;
        return retLen;

class ValueString(ValueBase):
    def __init__(self, _vname, value):
        super().__init__();
        self.vname = _vname;
        self.value = value; # str
        # only ascii 0-9 A-Z a-z
        pass;
    def toKeyValue(self):
        pass;
        return {self.vname : self.value };
    def setValue(self,v):
        self.value = v; # str
        pass;
    def setValueGUI(self,v):
        self.value = v; #str
        pass;
    def getValueGUI(self):
        return self.value;

    def readByteArray(self,_b1array, _offset):
        charList = [];
        
        ofs = 0;
        curLen = 4; # int32
        tmpV = struct.unpack_from('<i',_b1array,_offset+ofs);
        sz = int(tmpV[0]);
        ofs += curLen;

        curLen = 1;
        for n in range(sz):
            tmpV = struct.unpack_from('B',_b1array,_offset+ofs);
            charList.append( chr(tmpV[0]));
            ofs += curLen;
        retLen = ofs;
        
        tmpStr = '';
        for c in charList:
            tmpStr += c;
        self.value = tmpStr
        
        
        return retLen;        
    def writeByteArray(self, _b1array, _offset):
        slen = len( self.value); # str
        ofs = 0;
        
        curLen = 4;
        sz = slen;
        b4len = struct.pack('<i',int(sz));
        self.overwriteByte1Array(_b1array, _offset+ofs, b4len, curLen);
        ofs += curLen;
        
        for ch in self.value:
            #print(ch + ' = ' + str(ord(ch)))
            b1 = struct.pack('B',ord(ch));
            wLen = 1; # 1byte
            self.overwriteByte1Array(_b1array, _offset+ofs, b1, wLen);
            ofs += wLen;
        
        retLen = ofs;
        return retLen;

class ValueInt32(ValueBase):
    def __init__(self,_vname,_value):
        super().__init__();
        self.value = int(_value);
        self.vname = _vname;
        pass;
    def toKeyValue(self):
        pass;
        return {self.vname : self.value };
    def setValue(self,v):
        self.value = int(v);
        pass;
    def setValueGUI(self,v):
        self.value = int(v);
        pass;
    def getValueGUI(self):
        return self.value;
    def readByteArray(self,_b1array, _offset):
        retLen = 4; # 4byte
        tmpV = struct.unpack_from('<i',_b1array,_offset);
        ##  'tuple'
        #print(type(tmpV));
        #print(tmpV);
        self.value = int(tmpV[0]);
        return retLen;
    def writeByteArray(self, _b1array, _offset):
        #b1array = bytearray();
        retLen = 4; # 4byte
        b4 = struct.pack('<i',self.value);
        self.overwriteByte1Array(_b1array, _offset, b4, retLen);
        return retLen;
class ValueFloat32(ValueBase):
    def __init__(self,_vname,_value, x1000=False):
        self.value = float(_value);
        self.vname = _vname;
        self.x1000 = x1000;
        pass;
    def toKeyValue(self):
        print();
        ret = 0.0;
        if self.x1000:
            ret = self.value* 1000.0 ;
        else:
            ret = self.value;
        toKV = {self.vname : float(ret) };
        return toKV;
    def setValue(self,v):
        self.value = float(v);
        pass;
    def setValueGUI(self,v):
        if self.x1000:
            self.value = float( v / 1000.0);
        else:
            self.value = float(v);
        pass;
    def getValueGUI(self):
        ret = 0.0;
        if self.x1000:
            ret = self.value * 1000.0 ;
        else:
            ret = self.value;
        return float(ret);
    
    def readByteArray(self,_b1array, _offset):
        retLen = 4; # 4byte
        tmpV = struct.unpack_from('<f',_b1array,_offset);
        ##  'tuple'
        #print(type(tmpV));
        #print(tmpV);
        self.value = float(tmpV[0]);
        return retLen;
    def writeByteArray(self, _b1array, _offset):
        #b1array = bytearray();
        retLen = 4; # 4byte
        b4 = struct.pack('<f',self.value);
        self.overwriteByte1Array(_b1array, _offset, b4, retLen);
        return retLen;

class ValueFloat32Array(ValueBase):
    def __init__(self,_vname,_value):
        super().__init__();
        self.value = _value; # array
        self.vname = _vname;
        pass;
    def toKeyValue(self):
        pass;
        return {self.vname : self.getValueGUI() };
    def setValue(self,v):
        self.value = v;
        pass;
    def setValueGUI(self,v):
        list_str = v;
        listFloat = [float(x.strip()) for x in list_str.split(",")];

        #lst = [1,2,3]
        #lst_str = str(lst)[1:-1] 
        #print(lst_str)    
        
        #list_str = "100.0,200.0  , 300.0 , 400.0";
        #listFloat = [float(x.strip()) for x in list_str.split(",")];
        #print(listFloat);        
        
        self.value = listFloat
        pass;
    def getValueGUI(self):
        return str(self.value)[1:-1] ;
        
    def readByteArray(self,_b1array, _offset):
        self.value.clear();
        ofs = 0;
        curLen = 4; # int32
        tmpV = struct.unpack_from('<i',_b1array,_offset+ofs);
        sz = int(tmpV[0]);
        ofs += curLen;
        
        curLen = 4; # float32
        for n in range(sz):
            tmpV = struct.unpack_from('<f',_b1array,_offset+ofs);
            self.value.append(float(tmpV[0]));
            ofs += curLen;
        retLen = ofs;
        return retLen;
    def writeByteArray(self, _b1array, _offset):
        #b1array = bytearray();
        ofs = 0;
        
        curLen = 4;
        sz = len(self.value);
        b4len = struct.pack('<i',int(sz));
        self.overwriteByte1Array(_b1array, _offset+ofs, b4len, curLen);
        ofs += curLen;
        
        for n in range(sz):
            curLen = 4; # 4byte
            b4 = struct.pack('<f',float(self.value[n]));
            self.overwriteByte1Array(_b1array, _offset+ofs, b4, curLen);
            ofs += curLen;
        retLen = ofs;
        return retLen;



"""
class ValueFloat32Array2D(ValueBase):
    def __init__(self,_vname,_value):
        super().__init__();
        self.value = _value; # array
        self.vname = _vname;
        pass;
    def toKeyValue(self):
        pass;
        return {self.vname : self.getValueGUI() };
    def setValue(self,v):
        self.value = v;
        pass;
    def setValueGUI(self,v):
        list_str = v;
        listFloat = [float(x.strip()) for x in list_str.split(",")];

        #lst = [1,2,3]
        #lst_str = str(lst)[1:-1] 
        #print(lst_str)    
        
        #list_str = "100.0,200.0  , 300.0 , 400.0";
        #listFloat = [float(x.strip()) for x in list_str.split(",")];
        #print(listFloat);        
        
        self.value = listFloat
        pass;
    def getValueGUI(self):
        return str(self.value)[1:-1] ;
        
    def readByteArray(self,_b1array, _offset):
        self.value.clear();
        ofs = 0;
        curLen = 4; # int32
        tmpV = struct.unpack_from('<i',_b1array,_offset+ofs);
        sz = int(tmpV[0]);
        ofs += curLen;
        
        curLen = 4; # float32
        for n in range(sz):
            tmpV = struct.unpack_from('<f',_b1array,_offset+ofs);
            self.value.append(float(tmpV[0]));
            ofs += curLen;
        retLen = ofs;
        return retLen;
    def writeByteArray(self, _b1array, _offset):
        #b1array = bytearray();
        ofs = 0;
        
        curLen = 4;
        sz = len(self.value);
        b4len = struct.pack('<i',int(sz));
        self.overwriteByte1Array(_b1array, _offset+ofs, b4len, curLen);
        ofs += curLen;
        
        for n in range(sz):
            curLen = 4; # 4byte
            b4 = struct.pack('<f',float(self.value[n]));
            self.overwriteByte1Array(_b1array, _offset+ofs, b4, curLen);
            ofs += curLen;
        retLen = ofs;
        return retLen;
"""

class ValueInt32Array(ValueBase):
    def __init__(self,_vname,_value):
        super().__init__();
        self.value = _value; # array
        self.vname = _vname;
        pass;
    def toKeyValue(self):
        pass;
        return {self.vname : self.getValueGUI() };
    def setValue(self,v):
        self.value = v;
        pass;
    def setValueGUI(self,v):
        list_str = v;
        listInt = [int(x.strip()) for x in list_str.split(",")];

        #lst = [1,2,3]
        #lst_str = str(lst)[1:-1] 
        #print(lst_str)    
        
        #list_str = "100.0,200.0  , 300.0 , 400.0";
        #listFloat = [float(x.strip()) for x in list_str.split(",")];
        #print(listFloat);        
        
        self.value = listInt;
        pass;
    def getValueGUI(self):
        return str(self.value)[1:-1] ;
        
    def readByteArray(self,_b1array, _offset):
        self.value.clear();
        ofs = 0;
        curLen = 4; # int32
        tmpV = struct.unpack_from('<i',_b1array,_offset+ofs);
        sz = int(tmpV[0]);
        ofs += curLen;
        
        curLen = 4; # float32
        for n in range(sz):
            tmpV = struct.unpack_from('<i',_b1array,_offset+ofs);
            self.value.append(int(tmpV[0]));
            ofs += curLen;
        retLen = ofs;
        return retLen;
    def writeByteArray(self, _b1array, _offset):
        #b1array = bytearray();
        ofs = 0;
        
        curLen = 4;
        sz = len(self.value);
        b4len = struct.pack('<i',int(sz));
        self.overwriteByte1Array(_b1array, _offset+ofs, b4len, curLen);
        ofs += curLen;
        
        for n in range(sz):
            curLen = 4; # 4byte
            b4 = struct.pack('<i',int(self.value[n]));
            self.overwriteByte1Array(_b1array, _offset+ofs, b4, curLen);
            ofs += curLen;
        retLen = ofs;
        return retLen;

class ValueInt32Array2D(ValueBase):
    def __init__(self,_vname,_value):
        super().__init__();
        self.value = _value; # array
        self.vname = _vname;
        pass;
    def toKeyValue(self):
        pass;
        return {self.vname : self.getValueGUI() };
    def setValue(self,v):
        self.value = v;
        pass;
    def setValueGUI(self,v):
        print("ValueInt32Array2D");
        print("setValueGUI 01");
        print(v);
        
        listStr = [];
        separateYstr(listStr, v);
        
        listInt = [];
        for curStr in listStr:
            listCur = [int(x.strip()) for x in curStr.split(",")];
            listInt.append(listCur);
            
        #lst = [1,2,3]
        #lst_str = str(lst)[1:-1] 
        #print(lst_str)    
        
        #list_str = "100.0,200.0  , 300.0 , 400.0";
        #listFloat = [float(x.strip()) for x in list_str.split(",")];
        #print(listFloat);        
        
        self.value = listInt;
        print(self.value);
        pass;
    def getValueGUI(self):
        print(self.value);
        retS = str(self.value)[1:-1] ;
        print(retS);
        return retS;
    def readByteArray(self,_b1array, _offset):
        self.value.clear();
        ofs = 0;
        curLen = 4; # int32
        tmpV = struct.unpack_from('<i',_b1array,_offset+ofs);
        sz = int(tmpV[0]);
        ofs += curLen;
        
        for n in range(sz):
            curLen = 4; # int32
            tmpV = struct.unpack_from('<i',_b1array,_offset+ofs);
            onesz = int(tmpV[0]);
            ofs += curLen;
            #
            curM = [];
            for m in range(onesz):
                curLen = 4; # int32
                tmpV = struct.unpack_from('<i',_b1array,_offset+ofs);
                curM.append(int(tmpV[0]));
                ofs += curLen;
            self.value.append(curM);
        retLen = ofs;
        print(self.value);
        
        return retLen;
    def writeByteArray(self, _b1array, _offset):
        #b1array = bytearray();
        ofs = 0;
        
        curLen = 4;
        sz = len(self.value);
        b4len = struct.pack('<i',int(sz));
        self.overwriteByte1Array(_b1array, _offset+ofs, b4len, curLen);
        ofs += curLen;
        
        for n in range(sz):
            onevalue = self.value[n];
            onesz = len(onevalue);
            curLen = 4; # 4byte
            b4len = struct.pack('<i',int(onesz));
            self.overwriteByte1Array(_b1array, _offset+ofs, b4len, curLen);
            ofs += curLen;
            #
            for m in range(onesz):
                curLen = 4; # 4byte
                b4 = struct.pack('<i',int(onevalue[m]));
                self.overwriteByte1Array(_b1array, _offset+ofs, b4, curLen);
                ofs += curLen;
        retLen = ofs;
        print("ValueInt32Array2D");
        print("writeByteArray");
        print(self.value);
        return retLen;


class ValueBool8(ValueBase):
    def __init__(self,_vname,_value):
        self.value = bool(_value);
        self.vname = _vname;
        pass;
    def toKeyValue(self):
        pass;
        return {self.vname : self.value };
    def readByteArray(self,_b1array, _offset):
        retLen = 1; # 4byte
        tmpV = struct.unpack_from('b',_b1array,_offset);
        ##  'tuple'
        #print(type(tmpV));
        #print(tmpV);
        if tmpV[0] == 0:
            self.value = False;
        else:
            self.value = True;
        return retLen;
    def writeByteArray(self, _b1array, _offset):
        #b1array = bytearray();
        retLen = 1; # 1byte
        if self.value:
            tmpV = 1;
        else:
            tmpV = 0;
        b1 = struct.pack('b',tmpV);
        self.overwriteByte1Array(_b1array, _offset, b1, retLen);
        return retLen;
    def setValue(self,v):
        self.value = v;
        pass;
    def setValueGUI(self,v):
        self.value =  v;
        pass;
    def getValueGUI(self):
        return self.value;

class ValueRecBase:
    def __init__(self, _vname):
        self.vname = _vname;
        self.flagSetVal = False;
        pass;
    def overwriteByte1Array(self,_b1array, _offset, _bx, _blen):
        # flagSetVal
        for n in range(_blen):
            _b1array[_offset + n ] = _bx[n];
        pass;
    def writeByteArray(self, _barray, _offset):
        retLen = 0;
        return retLen;

class ValueRecFloat32(ValueRecBase):
    def __init__(self, _vname):
        super().__init__(_vname);
        self.value = 0.0;
        pass;
    def setValue(self,_val):
        if _val != None:
            self.flagSetVal = True;
            self.value = float(_val);
        else:
            self.flagSetVal = False;
    def getValue(self):
        ret = None;
        if self.flagSetVal:
            ret = self.value; 
        else:
            pass;
        return ret;
        
class ValueRecBool8(ValueRecBase):
    def __init__(self, _vname):
        super().__init__(_vname);
        self.value = False;
    def setValue(self,v):
        self.flagSetVal = True;
        self.value = v;
        pass;
    def getValue(self):
        ret = None;
        if self.flagSetVal:
            ret = self.value; 
        else:
            pass;
        return ret;
class ValueRecInt32(ValueRecBase):
    def __init__(self,_vname):
        super().__init__(_vname);
        self.value = int(0);
        pass;
    def setValue(self,v):
        self.flagSetVal = True;
        self.value = int(v);
        pass;
    def getValue(self):
        ret = None;
        if self.flagSetVal:
            ret = self.value;
        else:
            pass;
        return ret;
class ValueRecString(ValueRecBase):
    def __init__(self, _vname):
        super().__init__(_vname);
        self.value = False;
    def setValue(self,v):
        self.flagSetVal = True;
        self.value = v;
        pass;
    def getValue(self):
        ret = None;
        if self.flagSetVal:
            ret = self.value; 
        else:
            pass;
        return ret;
class ValueRecList(ValueRecBase):
    def __init__(self, _vname):
        super().__init__(_vname);
        self.value = False;
    def setValue(self,v):
        self.flagSetVal = True;
        self.value = v;
        pass;
    def getValue(self):
        ret = None;
        if self.flagSetVal:
            ret = self.value; 
        else:
            pass;
        return ret;


def testK():
    s = '[1,2,3,4],[5,6,7,8]';
    result = [];
    print(s);
    separateYstr(result,s);

    print("testK 01");    
    for curM in result:
        print(curM);
    pass;
def testJ():
    v = '[1,2,3,4],[5,6,7,8]';
    listStr = [];
    separateYstr(listStr, v);
    
    print("testJ 01");
    listInt = [];
    for curStr in listStr:
        listCur = [int(x.strip()) for x in curStr.split(",")];
        listInt.append(listCur);
    
    print(listInt);

def testI():
    s = '[1,2,3,4],[5,6,7,8]';
    result = [];
    print(s);
    separateXstr(result,s);

    print("testI 01");    
    for curM in result:
        print(curM);
    pass;
def testH():
    s = '[[1,2,3,4],[5,6,7,8]]';
    result = [];
    print(s);
    separateXstr(result,s);
    
    for curM in result:
        print(curM);
    pass;
            

def testG():
    s = '((((AAA,BBB),CCC),DDD), (EEE,FFF))'
    stack = []
    result = []

    for i, ch in enumerate(s):
        if ch == '(':
            stack.append(i)
        elif ch == ')':
            result.append(s[stack.pop():i + 1])

    print(*result, sep='\n')
    # (AAA,BBB)
    # ((AAA,BBB),CCC)
    # (((AAA,BBB),CCC),DDD)
    # (EEE,FFF)
    # ((((AAA,BBB),CCC),DDD), (EEE,FFF))
    
    
    pass;

def testMain():
    #testG();
    testJ();
    
    pass;

if __name__ == '__main__':
    testMain();

