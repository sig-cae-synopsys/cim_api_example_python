#!/usr/bin/python
'''
usage: getLastTriagedSinceCutoff.py [-h] [-s SERVER] [-p PORT] [-u USER]
                                    [-c PASSWORD] [-n PROJECTNAME]
                                    [-d LASTTRIAGED]

getMergedDefects for all streams in a projects which were triaged more
recently than the lasttriaged date

optional arguments:
  -h, --help            show this help message and exit
  -s SERVER, --server SERVER
                        server (default: localhost)
  -p PORT, --port PORT  port (default: 8080)
  -u USER, --user USER  user (default: admin)
  -c PASSWORD, --password PASSWORD
                        password (default: coverity)
  -n PROJECTNAME, --projectname PROJECTNAME
                        projectname (default: "*", meaning all)
  -d LASTTRIAGED, --lasttriaged LASTTRIAGED
                        last triaged after (default:"2016-10-10T01:01:01")

'''
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
import argparse
#import os
#import json
import inspect      # for getKeys()
import base64, zlib # for decoding file contents

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

def getKeys(obj):
    return inspect.getmembers(obj)[6][1]

# -----------------------------------------------------------------------------
if __name__ == '__main__':
    #
    parser = argparse.ArgumentParser(description='getMergedDefects for all streams in a projects which were triaged more recently than the lasttriaged date')
    parser.add_argument('-s','--server',  default= 'localhost', help='server (default: localhost)')    
    parser.add_argument('-p','--port',  default= '8080', help='port (default: 8080)')    
    parser.add_argument('-u','--user',  default= 'admin', help='user (default: admin)')    
    parser.add_argument('-c','--password',  default= 'coverity', help='password (default: coverity)')    
    parser.add_argument('-n','--projectname',  default= '*', help='projectname (default: "*", meaning all)')    
    parser.add_argument('-d','--lasttriaged',  default= '2016-10-10T01:01:01', help='last triaged after (default:"2016-10-10T01:01:01")')    
    args = parser.parse_args()
    #
    host = args.server #'localhost'
    port = args.port   #'8080'
    ssl = False
    username = args.user #'admin'
    password = args.password #'coverity'       
    #
    projectpattern=args.projectname
    cutoffdate=args.lasttriaged
    #---------------------------------------------------------
    list_merged_defects = True  #Before drilling down
    drill_down = False
    list_md_detection_history = False
    list_md_history = False
    list_stream_defects = False
    list_sd_history= False
    list_sd_defect_instances= False
    #
    max_retrieved = 2
    #----------------------------------------------------------
    defectServiceClient = DefectServiceClient(host, port, ssl, username, password)
    configServiceClient = ConfigServiceClient(host, port, ssl, username, password)
    print '------------getProjects'
    projectIdDO = configServiceClient.client.factory.create('projectFilterSpecDataObj')
    projectIdDO.namePattern=projectpattern 
    projectIdDO.includeStreams=True
    results = configServiceClient.client.service.getProjects(projectIdDO)
    for v in results:
        print 'Project:', v.id.name,
        if hasattr(v,'description'):
            print v.description
        else:
            print '-'
        if hasattr(v,'streams'):
            for s in v.streams:
                print 'Stream:',s.id.name, 
                if hasattr(s,'description'):
                    print s.description, 
                else:
                    print '-',
                print s.language,s.triageStoreId.name, s.componentMapId.name, s.outdated, s.autoDeleteOnExpiry, 
                print s.enableDesktopAnalysis, 
                if hasattr(s,'summaryExpirationDays'):
                    print s.summaryExpirationDays
                else:
                    print '-'
                mds_retrieved=0
                totalrecords=1 #try at least one
                print '------------getMergedDefectsForStreams'
                mergedDefectFilterDO = defectServiceClient.client.factory.create('mergedDefectFilterSpecDataObj')
                #print dir(mergedDefectFilterDO)
                #print mergedDefectFilterDO.__keylist__
    #             mergedDefectFilterDO.cidList= []  
    #             mergedDefectFilterDO.componentIdList= []  
                #mergedDefectFilterDO.statusNameList = ["New","Triaged","Dismissed"]   
                mergedDefectFilterDO.classificationNameList= ["Unclassified","Pending","Bug"]  
    #             mergedDefectFilterDO.actionNameList= []  
    #             mergedDefectFilterDO.fixTargetNameList= []  
    #             mergedDefectFilterDO.severityNameList= []  
#                 mergedDefectFilterDO.legacyNameList= ["False"]  
    #             mergedDefectFilterDO.ownerNameList= []  
    #             mergedDefectFilterDO.checkerList= []  
    #             mergedDefectFilterDO.cweList= []  
    #             mergedDefectFilterDO.checkerCategoryList= []  
    #             mergedDefectFilterDO.checkerTypeList= []  
    #             mergedDefectFilterDO.impactList= []  
    #             mergedDefectFilterDO.issueKindList= []  
    #             mergedDefectFilterDO.componentIdExclude= []  
    #             mergedDefectFilterDO.defectPropertyKey= [] 
    #             mergedDefectFilterDO.streamExcludeNameList= []  
                #mergedDefectFilterDO.streamIncludeNameList= ['SAG_tools_java']  
    #             #---------------patterns, pattern lists
    #             mergedDefectFilterDO.filenamePatternList= ['"']  
    #             mergedDefectFilterDO.defectPropertyPattern= '"'  
    #             mergedDefectFilterDO.externalReferencePattern= '"'  
    #             mergedDefectFilterDO.functionNamePattern= '"'   
    #             mergedDefectFilterDO.ownerNamePattern= '"'   
    #             #---------------dates
    #             mergedDefectFilterDO.firstDetectedEndDate= '2020-09-05'
    #             mergedDefectFilterDO.firstDetectedStartDate= '2010-09-05'  
    #             mergedDefectFilterDO.lastDetectedEndDate= '2020-09-05'  
    #             mergedDefectFilterDO.lastDetectedStartDate= '2010-09-05'  
    #             mergedDefectFilterDO.lastFixedEndDate= '2020-09-05'  
    #             mergedDefectFilterDO.lastFixedStartDate= '2010-09-05'  
                #mergedDefectFilterDO.lastTriagedStartDate = cutoffdate 
    #             mergedDefectFilterDO.lastTriagedEndDate= '2020-09-05'  
    #             #----------------counts
    #             mergedDefectFilterDO.maxCid= 9000000  
    #             mergedDefectFilterDO.minCid= 0 
    #             mergedDefectFilterDO.maxOccurrenceCount= 9000000 
    #             mergedDefectFilterDO.minOccurrenceCount= 0  
    #             #----------------
                #mergedDefectFilterDO.snapshotComparisonField= 'Present'
    #             mergedDefectFilterDO.streamExcludeQualifier=   
    #             mergedDefectFilterDO.streamIncludeQualifier=
    #             mergedDefectFilterDO.mergedDefectIdDataObjs=   
    #            #------------------complex objects         
    #             attributeDefinitionValueFilterMapDO = defectServiceClient.client.factory.create('attributeDefinitionValueFilterMapDataObj')
    #             attributeDefinitionIdDO = defectServiceClient.client.factory.create('attributeDefinitionIdDataObj')
    #             attributeValueIdDO = defectServiceClient.client.factory.create('attributeValueIdDataObj')
    #             attributeDefinitionIdDO.name = 'scope'
    #             attributeValueIdDO.name = 'Unchanged'
    #             attributeDefinitionValueFilterMapDO.attributeDefinitionId = attributeDefinitionIdDO 
    #             attributeDefinitionValueFilterMapDO.attributeValueIds = attributeValueIdDO 
    #             #
    #             mergedDefectFilterDO.attributeDefinitionValueFilterMap=[attributeDefinitionValueFilterMapDO]
                #
                pageSpecDO = defectServiceClient.client.factory.create('pageSpecDataObj')
                pageSpecDO.pageSize = 20
                #
                # Grammar for snapshot show selector
                    # Snapshot ID
                    # first()
                    # last()
                    # expression, expression
                    # expression..expression
                    # lastBefore(expression)
                    # lastBefore(date)
                    # firstAfter(expression)
                    # firstAfter(date)
                    # Examples
                    # 10017, 10021
                    # lastBefore(last())
                    # firstAfter(2012-11-30)
                    # firstAfter(1 day ago)..last()
                snapshotScopeDO=defectServiceClient.client.factory.create('snapshotScopeSpecDataObj')
                snapshotScopeDO.compareOutdatedStreams = True
                #snapshotScopeDO.compareSelector = 'first()'
                snapshotScopeDO.showOutdatedStreams = True
                snapshotScopeDO.showSelector = 'last()' #'first()..last()'      
                #
                while mds_retrieved < totalrecords and mds_retrieved < max_retrieved :
                    pageSpecDO.startIndex=mds_retrieved
                    mergedDefects = defectServiceClient.client.service.getMergedDefectsForStreams(s.id, mergedDefectFilterDO, pageSpecDO,snapshotScopeDO)
                    #print mergedDefects.__keylist__
                    totalrecords=mergedDefects.totalNumberOfRecords
                    if mds_retrieved == 0:
                        print 'totalrecords: ',totalrecords
                    if totalrecords > 0 :
                        thispage=len(mergedDefects.mergedDefectIds)
                        mds_retrieved += thispage
                        #
                        # FOR current attributes no drill down necessary
                        #
                        if list_merged_defects == True:
                            for md in mergedDefects.mergedDefects:
                                #print md.__keylist__
                                #
                                #alternatively:  md.cid, md.checkerName ... would  also work
                                #                       
                                md_keys=md.__keylist__
#                                 ['checkerName', 'cid', 'componentName', 'cwe', 'defectStateAttributeValues', 
#                                          'displayCategory', 'displayImpact', 'displayIssueKind', 'displayType', 'domain', 
#                                          'filePathname', 'firstDetected', 'firstDetectedBy', 'firstDetectedSnapshotId', 
#                                          'firstDetectedStream', 'firstDetectedVersion', 'functionDisplayName', 'functionName', 
#                                          'issueKind', 'lastDetected', 'lastDetectedSnapshotId', 'lastDetectedStream', 
#                                          'lastDetectedVersion', 'lastTriaged', 'mergeKey', 'occurrenceCount']
                                for k in md_keys:
                                    if k not in ['defectStateAttributeValues']:
                                        print k,'=' ,md[k]
                                    else:
                                        for a in md[k]:
                                            print a.attributeDefinitionId.name,'=',
                                            if hasattr(a.attributeValueId, 'name'):
                                                print a.attributeValueId.name
                                            else:
                                                print a.attributeValueId
        
                        #
                        # DRILL DOWN FOR 
                        #    Detection History
                        #    Triage History
                        #    Stream Defects
                        #        optional Defect Instances and Defect History
                        #
                        if drill_down == True:                                    
                            for mdid in mergedDefects.mergedDefectIds:
                                print mdid.cid,mdid.mergeKey
                                #
                                #    DRILL DOWN Detection History
                                #
                                #
                                if list_md_detection_history == True :
                                    print '------------getMergedDefectDetectionHistory'
                                    defectDetectionHistory = defectServiceClient.client.service.getMergedDefectDetectionHistory(mdid, s.id)
                                    for mdh in defectDetectionHistory:
                                        print mdh.userName, mdh.defectDetection, mdh.detection, mdh.snapshotId, mdh.streams[0].name
                                #
                                #    DRILL DOWN Triage History
                                #
                                #
                                if list_md_history == True :
                                    print '------------getMergedDefectHistory'
                                    defectChanges = defectServiceClient.client.service.getMergedDefectHistory(mdid, s.id)
                                    for dc in defectChanges:
                                        #print getKeys(dc) 
                                        print dc.userModified,dc.dateModified,
                                        for sa in dc.affectedStreams:
                                            print sa.name
                                        for ca in dc.attributeChanges:
                                            if ca :
                                                for fc in ca:
                                                    print fc[0],'=',fc[1]#.fieldName,fc.oldValue,fc.newValue
                                        if hasattr(dc,'comments'):
                                            print 'comments = ',dc.comments
                                #
                                #    DRILL DOWN Stream Defects
                                #        optionally also get Triage History and Defect Instances
                                #
                                if list_stream_defects == True:
                                    print '------------getStreamDefects'
                                    streamDefectFilterDO = defectServiceClient.client.factory.create('streamDefectFilterSpecDataObj')
                                    streamDefectFilterDO.streamIdList=[s.id]
                                    streamDefectFilterDO.defectStateStartDate = '2010-09-05'
                                    streamDefectFilterDO.defectStateEndDate = '2017-09-05'       
                                    streamDefectFilterDO.includeDefectInstances = list_sd_defect_instances
                                    streamDefectFilterDO.includeHistory = list_sd_history 
                                    streamDefects = defectServiceClient.client.service.getStreamDefects(mdid, streamDefectFilterDO)
                                    for sd in streamDefects:
                                        print sd.cid, sd.checkerName,sd.domain,sd.id.defectTriageId, sd.id.defectTriageVerNum, sd.id.id,sd.id.verNum
                                        for a in sd.defectStateAttributeValues:
                                            print a.attributeDefinitionId.name,'=',a.attributeValueId.name
                                        if hasattr(sd,'history'):
                                            for dh in sd.history:
                                                print getKeys(dh)
                                                print dh.dateCreated,dh.userCreated
                                                for a in dh.defectStateAttributeValues:
                                                    print a.attributeDefinitionId.name,'=',a.attributeValueId.name
                                        if hasattr(sd,'defectInstances'):
                                            for di in sd.defectInstances:
                                                print di.category.name,di.category.displayName
                                                print di.checkerName
                                                print di.component
                                                print di.cwe
                                                print di.domain
                                                print di.extra
                                                print di.function.functionDisplayName, di.function.functionMangledName, di.function.functionMergeName
                                                print di.function.fileId.filePathname, di.function.fileId.contentsMD5 
                                                print di.id.id
                                                print di.impact.displayName,di.impact.name 
                                                for ik in di.issueKinds:
                                                    print ik.displayName, ik.name
                                                print di.localEffect
                                                print di.longDescription
                                                print di.type.displayName, di.type.name
                                                for e in di.events:
                                                    if e.main:
                                                        print e.main,e.polarity,e.eventKind, e.eventNumber, e.eventSet, e.eventTag, e.lineNumber, e.fileId.filePathname, e.fileId.filePathname, e.fileId.contentsMD5
                                                        print '------------getFileContents'
                                                        v = defectServiceClient.client.service.getFileContents(s.id, di.function.fileId)
                                                        decompressedContent=zlib.decompress(bytes(bytearray(base64.b64decode(v['contents']))), 15+32)
                                                        print 'decompressed:',len(decompressedContent) ,"bytes"
                                                        if len(decompressedContent) > 0:
                                                            ln=e.lineNumber-5
                                                            for l in decompressedContent.split('\n')[e.lineNumber-5:e.lineNumber+5]:
                                                                print ln,'>',l
                                                                ln += 1
                                                                                    
            
            
            
            
            
    

