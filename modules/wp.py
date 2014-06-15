import variables, re, string, np, json, urllib
from time import sleep
def wp(send_data, msgarr, user):
	lastfm = json.load(open("lastfm.json", "r"))
	done = False
	send_data("NAMES %s" % variables.channel)
	while not done:
		if "353" in variables.buffer or "stop" in variables.buffer:
			input = variables.buffer
			done = True
	names = string.split(input)[6:]
	for name in names:
		if re.match(r'^(\@|\&|%|\+).*', name):
			name = name[1:]
		print name
		if name in lastfm:
			print lastfm [name]
			url = "http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=%s&api_key=%s&limit=1&format=json" % (lastfm[name], variables.lastFMKey)
			lfmjson = json.load(urllib.urlopen(url))
			try:
				artist = lfmjson['recenttracks']['track'][0]['artist']['#text']
				title = lfmjson['recenttracks']['track'][0]['name']
				playstatus = "is"
			except:
				artist = lfmjson['recenttracks']['track']['artist']['#text']
				title = lfmjson['recenttracks']['track']['name']
				playstatus = "was"
			send_data("PRIVMSG %s :%s %s playing: %s - %s" % (variables.channel, name, playstatus, artist, title))