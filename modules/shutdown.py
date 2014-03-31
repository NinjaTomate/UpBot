def shutdown(send_data, msgarr, user):
	if user == variables.owner:
		exec(send_data("QUIT"))
		sys.exit(1)