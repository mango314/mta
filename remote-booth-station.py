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
def timeSeries(remote):
	t = turnstile.find({'remote':remote, 'status':'REGULAR'}, {'_id':0, 'in':1, 'date':1, 'code':1, 'out':1})
	result = {}
	for x in t:
		if x['code'] not in result.keys():
			result[x['code']] = []
		result[x['code']] += [{'date': x['date'],'in':int(x['in']), 'out': int(x['out'])}]
	return result

def scrub(result):
	cleaned = {}
	for x in result.keys():
		first = result[x][0]
		cleaned[x] = [{'hour': y['date'].hour/4, 'in': y['in']- first['in'], 'out': y['out'] - first['out']  } for y in result[x]]
	return cleaned


if __name__ == "__main__":
	w = {}
	for x in stat('KINGSBRIDGE RD')['RB']:
		result = timeSeries(x['booth'])
		w = dict(w.items() + scrub(result).items())
	#print [len(w[x]) for x in w.keys()]
	'''for code in w.keys():
		count = 0
		turnstile = w[code]
		fT = []
		for i,x in enumerate(turnstile[:-1]):
			if x['hour'] != turnstile[i+1]['hour']:
				print count, x
				count += 1
				fT += [x]
			#if count % 6 == 0: print
		print count, turnstile[-1]
		print
		fT += [turnstile[-1]]
		w[code] = fT'''

	# w is a fairly clean turnstile count : every 4 hours * 7 days a week = 42 data points
	print [len(w[code]) for code in w]

	# if I want merge the turnstile streams I have to "shuffle a deck of cards"
	


