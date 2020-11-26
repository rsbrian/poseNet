import sys
import ctypes

FUNCTYPE = ctypes.CFUNCTYPE(ctypes.py_object)

@FUNCTYPE
def func():
    return None

c = 0
while True:
    # if c > 100:
    #     break
    x = func()
    # for i in range()
    print(sys.getrefcount(x))
    # del x
    # ctypes.pythonapi._Py_Dealloc(ctypes.py_object(x))
    print(c)
    c += 1

# C:\Users\iiids\Documents\openpose\src\openpose\net\bodyPartConnectorBase.cpp(902)
# peopleVectorToPeopleArray