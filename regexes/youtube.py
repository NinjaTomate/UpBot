import string, json as simplejson, urllib, re, variables

def setup():
	return "if re.match(r'.*http(s)?://(www\.)?youtu(\.)?be(\..*/)?(watch)?.*', msg):\
				youtube.execute(msg, send_data)"

def execute(msg, send_data):
    try:
        url = re.search(r'http(s)?://(www\.)?youtu(\.)?be(\..*/)?(watch)?.*', msg).group(0)
        yURL = re.split(r'((\?|&)?(v=|\.be/)|&)', url)[4].split()[0]
        url='http://gdata.youtube.com/feeds/api/videos/%s?alt=json&v=2' % yURL
        json = simplejson.load(urllib.urlopen(url))
        title = json['entry']['title']['$t']
        author = json['entry']['author'][0]['name']['$t']
        print "Youtube URL: %s" % yURL
        print "%s by %s - %s" % (title, author, url)

        send_data("PRIVMSG %s :YouTube: \x02%s\x02 - Uploaded by \x02%s\x02" % (variables.channel, title, author))
    except Exception as e:
        "Youtube regex crashed with error: %s" % e