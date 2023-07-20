'''
Created on 2023/06/05

@author: komine
'''
class BuilderEnv:
    def __init__(self):
        self.codeFINISHED = 0; # FINISHED
        self.codeSTARTED = 0;  # STARTED
        pass;

class ScreenEnv:
    def __init__(self, _win, _dPos, _dSize ):
        self.win = _win;
        self.dPos = _dPos;
        self.dSize = _dSize;
        # win.units =='height':
        pass;
            
    def transXY(self, _xy):
        # tuple _xy
        dx = self.dPos[0];
        dy = self.dPos[1];
        dsx = self.dSize[0];
        dsy = self.dSize[1];
        
        t_xy = (dx + _xy[0]*dsx,  dy + _xy[1]*dsy  );
        return t_xy;
    def transSize(self, _xy):
        # tuple _xy
        dsx = self.dSize[0];
        dsy = self.dSize[1];
        
        t_xy = (_xy[0] * dsx ,_xy[1] * dsy );
        return t_xy;

class BuilderSession:
    def __init__(self):
        self.ppEnv = BuilderEnv();
        self.curTask = None;
        pass;
    
    def init_session(self,  _win, _expInfo):
        #
        dPos_x = float(_expInfo['trans_pos_x']);
        dPos_y = float(_expInfo['trans_pos_y']);
        dSize_x = float(_expInfo['trans_size_x']);
        dSize_y = float(_expInfo['trans_size_y']);
        
        dPos =(dPos_x,dPos_y);
        dSize = (dSize_x, dSize_y);
        self.curVScreen = ScreenEnv(_win, dPos,dSize);
        self.curTask = None;
        pass;
    def set_task(self, _task):
        self.curTask = _task;
        pass;
    def getCurrentTask(self):
        return self.curTask;
    