from bs4 import BeautifulSoup as bs
import urllib
import os
import sys
import unicodedata
import re
import datetime
import webbrowser


url = 'http://matchcenter.mlssoccer.com'

soup = bs(urllib.urlopen(url), "html.parser")

for link in soup.findAll('a', {'class': 'ml-link'}):
    try:
        print link['href']
    except KeyError:
        pass

print "Select this weeks game: "

game = raw_input()

match = re.search(r'\d{4}-\d{2}-\d{2}', game)
match = datetime.datetime.strptime(match.group(), '%Y-%m-%d').date()
match = str(match)
match = match.replace("-","")
date = match[2:]

boxscore = url + game + "/boxscore"

print "                                   "
print "                                   "
webbrowser.open( str(boxscore) )

soup = bs(urllib.urlopen(boxscore), "html.parser")
home      = soup.select('.sb-home .sb-club-name-short')[0].text
away      = soup.select('.sb-away .sb-club-name-short')[0].text
length    = len(soup.select('div.match-info > div'))
# capacity  = soup.select('div.match-info > div:nth-of-type(' + str(length - 1) + ')'.text
# weather   = soup.select('div.match-info > div:nth-of-type(' + str(length) + ')'.text
event     = "MLS Regular Season"

if home == "LA":
  home = "LAG"
if away == "LA":
  away = "LAG"
if home == "DC":
  home = "DCU"
if away == "DC":
  away = "DCU"
if home == "NY":
  home = "NYR"
if away == "NY":
  away = "NYR"

homePlayers = []
awayPlayers = []

table = soup.find_all("table", class_="ps-table")

tablePlayers1 = table[0].find_all("td", class_="ps-name")
for player in tablePlayers1:
  homePlayers.append(player("a")[0].text)

tablePlayers2 = table[1].find_all("td", class_="ps-name")
for player in tablePlayers2:
  awayPlayers.append(player("a")[0].text)

goals = soup.select('table.bx-goals')
goalScorers = goals[0].select("td.bx-desc")


print "                                   "
print "                                   "
print "GOALS:                             "
print "                                   "


for test in goalScorers:
  theGoalScorer = test.select(" > span.pi-target")[0].text
  if theGoalScorer in homePlayers:
    scoreTeam = home
    line = "GOAL XXX " + scoreTeam + " " + unicodedata.normalize('NFKD', theGoalScorer).encode('ascii','ignore').upper()
  else:
    scoreTeam = away
    line = "GOAL XXX " + scoreTeam + " " + unicodedata.normalize('NFKD', theGoalScorer).encode('ascii','ignore').upper()
  try:
      assit = test.findAll('div', {'class': 'bx-assist'})
      for player in assit:
        theAssit = player.select("span.pi-target")
        for x in theAssit:
          line += ", ASST " + scoreTeam + " " + unicodedata.normalize('NFKD', x.text).encode('ascii','ignore').upper()
  except KeyError:
      pass

  print line


print "                                   "
print "                                   "
print "CARDS:                             "
print "                                   "


bookings = soup.select('table.bx-bookings')
bookings = bookings[0].select("tr")
for x in bookings:
  try:
    if(x.select("td.bx-icon > div.bx-yellow")):
      card = "YELLOW "
  except KeyError:
    pass
  try:
    if(x.select("td.bx-icon > div.bx-straightred")):
      card = "RED "
  except KeyError:
    pass
  try:
    if(x.select("td.bx-icon > div.bx-red")):
      card = "RED "
  except KeyError:
    pass
  foulPlayer = x.select("td.bx-desc > span.pi-target")[0].text

  if foulPlayer in homePlayers:
    scoreTeam = home
    line = card + scoreTeam + " " + unicodedata.normalize('NFKD', foulPlayer).encode('ascii','ignore').upper()
  else:
    scoreTeam = away
    line = card + scoreTeam + " " + unicodedata.normalize('NFKD', foulPlayer).encode('ascii','ignore').upper()
  print line

teamData = dict(
CHI = {'city': 'Bridgeview', 'state': 'Illinois', 'country': 'USA', 'stadium': 'Toyota Park'},
CLB = {'city': 'Columbus', 'state': 'Ohio', 'country':  'USA', 'stadium': 'Columbus Crew stadium'},
COL = {'city': 'Commerce', 'state': 'Colorado', 'country':  'USA', 'stadium': "Dick's Sporting Goods Park"},
DAL = {'city': 'Frisco', 'state': 'Texas', 'country': 'USA', 'stadium': 'Toyota Stadium'},
DCU = {'city': 'Washington', 'state': 'D.C.', 'country':  'USA', 'stadium': 'RFK Stadium'},
HOU = {'city': 'Houston', 'state':'Texas', 'country': 'USA', 'stadium': 'BBVA Compass Stadium'},
LAG = {'city': 'Carson', 'state': 'California', 'country': 'USA', 'stadium': 'StubHub Center'},
MTL = {'city': 'Montreal', 'state': 'QC', 'country':  'Canada', 'stadium': 'Saputo Stadium'},
NE  = {'city': 'Foxborough', 'state': 'Massachusetts', 'country': 'USA', 'stadium': 'Gillette Stadium'},
NYR = {'city': 'Harrison', 'state': 'New Jersey', 'country':  'USA', 'stadium': 'Red Bull Arena'},
NYC = {'city': 'New York City', 'state': 'New York', 'country':  'USA', 'stadium': 'Yankees Stadium'},
ORL = {'city': 'Orlando', 'state': 'Florida', 'country': 'USA', 'stadium': 'Citrus Bowl'},
PHI = {'city': 'Chester', 'state': 'Pennsylvania', 'country':  'USA', 'stadium': 'PPL Park'},
POR = {'city': 'Portland', 'state': 'Oregan', 'country':  'USA', 'stadium': 'Jeld-Wen Field'},
RSL = {'city': 'Sandy', 'state': 'Utah', 'country':  'USA', 'stadium': 'Rio Tinto Stadium'},
SEA = {'city': 'Seattle', 'state': 'Washington', 'country':  'USA', 'stadium': 'CenturyLink Field'},
SJ  = {'city': 'Santa Clara', 'state': 'California', 'country':  'USA', 'stadium': 'Avaya Stadium'},
SKC = {'city': 'Kansas City', 'state': 'Kansas', 'country':  'USA', 'stadium': 'Childrens Mercy Park'},
TOR = {'city': 'Toronto', 'state': 'Ontario', 'country': 'Canada', 'stadium': 'BMO Field'},
VAN = {'city': 'Vancouver', 'state': 'British Columbia', 'country': 'Canada', 'stadium': 'BC Place'},
)

time = soup.select(".sb-match-time")[0].text
city = teamData[home]['city']
state = teamData[home]['state']
country = teamData[home]['country']
stadium = teamData[home]['stadium']
logger = "Roxbury"
shooter = "Broadcast"


print "                                   "
print "                                   "
print "DATA:                              "
print "                                   "


print "Away Team: %s"       % away
# print "Capacity: %s"        % capacity
print "The City: %s"        % city
print "The Country: %s"     % country
print "Game Date: %s"       % date
print "Description: %s"     % event
print "Event: %s"           % event
print "Game Date: %s"       % date
print "Home Team: %s"       % home
print "Logger: %s"          % logger
print "Shooter: %s"         % shooter
print "The Stadium: %s"     % stadium
print "The State: %s"       % state
print "Game Time: %s"       % time
# print "Weather: %s"         % weather

print "                                   "
print "                                   "

lineup = url + game + "/lineup"

soup = bs(urllib.urlopen(lineup), "html.parser")

managers = soup.select("table.manager-table td.name")

i = 0
for manager in managers:
  if (i == 0):
    print home + " " + manager.text.upper() + " COACH"
  else:
    print away + " " + manager.text.upper() + " COACH"
  i += 1











