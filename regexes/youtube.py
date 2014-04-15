import string, json as simplejson, urllib, re, variables
def setup():
	return "if re.match(r'(.*)https?://(?:www\.)?youtube', msg):\
				youtube.execute(msg, send_data)"
def execute(msg, send_data):
	yURL = string.split(string.split(re.split('(&|\?)v=', msg)[2], '&')[0])[0]
  	url='http://gdata.youtube.com/feeds/api/videos/%s?alt=json&v=2' % yURL
  	json = simplejson.load(urllib.urlopen(url))
  	title = json['entry']['title']['$t']
  	author = json['entry']['author'][0]['name']['$t']
  	send_data("PRIVMSG %s :YouTube: %s - Uploaded by %s" % (variables.channel, title, author))
  	print "Youtube URL: %s" % yURL
  	print "%s by %s - %s" % (title, author, url)