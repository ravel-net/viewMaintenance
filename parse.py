import re
prefix = ["CREATE OR REPLACE VIEW", "CREATE VIEW"]
 

def parseQueryString(query):

	def findIgnoreCase(sen,token):
		newS = sen.lower()
		token = token.lower()
		return newS.find(token)
	def splitIgnoreCase(sen, token):
		index = findIgnoreCase(sen,token)
		if(index == -1):
			return [sen]
		else:
			return [sen[:index],sen[index+len(token)+1:]]
	def getTuple(t):
		if findIgnoreCase(t,"AS") != -1:
			tt = splitIgnoreCase(t,"AS")
			return (tt[0].strip(),tt[1].strip())
		else:
			return (t.strip(), t.strip())

	query = re.sub('\s{2,}|\n|\t','',query)
	queryWithoutColon = query.split(");")[0]
	print queryWithoutColon
	for p in prefix:
		index = findIgnoreCase(queryWithoutColon,p)
		if p == -1:
			continue
		else:
			query = queryWithoutColon[len(p)+index:]
			break
	if index == -1:
		print "No prefix found"
		return
	print query

	index = findIgnoreCase(query,"AS")
	tableName = query[:index].strip()
	print "viewName: " + tableName
	index = query.find("(")
	query = query[index+1:]
	print query
	query = splitIgnoreCase(query[findIgnoreCase(query,"SELECT")+7:],"FROM")
	selectS = query[0].strip()
	query = splitIgnoreCase(query[1],"WHERE")
	fromS = query[0].strip()
	try:
		whereS = query[1].strip()
	except:
		pass
	print selectS
	print fromS
	print whereS
	
	selectResult = []
	if selectS.find(",") != -1:
		selectS = selectS.split(",")
		selectResult = dict([getTuple(t) for t in selectS])
	else:
		selectResult = dict(getTuple(selectS))
	
	fromResult = []
	if fromS.find(",") != -1:
		fromS = fromS.split(",")
		fromResult = dict([getTuple(t) for t in fromS])
	else:
		fromResult = dict(getTuple(fromS))

	print selectResult
	print fromResult
		


parseQueryString("""CREATE OR REPLACE VIEW MERLIN_violation AS (
       SELECT tm.fid, rate AS req, vol AS asgn
       FROM tm, Merlin_policy
       WHERE tm.fid = Merlin_policy.fid AND rate > vol
);""")
