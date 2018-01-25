#! python3
# coding: utf-8

import uuid
import random

def singleton(cls,*args,**kargs):
    instance = {}
    def _singleton(*args,**kargs):
        if cls not in instance :
            instance[cls] = cls(*args,**kargs)
        return instance[cls]
    return _singleton

def guid():
    return str(uuid.uuid1())

def tid():
    return int(random.random()*0xFFFFFFFF)


class EnumBase(object):
    NUMBER = 0
    BIT_SHIFT = 1
    def __init__(self,prefix='',members=None,type=NUMBER):
        self._keys = []
        self._type = type
        self._create_member(self._type,0,prefix,members)

    def extend(self,prefix='',members=None):
        self._create_member(self._type,len(self._keys),prefix,members)


    def _create_member(self,type,start,prefix,members):
        vi = start
        for m in members:
            k = prefix + m
            if k in self._keys :
                assert "key " + k + " already exists"

            self._keys.append(k)

            if type == EnumBase.NUMBER :
                v = vi
            elif type == EnumBase.BIT_SHIFT :
                v = 1 << vi
            print(k,v)
            setattr(self,k,v)
            vi = vi + 1


if __name__ == "__main__":
    e = EnumBase(prefix='OFPT_',members=["HELLO","ECHO_REQUEST","HELLO"],type=EnumBase.BIT_SHIFT)
    e.extend(prefix='OFP_',members=["PACKET_IN","FEATURES_REPLY"])
    print(e.OFP_PACKET_IN)

