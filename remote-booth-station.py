import pymongo
from pymongo import MongoClient
client = MongoClient()
db = client.OGP

station = db.mta_station

def RBS():
	rbs = file("Remote-Booth-Station.csv")
	cats = rbs.readline()[:-1].split(',')

	for x in rbs.readlines():
		z = x[:-1].split(',')
		#rbs = "{'remote':%s,'booth':%s,'station':%s,'lines':%s,'division':%s}"%(z[0], z[1], z[2], list(z[3]), z[4])
		rbs = {'remote':z[0],'booth':z[1],'station':z[2],'lines':list(z[3]),'division':z[4]}
		station.insert(rbs)

	print station.find_one()
	print station.count()

print station.count()
# Ex. #1 All stations serviced by a particular line
def line( D ):
	sta = {}
	for x in station.aggregate( [{"$unwind": "$lines"} , {"$match":{"lines": D }}])['result']:
		if x['station'] not in sta.keys():
			sta[x['station']] = []
		sta[x['station']] += [ {"remote": x['remote'] , "booth": x['booth']  } ]
	return sta

# Ex. #2 All booths at a particular station

def stat( name ):
	stop = station.find( {"station": name }, {"division":1, "remote":1, "lines":1, "_id":0, "booth":1, "station":1  })
	return { "division": stop[0]["division"], 
	"lines": stop[0]["lines"], 
	"station": stop[0]["station"],'RB':
	[{"booth":x['booth'], "remote": x['remote']} for x in stop] }

# Ex. #3 load turnstile data into mongo
import datetime
turnstile = db.mta_turnstile
def load_turnstile():
	t = file('turnstile_130803.txt')
	for x in t.readlines():
		z = x.replace(' ', '')[:-2].split(',')
		print z[:3]
		for x in range((len(z)-3)/5):
			c = 3 + 5*x
			date = [int(w) for w in z[c].split('-')]
			hour = [int(w) for w in z[c+1].split(':')]
			row = {'remote': z[0], 'booth': z[1], 'code': z[2], 
			'date':datetime.datetime(2000 + date[2], date[0], date[1], hour[0], hour[1], hour[2]), 'time':z[c+1],  'status': z[c+2], 'in': int(z[c+3]), 'out': int(z[c+4]) }
			turnstile.insert(row)
	return turnstile.count()

# Ex. #4 Get turnstile data by Remote
t = turnstile.find({'remote':"A002", 'status':'REGULAR'}, {'_id':0, 'in':1, 'date':1, 'code':1, 'out':1})
result = {}
for x in t:
	if x['code'] not in result.keys():
		result[x['code']] = []
	result[x['code']] += [x]
for x in result.keys():
	for y in result[x]:
		print y
	print '\n\n'
