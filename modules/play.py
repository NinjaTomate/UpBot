import variables, urllib, json as simplejson, string, HTMLParser
def play(send_data, msgarr, user):
	if len(msgarr) < 2:
		send_data("PRIVMSG %s :No or invalid search string supplied." % variables.channel)
	else:
		try:
			playurl=""
			parser = HTMLParser.HTMLParser()
			query=string.join(msgarr)[6:]
			url = "http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=%s&api_key=112d55ba79c51c8509a4ef500716165f&limit=1&format=json" % query
			print query
			json = simplejson.load(urllib.urlopen(url))
			print json
			try:
				artist = parser.unescape(json['recenttracks']['track'][0]['artist']['#text'])
				title = parser.unescape(json['recenttracks']['track'][0]['name'])
			except:
				artist = parser.unescape(json['recenttracks']['track']['artist']['#text'])
				title = parser.unescape(json['recenttracks']['track']['name'])
			print artist
			url = "http://ws.spotify.com/search/1/track.json?q="
			query = "%s %s" % (artist, title)
			json = simplejson.load(urllib.urlopen(url+query))
			for entry in json['tracks']:
				print entry['name']
				print title
				print len(entry['name'])
				print len(title)
				if entry['name'].lower() == title.lower():
					print "TRUE"
					playurl = "http://open.spotify.com/track/%s" % entry['href'].split(":")[2]
			print "%s - %s" % (artist, title)
			send_data("PRIVMSG %s :%s: %s" % (variables.channel, user, playurl))
		except Exception as e:
			print e
			send_data("PRIVMSG %s :%s" % (variables.channel, "An error happened."))
def help(send_data):
	send_data("PRIVMSG %s :Links user's currently playing song. Usage: .play [lastfm user]"  % variables.channel)
