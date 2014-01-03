import variables
def initial():
	global COMMANDS
	COMMANDS = ["shutdown", "checkmode", "isup", "update"]
	print COMMANDS

def update(send_data):
	import commands.py

def shutdown(send_data):
	print "aaaaaaaaaaaaaaaaaaa"
	exec(send_data("QUIT"))
	sys.exit(1)

def checkmode(send_data):
	send_data("WHOIS %s" % variables.user)

def isup(website, user):
	output=urllib.request("http://isup.me/%s" % website).read().decode("utf-8")
	print output