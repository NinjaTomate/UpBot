import variables
def shutdown(send_data, msgarr, user):
	if user == variables.owner:
		send_data("QUIT")
		sys.exit(1)
def help(send_data):
	send_data("PRIVMSG %s :Shuts the bot down. Can only be used by owner." % variables.channel)