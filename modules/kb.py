import variables, os, string, json
def kb(send_data, msgarr, user, perms):
	target = ""
	message = ""
	if not len(msgarr) >= 2:
		send_data("PRIVMSG %s :Insufficient variables supplied." % variables.channel)
	elif int(perms) < 900 or msgarr[1] == variables.owner:
			send_data("NOTICE %s :Check your privilege." % user)
	else:
		target = msgarr[1]
		if len(msgarr) >= 3:
			message = string.join(msgarr[2:])
		else:
			message = "%s doesn't like you." % user
		channel = variables.channel
		send_data("MODE %s +b %s!*@*.*" % (channel, target))
		send_data("KICK %s %s :%s" % (channel, target, message))