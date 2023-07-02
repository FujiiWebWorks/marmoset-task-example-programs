# -*- coding: utf-8 -*-
import copy
import random

class BTTsRamdom:
    def __init__(self):
        random.seed();
        pass;
    def genRandomList1Array(self, _list):
        retList = copy.deepcopy(_list);
        random.shuffle(retList);
        return retList;

class RandomList:
    def __init__(self):
        self.listValue = [];
        self.randomListValue = None;
        self.index = 0;
        self.ramdom = BTTsRamdom();
        pass;
    def setListValue(self, _listValue):
        self.listValue = _listValue;
        pass;
    def init(self):
        self.index = 0;
        self.randomListValue = self.ramdom.genRandomList1Array(self.listValue);
        pass;
    def getValue(self):
        retValue = self.randomListValue[self.index];
        return retValue;
    def nextIndex(self):
        self.index += 1;
        if self.index < len(self.randomListValue):
            pass;
        else:
            self.index = 0;
            self.randomListValue = self.ramdom.genRandomList1Array(self.listValue);
            pass;
        pass;
    