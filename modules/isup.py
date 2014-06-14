import variables, urllib2

def isup(send_data, msgarr, user):
	if len(msgarr) < 2 or "9gag" in msgarr or "reddit" in msgarr:
		send_data("PRIVMSG %s :Whoops, seems like you forgot entering a website." % variables.channel)
	else:
		website = msgarr[1]
		output = urllib2.urlopen("http://isup.me/%s" % website).read().decode("utf-8")

		debug(output, 3)

		if "It's not" in output:
			send_data("PRIVMSG %s :It's not just you, %s looks down from here." % (variables.channel, website))

		if "It's just" in output:
			send_data("PRIVMSG %s :It's just you, %s is up." % (variables.channel, website))

		if "interwho" in output:
			send_data("PRIVMSG %s :Whoops, %s doesn't look like a place on the interwobble!" % (variables.channel, website))
def help(send_data):
	send_data("PRIVMSG %s :Checks if a website is up. Usage: .isup [websites]"  % variables.channel)