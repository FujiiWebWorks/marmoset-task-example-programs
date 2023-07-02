# -*- coding: utf-8 -*-
import os

class BTTsEnv:
    def __init__(self):
        pass;
        self.homepath = os.path.expanduser(os.getenv('USERPROFILE'));
        self.homePyBTTsFolder = self.homepath + "//Documents//PyBTTs";
        self.homePyBTTsEnvFolder = self.homePyBTTsFolder + "//Env";
        self.homePyBTTsRunFolder = self.homePyBTTsFolder + "//Run";
        self.homePyBTTsVarFolder = self.homePyBTTsFolder + "//Var";
    def createBTTsHomeHolder(self):
        self.createHomeFolder(self.homePyBTTsEnvFolder);
        self.createHomeFolder(self.homePyBTTsRunFolder);
        self.createHomeFolder(self.homePyBTTsVarFolder);
        pass;
    def createHomeFolder(self,_foldername):
        if os.path.isdir(_foldername):
            pass;
        else:
            os.mkdir(_foldername);
            pass;


def testMain():
    env = BTTsEnv();
    varFName = env.homePyBTTsVarFolder;
    print(varFName);
    pass;

if __name__ == '__main__':
    testMain();
    