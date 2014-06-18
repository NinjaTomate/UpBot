import variables
def myperm(send_data, msgarr, user, perms):
	send_data("PRIVMSG %s :Permission level for %s: %s" % (variables.channel, user, perms))