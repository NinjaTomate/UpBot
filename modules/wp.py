import variables, re, string, json as simplejson, urllib, HTMLParser
from time import sleep

def wp(send_data, msgarr, user, perms):
    lastfm = simplejson.load(open("lastfm.json", "r"))
    done = False
    send_data("NAMES %s" % variables.channel)

    while not done:
        if "353" in variables.buffer or "stop" in variables.buffer:
            input = variables.buffer
            done = True

    names = string.split(input)[6:]
    parser = HTMLParser.HTMLParser()

    for name in names:
        if re.match(r'^(\@|\&|%|\+).*', name):
            name = name[1:]

        variables.debug(name, 3)

        if name in lastfm:
            variables.debug(lastfm[name], 3)

            url = "http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=%s&api_key=%s&limit=1&format=json" % (lastfm[name], variables.lastFMKey)
            json = simplejson.load(urllib.urlopen(url))

            try:
                artist = json['recenttracks']['track'][0]['artist']['#text']
                title = json['recenttracks']['track'][0]['name']
                playstatus = "is"
            except:
                continue

            tagsurl = "http://ws.audioscrobbler.com/2.0/?method=track.getTopTags&artist=%s&track=%s&api_key=%s&format=json" % (artist, title, variables.lastFMKey)
            artisttagsurl = "http://ws.audioscrobbler.com/2.0/?method=artist.getTopTags&artist=%s&api_key=%s&format=json" % (artist, variables.lastFMKey)

            try:
                jsontags = simplejson.load(urllib.urlopen(tagsurl))
                toptags = "("\
                        + parser.unescape(jsontags['toptags']['tag'][0]['name']) + ", "\
                        + parser.unescape(jsontags['toptags']['tag'][1]['name']) + ", "\
                        + parser.unescape(jsontags['toptags']['tag'][2]['name']) + ")"
            except:
                try:
                    jsonartisttags = simplejson.load(urllib.urlopen(artisttagsurl))
                    toptags = "("\
                            + parser.unescape(jsonartisttags['toptags']['tag'][0]['name']) + ", "\
                            + parser.unescape(jsonartisttags['toptags']['tag'][1]['name']) + ", "\
                            + parser.unescape(jsonartisttags['toptags']['tag'][2]['name']) + ")"
                except:
                    toptags = ""

            send_data("PRIVMSG %s :%s %s playing: %s - %s %s" % (variables.channel, name, playstatus, artist, title, toptags))