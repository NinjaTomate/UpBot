import socket, string, os, sys, commands, variables, subprocess, re, urllib, json as simplejson, time

reload(sys)
sys.setdefaultencoding('utf8')
PORT = 6667
try:
    SERVER = sys.argv[3]
    NICKNAME = sys.argv[2]
    CHANNEL = '#' + sys.argv[1]
    OWNER = sys.argv[4]
except:
    print "Usage: python upbot.py [channel] [nickname] [server] [owner nick] [nickserv password (optional)]"
    sys.exit()
global COMMANDS
COMMANDS = []
variables.owner = OWNER
variables.channel = CHANNEL

IRC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def irc_conn():
    IRC.connect((SERVER, PORT))

def send_data(command):
    IRC.send(command + '\n')

def join(channel):
    time.sleep(2)
    send_data("JOIN %s" % channel)

def login(nickname, username=sys.argv[2], password = None, realname=sys.argv[2], hostname='Spurdo', servername='Server'):
    send_data("USER %s %s %s %s" % (username, hostname, servername, realname))
    send_data("NICK " + nickname)
    send_data("MODE %s +ir" % nickname)
    try:
        NSPW = sys.argv[5]
        time.sleep(2)
        send_data("PRIVMSG NickServ :IDENTIFY %s" % NSPW)
    except:
        print "No NickServ password supplied."
        
def restart_program():
    """Restarts the current program.
    Note: this function does not return. Any cleanup action (like
    saving data) must be done before calling this function."""
    send_data("QUIT")
    python = sys.executable
    os.execl(python, python, * sys.argv)
def execute(command, user, msgarr):
    print "Executing %s.%s" % (command, command)
    exec("%s.%s(send_data, msgarr, user)" % (command, command))
def help(command, user, msgarr):
    print "Executing %s.help()" % command
    try:
        exec("%s.help(send_data)" % command)
    except:
        send_data("PRIVMSG %s :No help available." % CHANNEL)
def reloader(module):
    exec("%s = reload(%s)" % (module, module))
def loader(module):
    exec("import modules.%s as %s" % (module, module)) in globals()
def recvloop():
    global COMMANDS
    while (1):
        buffer = IRC.recv(1024)
        variables.buffer = buffer
        print variables.buffer
        print string.split(string.split(buffer, ':')[1], '!')[0]
        if "VERSION" in buffer:
            print "Version request received."
            send_data("NOTICE %s :VERSION Funco Testing" % string.split(string.split(buffer, ':')[1], '!')[0])
        if string.split(buffer)[0] == "PING":
            send_data("PRIVMSG %s PONG" % string.split(buffer, ':')[1])
        if "INVITE" in buffer and string.split(string.split(buffer, ':')[1], '!')[0] == OWNER:
            channel = string.split(string.join(string.split(buffer)[3:])[1:])[0]
            send_data("JOIN %s" % channel)
        if "PRIVMSG" in buffer and string.split(string.split(buffer, ':')[1], '!')[0] == OWNER:
            msg = string.join(string.split(buffer)[3:])[1:]
            msg = string.split(msg)
            if msg[0] == "part":
                if "#" in msg[1]:
                    send_data("PART %s" % msg[1])
                else:
                    send_data("PART #%s" % msg[1])
        if "PRIVMSG" in buffer and "PING" in buffer:           
            msg = string.join(string.split(buffer)[3:])[1:]   
            sender = string.split(string.split(buffer, ':')[1], '!')[0]
            send_data("NOTICE %s :%s" % (sender, msg))

        if "PRIVMSG" in buffer and '#' in string.split(buffer.lower())[2]:
            msgChan = string.split(buffer.lower())[2]
            CHANNEL = msgChan
            variables.channel = CHANNEL
            msg = string.join(string.split(buffer)[3:])[1:]
            print msg
            msgarr = string.split(msg)
            user = string.split(string.split(buffer, ':')[1], '!')[0]
            variables.user=user
            if re.match(r'(.*)https?://(?:www\.)?youtube', msg):
                try:
                    yURL = string.split(string.split(re.split('(&|\?)v=', msg)[2], '&')[0])[0]
                    url='http://gdata.youtube.com/feeds/api/videos/%s?alt=json&v=2' % yURL
                    json = simplejson.load(urllib.urlopen(url))
                    title = json['entry']['title']['$t']
                    author = json['entry']['author'][0]['name']['$t']
                    send_data("PRIVMSG %s :YouTube: %s - Uploaded by %s" % (CHANNEL, title, author))
                    print "Youtube URL: %s" % yURL
                except:
                    send_data("PRIVMSG %s :Error, is the URL broken?" % CHANNEL)
            if ".commands" in msgarr[0]:
                commands = ""
                COMMANDS
                for item in COMMANDS:
                    commands = commands + item + " "
                send_data("PRIVMSG %s :Available commands: %s" % (CHANNEL, commands))

            if ".update" in msgarr[0] and user == OWNER:
                output=subprocess.Popen(["git", "pull", "git://github.com/NinjaTomate/UpBot.git", "testing"],  stdout=subprocess.PIPE)
                for PythonIsGreat in output.stdout:
                    print PythonIsGreat
                    send_data("PRIVMSG %s :%s" % (CHANNEL, PythonIsGreat))
            if ".restart" in msgarr[0] and user == OWNER:
                restart_program()
            if ".reload" in msgarr[0] and user == OWNER:
                ncount = 0
                count = 0
                oCOMMANDS = COMMANDS
                COMMANDS = []
                for item in os.listdir('./modules'):
                    module = string.split(item, '.')[0]
                    if not any(module in item for item in COMMANDS) and not module == "__init__":
                        if not any(module in item for item in oCOMMANDS) and not module == "__init__":
                            COMMANDS.append(module)
                            ncount = ncount +1
                            loader(module)
                        else:
                            COMMANDS.append(module)
                            count = count+1
                            reloader(module)
                if ncount > 0:
                    send_data("PRIVMSG %s :Successfully loaded %s new modules." % (CHANNEL, ncount))
                send_data("PRIVMSG %s :Successfully reloaded %s modules." % (CHANNEL, count))
            elif ".help" in msgarr[0]:
                print "Help command used."
                try:
                    for COMMAND in COMMANDS:
                        command =msgarr[1]
                        print "%s = %s?" % (command, COMMAND)
                        if command == COMMAND:
                            print "Found module %s" % command
                            help(command, user, msgarr)
                            break;
                except:
                    send_data("PRIVMSG %s :%s" % (CHANNEL, "Please supply a module."))
            elif "." in msgarr[0]:
                print "Command detected."
                for COMMAND in COMMANDS:
                    command = (string.split(string.split(msgarr[0], '.')[1], "\r\n"))[0]
                    print "%s = %s?" % (command, COMMAND)
                    if command == COMMAND:
                        print "Found module %s" % command
                        execute(command, user, msgarr)
                        break;
                        
for item in os.listdir('./modules'):
    module = string.split(item, '.')[0]
    if not any(module in item for item in COMMANDS) and not module == "__init__":
        exec("import modules.%s as %s" % (module, module))
        COMMANDS.append(module)
print COMMANDS
irc_conn()
login(NICKNAME)
join(CHANNEL)
recvloop()