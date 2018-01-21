#! python3
# coding: utf-8

import struct
from lib.openflow import base

class OpenFlowProtocol(object):
    OFPT_HELLO = 0
    OFP4 = 4
    OFP5 = 5
    VERSIONS = (OFP4,OFP5)

    def __init__(self,version,ofp,build,parse,oxm):
        self.version = version
        for x in dir(ofp):
            setattr(self,x,getattr(ofp,x))

        self.b = build
        self.p = parse
        self.oxm = oxm

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

    @classmethod
    def get_ofp_instance(cls,version):
        if version == 4:
            from lib.openflow import ofp4
            from lib.openflow.ofp4 import build,parse,oxm
            return OpenFlowProtocol(version,ofp4,build,parse,oxm)
        elif version == 5:
            from lib.openflow import ofp5
            from lib.openflow.ofp5 import build,parse,oxm
            return OpenFlowProtocol(version,ofp5,build,parse,oxm)
        else :
            assert "no openflow instance avalible"




if __name__ == "__main__":
    msg = b'\x04\x00\x00\x08\x00\x00\x00\x03'
    ret = OpenFlowProtocol.parse_ofp_header(msg)
    p = OpenFlowProtocol.get_ofp_instance(4)
    print(p.OFPT_FEATURES_REQUEST)
    print(p.build)

