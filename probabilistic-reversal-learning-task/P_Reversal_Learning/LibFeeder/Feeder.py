import sys
import serial

# change log 
# 20230629
# comstr upper

class ParamFeeder:
    def __init__(self, _comStr):
        self.feeder_device_comport = "COM3";
        #
        _comStrUpper = _comStr.upper();
        _noneStrUpper = 'None'.upper();
        if _comStrUpper == _noneStrUpper:
            self.feeder_device_use = False;
        else:
            self.feeder_device_use = True;
            self.feeder_device_comport = _comStrUpper;
        self.feeder_device_drink = False;
        
        print('self.feeder_device_use');
        print(self.feeder_device_use);
        print(self.feeder_device_comport);
        print(self.feeder_device_drink);
        pass;

class Feeder:
    def __init__(self, _envParam):
        self.envParam = _envParam;
        pass;
    def begin(self):
        if self.envParam.feeder_device_use:
            curCOM=self.envParam.feeder_device_comport;
        else:
            curCOM=None;
        pass;
        if curCOM != None:
            self.comXX = serial.Serial(curCOM,9600);
        else:
            self.comXX = None;
        pass;
    def end(self):
        if self.comXX != None:
            self.comXX.close()
        comXX = None;
        pass;
    
    def feed(self, count):
        #print(self.microlCommand, file=sys.stderr);
        comXX = self.comXX;
        
        for n in range(count):
            print('feed ' + str(n));
            if self.envParam.feeder_device_drink:
                if comXX != None:
                    wr = b'd1100x';
                    #wr = self.microlCommand;
                    comXX.write(wr);
            else:
                if comXX != None:
                    wr = b'A';
                    comXX.write(wr);


def testFunction():
    import time;
    
    print('testFunction 01');
    paramFeeder = ParamFeeder();
    paramFeeder.feeder_device_use = True;
    
    feeder = Feeder(paramFeeder);
    feeder.begin();
    time.sleep(1.0);
    
    for n in range(5):
        feeder.feed(1);
        time.sleep(1.0);
    pass;

    feeder.end();
    pass;
    print('testFunction end');

if __name__ == '__main__':
    testFunction()
    

