import variables, urllib2, string, subprocess
def moo(send_data, msgarr, user):
	message=""
	msghold=""
	for word in msgarr:
		print word
		if not (word == "") and not (word == ".moo"):
			message+= word + " "
	message=string.split(message, ".moo")
	for word in message:
		msghold+=word
	message=msghold
	output=subprocess.Popen(["cowsay", message],  stdout=subprocess.PIPE)
	for PythonIsGreat in output.stdout:
		send_data("PRIVMSG %s :%s" % (CHANNEL, PythonIsGreat))