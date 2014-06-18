import variables, os, string, json
def setperm(send_data, msgarr, user, perms):
	if not len(msgarr) == 3:
		send_data("PRIVMSG %s :Insufficient variables supplied." % variables.channel)
	elif int(perms) < 999:
		send_data("NOTICE %s :Check your privilege." % user)
	else:
		target = msgarr[1]
		perms = msgarr[2]
		accounts = json.load(open("accounts.json", 'r'))
		accfile = open("accounts.json", 'w')
		if not target in accounts:
			accounts[target] = {}
        accounts[target]['perms'] = perms
        json.dump(accounts, accfile)
        accfile.close()
        send_data("NOTICE %s :Successfully changed permissions of %s to %s" % (user, target, perms))