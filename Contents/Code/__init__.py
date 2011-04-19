# Plex Game Launcher Plugin
# by Nudgenudge <nudgenudge@gmail.com>

import os,subprocess,re,sqlite3
from PMS import *

MAIN_PATH  = "/Applications/Game Launcher"
EMU_ROOT   = os.path.expanduser('%s/Emulators' % (MAIN_PATH))
ROM_ROOT   = os.path.expanduser('%s/ROMs' % (MAIN_PATH))
API_KEY = "9d8ec266a4043716015d4be2857d62c89b69f462"
# to remove if I can select from DB
SELECT_CONNECTION = None

####################################################################################################
def Start():
	global SELECT_CONNECTION
	MediaContainer.thumb = R("icon-default.png")
	MediaContainer.art = R("art-default.png")
	DirectoryItem.thumb = R("icon-default.png")
	DirectoryItem.art = R("art-default.png")
	# dummy Select to create the DB if not created yet
	Database.Exec("SELECT game_id, console FROM games;")
	Database.Commit()
	SELECT_CONNECTION = sqlite3.connect(Database.__databasePath)
	
	
####################################################################################################
@handler("/applications/gamelauncher", "Game Launcher")
def MainMenu():
	dir = MediaContainer(title1="Game Launcher")
	dir.Append(Function(DirectoryItem(GetAllGamesList, title="All Games")))
	dir.Append(Function(DirectoryItem(GetConsoleList, title="Console")))
	dir.Append(Function(DirectoryItem(GetGenreList, title="Genre")))
	dir.Append(Function(DirectoryItem(GetYearList, title="Year")))
	dir.Append(Function(DirectoryItem(GetPublisherList, title="Publisher")))
	dir.Append(Function(DirectoryItem(RefreshDB, title="Refresh Game List")))
	return dir
	
####################################################################################################
def RefreshDB(sender, query=None):
	CleanUpRoms()
	FillRoms()
	MainMenu()

####################################################################################################
def GetAllGamesList(sender, query=None):
	dir = MediaContainer(title1=sender.title1, title2=sender.itemTitle)
	for game in SELECT_CONNECTION.execute("SELECT * FROM games;"):
		subtitle=""
		if game[5] != None:
			subtitle += game[5]
		if game[6] != None:
			if subtitle != "":
				subtitle += " - "
			subtitle += "%s" % (game[6])
		if game[7] != None:
			if subtitle != "":
				subtitle += " - "
			subtitle += game[7]
		dir.Append(Function(DirectoryItem(StartEmulator,
									      title=game[1],
										  infoLabel=game[2],
										  thumb=game[3],
										  summary=game[4],
										  subtitle=subtitle),
							 console=game[2],
							 rom=game[0]))
	dir.Sort("name")
	return dir
					
####################################################################################################
def GetConsoleList(sender, query=None):
	dir = MediaContainer(title1=sender.title1, title2=sender.itemTitle)
	for console in SELECT_CONNECTION.execute("SELECT distinct console FROM games ORDER BY console;"):
		dir.Append(Function(DirectoryItem(GetListForConsole, title=console[0])))
	return dir
					
####################################################################################################
def GetGenreList(sender, query=None):
	dir = MediaContainer(title1=sender.title1, title2=sender.itemTitle)
	for genre in SELECT_CONNECTION.execute("SELECT distinct genre FROM games ORDER BY genre;"):
		if (genre[0] != None):
			dir.Append(Function(DirectoryItem(GetListForGenre, title=genre[0])))
	return dir
					
####################################################################################################
def GetYearList(sender, query=None):
	dir = MediaContainer(title1=sender.title1, title2=sender.itemTitle)
	for year in SELECT_CONNECTION.execute("SELECT distinct year FROM games ORDER BY year;"):
		if (year[0] != None):
			dir.Append(Function(DirectoryItem(GetListForYear, title=("%s" % (year[0])))))
	return dir
					
####################################################################################################
def GetPublisherList(sender, query=None):
	dir = MediaContainer(title1=sender.title1, title2=sender.itemTitle)
	for publisher in SELECT_CONNECTION.execute("SELECT distinct publisher FROM games ORDER BY publisher;"):
		if (publisher[0] != None):
			dir.Append(Function(DirectoryItem(GetListForPublisher, title=publisher[0])))
	return dir
					
####################################################################################################
def GetListForConsole(sender, query=None):
	console = sender.itemTitle
	dir = MediaContainer(title1=sender.title1, title2=console)
	for game in SELECT_CONNECTION.execute("SELECT * FROM games WHERE console=?;", [console]):
		subtitle=""
		if game[5] != None:
			subtitle += game[5]
		if game[6] != None:
			if subtitle != "":
				subtitle += " - "
			subtitle += "%s" % (game[6])
		if game[7] != None:
			if subtitle != "":
				subtitle += " - "
			subtitle += game[7]
		dir.Append(Function(DirectoryItem(StartEmulator,
									      title=game[1],
										  infoLabel=game[2],
										  thumb=game[3],
										  summary=game[4],
										  subtitle=subtitle),
							 console=game[2],
							 rom=game[0]))
	dir.Sort("name")
	return dir
					
####################################################################################################
def GetListForGenre(sender, query=None):
	genre = sender.itemTitle
	dir = MediaContainer(title1=sender.title1, title2=genre)
	for game in SELECT_CONNECTION.execute("SELECT * FROM games WHERE genre=?;", [genre]):
		subtitle=""
		if game[5] != None:
			subtitle += game[5]
		if game[6] != None:
			if subtitle != "":
				subtitle += " - "
			subtitle += "%s" % (game[6])
		if game[7] != None:
			if subtitle != "":
				subtitle += " - "
			subtitle += game[7]
		dir.Append(Function(DirectoryItem(StartEmulator,
									      title=game[1],
										  infoLabel=game[2],
										  thumb=game[3],
										  summary=game[4],
										  subtitle=subtitle),
							 console=game[2],
							 rom=game[0]))
	dir.Sort("name")
	return dir
					
####################################################################################################
def GetListForYear(sender, query=None):
	year = sender.itemTitle
	dir = MediaContainer(title1=sender.title1, title2=year)
	for game in SELECT_CONNECTION.execute("SELECT * FROM games WHERE year=?;", [int(year)]):
		subtitle=""
		if game[5] != None:
			subtitle += game[5]
		if game[6] != None:
			if subtitle != "":
				subtitle += " - "
			subtitle += "%s" % (game[6])
		if game[7] != None:
			if subtitle != "":
				subtitle += " - "
			subtitle += game[7]
		dir.Append(Function(DirectoryItem(StartEmulator,
									      title=game[1],
										  infoLabel=game[2],
										  thumb=game[3],
										  summary=game[4],
										  subtitle=subtitle),
							 console=game[2],
							 rom=game[0]))
	dir.Sort("name")
	return dir
					
####################################################################################################
def GetListForPublisher(sender, query=None):
	publisher = sender.itemTitle
	dir = MediaContainer(title1=sender.title1, title2=publisher)
	for game in SELECT_CONNECTION.execute("SELECT * FROM games WHERE publisher=?;", [publisher]):
		subtitle=""
		if game[5] != None:
			subtitle += game[5]
		if game[6] != None:
			if subtitle != "":
				subtitle += " - "
			subtitle += "%s" % (game[6])
		if game[7] != None:
			if subtitle != "":
				subtitle += " - "
			subtitle += game[7]
		dir.Append(Function(DirectoryItem(StartEmulator,
									      title=game[1],
										  infoLabel=game[2],
										  thumb=game[3],
										  summary=game[4],
										  subtitle=subtitle),
							 console=game[2],
							 rom=game[0]))
	dir.Sort("name")
	return dir
	
####################################################################################################
def StartEmulator(sender, console, rom):
	gamePath = os.path.join(ROM_ROOT,console,rom)
	command = ""
	if console in ['NES']:
		command = "NES.sh"
	elif console in ['SNES']:
		command = "SNES.sh"
	elif console in ['Atari 2600']:
		command = "Atari 2600.sh"
	elif console in ['Genesis']:
		command = "Genesis.sh"
	elif console in ['Game Boy']:
		command = "Game Boy.sh"
	elif console in ['Game Boy Advance']:
		command = "Game Boy Advance.sh"
	elif console in ['Sega Master System']:
		command = "Sega Master System.sh"
	elif console in ['MAME']:
		command = "MAME.sh"
	elif console in ['Nintendo 64']:
		if (rom.find("[GLIDE]") > -1):
			command = "Nintendo 64 Glide.sh"
		else:
			command = "Nintendo 64 Rice.sh"
	PMS.Log(command + " " + gamePath)
	Helper.Run(command, gamePath)
			
####################################################################################################
def CleanUpRoms():
	for game in SELECT_CONNECTION.execute("SELECT game_id, console FROM games;"):
		gameID = game[0]
		console = game[1]
		gamePath = os.path.join(ROM_ROOT, console, gameID)
		if (not os.path.exists(gamePath)):
			PMS.Log("Removing game %s" % (gameID))
			Database.Exec("DELETE FROM games WHERE game_id=? AND console=?;", game)
	Database.Commit()

####################################################################################################
def FillRoms():
	tempGameList = SELECT_CONNECTION.execute("SELECT game_id, console FROM games;")
	gameList = []
	for game in tempGameList:
		gameList.append(game)
		
	for console in os.listdir(ROM_ROOT):
		if (console not in [".DS_Store", "BIOS_MESS"]):
			for game in os.listdir("%s/%s" % (ROM_ROOT, console)):
				if (game not in [".DS_Store"] and (game,console) not in gameList):
					gameID = os.path.splitext(game)[0]
					PMS.Log("Adding game %s" % (game))
					gameParams = FetchDataForId(game, gameID, console)
					Database.Exec("INSERT INTO games VALUES (?,?,?,?,?,?,?,?);", gameParams)
	Database.Commit()
						
####################################################################################################
def FetchDataForId(game, gameID,console):
		
	result = [game, gameID, console, R("icon-default.png"), None, None, None, None]
	try:
		if console == 'MAME':
			page = XML.ElementFromURL("http://maws.mameworld.info/maws/romset/%s" % (gameID), isHTML=True)
			
			# Name
			name = gameID
			tempName = page.xpath("//td[text()='title']/../td[last()]/text()")
			if (len(tempName) > 0):
				name = stripExtraMame(tempName[0])
				
			# Image
			thumbUrl = "http://maws.mameworld.info/img/ps/titles/%s.png" % (gameID)
			
			# Description
			description = ""
			tempDesc = page.xpath("//td[text()='history']/../td[last()]/text()")
			i = 0
			passedGameName = False
			while (i < len(tempDesc)):
				tempDescString = "%s" % (tempDesc[i])
				tempDescString = tempDescString.strip()
				if (tempDescString.find("- TECHNICAL -") != -1):
					break
				if (tempDescString != ""):
					if (not passedGameName):
						passedGameName = True
					else:
						description += tempDescString
						description += '\n\n'
				i += 1
				
			# Publisher
			publisher = None
			tempPublisher = page.xpath("//td[text()='manufacturer']/../td[last()]//text()")
			if (len(tempPublisher) > 0):
				publisher = stripExtraMame(tempPublisher[0])
				
			# Release date
			releaseDate = None
			tempReleaseDate = page.xpath("//td[text()='year']/../td[last()]//text()")
			if (len(tempReleaseDate) > 0):
				releaseDate = tempReleaseDate[0]
				
			# Genre
			genre = None
			tempGenre = page.xpath("//td[text()='genre']/../td[last()]//text()")
			if (len(tempGenre) > 0):
				genre = tempGenre[0]
				
			return [game, name, console, thumbUrl, description, publisher, releaseDate, genre]
		else:
			gameID = stripExtraMess(gameID)
			searchUrl = "http://api.giantbomb.com/search/?api_key=%s&query=%s&resources=game&field_list=name,id&format=json" % (API_KEY, String.Quote(gameID))
			searchResults = JSON.ObjectFromURL(searchUrl)
			
			for currentGame in searchResults['results']:
				queryUrl = "http://api.giantbomb.com/game/%s/?api_key=%s&field_list=name,deck,genres,releases,image,publishers&format=json" % (currentGame['id'],API_KEY)
				gameResults = JSON.ObjectFromURL(queryUrl)
				for possibleRelease in gameResults['results']['releases']:
					if compareReleaseNames(possibleRelease['name'],gameResults['results']['name']):
						releaseUrl = "http://api.giantbomb.com/release/%s/?api_key=%s&field_list=platform,image,release_date,publishers,region&format=json" % (possibleRelease['id'],API_KEY)
						releaseResults = JSON.ObjectFromURL(releaseUrl)
						if releaseResults['results']['platform']['name'] == console:
							# Name
							name = gameID
							if (gameResults['results']['name']):
								name = gameResults['results']['name']
								
							# Image
							thumbUrl = gameResults['results']['image']['super_url']
							if (releaseResults['results']['image']):
								if (releaseResults['results']['image']['super_url']):
									thumbUrl = releaseResults['results']['image']['super_url']
									
							# Description
							description = gameResults['results']['deck']
							
							# Publisher
							publisher = gameResults['results']['publishers'][0]['name']
							if (len(releaseResults['results']['publishers']) > 0):
								publisher = releaseResults['results']['publishers'][0]['name']
								
							# Release date
							releaseDate=None
							if (releaseResults['results']['release_date'] != None):
								releaseDate = releaseResults['results']['release_date'].split('-')[0]
								
							# Genre
							genre = None
							if (len(gameResults['results']['genres']) > 0):
								genre = gameResults['results']['genres'][0]['name']
							
							if (releaseResults['results']['region']['id'] == 1):
								return [game, name, console, thumbUrl, description, publisher, releaseDate, genre]
							else:
								result = [game, name, console, thumbUrl, description, publisher, releaseDate, genre]
							
	# Nothing was found
	except:
	 	PMS.Log("ROM name is invalid: %s" % (gameID))
	return result
	
####################################################################################################
def stripExtraMame(name):
	return name.split(u'(')[0].split(u'\xa9')[0].rstrip()
																
####################################################################################################
def stripExtraMess(name):
	name = name.split('[')[0].split('(')[0].rstrip()
	return re.sub('_', ' ', name)
																
####################################################################################################
def compareReleaseNames(release, game):
	gameTransformed = game.lower()
	releaseTransformed = release.lower()
	if (gameTransformed.find('the ') != -1):
		gameTransformed = gameTransformed.split('the ')[1]
	if (releaseTransformed.find('the ') != -1):
		releaseTransformed = releaseTransformed.split('the ')[1]
	if (gameTransformed.find('the ') != -1):
		gameTransformed = gameTransformed.split('the ')[1]
	if (releaseTransformed.find(', the') != -1):
		releaseTransformed = releaseTransformed.split(', the')[0]
	gameTransformed = gameTransformed.strip()
	releaseTransformed = releaseTransformed.strip()
	
	return gameTransformed == releaseTransformed
