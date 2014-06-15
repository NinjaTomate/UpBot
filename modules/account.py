import variables, json, string, os
debug = False
def account(send_data, msgarr, user):
	if len(msgarr) != 2:
		send_data("PRIVMSG %s :Too many arguments." % variables.channel)
	else:
		lfmjson = json.load(open("lastfm.json", "r"))
		lastfm = open("lastfm.json", "w")
		lfmjson[user] = msgarr[1]
		json.dump(lfmjson, lastfm)
		lastfm.close()
		send_data("NOTICE %s :Set your account to %s." % (user, msgarr[1]))
		if debug == True:
			lastfm = json.load(open("lastfm.json", 'r'))
			print "Changed %s's LastFM user to %s." % (user, msgarr[1])
def help(send_data):
	send_data("PRIVMSG %s :Sets your LastFM username to be used with the .np and .wp moduels. Usage: .account [LastFM username]" % variables.channel)