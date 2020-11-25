import sys
import ctypes

FUNCTYPE = ctypes.CFUNCTYPE(ctypes.py_object)

@FUNCTYPE
def func():
    return None

c = 0
while True:
    if c < 2:
        func()
    else:
        c = 0
    c += 1


# C:\Users\iiids\Documents\openpose\src\openpose\net\bodyPartConnectorBase.cpp(902)
# peopleVectorToPeopleArray