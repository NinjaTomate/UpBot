import variables, urllib2, json
def isup(send_data, msgarr, user):
	if len(msgarr) < 2 or "porn" in msgarr:
		send_data("PRIVMSG %s :No or invalid search string supplied." % variables.channel)
	else:
		query=string.join(msgarr)[1:]
		print query
		json = simplejson.loads(urllibb.request.urlopen("http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s") % query)