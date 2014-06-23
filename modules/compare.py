import variables, re, string, json as simplejson, urllib

def compare(send_data, msgarr, user, perms):
    if len(msgarr) == 2:
        lastfm = simplejson.load(open("lastfm.json", "r"))
        target = msgarr[1]

        if user in lastfm:
            user = lastfm[user]
        else:
            send_data("NOTICE %s :Please set your account by using .account before using this command." % user)

        if target in lastfm:
            target = lastfm[target]

        variables.debug(user, 3)
        url = "http://ws.audioscrobbler.com/2.0/?method=tasteometer.compare&type1=user&type2=user&value1=%s&value2=%s&api_key=%s&format=json" % (user, target, variables.lastFMKey)
        json = simplejson.load(urllib.urlopen(url))
        print json
        score = float(json['comparison']['result']['score']) * 100
        score=int(score * 100) / 100.0 # this is kinda hacky
        variables.debug(score, 3)
        artists = []
        for i in range(0,5):
            try:
                artist = json['comparison']['result']['artists']['artist'][i]['name']
                artists.append(artist)
            except:
                break
        artists = ", ".join(artists)
        send_data("PRIVMSG %s :Compare [\x02%s\x02/\x02%s\x02]: %s%%, featuring %s" % (variables.channel, user, target, score, artists))
        print score

    elif len(msgarr) == 3:
        lastfm = simplejson.load(open("lastfm.json", "r"))
        target = msgarr[1]
        user = msgarr[2]
        if user in lastfm:
            user = lastfm[user]

        if target in lastfm:
            target = lastfm[target]

        variables.debug(user, 3)
        url = "http://ws.audioscrobbler.com/2.0/?method=tasteometer.compare&type1=user&type2=user&value1=%s&value2=%s&api_key=%s&format=json" % (user, target, variables.lastFMKey)
        json = simplejson.load(urllib.urlopen(url))
        print json
        score = float(json['comparison']['result']['score']) * 100
        score=int(score * 100) / 100.0 # this is kinda hacky
        variables.debug(score, 3)
        artists = []
        for i in range(0,5):
            try:
                artist = json['comparison']['result']['artists']['artist'][i]['name']
                artists.append(artist)
            except:
                break
        artists = ", ".join(artists)
        send_data("PRIVMSG %s :Compare [\x02%s\x02/\x02%s\x02]: %s%%, featuring %s" % (variables.channel, user, target, score, artists))
        print score

    else:
        send_data("NOTICE %s :Syntax error in .compare module." % user)