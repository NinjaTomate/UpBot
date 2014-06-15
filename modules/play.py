import variables, urllib, json as simplejson, string, HTMLParser, os

def play(send_data, msgarr, user):
    if len(msgarr) < 2:
        lastfm = simplejson.load(open("lastfm.json", "r"))
        if user in lastfm:
            username = lastfm[user]
        else:
            send_data("PRIVMSG %s :No or invalid search string supplied." % variables.channel)
    else:
        username = string.join(msgarr)[6:]
    if username != "":
        query = username
        try:
            playurl = ""
            parser = HTMLParser.HTMLParser()
            url = "http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=%s&api_key=%s&limit=1&format=json" % (query, variables.lastFMKey)
            variables.debug(query, 3)
            json = simplejson.load(urllib.urlopen(url))
            variables.debug(json, 3)

            try:
                artist = parser.unescape(json['recenttracks']['track'][0]['artist']['#text'])
                title = parser.unescape(json['recenttracks']['track'][0]['name'])
            except:
                artist = parser.unescape(json['recenttracks']['track']['artist']['#text'])
                title = parser.unescape(json['recenttracks']['track']['name'])

            variables.debug(artist)
            url = "http://ws.spotify.com/search/1/track.json?q="
            query = "%s %s" % (artist, title)
            json = simplejson.load(urllib.urlopen(url + query))

            for entry in json['tracks']:
                variables.debug(entry['name'], 3)
                variables.debug(title, 3)
                variables.debug(len(entry['name']), 3)
                variables.debug(len(title), 3)

                if entry['name'].lower() == title.lower():
                    variables.debug("TRUE", 3)
                    playurl = "http://open.spotify.com/track/%s" % entry['href'].split(":")[2]

            variables.debug("%s - %s" % (artist, title), 3)

            send_data("PRIVMSG %s :%s: %s" % (variables.channel, user, playurl))
        except Exception as e:
            print e
            send_data("PRIVMSG %s :%s" % (variables.channel, "An error happened."))

def help(send_data):
    send_data("PRIVMSG %s :Links user's currently playing song. Usage: .play [lastfm user]"  % variables.channel)
