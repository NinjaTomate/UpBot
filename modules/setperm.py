import variables, string
def setperm(send_data, msgarr, user):
	permission = False
	for person in variables.permissions:
		if string.split(person)[0] == user and string.split(person)[1] >= 900:
			permission = True
	if len(msgarr) == 3 and permission == True:
		newperm = msgarr[2]
		guy = msgarr[1]
		for person in variables.permissions:
			if string.split(person)[0] == guy:
				variables.permissions.remove(person)
			variables.permissions.append("%s %s" % (guy, newperm))
	else:
		send_data("PRIVMSG %s :Not permitted." % variables.channel)

def help(send_data):
	send_data("PRIVMSG %s :%s" % (variables.channel, "Prints the specified user's permission level."))