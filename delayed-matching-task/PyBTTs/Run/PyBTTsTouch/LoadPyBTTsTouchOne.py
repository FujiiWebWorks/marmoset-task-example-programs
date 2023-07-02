import os
import sys
import ctypes
import time;

curPath = os.path.dirname(__file__);

fullPathDLL = curPath +'/'+'PyBTTsTouchOne.dll';
print(fullPathDLL);
PyBTTsTouchOneDLL=ctypes.cdll.LoadLibrary(fullPathDLL);

add_double_PtrCall=PyBTTsTouchOneDLL['add_double'];
add_double_PtrCall.restype=ctypes.c_double;
add_double_PtrCall.argtypes=(ctypes.c_double,ctypes.c_double)
def add_double_PyBTTs(_a,_b):
    return add_double_PtrCall(_a,_b);
    
retd = add_double_PyBTTs(1.1,2.1);
print(type(retd));
print(retd);

addd=PyBTTsTouchOneDLL.add_double
addd.restype=ctypes.c_double
addd.argtypes=(ctypes.c_double,ctypes.c_double)
retd = addd(1.1,2.1);
print(type(retd));
print(retd);



RemoveHook_PtrCall=PyBTTsTouchOneDLL['RemoveHook'];
RemoveHook_PtrCall.restype=ctypes.c_bool;
RemoveHook_PtrCall.argtypes=None;
def RemoveHook_PyBTTs():
    return RemoveHook_PtrCall();

InstallHookFromWindowTitlePyschopy_PtrCall=PyBTTsTouchOneDLL['InstallHookFromWindowTitlePyschopy'];
InstallHookFromWindowTitlePyschopy_PtrCall.restype=ctypes.c_bool;
InstallHookFromWindowTitlePyschopy_PtrCall.argtypes=None;
def InstallHookFromWindowTitlePyschopy_PyBTTs():
    return InstallHookFromWindowTitlePyschopy_PtrCall();


if __name__ == '__main__':
    retB = InstallHookFromWindowTitlePyschopy_PyBTTs();
    print(type(retB));
    print(retB);
    time.sleep(2);
    retB = RemoveHook_PyBTTs();
    print(type(retB));
    print(retB);


