import requests


def get_horaire(tipe, ligne, station, destination):
	"""
	take the type of transport (ex: RER, metro, ...), line (ex: 3b), stations (ex: porte des lilas), and ways (A or R)
	retrun str : either time (ex : 0mn, 5mn) or specific messages ("Train a l'approche", "Train a quai", ...)
	"""
	return requests.get("https://api-ratp.pierre-grimaud.fr/v4/schedules/"+str(tipe)+"/"+str(ligne)+"/"+str(station)+"/" + str(destination)).json()


def get_stations(tipe, ligne):
	"""
	take the type of transport (ex: RER, metro, ...), and line (ex: 3b)
	return a list of all the stations of this line
	"""
	return [a["name"] for a in requests.get("https://api-ratp.pierre-grimaud.fr/v4/stations/"+str(tipe)+"/"+str(ligne)).json()["result"]["stations"]]

def get_horaire_ligne(tipe, ligne):
	#print(get_horaire(tipe, ligne, "Chatelet", "A"))
	stations = get_stations(tipe, ligne)
	la = {}
	lr = {}
	last = 10
	if get_horaire(tipe, ligne, stations[0], "A")["result"]["schedules"][0]["destination"] != stations[0]:
		print("AAAAAAAAA")
		for a in stations:
			#print(a)
			la[a] = get_horaire(tipe, ligne, a, "A")["result"]["schedules"][0]["message"]
			#print(la[a])
		stations.reverse()
		for a in stations:
			#print(a)
			lr[a] = get_horaire(tipe, ligne, a, "R")["result"]["schedules"][0]["message"]
			#print(lr[a])
	else:
		print("RRRRRRR")
		for a in stations:
			#print(a)
			lr[a] = get_horaire(tipe, ligne, a, "R")["result"]["schedules"][0]["message"]
			#print(lr[a])
		stations.reverse()
		for a in stations:
			#print(a)
			la[a] = get_horaire(tipe, ligne, a, "A")["result"]["schedules"][0]["message"]
			#print(la[a])
	print(la)
	print(lr)


	"""
	stations = get_stations(tipe, ligne)
	for a in stations:
		print(a)
		nexte = get_horaire(tipe, ligne, a, "A")["result"]["schedules"][0]["message"]
		print(nexte)
		if nexte == "Train a l'approche" or nexte == "Service termine" or nexte == "Train a quai":
			nexte = 0
		else:
			nexte = int(nexte[0])

		print("NEXT : " + str(nexte) + " LAST : " + str(last))
		if nexte < last:
			print("TRAIN")
		last = nexte
		print("\n")
	"""
	
	return la, lr

def get_train_loc(tipe, ligne):
	la, lr = get_horaire_ligne(tipe, ligne)
	ta, tr = [], []
	last = 100
	for a, b in la.items():
		nexte = b
		if nexte == "Train a l'approche" or nexte == "Service termine" or nexte == "Train a quai":
			nexte = 0
		else:
			nexte = int(nexte[0])
		if nexte < last:
			#print(a)
			#print("TRAIN")
			ta.append([a, nexte])
		last = nexte

	print(ta)
	print("RRRRRRRRRRRRRR")
	last = 100
	for a, b in lr.items():
		nexte = b
		if nexte == "Train a l'approche" or nexte == "Service termine" or nexte == "Train a quai":
			nexte = 0
		else:
			nexte = int(nexte[0])
		if nexte < last:
			#print(a)
			#print("TRAIN")
			tr.append([a, nexte])
		last = nexte
	print(tr)


#print(requests.get("https://api-ratp.pierre-grimaud.fr/v4/stations/metros/3b").json())
#print(get_horaire("metros", "3b", "Porte des Lilas", "R"))


get_train_loc("metros", "11")