import ctypes
import time
import os


#os.add_dll_directory("./");
p = os.getcwd();
print(p);
os.add_dll_directory(p)

mydll = ctypes.cdll.LoadLibrary("DllPyNIDIONor.dll");

deleteDeviceNIDIO=mydll.deleteDeviceNIDIO;
deleteDeviceNIDIO.argtypes=[ctypes.c_int];
deleteDeviceNIDIO.restype=ctypes.c_int;


createDeviceNIDIO=mydll.createDeviceNIDIO;
createDeviceNIDIO.argtypes=[ctypes.c_int,ctypes.c_int];
createDeviceNIDIO.restype=ctypes.c_int;


beginNIDIO=mydll.beginNIDIO;
beginNIDIO.argtypes=[ctypes.c_int];
beginNIDIO.restype=None;


endNIDIO=mydll.endNIDIO;
endNIDIO.argtypes=[ctypes.c_int];
endNIDIO.restype=None;

writeDIODeviceNIDIO=mydll.writeDIODeviceNIDIO;
writeDIODeviceNIDIO.argtypes=[ctypes.c_int,ctypes.c_int];
writeDIODeviceNIDIO.restype=None;

readDIODeviceNIDIO=mydll.readDIODeviceNIDIO;
readDIODeviceNIDIO.argtypes=[ctypes.c_int];
readDIODeviceNIDIO.restype=ctypes.c_int;

retIndex = createDeviceNIDIO(6,1);
print(str(retIndex));
time.sleep(1.0);


beginNIDIO(retIndex);

writeDIODeviceNIDIO(retIndex,3 );
retData = readDIODeviceNIDIO(retIndex)
print(str(retData));

endNIDIO(retIndex);


retIndex2 = deleteDeviceNIDIO(retIndex);

print(str(retIndex) + " " +str(retIndex2));


