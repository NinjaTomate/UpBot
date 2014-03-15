import variables, urllib, json as simplejson, string, HTMLParser
def yt(send_data, msgarr, user):
	if len(msgarr) < 2 in msgarr:
		send_data("PRIVMSG %s :No or invalid search string supplied." % variables.channel)
	else:
		parser = HTMLParser.HTMLParser()
		query=string.join(msgarr)[3:]
		url = "https://gdata.youtube.com/feeds/api/videos?q=%s&alt=json" % query
		print query
		json = simplejson.load(urllib.urlopen(url))
		url = parser.unescape(json['feed']['entry'][0]['link'][0]['href'])
		title = parser.unescape(json['feed']['entry'][0]['title']['$t'])
		send_data("PRIVMSG %s :\"%s\" - %s" % (variables.channel, title, content, url))
