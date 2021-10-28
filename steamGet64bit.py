import requests, json, sys

username = sys.argv[1] if len(sys.argv) > 1 else str(input("vanity url: "))
needDownload = sys.argv[2] if len(sys.argv) > 2 else str(input("need download avatar? (y/n): "))

def writeSteam(steamProfile):
	open(username+".json", "w").write(json.dumps(steamProfile, indent = 5))
def downloadPhoto(steamProfile):
	for i in steamProfile["response"]["players"]:
		with open(username+".png", "wb") as avatar:
			avatar.write(requests.get(i["avatarfull"]).content)
def convTime(secTime):
	from datetime import datetime
	return datetime.utcfromtimestamp(secTime).strftime(r"%H:%M:%S %d-%m-%y")

key = "" # steam api key
url = "http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key="+key+"&vanityurl="+username

steamId = requests.get(url).json()["response"]["steamid"]

url = "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key="+key+"&steamids="+steamId

steamProfile = requests.get(url).json()
steamProfile["response"]["players"][0].update({"lastlogoff":convTime(steamProfile["response"]["players"][0]["lastlogoff"])})
steamProfile["response"]["players"][0].update({"timecreated":convTime(steamProfile["response"]["players"][0]["timecreated"])})

writeSteam(steamProfile)
if needDownload == "y":
	downloadPhoto(steamProfile)
