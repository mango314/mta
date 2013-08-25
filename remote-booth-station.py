import pymongo
from pymongo import MongoClient
import simplejson as json
import datetime

client = MongoClient()
db = client.OGP
station = db.mta_station
turnstile = db.mta_turnstile


def RBS():
	'''rbs = file("Remote-Booth-Station.csv")
	#cats = rbs.readline()[:-1].split(',')

	for x in rbs.readlines():
		z = x[:-1].split(',')
		rbs = {'remote':z[0],'booth':z[1],'station':z[2],'lines':list(z[3]),'division':z[4]}
		station.insert(rbs)

	print station.find_one()
	print station.count()'''
	return station.find()


# Ex. #1 All stations serviced by a particular line
def line( D ):
	sta = {}
	for x in station.aggregate( [{"$unwind": "$lines"} , {"$match":{"lines": D }}])['result']:
		if x['station'] not in sta.keys():
			sta[x['station']] = []
		sta[x['station']] += [ {"remote": x['remote'] , "booth": x['booth']  } ]
	return sta

# Ex. #2 All booths at a particular station

def booths( stationName ):
	# occasionally same station has two names
	stop = station.find( {"station": stationName }, {"division":1, "remote":1, "lines":1, "_id":0, "booth":1, "station":1  })
	
	return { "division": stop[0]["division"], 
	"lines": stop[0]["lines"], 
	"station": stop[0]["station"],'RB':
	[{"booth":x['booth'], "remote": x['remote']} for x in stop] }

# Ex. #3 load turnstile data into mongo


def load_turnstile():
	turnstile.remove()
	t = file('turnstile_130803.txt')
	cur = None
	row = None
	for x in t.readlines():
		z = x.replace(' ', '')[:-2].split(',')

		if( z[0] != cur):
			if(row):
				print "insert row", z[:3]
				turnstile.insert(row)
			turnstileReading = []

		cur = z[0]
		for x in range((len(z)-3)/5):
			c = 3 + 5*x
			date = [int(w) for w in z[c].split('-')]
			hour = [int(w) for w in z[c+1].split(':')]
			turnstileReading += [
				{'date':datetime.datetime(2000 + date[2], date[0], date[1], hour[0], hour[1], hour[2]), 
				'time':z[c+1],  'status': z[c+2], 'in': int(z[c+3]), 'out': int(z[c+4]) }
			]
		row = {'booth':z[0], 'remote': z[1], 'code': z[2], 'readings': turnstileReading}
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
		cleaned[x] = [{'hour': (y['date']-first['date']).total_seconds(), 'in': y['in']- first['in'], 'out': y['out'] - first['out']  } for y in result[x]]
	return cleaned



def ridesByStation():
	w = {}
	for x in stat('KINGSBRIDGE RD')['RB']:
		result = timeSeries(x['booth'])
		w = dict(w.items() + scrub(result).items())
	#print [len(w[x]) for x in w.keys()]
	for code in w.keys():
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
		w[code] = fT

	# w is a fairly clean turnstile count : every 4 hours * 7 days a week = 42 data points
	print [len(w[code]) for code in w]

	w2 = {}
	for code in w.keys():
		for i,x in enumerate(w[code][1:]):
			print {'out': x['out']-w[code][i]['out'], 'in': x['in']-w[code][i]['in'], 'hour': x['hour']}
		w2[code] = [{'out': x['out']-w[code][i]['out'], 'in': x['in']-w[code][i]['in'], 'hour': x['hour']} for i,x in enumerate(w[code][1:])]
		w2[code] = [{"out":w2[code][-1]["out"],"hour":0, "in":w2[code][-1]["in"]}] + w2[code]

	file( "bedford_park.json" , 'w').write(json.dumps([{"key":x, "values":w2[x]} for x in w.keys()]))

	# if I want merge the turnstile streams I have to "shuffle a deck of cards"
	
if __name__ == "__main__":

	print station.count()
	print RBS()
	#Dstations = line('D')
	#for x in Dstations:
	#	print x, Dstations[x]

	#print booths('161 ST-YANKEE')
	print load_turnstile()

	

