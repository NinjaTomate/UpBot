import variables, string
def getperm(send_data, msgarr, user):
	if len(msgarr) == 2:
		req = msgarr[1]
		for user in variables.permissions:
			if string.split(user," ")[0] == req:
				send_data("PRIVMSG %s :%s" % (variables.channel, "Permission level" + \
					" for user %s: %s" % (req, string.split(user)[1])))
			else:
				send_data("PRIVMSG %s :%s" % (variables.channel, "User %s not found." % req))
	else:
		send_data("PRIVMSG %s :Syntax error." % variables.channel)
def help(send_data):
	send_data("PRIVMSG %s :%s" % (variables.channel, "Prints the specified user's permission level."))