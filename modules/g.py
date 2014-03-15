import variables, urllib, json as simplejson, string, HTMLParser
def g(send_data, msgarr, user):
	if len(msgarr) < 2 or "porn" in msgarr:
		send_data("PRIVMSG %s :No or invalid search string supplied." % variables.channel)
	else:
		parser = HTMLParser.HTMLParser()
		query=string.join(msgarr)[3:]
		url = "http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=%s" % query
		print query
		json = simplejson.load(urllib.urlopen(url))
		content = parser.unescape(json['responseData']['results'][0]['content']).replace("\n", "").replace("<b>", "").replace("</b>", "")
		title = parser.unescape(json['responseData']['results'][0]['title']).replace("<b>", "").replace("</b>", "")
		url = json['responseData']['results'][0]['url']
		send_data("PRIVMSG %s :%s - %s - %s" % (variables.channel, title, content, url))
