#! python3
# coding: utf-8

import struct
from lib.openflow import base

class OpenFlowProtocol(object):
    OFPT_HELLO = 0
    def __init__(self):
        pass

    @classmethod
    def parse_ofp_header(cls,msg):
        return base.parse_ofp_header(msg)

    @classmethod
    def hello(cls,versions,**kargs):
        xid = kargs.get("xid",base.hms_xid())
        if versions :
            vset = base.ofp_version_normalize(versions)
        else :
            vset = set((1,))
        version = max(vset)

        if version < 4 :
            return struct.pack("!BBHI", version, 0, 8, xid)
        else :
            units = [0, ] * (1 + version // 32)
            for v in vset:
                units[v // 32] |= 1 << (v % 32)

            versionbitmap_length = 4 + len(units) * 4
            fmt = "!BBHIHH%dI%dx" % (len(units), 8 * ((len(units) - 1) % 2))
            return struct.pack(fmt, version, 0, struct.calcsize(fmt), xid,  # HELLO
                              1, versionbitmap_length, *units)  # VERSIONBITMAP
    @classmethod
    def hello_failed(cls,accept_versions):
        ascii_txt = "Accept versions: %s" % ["- 1.0 1.1 1.2 1.3 1.4".split()[x] for x in list(accept_versions)]
        return struct.pack("!BBHIHH", max(accept_versions), 1,struct.calcsize("!BBHIHH") + len(ascii_txt), base.hms_xid(),0, 0) + ascii_txt

    @classmethod
    def parse_hello(cls,msg):
        return base.parse_hello(msg)

    @classmethod
    def negotiate_version(cls,versions,accept_versions):
        client = base.ofp_version_normalize(versions)
        server = base.ofp_version_normalize(accept_versions)
        cross = client & server
        if cross :
            version = max(cross)
            return version
        return None

if __name__ == "__main__":
    msg = b'\x04\x00\x00\x08\x00\x00\x00\x03'
    ret = OpenFlowProtocol.parse_ofp_header(msg)
    print(ret)
    vers = [1.1,1.3]
    print(OpenFlowProtocol.hello(vers))