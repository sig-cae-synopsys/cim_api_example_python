#!/usr/bin/python
# This script requires suds that provides SOAP bindings for python.
# Download suds from https://fedorahosted.org/suds/
#   unpack it and then run:
#     python setup.py install
#
#   or unpack the 'suds' folder and place it in the same place as this script
from suds.client import Client
from suds.wsse import Security, UsernameToken
#
#For basic logging
import logging
logging.basicConfig()
#Uncomment to debug SOAP XML
#logging.getLogger('suds.client').setLevel(logging.DEBUG)
#logging.getLogger('suds.transport').setLevel(logging.DEBUG)
#
#getFileContents result requires decompress and decoding
#import base64, zlib
#
# -----------------------------------------------------------------------------
class WebServiceClient:
    def __init__(self, webservice_type, host, port, ssl, username, password):
        url = ''
        if (ssl):
            url = 'https://' + host + ':' + port
        else:
            url = 'http://' + host + ':' + port
        if webservice_type == 'configuration':
            self.wsdlFile = url + '/ws/v9/configurationservice?wsdl'
        elif webservice_type == 'defect':
            self.wsdlFile = url + '/ws/v9/defectservice?wsdl'
        else:
            raise "unknown web service type: " + webservice_type

        self.client = Client(self.wsdlFile)
        self.security = Security()
        self.token = UsernameToken(username, password)
        self.security.tokens.append(self.token)
        self.client.set_options(wsse=self.security)

    def getwsdl(self):
        print(self.client)

# -----------------------------------------------------------------------------
class DefectServiceClient(WebServiceClient):
    def __init__(self, host, port, ssl, username, password):
        WebServiceClient.__init__(self, 'defect', host, port, ssl, username, password)

# -----------------------------------------------------------------------------
class ConfigServiceClient(WebServiceClient):
    def __init__(self, host, port, ssl, username, password):
        WebServiceClient.__init__(self, 'configuration', host, port, ssl, username, password)
    def getProjects(self):
        return self.client.service.getProjects()		

# -----------------------------------------------------------------------------
if __name__ == '__main__':
#-------------TODO
    #
    #------------connection details,   
    #To run these examples adjust these connection parameters 
    #to match your instance URL and credentials
    #
    #
    host = 'localhost'
    port = '8080'
    ssl = False
    username = 'admin'
    password = 'coverity'	    
    #

 #-------------end of TODO
    
    defectServiceClient = DefectServiceClient(host, port, ssl, username, password)
    configServiceClient = ConfigServiceClient(host, port, ssl, username, password)

#
#---------------
#
    streamname='bookreader'
    cid=46089
    print 'CID= ',cid,' in stream= ', streamname
    print 'eventTag|eventDescription|lineNumber|filePathname'
    mergedDefectIdDO = defectServiceClient.client.factory.create('mergedDefectIdDataObj')
    mergedDefectIdDO.cid=cid
    streamIdDO = defectServiceClient.client.factory.create('streamIdDataObj')
    streamIdDO.name=streamname
    streamsList = [streamIdDO]
    filterSpecDO = defectServiceClient.client.factory.create('streamDefectFilterSpecDataObj')
    filterSpecDO.includeDefectInstances = True
    filterSpecDO.includeHistory = True
    streamDefects = defectServiceClient.client.service.getStreamDefects(mergedDefectIdDO, filterSpecDO, streamsList)
    for streamDefect in streamDefects:
        for defectInstance in streamDefect.defectInstances:
            for ev in defectInstance.events:
                if ev.eventKind == 'REMEDIATION' :
                    print ev.eventTag, '|',ev.eventDescription,'|', ev.lineNumber,'|', ev.fileId.filePathname
   
