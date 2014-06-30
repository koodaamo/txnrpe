import logging, sys, struct
from zlib import crc32

from twisted.internet.protocol import BaseProtocol, ClientFactory
from twisted.internet import reactor, ssl
from twisted.python import log
from twisted.python.modules import getModule
from twisted.internet.error import ConnectionDone, ConnectionLost

# version, type, crc32, result, query, 'N', 'D' (why the N&D???)
message = struct.Struct(">2hih1024scc")

# NRPE query & response types
QUERY = 01
RESPONSE = 02

# NAGIOS check result types
OK, WARNING, CRITICAL, UNKNOWN = 1,2,3,4

# possible protocol versions, V3 being most common
V1, V2, V3 = 01,02,03

# default port
PORT = 12489

#observer = log.PythonLoggingObserver()
#observer.start()
#log.startLogging(sys.stdout)

logging.basicConfig()
logger = logging.getLogger("NRPE")
logger.setLevel(logging.DEBUG)

class NRPEClientProtocol(BaseProtocol):
    "client that calls the NSClient++"

    VERSION = V2

    def __init__(self, addr, *args, **kwargs):
       self.host, self.port = addr.host, addr.port

    def connectionMade(self):
        logger.debug("connection to %s:%s made" % (self.host, self.port))
        self.sendQuery(r'check_cpu!10!10')

    def connectionLost(self, reason):
       if reason.type == ConnectionDone:
          logger.debug("connection closed ok")
       elif reason.type == ConnectionLost:
          logger.warn("connection lost")
       else:
          logger.warn("lost connection: %s" % reason)
     
    def dataReceived(self, data):
        
        #logger.info("response: %s" %
        proto_version, msg_type, crc, resp_type, data, n, d = message.unpack(data)
        logger.info("response: %s" % data)

    def handleResponse(self, response):
       "handle NRPE response to our query"

    def sendQuery(self, query):
       "send a query to NSClient++"
       data = (self.VERSION, QUERY, 0, 0, query, 'N', 'D')
       packet = message.pack(*data)
       checksum = crc32(packet)
       data = (self.VERSION, QUERY, checksum, 0, query, 'N', 'D')
       packet = message.pack(*data)
       self.transport.write(packet)


class NRPEClientProtocolFactory(ClientFactory):

   def buildProtocol(self, addr):
      return NRPEClientProtocol(addr)


if __name__=="__main__":

   try:
      host, port = sys.argv[1].split(":")
   except:
      host = sys.argv[1]
      port = PORT

   factory = NRPEClientProtocolFactory()
   #certData = getModule(__name__).filePath.sibling('public.pem').getContent()
   #authData = getModule(__name__).filePath.sibling('server.pem').getContent()
   #clientCertificate = ssl.PrivateCertificate.loadPEM(authData)
   #authority = ssl.Certificate.loadPEM(certData)
   #options = ssl.optionsForClientTLS(u'10.211.55.3', authority,
   #                                   clientCertificate)
   #factory.options = ssl.optionsForClientTLS(
   #   u"10.211.55.3", ssl.PrivateCertificate.loadPEM(certData)
   #)
   reactor.connectTCP(host, int(port), factory, bindAddress=("10.211.55.2",0))
   reactor.run()

