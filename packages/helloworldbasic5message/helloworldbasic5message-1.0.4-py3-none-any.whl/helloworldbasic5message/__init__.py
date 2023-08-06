# description like this
# abc
# 123

import numpy as np

# not recommended, imports everything as hb2
import helloworldbasic4message.utility2 as hb2

# recommended import only what's needed
from helloworldbasic4message.utility2 import SomeClass
from helloworldbasic4message.utility2 import somefunction













def getSomelass(v):
    return hb2.SomeClass(v)


def test101():
    #hb2.utilB_saygoodbye("abc")

    print("test 101")
    a=hb2.SomeClass(208)
    hb2.somefunction(a)
    return 1


def test102():
    print("test 102")
    b=SomeClass(3)
    hb2.somefunction(b)
    return 1

def test103():
    print("test 103")
    d=SomeClass(1)
    somefunction(d)
    return 1




def test201():
    l=np.array([100,200])
    return l




def saygreeting(name):
    return hb2.utilA_sayhello(name)


test103()










