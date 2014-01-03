import variables
def testmodule(send_data, msgarr, user):
	send_data("PRIVMSG %s :Seems to be working, %s." % (variables.channel, user))