import os
import sys
import ctypes

curPath = os.getcwd();
print(curPath);

sys.path.append('./');

fullPathDLL = curPath +'/'+'PyBTTsTouchTUIO.dll';
#fullPathDLL = 'PyBTTsTouchTUIO';
PyBTTsTouchTUIODLL=ctypes.cdll.LoadLibrary(fullPathDLL)

add_double_PtrCall=PyBTTsTouchTUIODLL['add_double'];
add_double_PtrCall.restype=ctypes.c_double;
add_double_PtrCall.argtypes=(ctypes.c_double,ctypes.c_double)
def add_double_PBTTsT(_a,_b):
    return add_double_PtrCall(_a,_b);
    
retd = add_double_PBTTsT(1.1,2.1);
print(type(retd));
print(retd);

addd=PyBTTsTouchTUIODLL.add_double
addd.restype=ctypes.c_double
addd.argtypes=(ctypes.c_double,ctypes.c_double)
retd = addd(1.1,2.1);
print(type(retd));
print(retd);


