import re, variables, urllib, json as simplejson, string, HTMLParser

def yt(send_data, msgarr, user):
	if len(msgarr) < 2:
		send_data("PRIVMSG %s :No or invalid search string supplied." % variables.channel)
	else:
		try:
			parser = HTMLParser.HTMLParser()
			query=string.join(msgarr)[3:]
			url = "https://gdata.youtube.com/feeds/api/videos?q=%s&alt=json" % query
			debug(query, 2)
			json = simplejson.load(urllib.urlopen(url))
			url = parser.unescape(json['feed']['entry'][0]['link'][0]['href'])
			url = "https://youtu.be/" + re.split(r'((\?|&)?(v=|\.be/)|&)', url)[4]
			title = parser.unescape(json['feed']['entry'][0]['title']['$t'])
			author = parser.unescape(json['feed']['entry'][0]['author'][0]['name']['$t'])

			send_data("PRIVMSG %s :\x02\"%s\"\x02 by \x02%s\x0F - %s" % (variables.channel, title, author, url))
		except:
			send_data("PRIVMSG %s :No results found or other error." % variables.channel)

def help(send_data):
	send_data("PRIVMSG %s :Seaches YouTube for a query. Usage: .yt [query]"  % variables.channel)
