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
import base64, zlib
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
    #------------configuration, project details,   
    #For testing the individual call examples adjust the example project, stream, defect
    #specifics to match your projects, streams, etc...
    #
    # use the getProjects call if don't have one ready
    projectname='gzip'
    # 
    streamnamepattern='gz*'
    # use getStreams with streamnamepattern if you don't have one ready
    streamname='HPUX_ACCSHARED' #'gzip-trunk-misra'
    #  use getStreams with streamnamepattern if you don't have one ready
    snapshotid=10006
    # for getFileContents...
    # use getStreamDefects  v[0].defectInstances[0].events[0].fileId.contentsMD5 and filePathname
#     filepath='/idirs-7.7.0-misra/gzip-trunk-misra/lib/quotearg.c'
#     filecontentsMD5='cd583eecf0af533e6f93f31bb7390065'
    filepath='/opt/aCC/include_std/ios'
    filecontentsMD5='6f871b7419e04b662c1d48517cfbd258'
         # use getComponentMaps, getComponent if you don't have one ready
    componentname1='gzip.lib'
    componentname2='gzip.Other'
    # a cid which has instances, triage and detectionhistory
    # use one of the getMergedDefect calls if don't have one ready
    cid=10161 
#-------------end of TODO
    
    defectServiceClient = DefectServiceClient(host, port, ssl, username, password)
    configServiceClient = ConfigServiceClient(host, port, ssl, username, password)

#
#--------configservice calls---------------------------
#
    results = configServiceClient.client.service.getAllLdapConfigurations()
    print '------------getAllLdapConfigurations'
#    for v in results:
#        print v.serverDomain, v.serverPort, v.baseDN

    results = configServiceClient.client.service.getAllPermissions()
    print '------------getAllPermissions'
#    for v in results:
#        print v.permissionValue

    results = configServiceClient.client.service.getAllRoles()
    print '------------getAllRoles'
#    for v in results:
#        print v.roleId.name

    results = configServiceClient.client.service.getAttributes()
    print '------------getAttributes'
#    for v in results:
#        print v.attributeDefinitionId.name, v.attributeType

    v = configServiceClient.client.service.getBackupConfiguration()
    print '------------getBackupConfiguration'
#    print v.backupLocation, v.backupTime

    results = configServiceClient.client.service.getCategoryNames()
    print '------------getCategoryNames'
#    for v in results:
#        print v.displayName

    results = configServiceClient.client.service.getCheckerNames()
    print '------------getCheckerNames'
#    for v in results:
#        print v

    v = configServiceClient.client.service.getCommitState()
    print '------------getCommitState'
#    print "currentCommitCount=",v.currentCommitCount,  " isAcceptingNewCommits=", v.isAcceptingNewCommits
    
    componentIdDO = configServiceClient.client.factory.create('componentIdDataObj')
    componentIdDO.name='Default.Other'
    v = configServiceClient.client.service.getComponent(componentIdDO)
    print '------------getComponent'
#    print v.componentId.name
    
    componentMapFilterSpecDO = configServiceClient.client.factory.create('componentMapFilterSpecDataObj')
    componentMapFilterSpecDO.namePattern='*'
    results = configServiceClient.client.service.getComponentMaps(componentMapFilterSpecDO)
    print '------------getComponentMaps'
#    for v in results:
#        print v.componentMapId.name

    results = configServiceClient.client.service.getDefectStatuses()
    print '------------getDefectStatuses'
#    for v in results:
#        print v

    groupIdDO = configServiceClient.client.factory.create('groupIdDataObj')
    groupIdDO.name='Users'
    v = configServiceClient.client.service.getGroup(groupIdDO)
    print '------------getGroup'
#    print v.name.displayName, v.local
    
    groupFilterSpecDO = configServiceClient.client.factory.create('groupFilterSpecDataObj')
    groupFilterSpecDO.namePattern='*'
    pageSpecDO = defectServiceClient.client.factory.create('pageSpecDataObj')
    pageSpecDO.pageSize=2
    pageSpecDO.startIndex=0
    results = configServiceClient.client.service.getGroups(groupFilterSpecDO,pageSpecDO)
    print '------------getGroups'
#    print results.totalNumberOfRecords 
    
    results = configServiceClient.client.service.getLastUpdateTimes()
    print '------------getLastUpdateTimes'
#    for v in results:
#        print v
#        print v.featureName, v.lastUpdateDate
    
    results = configServiceClient.client.service.getLdapServerDomains()
    print '------------getLdapServerDomains'
#    for v in results:
#        print v.name
    
    v = configServiceClient.client.service.getLicenseConfiguration()
    print '------------getLicenseConfiguration'
#    print v.loc
    
    v = configServiceClient.client.service.getLicenseState()
    print '------------getLicenseState'
#    print v.desktopAnalysisEnabled
    
    v = configServiceClient.client.service.getLoggingConfiguration()
    print '------------getLoggingConfiguration'
#    print v.databaseLogging
    
    projectIdDO = configServiceClient.client.factory.create('projectFilterSpecDataObj')
    projectIdDO.namePattern='*'
    results = configServiceClient.client.service.getProjects(projectIdDO)
    print '------------getProjects'
#    for v in results:
#        print v.projectKey, v.id.name, v.dateCreated, v.userCreated, v.dateModified, v.userModified
    
    roleIdDO = configServiceClient.client.factory.create('roleIdDataObj')
    roleIdDO.name='Developer'
    v = configServiceClient.client.service.getRole(roleIdDO)
    print '------------getRole'
#    print v.description
    
    v = configServiceClient.client.service.getServerTime()
    print '------------getServerTime'
#    print v
    
    v = configServiceClient.client.service.getSignInConfiguration()
    print '------------getSignInConfiguration'
#    print v.maxFailedSignInAttempts
    
    v = configServiceClient.client.service.getSkeletonizationConfiguration()
    print '------------getSkeletonizationConfiguration'
#    print v.minSnapshotsToKeep
    
    snapshotIdDO = configServiceClient.client.factory.create('snapshotIdDataObj')
    snapshotIdDO.id=snapshotid
    results = configServiceClient.client.service.getSnapshotInformation(snapshotIdDO)
    print '------------getSnapshotInformation'
#    for v in results:
#        print v.snapshotId.id, v.commitUser, v.dateCreated 
    
    v = configServiceClient.client.service.getSnapshotPurgeDetails()
    print '------------getSnapshotPurgeDetails'
#    print v.minSnapshotsToKeep
    
    streamIdDO = configServiceClient.client.factory.create('streamIdDataObj')
    streamIdDO.name=streamname
#    results = configServiceClient.client.service.getSnapshotsForStream(streamIdDO)
    print '------------getSnapshotsForStream'
#    for v in results:
#        print v.id
    
    streamIdDO = configServiceClient.client.factory.create('streamFilterSpecDataObj')
    streamIdDO.namePattern=streamnamepattern
    results = configServiceClient.client.service.getStreams(streamIdDO)
    print '------------getStreams'
#    for v in results:
#        print v.id.name

    v = configServiceClient.client.service.getSystemConfig()
    print '------------getSystemConfig'
#    print v.commitPort
    
    triageStoreIdDO = configServiceClient.client.factory.create('triageStoreFilterSpecDataObj')
    triageStoreIdDO.namePattern='*'
    results = configServiceClient.client.service.getTriageStores(triageStoreIdDO)
    print '------------getTriageStores'
#    for v in results:
#        print v.id.name
    
    results = configServiceClient.client.service.getTypeNames()
    print '------------getTypeNames'
#    for v in results:
#        print v.displayName
    
    v = configServiceClient.client.service.getUser('admin')
    print '------------getUser'
#    print v.email
    
    userIdDO = configServiceClient.client.factory.create('userFilterSpecDataObj')
    userIdDO.namePattern='*'
    pageSpecDO = defectServiceClient.client.factory.create('pageSpecDataObj')
    pageSpecDO.pageSize=100
    pageSpecDO.startIndex=0
    v = configServiceClient.client.service.getUsers(userIdDO, pageSpecDO)
    print '------------getUsers'
#    print v.totalNumberOfRecords
#    for u in v.users:
#        print u.username
    
    v = configServiceClient.client.service.getVersion()
    print '------------getVersion'
#    print v.internalVersion
    
    #------------defectservice calls-----------------------
     
    projectIdDO = defectServiceClient.client.factory.create('projectIdDataObj')
    projectIdDO.name = projectname
    
    componentIdDO = configServiceClient.client.factory.create('componentIdDataObj')
    componentIdDO.name=componentname1
    
    componentIds = [componentIdDO]
    componentIdDO = configServiceClient.client.factory.create('componentIdDataObj')
    componentIdDO.name=componentname2
    componentIds.append(componentIdDO)
#    results = defectServiceClient.client.service.getComponentMetricsForProject(projectIdDO, componentIds)
    print '------------getComponentMetricsForProject'
#    for v in results:
#        print v.componentId.name, v.metricsDate, v.totalCount, v.dismissedCount, v.newCount, v.fixedCount, v.codeLineCount
    
    streamIdDO = defectServiceClient.client.factory.create('streamIdDataObj')
    streamIdDO.name=streamname
    fileIdDO = defectServiceClient.client.factory.create('fileIdDataObj')
    fileIdDO.filePathname=filepath
    fileIdDO.contentsMD5=filecontentsMD5
    v = defectServiceClient.client.service.getFileContents(streamIdDO, fileIdDO)
    decompressedContent=zlib.decompress(bytes(bytearray(base64.b64decode(v['contents']))), 15+32)
    print '------------getFileContents'
    print decompressedContent
    
    mergedDefectIdDO = defectServiceClient.client.factory.create('mergedDefectIdDataObj')
    mergedDefectIdDO.cid=cid
    streamIdDO = defectServiceClient.client.factory.create('streamIdDataObj')
    streamIdDO.name=streamname
    results = defectServiceClient.client.service.getMergedDefectDetectionHistory(mergedDefectIdDO, streamIdDO)
    print '------------getMergedDefectDetectionHistory'
    for v in results:
        print v.userName, v.defectDetection, v.detection, v.snapshotId, v.streams[0].name
    
    mergedDefectIdDO = defectServiceClient.client.factory.create('mergedDefectIdDataObj')
    mergedDefectIdDO.cid=cid
    streamIdDO = defectServiceClient.client.factory.create('streamIdDataObj')
    streamIdDO.name=streamname
    defectChanges = defectServiceClient.client.service.getMergedDefectHistory(mergedDefectIdDO, streamIdDO)
    print '------------getMergedDefectHistory'
    for dc in defectChanges:
        print dc.userModified, dc.dateModified
    
    projectIdDO = defectServiceClient.client.factory.create('projectIdDataObj')
    projectIdDO.name = projectname
    filterSpecDO = defectServiceClient.client.factory.create('projectScopeDefectFilterSpecDataObj')
    pageSpecDO = defectServiceClient.client.factory.create('pageSpecDataObj')
    pageSpecDO.pageSize=2
    pageSpecDO.startIndex=0
    v = defectServiceClient.client.service.getMergedDefectsForProjectScope(projectIdDO, filterSpecDO,pageSpecDO)
    print '------------getMergedDefectsForProjectScope'
#    print v
    
    streamIdDO = defectServiceClient.client.factory.create('streamIdDataObj')
    streamIdDO.name=streamname
    filterSpecDO = defectServiceClient.client.factory.create('snapshotScopeDefectFilterSpecDataObj')
    pageSpecDO = defectServiceClient.client.factory.create('pageSpecDataObj')
    pageSpecDO.pageSize=2
    pageSpecDO.startIndex=0
    snapshotScopeDO=defectServiceClient.client.factory.create('mergedDefectFilterSpecDataObj')
    snapshotScopeDO.showSelector='last()'
    mergedDefects = defectServiceClient.client.service.getMergedDefectsForStreams(streamIdDO, filterSpecDO, pageSpecDO)
    print '------------getMergedDefectsForStreams'
#    print v
    
    projectIdDO = defectServiceClient.client.factory.create('projectIdDataObj')
    projectIdDO.name = projectname
    filterSpecDO = defectServiceClient.client.factory.create('snapshotScopeDefectFilterSpecDataObj')
    pageSpecDO = defectServiceClient.client.factory.create('pageSpecDataObj')
    pageSpecDO.pageSize=2
    pageSpecDO.startIndex=0
    snapshotScopeDO=defectServiceClient.client.factory.create('snapshotScopeSpecDataObj')
    snapshotScopeDO.showSelector='last()'
    mergedDefects = defectServiceClient.client.service.getMergedDefectsForSnapshotScope(projectIdDO, filterSpecDO, pageSpecDO, snapshotScopeDO)
    print '------------getMergedDefectsForSnapshotScope'
#    for id in mergedDefects.mergedDefectIds:
#        print id.cid, id.mergeKey
    
    mergedDefectIdDO = defectServiceClient.client.factory.create('mergedDefectIdDataObj')
    mergedDefectIdDO.cid=cid
    streamIdDO = defectServiceClient.client.factory.create('streamIdDataObj')
    streamIdDO.name=streamname
    streamsList = [streamIdDO]
    filterSpecDO = defectServiceClient.client.factory.create('streamDefectFilterSpecDataObj')
    filterSpecDO.includeDefectInstances = True
    filterSpecDO.includeHistory = True
    v = defectServiceClient.client.service.getStreamDefects(mergedDefectIdDO, filterSpecDO, streamsList)
    f = v[0].defectInstances[0].events[0].fileId
    print '------------getStreamDefects'
#    print v
#    print f.contentsMD5, f.filePathname
    
    projectIdDO = defectServiceClient.client.factory.create('projectIdDataObj')
    projectIdDO.name = projectname
    results = defectServiceClient.client.service.getTrendRecordsForProject(projectIdDO)
#    print '------------getTrendRecordsForProject'
#    for v in results:
#        print v
    
    mergedDefectIdDO = defectServiceClient.client.factory.create('mergedDefectIdDataObj')
    mergedDefectIdDO.cid=cid 
    triageStoreIdDO = configServiceClient.client.factory.create('triageStoreIdDataObj')
    triageStoreIdDO.name='Default Triage Store'
    results = defectServiceClient.client.service.getTriageHistory(mergedDefectIdDO,triageStoreIdDO)
#    print '------------getTriageHistory'
#    for v in results:
#        print v.id
#        for a in v.attributes:
#            print a.attributeDefinitionId.name,"=",a.attributeValueId.name
#        print "-"
    
