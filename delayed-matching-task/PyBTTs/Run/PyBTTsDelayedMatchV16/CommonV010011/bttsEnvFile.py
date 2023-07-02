# -*- coding: utf-8 -*-
import os
import configparser

from bttsEnv import BTTsEnv

class BTTsEnvParam:
    def __init__(self):
        self.screen_background_color_rgb255 = [64,64,64];
        self.screen_background_color = [-0.5,-0.5,-0.5];
        self.feeder_device_comport = "COM3";
        self.fedder_device_use = False;
        self.feeder_device_drink = False;
        pass;
    def pr(self):
        print(self.screen_background_color);
        print(self.feeder_device_comport);
        print(self.fedder_device_use);
        print(self.feeder_device_drink);
        pass;


class BTTsHardEnvParamTTLAOut:
    def __init__(self, _num):
        self.num = _num;
        self.hard_ttlaout_device_use = False;
        self.hard_ttlaout_device_devicename = "dev1";
        self.hard_ttlaout_device_nidaq_use = False
        self.hard_ttlaout_device_nidaq_ttlony = False;
    def pr(self):
        print(str(self.num));
        print(str(self.hard_ttlaout_device_use));
        print(str(self.hard_ttlaout_device_devicename));
        print(str(self.hard_ttlaout_device_nidaq_use));
        print(str(self.hard_ttlaout_device_nidaq_ttlony));
        

class BTTsEnvHardParam:
    def __init__(self):
        self.ttlaout = [];
        tmpHard = BTTsHardEnvParamTTLAOut(1);
        self.ttlaout.append(tmpHard);
        tmpHard = BTTsHardEnvParamTTLAOut(2);
        self.ttlaout.append(tmpHard);
        #
        self.session = "default";
        pass;
    def pr(self):
        for tt in self.ttlaout:
            tt.pr();
        pass;
    def toStringDeviceNumber(self,_num):
        retStr ="hard.ttlaout";
        retStr += ".";
        retStr += str(_num);
        retStr += ".";
        retStr += "device";
        return retStr;
    def loadOneH(self,_oneH, _bttsEnvFile):
        baseStr = self.toStringDeviceNumber(_oneH.num);
        print(baseStr);
        (retF, retV) =_bttsEnvFile.getBoolKey(baseStr + ".use");
        if retF :
            _oneH.hard_ttlaout_device_use = retV;
            
        retS = _bttsEnvFile.getStringKey(baseStr + ".devicename");
        if retS != None :
            _oneH.hard_ttlaout_device_devicename = retS;
        
        (retF, retV) =_bttsEnvFile.getBoolKey(baseStr + ".nidaq.use");
        if retF :
            _oneH.hard_ttlaout_device_nidaq_use = retV;
        (retF, retV) =_bttsEnvFile.getBoolKey(baseStr + ".nidaq.ttlonly");
        if retF :
            _oneH.hard_ttlaout_device_nidaq_ttlony = retV;
        pass;
    
    def load(self,_bttsEnvFile ):
        for oneH in self.ttlaout:
            self.loadOneH(oneH, _bttsEnvFile);
        pass;

class BTTsEnvFile:
    def __init__(self,_envParam, _normal=True):
        
        self.envParam = _envParam;
        self.env = BTTsEnv();
        self.env.createBTTsHomeHolder();
        self.config_ini = None;  
        self.sessionDefault = "default";
        pass;
        
        #self.homepath = os.path.expanduser(os.getenv('USERPROFILE'));
        #if _normal:
        #    self.envfile = self.homepath + "//Documents//PyBTTs//Env//envPyBTTs.txt";
        #else:
        #    self.envfile = self.homepath + "//Documents//usr//ec202112//ec202112-pyPsycopyDM//PyBTTs//Env//envPyBTTs.txt";
        self.envfile = self.env.homePyBTTsEnvFolder + "//envPyBTTs.txt";
        self.readFile(self.envfile);
        self.loadenv();
    def str2bool(self,s):
        return s.lower() in ["true", "t", "yes", "1"];
    def readFile(self, envFile):
        print(envFile);
        config_ini = configparser.ConfigParser(allow_no_value=True);
        config_ini.read(envFile, encoding='utf-8')
        print(envFile);
        return config_ini;
    def loadColorRGB255(self, _config_ini,_session, _key,_defaultValue):
        print(_key);
        print(_session);
        r = 0;
        g = 0;
        b = 0;
        tmpStr = _config_ini.get(_session, _key+ '.r');
        if(tmpStr):
            r = int(tmpStr);
        else:
            r = _defaultValue[0];
        tmpStr = _config_ini.get(_session, _key+ '.g');
        if(tmpStr):
            g = int(tmpStr);
        else:
            g = _defaultValue[1];
        tmpStr = _config_ini.get(_session, _key+ '.b');
        if(tmpStr):
            b = int(tmpStr);
        else:
            b = _defaultValue[2];
        return [r,g,b];
    def loadColor(self, _config_ini,_session, _key,_defaultValue):
        print(_key);
        print(_session);
        r = 0;
        g = 0;
        b = 0;
        tmpStr = _config_ini.get(_session, _key+ '.r');
        if(tmpStr):
            r = float(tmpStr);
        else:
            r = _defaultValue[0];
        tmpStr = _config_ini.get(_session, _key+ '.g');
        if(tmpStr):
            g = float(tmpStr);
        else:
            g = _defaultValue[1];
        tmpStr = _config_ini.get(_session, _key+ '.b');
        if(tmpStr):
            b = float(tmpStr);
        else:
            b = _defaultValue[2];
        return [r,g,b];

    def getStringKeySub(self,_config_ini, _session, _key):
        tmpStr = None;
        try:
            tmpStr = _config_ini.get(_session,_key);
        except configparser.NoOptionError:
            pass;
        return tmpStr;
    def getBoolKeySub(self,_config_ini, _session, _key):
        retFound = False;
        retValue = False;
        try:
            tmpStr = _config_ini.get(_session,_key);
            if tmpStr != None:
                retValue = self.str2bool(tmpStr);
                retFound = True;
        except configparser.NoOptionError:
            pass;
        return (retFound, retValue);
    def getBoolKey(self, _key):
        return self.getBoolKeySub(self.config_ini,self.sessionDefault, _key);
    def getStringKey(self,_key):
        return self.getStringKeySub(self.config_ini,self.sessionDefault, _key);
    
    def loadenv(self):
        self.config_ini = self.readFile(self.envfile)
        self.sessionDefault =  'default';
        self.envParam.screen_background_color_rgb255 = self.loadColorRGB255(self.config_ini,self.sessionDefault,'screen.background.color.rgb255',self.envParam.screen_background_color_rgb255)
        self.envParam.screen_background_color = self.loadColor(self.config_ini,self.sessionDefault,'screen.background.color',self.envParam.screen_background_color);

        tmpStr = self.getStringKey('feeder.device.comport');
        if(tmpStr != None):
            self.envParam.feeder_device_comport = tmpStr;

        (retFound, retValue) = self.getBoolKey('feeder.device.use');
        if retFound:
            self.envParam.fedder_device_use = retValue;
            
        (retFound, retValue) = self.getBoolKey('feeder.deivce.drink');
        if retFound:
            self.envParam.feeder_device_drink = retValue;

    def pr(self):
        pass;

if __name__ == '__main__':
    envParam = BTTsEnvParam();
    ec = BTTsEnvFile(envParam,_normal=False);
    envParam.pr();
    pass;

