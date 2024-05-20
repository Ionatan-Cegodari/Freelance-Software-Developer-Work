import schedule
import datetime as dt
from datetime import datetime
import requests
import time
import json

# Defining global variables

# Variables that you can change to tweak program
time_to_sleep_between_internet_connectivity_checks_seconds = 1

# currently not implemented in the program
time_before_race_to_fallback_odds_seconds = 7


# Matchbook urls
login_url = "https://api.matchbook.com/bpapi/rest/security/session"
market_info_url = "https://api.matchbook.com/edge/rest/events/"  # append eventID then "/markets/" then marketID
place_offer_url = "https://www.matchbook.com/edge/rest/v2/offers"


# Login handling information.
login_response = None
session_token = 0
headers = {}
#Class variables initiation
GreyHoundNames = []
MainDogsUsed = []
matchbookDogNames = []
main_runner_id = []
mainOddsList = []
dogNumberList =[]
chosenTime = "10:00:00"
endTime = "23:00:00"

def TodaysDate():
	global querystring, currentDate, currentTime, DateandTimeNow
	currentDate = dt.date.today()  # this assigns current date and auto updates
	now = datetime.now()
	currentTime = now.strftime("%H:%M:%S")
	DateandTimeNow = now.strftime("%Y-%m-%d %H:%M")

#This is where it all logs in so that we can access odds and all that
def connected_to_internet(url='http://www.google.com/', timeout=10):
    try:
        _ = requests.get(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        print("No internet connection available.")
        print(" ")
    return False

def login():
	global session_token, login_request, headers, login_url

	while not connected_to_internet():
		time.sleep(time_to_sleep_between_internet_connectivity_checks_seconds)

	credentials = {
		"username": "***********",
		"password": "***********"
	}

	login_request = requests.post(login_url, json=credentials)

	while login_request.status_code != 200:
		login_request = requests.post(login_url, json=credentials)

		if login_request.status_code != 200:
			print("Login failed on code: " +
				  str(login_request.status_code) + ". Retrying...")
			time.sleep(2)

	session_token = login_request.headers['session-token']
	headers = {
		'content-type': "application/json", 'session-token': session_token
	}
	print("Login successful.")
	print("Session token:")
	print(login_request.headers['session-token'])



def getOdds(): # this method gets the odds from the api
	try:
		headers = {
			"X-RapidAPI-Key": "dcdcfe1114msh91aeaf7b19bb1fcp10f036jsn3355a594e181",
			"X-RapidAPI-Host": "greyhound-racing-uk.p.rapidapi.com"
		}

		GreyhoundAPI = "https://greyhound-racing-uk.p.rapidapi.com/racecards"
		querystring = {"date": currentDate}

		Racecards_data = requests.request("GET", GreyhoundAPI, headers=headers, params=querystring)
		Racecards_decoded = json.loads(Racecards_data.text)
		time.sleep(1)
		print(Racecards_decoded)
		for id in Racecards_decoded:

			ids = id["id_race"]
			greyhoundEvents = "https://greyhound-racing-uk.p.rapidapi.com/race/" + ids
			greyhoundEvents_data = requests.request("GET", greyhoundEvents, headers=headers, params=querystring)
			greyhoundEvents_decoded = json.loads(greyhoundEvents_data.text)
			print(greyhoundEvents_decoded)
			time.sleep(1)

			try:
				if greyhoundEvents_decoded["greyhounds"]:
					for dog in greyhoundEvents_decoded["greyhounds"]:

						for num in dog["number"]:  # gets the dog numbers
							dogNumber = num
							convertedNumber = int(dogNumber)
							print("Dog Number ", convertedNumber)
							print("")
							dogNumberList.append(convertedNumber)

						if dog["odds"] == None:
							dogNumberList.clear

						for odd in dog["odds"]:
							dogName = dog["greyhound"].lower()
							print(dogName)
							print(odd["odd"])

							currentOdds = odd["odd"]
							bookie = odd["bookie"]
							if bookie == "BoyleSports":  # this makes it so that the odds are only extracted from the Boyle sports
								print(dog["greyhound"])
								print("")
								print("    Bookie: " + bookie)
								print("    Odds: " + currentOdds)
								print("")
								convertedOdds = float(currentOdds)

								if convertedOdds <= 5:
									if dogName in matchbookDogNames:
										if 9 in dogNumberList:
											print("Dog Placement Less Than 8")
											print("successful")
											print("    Bookie: " + bookie)
											print("    Odds: " + convertedOdds)

											calculatedOdds = convertedOdds

											mainOddsList.append(calculatedOdds)  # this is where i put in the odds that passed into the list
											GreyHoundNames.append(dogName)

											dogNumberList.clear()
										else:
											if dogName in matchbookDogNames:
												print("Dog Placement Less Than 8")
												print("successful")
												print("    Bookie: " + bookie)
												print("    Odds: " + currentOdds)

												calculatedOdds = convertedOdds #maths brie

												mainOddsList.append(calculatedOdds)  # this is where i put in the odds that passed into the list
												GreyHoundNames.append(dogName)

												dogNumberList.clear()
							elif bookie == "UniBet":
								print(dog["greyhound"])
								print("")
								print("    Bookie: " + bookie)
								print("    Odds: " + currentOdds)
								print("")
								convertedOdds = float(currentOdds)

								if convertedOdds <= 5:
									if dogName in matchbookDogNames:
										if 9 in dogNumberList:
											print("Dog Placement Less Than 8")
											print("successful")
											print("    Bookie: " + bookie)
											print("    Odds: " + convertedOdds)

											calculatedOdds = convertedOdds - 1 # maths brie
											calculatedOdds1 = calculatedOdds * 2 # maths brie
											calculatedOdds2 = calculatedOdds1 + 1 # maths brie

											mainOddsList.append(calculatedOdds2)  # this is where I put in the odds that passed into the list
											GreyHoundNames.append(dogName)

											dogNumberList.clear()
										else:
											if dogName in matchbookDogNames:
												print("Dog Placement Less Than 8")
												print("successful")
												print("    Bookie: " + bookie)
												print("    Odds: " + currentOdds)

												calculatedOdds = convertedOdds - 1 # maths brie
												calculatedOdds1 = calculatedOdds * 2 # maths brie
												calculatedOdds2 = calculatedOdds1 + 1  # maths brie

												mainOddsList.append(calculatedOdds2)  # this is where i put in the odds that passed into the list
												GreyHoundNames.append(dogName)

												dogNumberList.clear()
							elif bookie == "Bet365":
								print(dog["greyhound"])
								print("")
								print("    Bookie: " + bookie)
								print("    Odds: " + currentOdds)
								print("")
								convertedOdds = float(currentOdds)

								if convertedOdds <= 5:
									if dogName in matchbookDogNames:
										if 9 in dogNumberList:
											print("Dog Placement Less Than 8")
											print("successful")
											print("    Bookie: " + bookie)
											print("    Odds: " + convertedOdds)

											calculatedOdds = convertedOdds - 1 # maths brie
											calculatedOdds1 = calculatedOdds * 2 # maths brie
											calculatedOdds2 = calculatedOdds1 + 1 # maths brie

											mainOddsList.append(calculatedOdds2)  # this is where I put in the odds that passed into the list
											GreyHoundNames.append(dogName)

											dogNumberList.clear()
										else:
											if dogName in matchbookDogNames:
												print("Dog Placement Less Than 8")
												print("successful")
												print("    Bookie: " + bookie)
												print("    Odds: " + currentOdds)

												calculatedOdds = convertedOdds - 1 # maths brie
												calculatedOdds1 = calculatedOdds * 2 # maths brie
												calculatedOdds2 = calculatedOdds1 + 1  # maths brie

												mainOddsList.append(calculatedOdds2)  # this is where i put in the odds that passed into the list
												GreyHoundNames.append(dogName)

												dogNumberList.clear()
			except Exception:
				print()
				print("**Out of pings**")
				print()
	except Exception:
		print()
		print("**Out of pings**")
		print()


def matchDogs():
	global headers

	dog_url = "https://api.matchbook.com/edge/rest/events?offset=0&per-page=20&sport-ids=241798357140019&states=open%2Csuspended%2Cclosed%2Cgraded&exchange-type=back-lay&odds-type=DECIMAL&include-prices=false&price-depth=3&price-mode=expanded&include-event-participants=false&exclude-mirrored-prices=false"

	dog_url_response = requests.get(dog_url, headers=headers)
	dog_url_decoded = json.loads(dog_url_response.text)

	for id in dog_url_decoded["events"]: # this gets the ids for events and then puts them in for events and markets
		ids = id["id"]
		convertedIds = str(ids)
		markets_url = "https://api.matchbook.com/edge/rest/events/" + convertedIds + "/markets?offset=0&per-page=20&states=open%2Csuspended&exchange-type=back-lay&odds-type=DECIMAL&include-prices=false&price-depth=3&price-mode=expanded&exclude-mirrored-prices=false"

		markets_response = requests.get(markets_url, headers=headers)
		markets_response_decoded = json.loads(markets_response.text)

		if "markets" in markets_response_decoded:
			for marketId in markets_response_decoded["markets"]:

				if marketId["name"] == "WIN":
					for runner in marketId["runners"]:

						name = runner["name"].lower()

						main_names = name.replace('0', '').replace('1', '').replace('2', '').replace('3', '').replace('4','').replace('5', '').replace('6', '').replace('7', '').replace('8', '').replace('9', '').replace('10', '').replace('11', '').replace(':', '')
						strippedNames = main_names.strip()

						print(strippedNames)
						matchbookDogNames.append(strippedNames)


def RunnerID():
	global headers
	sizeOfList = len(GreyHoundNames)
	print(sizeOfList)
	iteration = 0
	mainIteration = 0
	while mainIteration <= sizeOfList - 1:

		if mainIteration == 0:
			iteration = iteration
		else:
			iteration = iteration + 1

		dog_url = "https://api.matchbook.com/edge/rest/events?offset=0&per-page=20&sport-ids=241798357140019&states=open%2Csuspended%2Cclosed%2Cgraded&exchange-type=back-lay&odds-type=DECIMAL&include-prices=false&price-depth=3&price-mode=expanded&include-event-participants=false&exclude-mirrored-prices=false"

		dog_url_response = requests.get(dog_url, headers=headers)
		dog_url_decoded = json.loads(dog_url_response.text)

		for id in dog_url_decoded["events"]:  # this gets the ids for events and then puts them in for events and markets
			ids = id["id"]
			convertedIds = str(ids)
			markets_url = "https://api.matchbook.com/edge/rest/events/" + convertedIds + "/markets?offset=0&per-page=20&states=open%2Csuspended&exchange-type=back-lay&odds-type=DECIMAL&include-prices=false&price-depth=3&price-mode=expanded&exclude-mirrored-prices=false"

			markets_response = requests.get(markets_url, headers=headers)
			markets_response_decoded = json.loads(markets_response.text)

			if "markets" in markets_response_decoded:
				for marketId in markets_response_decoded["markets"]:

					if marketId["name"] == "WIN":
						for runner in marketId["runners"]:
							name = runner["name"].lower()
							runner_id = runner["id"]

							main_name = name.replace('0', '').replace('1', '').replace('2', '').replace('3', '').replace('4', '').replace('5', '').replace('6', '').replace('7', '').replace('8', '').replace('9','').replace('10', '').replace('11', '')
							strippedName = main_name.strip()

							if strippedName == GreyHoundNames[iteration]:
								print(iteration)
								print(strippedName)
								print(runner_id)
								main_runner_id.append(runner_id)
								mainIteration = mainIteration + 1

def offerOdds(): #this is where it offer odds
	global headers, place_offer_url
	iteration = 0;

	try:
		for Mainodds in mainOddsList:  # goes through each odd and offers that odd

			stake = 0.3

			if (main_runner_id == None):
				print("There were no runner id's matched")
			else:
				print("Offering lay.")

				new_offer = {
					"odds-type": "DECIMAL",
					"exchange-type": "back-lay",
					"offers": [
						{
							"odds": Mainodds,
							"runner-id": main_runner_id[iteration],
							"side": "lay",
							"stake": float(stake),
							"keep-in-play": False,
						}
					]
				}

				iteration = iteration + 1;

				print(new_offer)
				offer_response = requests.post(place_offer_url, json=new_offer, headers=headers)

				if offer_response.status_code != 200:
					print("Offer posting failed: status code " + str(offer_response.status_code))
					print("Tried to offer")
					print("No Money")
					print(offer_response.text)
					print(" ")
				elif offer_response.status_code == 200:
					print("Offer posted successfully")
					offer_response_json = offer_response.json()
					print("Status:")
					print(offer_response_json['offers'][0]['status'])
					print(" ")
	except Exception:
		print("Index out, nothing left to offer")

def MainRunLoop():
	TodaysDate()

	if currentTime >= chosenTime:

		x = 0

		while x == 0:

			TodaysDate()
			login()
			matchDogs()
			getOdds()
			RunnerID()
			print("")
			print(mainOddsList)
			print(GreyHoundNames)
			print(matchbookDogNames)
			print("")
			offerOdds()

			# Login handling information.
			login_response = None
			session_token = 0
			headers = {}
			# Class variables initiation
			GreyHoundNames = []
			main_runner_id = []
			matchbookDogNames = []
			mainOddsList = []
			dogNumberList = []

			time.sleep(3600)

			if currentTime >= endTime:
				time.sleep(39600)
	else:
		time.sleep(7200)
		MainRunLoop()

TodaysDate()

if currentTime >= chosenTime:

	x = 0

	while x == 0:

		TodaysDate()
		login()
		matchDogs()
		getOdds()
		RunnerID()
		print("")
		print(mainOddsList)
		print(GreyHoundNames)
		print(matchbookDogNames)
		print("")
		offerOdds()

		# Login handling information.
		login_response = None
		session_token = 0
		headers = {}
		#Class variables initiation
		GreyHoundNames = []
		main_runner_id = []
		matchbookDogNames = []
		mainOddsList = []
		dogNumberList =[]

		time.sleep(3600)

		if currentTime >= endTime:

			time.sleep(39600)
else:
	time.sleep(7200)
	MainRunLoop()

