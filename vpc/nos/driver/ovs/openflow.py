#! python3
# coding: utf-8

from lib.openflow import base

class OpenFlowProtocol(object):
    def __init__(self):
        pass

    @classmethod
    def parse_ofp_header(cls,message):
        return base.parse_ofp_header(message)


if __name__ == "__main__":
    pass