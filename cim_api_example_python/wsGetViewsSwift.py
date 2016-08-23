import requests
import json
#-------------TODO
#
#------------connection details,   
#To run these examples adjust these connection parameters 
#to match your instance URL and credentials
#https://prapier-840g2:8443/reports.htm#n10068/d10018
#
host='http://prapier-840g2:8081'
user='admin'
passcode='password'
#
#------------configuration, project details,   
#For testing the call examples adjust the example view parameters
#to match a view in your instance
#Use the result of the getViews call if don't have one ready
projectname='bzip800'
viewtype='trends'
viewname='Project Lifetime'
# 
#-------------end of TODO

def getViews():
	url=host+'/api/views/v1'
	r = requests.get(url,auth=(user,passcode))
	if(r.ok):
		return (json.loads(r.content))
	else:
		r.raise_for_status()
		
fieldsObject={}
rowObject={}
fieldsHeader=[]
	
def getViewContents(vtype, view, project):
	headers = {"Accept": "application/json"}
	url=host+'/api/viewContents/'+vtype+'/v1/'+view+'?projectId='+project+'&rowCount=0' 
	r = requests.get(url, auth=(user,passcode), headers = headers) 
	if(r.ok):
		return json.loads(r.content)
	else:
		r.raise_for_status()

def getViewContentsCSV(vtype, view, project):
	rtext=[]
	headers = {"Accept": "text/csv"}
	url=host+'/api/viewContents/'+vtype+'/v1/'+view+'?projectId='+project+'&rowCount=0' 
	r = requests.get(url, auth=(user,passcode), headers = headers) 
	if(r.ok):
		rtext=r.text.splitlines()
		totalRows = len(rtext)-1
		print url,'total:', totalRows,
	else:
		r.raise_for_status()
	return rtext

#-----print views
jData = getViews()
for v in jData['views'] :
	#print v
	#print "|" +v['type']+"|" +v['name']+"|" ,v['id'],"|" ,v['groupBy'] 
	#v['columns'] is an array of dicts with name, label keys
	pass

#-----print view contents in project as "|" separated
jData = getViewContents(viewtype,viewname,projectname)
ro=jData['viewContentsV1']
totalRows=ro['totalRows']
rrows = len(ro['rows'])
roffset= ro['offset']

headerRow=''
print 'total_rows:',totalRows
for c in ro['columns']:
	fieldsObject[str(c['label'])]=str(c['name'])
	fieldsHeader.append(str(c['label']))
for key in fieldsHeader:
	headerRow += key+" | " 
print headerRow

for rr in ro['rows']:
	for c in rr.items():
		rowObject[str(c[0])]=str(c[1])
	row=''
	for key in fieldsHeader:
		row += rowObject[fieldsObject[key]]+" | " 
	print row
	
#-----print view contents in project as CSV
lines=getViewContentsCSV(viewtype,viewname,projectname)
for line in lines:
	print line
	