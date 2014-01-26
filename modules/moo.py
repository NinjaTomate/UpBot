import variables, urllib2, string, subprocess
def moo(send_data, msgarr, user):
	message=""
	msghold=""
	if not len(msgarr) < 2:
		for word in msgarr:
			print word
			if not (word == "") and not (word == ".moo"):
				message+= word + " "
		message=string.split(message, ".moo")
		for word in message:
			msghold+=word
		message=msghold
		print message
		if not ("&" in word) and not ("-" in word):
			output=subprocess.Popen(["cowsay", message],  stdout=subprocess.PIPE)
			for PythonIsGreat in output.stdout:
				send_data("PRIVMSG %s :%s" % (variables.channel, PythonIsGreat))
		else:
			send_data("PRIVMSG %s :%s" % (variables.channel, "Syntax error."))
def help(send_data):
	print "Help has been called."
	send_data("PRIVMSG %s :%s" % (variables.channel, "Prints a cow with the supplied string."))