import sys
import ctypes
import gc
import weakref
from weakref import ref

FUNCTYPE = ctypes.CFUNCTYPE(ctypes.py_object)

class X:
    @FUNCTYPE
    def func():
        return None

c = 0
x = X()
y = weakref.proxy(x)
while True:
    z = y.func()
    collected = gc.collect()
    print(c)
    c += 1

# C:\Users\iiids\Documents\openpose\src\openpose\net\bodyPartConnectorBase.cpp(902)
# peopleVectorToPeopleArray