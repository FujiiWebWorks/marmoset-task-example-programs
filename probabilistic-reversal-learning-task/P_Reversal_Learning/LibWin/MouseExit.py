# -*- coding: utf-8 -*-
import os

class MouseExit():
    def __init__(self, _win):
        self.eventMouse = None;
        self.win = _win;
        
        self.count = 0;
        self.areaIndex = 0;
        self.numOfCount = 6;
        
        wsz = self.win.windowedSize;
        uParDot =  1.0 / wsz[1]; # size is    Unit is height
        xPos = (wsz[0] * uParDot) / 2.0;
        yPos = 1.0 / 2.0;
        #
        xPosA = 0.56165;
        yPosA = 0.3509;
        xDiff = -0.0234;
        yDiff = -0.02205;
        
        self.area = [[xPosA+xDiff,yPosA+yDiff],[-xPosA+xDiff,-yPosA+yDiff]]; 
        #self.area =  [[xPos,yPos],[-xPos,-yPos]]; 
        self.areaSize = [0.4,0.4];
        
        self.reset();
        pass;
    def reset(self):
        self.seqBtn = 0;
        self.areaIndex = 0;
        self.count = 0;
        pass;
    def incCounter(self):
        self.count += 1;
        pass;
    def isOk(self):
        retB = False;
        #print("count"+str(self.count));
        if self.count < self.numOfCount:
            pass;
        else:
            retB = True;
            pass;
        pass;
        return retB;
    def incAreaIndex(self):
        self.areaIndex += 1;
        if self.areaIndex < len(self.area):
            pass;
        else:
            self.areaIndex = 0;
            pass;
        #print("incAreaIndex" + str(self.areaIndex) );
        pass;
    @staticmethod
    def areaIn( _cPosX, _cSizeX, _posX):
        ret = False;
        x = _posX - _cPosX;
        halfx = _cSizeX / 2.0;
        if -halfx <= x and x < halfx:
            ret = True;
        return ret;
    @staticmethod
    def containPos(_cPos, _cSize, _pos):
        flagX = MouseExit.areaIn(_cPos[0], _cSize[0], _pos[0]);
        flagY = MouseExit.areaIn(_cPos[1], _cSize[1], _pos[1]);
        #print(str(flagX) + str(flagY));
        pass;
        return flagX and flagY;
    
    def oneFrame(self):
        buttonIndex = 0;
        curArea = self.area[self.areaIndex];
        buttons = self.eventMouse.getPressed();
        x,y = self.eventMouse.getPos();
        #
        #
        if self.seqBtn == 0:
            if buttons[buttonIndex]:
                print( self.win.windowedSize );
                print( self.count );
                curFlag = MouseExit.containPos(curArea,self.areaSize,[x,y])
                pass;
                if curFlag:
                    self.seqBtn = 1;
                    pass;
                else:
                    self.reset();
                    self.seqBtn = 0;
                    pass;
            else:
                pass;
        elif self.seqBtn == 1:
            if buttons[buttonIndex]:
                pass;
            else:
                pass;
                print( self.win.windowedSize );
                print( self.count );
                curFlag = MouseExit.containPos(curArea,self.areaSize,[x,y])
                # right release button
                if curFlag:
                    self.seqBtn = 0;
                    self.incAreaIndex();
                    self.incCounter();
                    pass;
                else:
                    self.reset();
                    self.seqBtn = 0;
                    pass;
                pass;
        pass;
        retB = self.isOk();
        return retB;

