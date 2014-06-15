import string, json as simplejson, urllib, re, variables, sys
def setup():
    return "if re.match(r'.*http(s)?://(www\.)?youtu(\.)?be(\..*/)?(watch)?.*', msg):\
            youtube.execute(msg, send_data)"

def execute(msg, send_data):
    sys.setdefaultencoding('utf8')
    try:
        url = re.search(r'http(s)?://(www\.)?youtu(\.)?be(\..*/)?(watch)?.*', msg).group(0)
        yURL = re.split(r'((\?|&)?(v=|\.be/)|&)', url)[4].split()[0]
        url = 'http://gdata.youtube.com/feeds/api/videos/%s?alt=json&v=2' % yURL
        json = simplejson.load(urllib.urlopen(url))
        title = json['entry']['title']['$t']
        author = json['entry']['author'][0]['name']['$t']
        variables.debug("Youtube URL: %s" % yURL,2)
        #variables.debug("%s by %s - %s" % (title, author, url),2)

        send_data("PRIVMSG %s :YouTube: \x02%s\x02 - Uploaded by \x02%s\x02" % (variables.channel, title, author))
    except Exception as e:
        print "Youtube regex crashed with error: %s" % e