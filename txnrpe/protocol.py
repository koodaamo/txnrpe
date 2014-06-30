import logging, sys
from struct import Struct
from zlib import crc32

from twisted.internet.protocol import BaseProtocol, ClientFactory
from twisted.internet import reactor
from twisted.python import log

# version, type, crc32, result, query
message = Struct("!hhIh1024s")

# NRPE query & response types
QUERY = 1
RESPONSE = 2

# NAGIOS check result types
OK, WARNING, CRITICAL, UNKNOWN = 1,2,3,4

# possible protocol versions
V1, V2, V3 = 1,2,3


logging.basicConfig()
logger = logging.getLogger("NRPE")
log.startLogging(sys.stdout)

class NRPEClientProtocol(BaseProtocol):
    "client that calls the NSClient++"

    VERSION = V3

    #def makeConnection(self, transport):
    #    print transport       
        
    def connectionLost(self, reason):
        print reason
        
    def connectionMade(self):
        print "connection made"
        print self.transport
        #self.transport.writeSomeData("www")
        
    def dataReceived(self, data):
        print data

    def handleResponse(self, response):
       "handle NRPE response to our query"

    def sendQuery(self, query):
       "send a query to NSClient++"
       data = [self.VERSION, QUERY, 0, 0, query]
       packet = message.pack(data)
       checksum = crc32(packet)
       data[2] = checksum
       self.transport.write(packed)


class NRPEClientProtocolFactory(ClientFactory):

   def startedConnecting(self, connector):
      logger.debug("started connecting")

   def clientConnectionFailed(self, connector, reason):
      logger.error("connection failed: %s" % reason)

   def clientConnectionLost(self, connector, reason):
      logger.error("connection lost: %s" % reason)

   def buildProtocol(self, addr):
      return NRPEClientProtocol


if __name__=="__main__":
   host, port = sys.argv[1].split(":")
   factory = NRPEClientProtocolFactory()
   reactor.connectTCP(host, int(port), factory)
   reactor.run()
