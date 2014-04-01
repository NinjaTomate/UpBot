import variables
def shutdown(send_data, msgarr, user):
	if user == variables.owner:
		send_data("QUIT")
		sys.exit(1)