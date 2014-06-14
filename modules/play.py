import variables, urllib, json as simplejson, string, HTMLParser

def play(send_data, msgarr, user):
	if len(msgarr) < 2:
		send_data("PRIVMSG %s :No or invalid search string supplied." % variables.channel)
	else:
		try:
			playurl = ""
			parser = HTMLParser.HTMLParser()
			query = string.join(msgarr)[6:]
			url = "http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=%s&api_key=112d55ba79c51c8509a4ef500716165f&limit=1&format=json" % query
			debug(query, 3)
			json = simplejson.load(urllib.urlopen(url))
			debug(json, 3)

			try:
				artist = parser.unescape(json['recenttracks']['track'][0]['artist']['#text'])
				title = parser.unescape(json['recenttracks']['track'][0]['name'])
			except:
				artist = parser.unescape(json['recenttracks']['track']['artist']['#text'])
				title = parser.unescape(json['recenttracks']['track']['name'])

			debug(artist)
			url = "http://ws.spotify.com/search/1/track.json?q="
			query = "%s %s" % (artist, title)
			json = simplejson.load(urllib.urlopen(url + query))

			for entry in json['tracks']:
				debug(entry['name'], 3)
				debug(title, 3)
				debug(len(entry['name']), 3)
				debug(len(title), 3)

				if entry['name'].lower() == title.lower():
					debug("TRUE", 3)
					playurl = "http://open.spotify.com/track/%s" % entry['href'].split(":")[2]

			debug("%s - %s" % (artist, title), 3)

			send_data("PRIVMSG %s :%s: %s" % (variables.channel, user, playurl))
		except Exception as e:
			print e
			send_data("PRIVMSG %s :%s" % (variables.channel, "An error happened."))

def help(send_data):
	send_data("PRIVMSG %s :Links user's currently playing song. Usage: .play [lastfm user]"  % variables.channel)
