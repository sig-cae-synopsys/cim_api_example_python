import requests
import json
import sys
#
host=sys.argv[1] 		#'http://localhost:8080'
user=sys.argv[2] 		#'admin'
passcode=sys.argv[3] 	#'coverity' 
cid=sys.argv[4] 		#'10641'

def getDbQuery():
	url=host+'/diagnostics/database/query/CurrentParent' 
	r = requests.get(url,auth=(user,passcode))
	if(r.ok):
		return (json.loads(r.content))
	else:
		r.raise_for_status()
		
jData = getDbQuery()
result=jData['customQueryResult']
rows=result['rows']
columns=result['columns']
for c in columns:
	print c,'|',
print
for v in rows :
	if v['cid'] == cid:
		for c in columns:
			print v[c],'|',
		print
 