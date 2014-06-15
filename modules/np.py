import variables, urllib, json as simplejson, string, HTMLParser

def np(send_data, msgarr, user):
    username = ""

    if len(msgarr) < 2:
        lastfm = simplejson.load(open("lastfm.json", "r"))

        if user in lastfm:
            username = lastfm[user]
            listener = user
        else:
            send_data("PRIVMSG %s :No or invalid search string supplied." % variables.channel)
    else:
        username = string.join(msgarr)[4:]
        listener = username

    if username != "":
        query = username

        try:
            parser = HTMLParser.HTMLParser()
            url = "http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=%s&api_key=%s&limit=1&format=json" % (query, variables.lastFMKey)

            variables.debug(query, 3)
            json = simplejson.load(urllib.urlopen(url))
            variables.debug(json, 3)

            try:
                artist = parser.unescape(json['recenttracks']['track'][0]['artist']['#text'])
                title = parser.unescape(json['recenttracks']['track'][0]['name'])
                playstatus = "is"
            except:
                artist = parser.unescape(json['recenttracks']['track']['artist']['#text'])
                title = parser.unescape(json['recenttracks']['track']['name'])
                playstatus = "was"

            tagurl = "http://ws.audioscrobbler.com/2.0/?method=track.getTopTags&artist=%s&track=%s&api_key=%s&format=json" % (artist, title, variables.lastFMKey)
            artisttagurl = "http://ws.audioscrobbler.com/2.0/?method=artist.getTopTags&artist=%s&api_key=%s&format=json" % (artist, variables.lastFMKey)

            try:
                jsontag = simplejson.load(urllib.urlopen(tagurl))
                toptags = "("\
                        + parser.unescape(jsontag['toptags']['tag'][0]['name']) + ", "\
                        + parser.unescape(jsontag['toptags']['tag'][1]['name']) + ", "\
                        + parser.unescape(jsontag['toptags']['tag'][2]['name']) + ")"
            except:
                try:
                    jsonartisttag = simplejson.load(urllib.urlopen(artisttagurl))
                    toptags = "("\
                            + parser.unescape(jsonartisttag['toptags']['tag'][0]['name']) + ", "\
                            + parser.unescape(jsonartisttag['toptags']['tag'][1]['name']) + ", "\
                            + parser.unescape(jsonartisttag['toptags']['tag'][2]['name']) + ")"
                except:
                    toptags = ""

            send_data("PRIVMSG %s :%s %s playing: %s - %s %s" % (variables.channel, listener, playstatus, artist, title, toptags))
        except Exception as e:
            print e
            send_data("PRIVMSG %s :%s" % (variables.channel, "I just broke. Pester Spacecode about it."))

def help(send_data):
    send_data("PRIVMSG %s :Displays user's currently playing song. Usage: .np [lastfm username (optional)]"  % variables.channel)
