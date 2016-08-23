Notes for python WS API client example code

If the information you need can be set up as a view in the GUI (filters, columns), we recommend using the View Management REST API.
For others use the traditional SOAP XML API
When needed, we have example of the creation of the filter, spec, etc. objects, however usually in the simplest form.
Processing the results demonstrated with commented out print commands.
For additional fields of the spec and result objects refer to the full API documentation.

Only the necessary class and function definitions are provided, the API calls themselves are intended for example snippets.
Helper functions, classes, call parameters, modularization are left to the implementers for simplicity and clarity.
Create update delete calls involve the same spec object creations (see API doc), they are not provided here.

=========View Management REST API calls

USAGE:
python wsGetViews.py

DEPENDENCIES: 
required=requests
optional=json (if parsing the view content json is required)

TODO:
To run these examples adjust the connection parameters to match your instance URL and credentials.
host='http://localhost:8080'
user='admin'
passcode='coverity'

For testing the call examples adjust the example view parameters to match a view in your instance.
Use the result of the getViews call if don't have one ready.
projectname='gzip'
viewtype='issues'
viewname='Outstanding Defects'

=========SOAP XML API calls

USAGE:
python wsGetAll.py

DEPENDENCIES: 
required=suds 
optional=logging, base64, zlib

This script requires suds that provides SOAP bindings for python.
-Download suds from https://fedorahosted.org/suds/
-Unpack it and then run:
--python setup.py install

Or unpack the 'suds' folder and place it in the same place as this script.

For basic logging no change, uncomment debug logging for SOAP XML and transport level logging

For plain text getFileContents result requires zlib to decompress and base64 for decoding

TODO:
To run these examples adjust these connection parameters in the source file to match your instance URL and credentials

host = 'localhost'
port = '8080'
ssl = False
username = 'admin'
password = 'coverity'	    

For testing the individual call examples adjust in the source file the example project, stream, defect #specifics to match your projects, streams, etc...

projectname='gzip' # use the getProjects call if don't have one ready
streamnamepattern='gz*'
streamname='gzip-trunk-misra' # use getStreams with streamnamepattern if you don't have one ready
snapshotid=10006 #use getSnapshotsForStream if you don't have one ready

For getFileContents (use getStreamDefects  v[0].defectInstances[0].events[0].fileId.contentsMD5 and filePathname)
filepath='/idirs-7.7.0-misra/gzip-trunk-misra/lib/quotearg.c'
filecontentsMD5='cd583eecf0af533e6f93f31bb7390065'

componentname1='gzip.lib' # use getComponentMaps, getComponent if you don't have one ready
componentname2='gzip.Other'

For a cid which has instances, triage and detectionhistory
cid=10161  # use one of the getMergedDefect calls if don't have one ready


EXAMPLE CALLS:

getAllLdapConfigurations
getAllPermissions
getAllRoles
getAttributes
getBackupConfiguration
getCategoryNames
getCheckerNames
getCommitState
getComponent
getComponentMaps
getDefectStatuses
getGroup
getGroups
getLastUpdateTimes
getLdapServerDomains
getLicenseConfiguration
getLicenseState
getLoggingConfiguration
getProjects
getRole
getServerTime
getSignInConfiguration
getSkeletonizationConfiguration
getSnapshotInformation
getSnapshotPurgeDetails
getSnapshotsForStream
getStreams
getSystemConfig
getTriageStores
getTypeNames
getUser
getUsers
getVersion
getComponentMetricsForProject
getFileContents
getMergedDefectDetectionHistory
getMergedDefectHistory
getMergedDefectsForProjectScope
getMergedDefectsForStreams
getMergedDefectsForSnapshotScope
getStreamDefects
