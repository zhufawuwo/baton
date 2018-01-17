#! python3
# coding:utf-8
from twisted.internet import reactor
from twisted.internet.protocol import Protocol,Factory,connectionDone
from pub import *

class OpenFlowChannel(Protocol):
    def dataReceived(self, data):
        print(data)

    def connectionMade(self):
        pass

    def connectionLost(self, reason=connectionDone):
        pass


class OpenFlowListener(Factory):
    protocol = OpenFlowChannel
    def __init__(self):
        pass

if __name__ == "__main__" :
    of_port = conf.getint("protocol","openflow")
    reactor.listenTCP(of_port,OpenFlowListener())
    reactor.run()