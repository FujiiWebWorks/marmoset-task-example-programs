# -*- coding: utf-8 -*-

import os
from psychopy import sound

from LibFeeder.Feeder import Feeder, ParamFeeder


class ValueObject:

    def __init__(self):
        self.value = None;
        pass;


class Rec_data:

    def __init__(self, _obj):
        self.obj = _obj;

    def initialRecMouse(self, _trials):
        obj = self.obj;
        if obj != None:
            obj.x = None;
            obj.y = None;
            obj.leftButton = None;
            obj.midButton = None;
            obj.rightButton = None;
            obj.time = None;
            obj.clicked_name = None;
        if obj != None:
            objname = self.obj.name;
            self.appendDataName(_trials, objname + '.mouse.x');
            self.appendDataName(_trials, objname + '.mouse.y');
            self.appendDataName(_trials, objname + '.mouse.leftButton');
            self.appendDataName(_trials, objname + '.mouse.midButton');
            self.appendDataName(_trials, objname + '.mouse.rightButton');
            self.appendDataName(_trials, objname + '.mouse.time');
            self.appendDataName(_trials, objname + '.mouse.clicked_name');
            pass;
        pass;

    def initialName(self, _trials, _isBlank):
        obj = self.obj;
        if obj != None:
            objname = self.obj.name;
            self.appendDataName(_trials, objname + '.started');
            self.appendDataName(_trials, objname + '.stopped');
        if obj != None:
            if not _isBlank:
                objname = self.obj.name;
                self.appendDataName(_trials, objname + '.x_pos');
                self.appendDataName(_trials, objname + '.y_pos');
                self.appendDataName(_trials, objname + '.x_size');
                self.appendDataName(_trials, objname + '.y_size');
        pass;

    def initial(self, _trials, _isBlank):
        self.initialName(_trials, _isBlank);
        pass;

    def appendDataName(self, _trials, _dataName):
        expr = _trials.getExp();

        if _dataName not in expr.dataNames:
            expr.dataNames.append(_dataName);
        pass;

    def addMouseData(self, _mouse):
        obj = self.obj;
        obj.clicked_name = obj.name;
        x, y = _mouse.getPos();
        obj.x = x;
        obj.y = y;
        buttons = _mouse.getPressed();
        obj.leftButton = buttons[0];
        obj.midButton = buttons[1];
        obj.rightButton = buttons[2];
        obj.time = _mouse.mouseClock.getTime();
        pass;

    def prAddRecData(self, _label, _value):
        print(_label + " " + str(_value));
        pass;

    def addRecData(self, _trials):
        obj = self.obj;
        objname = self.obj.name;
        #
        pos = obj.pos;
        sz = obj.size;
        _trials.addData(objname + '.x_pos', pos[0]);
        _trials.addData(objname + '.y_pos', pos[1]);
        _trials.addData(objname + '.x_size', sz[0]);
        _trials.addData(objname + '.y_size', sz[1]);
        _trials.addData(objname + '.mouse.x', obj.x)
        _trials.addData(objname + '.mouse.y', obj.y)
        _trials.addData(objname + '.mouse.leftButton', obj.leftButton)
        _trials.addData(objname + '.mouse.midButton', obj.midButton)
        _trials.addData(objname + '.mouse.rightButton', obj.rightButton)
        _trials.addData(objname + '.mouse.time', obj.time)
        _trials.addData(objname + '.mouse.clicked_name', obj.clicked_name)
        print('addRecData');
        self.prAddRecData(objname + '.mouse.x', obj.x);
        self.prAddRecData(objname + '.mouse.y', obj.y)
        pass;


class StimObject:

    def __init__(self, _curTask):
        self.curTask = _curTask;
        self.curTrialValue = _curTask.curTrialValue;
        self.curVScreen = _curTask.curVScreen;
        self.stim = None;
        self.stimParam = None;
        self.rec_data = None;
        self.duration = 0.995;
        self.flagClicked = False;
        pass;

    def initial(self, _trials):
        self.rec_data = Rec_data(self.stim);
        self.flagClicked = False;
        pass;

    def clicked(self):
        self.flagClicked = True;
        pass;

    def getDuration(self):
        retVal = self.duration;
        return retVal;

    def getXY(self):
        # tuple
        obj = self.stimParam;
        o_xy = obj.getXY();
        t_xy = self.curVScreen.transXY(o_xy);
        ret = t_xy;
        return ret;

    def getSize(self):
        # tuple
        obj = self.stimParam;
        o_sz = obj.getSize();
        t_sz = self.curVScreen.transSize(o_sz);
        ret = t_sz;
        return ret;


class Seq_base:

    def __init__(self, _curTask):
        self.prevButtonState = None;
        self.curTask = _curTask;
        self.curEnv = _curTask.curEnv;
        self.curParam = _curTask.curParam;
        self.curVScreen = _curTask.curVScreen;
        self.curTrialValue = _curTask.curTrialValue;
        self.polygonList = [];
        self.mouse = None;
        self.blank = None;
        self.flagContinue = True;
        self.flagTouched = False;
        self.flagMouseSt = True;
        self.mouseHold = None;
        #
        self.flagMouseCursor = int(self.curTask.curExpInfo['mouse_cursor']);

        pass;

    def begin(self):
        pass;

    def end(self):
        pass;

    def onBeginRoutine(self):
        self.prevButtonState = None;
        self.flagContinue = True;
        self.flagTouched = False;
        #
        if self.mouse != None:
            self.mouse.setVisible(self.flagMouseCursor);
        pass;
        for sobj in self.polygonList:
            sobj.initial(self.curTask.curTrials);
            sobj.rec_data.initial(self.curTask.curTrials, False)
            sobj.rec_data.initialRecMouse(self.curTask.curTrials);
        if self.blank != None:
            sobj = self.blank;
            sobj.initial(self.curTask.curTrials);
            sobj.rec_data.initial(self.curTask.curTrials, True)
        if self.blank != None:
            sobj = self.blank;
            sobj.stim.setSize((0, 0));

        pass;
        self.begin();
        pass;

    def onEndRoutine(self):
        for sobj in self.polygonList:
            sobj.rec_data.addRecData(self.curTask.curTrials);

        if self.mouse != None:
            if self.flagContinue:
                self.curTask.time_over = True;
            else:
                pass;
        self.end();
        pass;

    def setTouched(self):
        self.flagTouched = True;
        pass;

    def isTouched(self):
        return self.flagTouched;
        pass;

    def onOneFrame(self, _routineTime):
        pass;

    def isContinue(self):
        return self.flagContinue;

    def mouseSt(self, _routineTime):
        if self.mouse != None:
            if self.flagMouseSt:
                self.mouseStMouseMovePos(_routineTime);
            else:
                self.mouseStMouseClick(_routineTime);
            pass;
        pass;

    def mouseStMouseMovePos(self, _routineTime):
        pstr = 'mouseStMouseMovePos';
        # print(pstr + '_01');
        minWaitTime = 0.005;  # 100 msec
        polygon_t = self.polygonList;
        mouse = self.mouse;
        mouseloc = mouse.getPos();
        if self.mouseHold == None:
            self.mouseHold = ValueObject();
            self.mouseHold.value = mouseloc;
        if mouseloc[0] == self.mouseHold.value[0] and mouseloc[1] == self.mouseHold.value[1]:
            pass;
        else:
            self.mouseHold.value = mouseloc;
            try:
                iter(polygon_t)
                clickableList = polygon_t
            except:
                clickableList = [polygon_t]
            pass;
            gotValidClick = False
            for sobj in clickableList:
                obj = sobj.stim;
                rec_data = sobj.rec_data;
                if obj.contains(mouse):
                    if _routineTime >= minWaitTime:
                        sobj.clicked();
                        gotValidClick = True
                        if hasattr(obj, "status"):
                            obj.status = self.curEnv.codeFINISHED;
                        pass;
                        rec_data.addMouseData(mouse);
                        if gotValidClick:
                            self.flagContinue = False  # abort routine on response
                            self.setTouched();
                        pass;
                    else:
                        pass;
                else:
                    pass;
                pass;
            pass;
        # print(pstr + '_end');
        pass;

    def mouseStMouseClick(self, _routineTime):
        pstr = 'mouseStMouseClick';
        # print(pstr + '_01');
        polygon_t = self.polygonList;
        mouse = self.mouse;
        if mouse.status == self.curEnv.codeSTARTED:
            # print(pstr + '_02');
            buttons = mouse.getPressed();
            if self.prevButtonState == None:
                self.prevButtonState = buttons;
            if buttons != self.prevButtonState:
                self.prevButtonState = buttons;
                if sum(buttons) > 0:  # state changed to a new click
                    # check if the mouse was inside our 'clickable' objects
                    gotValidClick = False
                    try:
                        iter(polygon_t)
                        clickableList = polygon_t
                    except:
                        clickableList = [polygon_t]
                    for sobj in clickableList:
                        obj = sobj.stim;
                        rec_data = sobj.rec_data;
                        if obj.contains(mouse):
                            sobj.clicked();
                            gotValidClick = True
                            if hasattr(obj, "status"):
                                obj.status = self.curEnv.codeFINISHED;
                            pass;
                            rec_data.addMouseData(mouse);
                            if gotValidClick:
                                self.flagContinue = False  # abort routine on response
                                self.setTouched();

        pass;
        # print(pstr + '_end');
        pass;


class Seq_warning_square(Seq_base):

    def __init__(self, _curTask):
        super().__init__(_curTask);
        #
        self.warning_square = StimObject(self);
        self.warning_square.stimParam = self.curParam.stim_warning_square;
        print(self.warning_square.stimParam);
        self.polygonList.append(self.warning_square);
        self.blank = StimObject(self);

    def begin(self):
        self.warning_square.duration = self.curParam.touch_limit_sec - 0.005;
        self.blank.duration = 1.0 - 0.005;
        pass;

    def end(self):
        pass;

    def onOneFrame(self, _routineTime):
        super().onOneFrame(_routineTime);
        pstr = 'seq_warning_square:oneFrame';
        self.mouseSt(_routineTime);
        # print(pstr + '_end');
        pass;


class Seq_stimuli_AB(Seq_base):

    def __init__(self, _curTask):
        super().__init__(_curTask);

        self.target = StimObject(self);
        self.target.stimParam = self.curTrialValue.stim_target;
        #
        self.distractor = StimObject(self);
        self.distractor.stimParam = self.curTrialValue.stim_distractor;
        #
        self.polygonList.append(self.target);
        self.polygonList.append(self.distractor);
        #
        pass;

    def onOneFrame(self, _routineTime):
        super().onOneFrame(_routineTime);
        self.mouseSt(_routineTime);
        pass;

    def begin(self):
        self.target.duration = self.curParam.touch_limit_sec - 0.005;
        self.distractor.duration = self.curParam.touch_limit_sec - 0.005;
        pass;

    def end(self):
        flag = self.target.flagClicked or self.distractor.flagClicked;
        if flag:
            if self.target.flagClicked:
                self.curTask.setFlagCorrect(True);
                self.curTask.setSelected('target');
                self.curTask.setResponseTime(self.target.stim.time);
            elif self.distractor.flagClicked:
                self.curTask.setFlagCorrect(False);
                self.curTask.setSelected('distractor');
                self.curTask.setResponseTime(self.distractor.stim.time);
        else:
            pass;  # flagOmission = true;
        pass;


class Seq_reward_ITI(Seq_base):

    def __init__(self, _curTask):
        super().__init__(_curTask);
        self.flagFed = False;
        self.flagPlayed = False;
        self.flagCorrect = False;
        self.flagIncorrect = False;
        self.sound_correct_reward = None;
        self.sound_incorrect_reward = None;

        self.sound_correct_reward = sound.Sound('resource/sound/sin4KHz100ms_10msFadeInOut.wav', secs=0, stereo=True, hamming=False, name='sound_correct_reward');
        self.sound_correct_reward.setVolume(1.0);
        #self.sound_incorrect_reward = sound.Sound('A', secs=0.1, stereo=True, hamming=False, name='sound_incorrect_reward');
        #self.sound_incorrect_reward.setVolume(1.0);

        self.blank = StimObject(self);
        pass;

    def onOneFrame(self, _routineTime):
        super().onOneFrame(_routineTime);
        pstr = 'seq_warning_square:oneFrame';
        self.mouseSt(_routineTime);
        # print(pstr + '_end');

        if True:
            if self.flagFed:
                pass;
            else:
                if self.flagCorrect:
                    self.curTask.feeder.feed(1);
                    self.curTask.countReward += 1;
                    self.flagFed = True;
                    self.curTask.prReward();
                else:
                    pass;
            if self.flagPlayed:
                pass;
            else:
                if self.flagCorrect:
                    if self.sound_correct_reward != None:
                        self.sound_correct_reward.stop(reset=True);
                        self.sound_correct_reward.play();
                    self.flagPlayed = True;
                if self.flagIncorrect:
                    if self.sound_incorrect_reward != None:
                        self.sound_incorrect_reward.stop(reset=True);
                        self.sound_incorrect_reward.play();
                    self.flagPlayed = True;
                pass;
            pass;
        pass;

    def begin(self):
        self.blank.duration = self.curParam.ITI_duration_sec - 0.005;
        #
        self.flagPlayed = False;
        self.flagFed = False;
        #
        self.flagCorrect = False;
        self.flagIncorrect = False;
        self.flagOmission = False;
        if self.curTask.flagOmission:
            self.flagOmission = True;
        else:
            if self.curTask.flagCorrect:
                self.flagCorrect = True;
            else:
                self.flagIncorrect = True;
            pass;
        pass;

    def end(self):
        _trials = self.curTask.curTrials;
        _trials.addData('selected', self.curTask.selected);
        _trials.addData('responseTime', self.curTask.responseTime);
        _trials.addData('correct', self.curTask.flagCorrect);
        _trials.addData('omission', self.curTask.flagOmission);
        _trials.addData('rewad_count', self.curTask.countReward);
        self.curTask.prReward();
        pass;


class Seq_extra_ITI(Seq_base):

    def __init__(self, _curTask):
        super().__init__(_curTask);
        self.blank = StimObject(self);
        pass;

    def begin(self):
        self.blank.duration = self.curParam.ITI_Extra_duration_sec - 0.005;  # sec
        pass;

    def end(self):
        pass;

    def onOneFrame(self, _routineTime):
        super().onOneFrame(_routineTime);
        self.mouseSt(_routineTime);

        if(self.curTask.flagCorrect):
            self.flagContinue = False;
        else:
            pass;
        pass;


class ParamProbabilisticReversalLearning:

    def __init__(self):
        self.warning__x_pos = 0.0;
        self.warning__y_pos = 0.25;
        self.warning__x_size = 0.25;
        self.warning__y_size = 0.25;
        #
        self.touch_y = 0;
        self.touch_x = 0;
        self.touch_rt_msec = 0;
        self.touch_limit_sec = 900;
        self.title = "ProbabilisticReversalLearning";
        #
        self.ITI_duration_sec = 3.0;  # 3.0sec
        self.ITI_Extra_duration_sec = 5.0;  # 5.0

        #
    def initial(self):
        self.stim_warning_square = StimParamObject();
        self.stim_warning_square.x_pos = self.warning__x_pos;
        self.stim_warning_square.y_pos = self.warning__y_pos;
        self.stim_warning_square.x_size = self.warning__x_size;
        self.stim_warning_square.y_size = self.warning__y_size;
        pass;


class StimParamObject:

    def __init__(self):
        self.x_pos = 0;
        self.y_pos = 0;
        self.x_size = 0;
        self.y_size = 0;

    def getXY(self):
        # tuple
        return (self.x_pos, self.y_pos);

    def getSize(self):
        # tuple
        return (self.x_size, self.y_size);


class TrialValue:

    def __init__(self):
        self.delay_msec = 0;
        self.stim_distractor = StimParamObject();
        self.stim_target = StimParamObject();
        self.target_LR = None;
        self.correct_LR = None;
        self.trial_name = "trial_name"
        pass;


class StatusTask:

    def __init__(self):
        self.flagOmission = True;
        self.flagCorrect = False;
        pass;

    def initialize(self):
        self.flagOmission = True;
        self.flagCorrect = False;


class BaseTask:

    def __init__(self, _curSession, _expInfo):
        self.curExpInfo = _expInfo;
        self.curTrials = None;
        self.curSession = _curSession;
        self.curEnv = _curSession.ppEnv;
        self.curVScreen = _curSession.curVScreen;
        #
        self.flagCorrect = False;
        self.flagOmission = True;
        self.selected = 'None';
        self.responseTime = -1;
        #
        self.countReward = 0;
        #
        self.flagTouched = False;
        self.time_over = False;
        #
        _comStr = self.curExpInfo['reward_serial_COM'];
        self.paramFeeder = ParamFeeder(_comStr);
        self.feeder = Feeder(self.paramFeeder);
        #

        pass;

    def appendDataName(self, _trials, _dataName):
        expr = _trials.getExp();

        if _dataName not in expr.dataNames:
            expr.dataNames.append(_dataName);
        pass;

    def initialize(self, _trials):
        self.curTrials = _trials;
        self.flagCorrect = False;
        self.flagOmission = True;
        #
        self.selected = 'None';
        self.responseTime = -1;
        #
        self.optionReward = None;
        #
        self.time_over = False;
        #
        self.appendDataName(_trials, 'selected');
        self.appendDataName(_trials, 'responseTime');
        self.appendDataName(_trials, 'correct');
        self.appendDataName(_trials, 'omission');
        self.appendDataName(_trials, 'rewad_count');

        pass;

    def begin(self):
        self.feeder.begin();
        pass;

    def end(self):
        self.feeder.end();
        pass;

    def setFlagCorrect(self, _flagCorrect):
        self.flagCorrect = _flagCorrect;
        self.flagOmission = False;
        pass;
    def setSelected(self,_selectedName):
        self.selected = _selectedName;
        pass;
    def setResponseTime(self, _responseTime):
        self.responseTime = _responseTime;
        pass;

    def setOptionReward(self, _option):
        self.optionReward = _option;
        pass;

        pass;

    def prReward(self):
        print('prReward');
        print(str(self.countReward));
        print(str(self.flagCorrect));
        print(str(self.flagOmission));
        pass;


class TaskProbabilisticReversalLearning(BaseTask):

    def __init__(self, _curSession, _expInfo):
        super().__init__(_curSession, _expInfo);
        self.curParam = ParamProbabilisticReversalLearning();
        self.curParam.initial();
        self.curTrialValue = TrialValue();
        #
        self.seq_warning_square = Seq_warning_square(self);
        self.seq_stimuli_AB = Seq_stimuli_AB(self);
        self.seq_reward_ITI = Seq_reward_ITI(self);
        self.seq_extra_ITI = Seq_extra_ITI(self);
        pass;

    def initialize(self, _trials):
        super().initialize(_trials);
        pass;
