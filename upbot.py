import socket, string, os, sys, commands, variables, subprocess, re, urllib, json as simplejson, time
from threading import Thread

reload(sys)
sys.setdefaultencoding('utf8')

if (os.path.isfile("startsettings.json")):
    variables.debug("Config file detected", 1)

    settingsFile = open("startsettings.json",'r')
    jsonSettingsObj = simplejson.load(settingsFile)

    SERVER = jsonSettingsObj["server"]
    PORT = jsonSettingsObj["port"]
    USERNAME = jsonSettingsObj["username"]
    PASSWORD = jsonSettingsObj["password"]
    NICKNAME = jsonSettingsObj["nickname"]
    NICKPASS = jsonSettingsObj["nickpass"]
    OWNER = jsonSettingsObj["owner"]
    CHANNEL = jsonSettingsObj["channel"]
    variables.lastFMKey = jsonSettingsObj["lastfmkey"]
else:
    print "Looks like this is your first time running this bot."
    SERVER = raw_input("Please enter the server to connect to: ")
    PORT = raw_input("Please enter the server port (leave blank for default): ")
    USERNAME = raw_input("Please enter the user name: ")
    PASSWORD = raw_input("Please enter the server password (leave blank if none): ")
    NICKNAME = raw_input("Enter the bots nick: ")
    NICKPASS = raw_input("Please enter the nickserv password (leave blank if none): ")
    OWNER = raw_input("Enter the owners nick: ")
    CHANNEL = raw_input("Please enter the home channel: ")
    variables.lastFMKey = raw_input("Please enter your last.fm api key: ")

    if (PORT == "" or PORT == ''):
        PORT = "6667"

    settings = {}
    settings["server"] = SERVER
    settings["port"] = PORT
    settings["username"] = USERNAME
    settings["password"] = PASSWORD
    settings["nickname"] = NICKNAME
    settings["nickpass"] = NICKPASS
    settings["owner"] = OWNER
    settings["channel"] = CHANNEL
    settings["lastfmkey"] = variables.lastFMKey

    configfile = open("startsettings.json",'w')
    configfile.write(simplejson.dumps(settings))
    configfile.close()

if (PASSWORD == "" or PASSWORD == ''):
    PASSWORD = None

if (NICKPASS == "" or NICKPASS == ''):
    NICKPASS = None

global COMMANDS
COMMANDS = []
variables.regexes = []
variables.debuglevel = 3
variables.owner = OWNER
variables.channel = CHANNEL
variables.nickname = NICKNAME

IRC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def irc_conn():
    IRC.connect((SERVER, int(PORT)))

def send_data(command):
    IRC.send(command + '\n')

def join(channel):
    time.sleep(1)
    send_data("JOIN %s" % channel)

def login(nickname = NICKNAME, username = USERNAME, password = PASSWORD, nickpass = NICKPASS, realname = NICKNAME, hostname = "Spurdo", servername = "Server"):
    send_data("USER %s %s %s %s" % (username, hostname, servername, realname))
    if (password != None):
        send_data("PASS " + password)
    send_data("NICK " + nickname)
    send_data("MODE %s +ir" % nickname)

    if (NICKPASS != None):
        time.sleep(1)
        send_data("PRIVMSG NickServ :IDENTIFY %s" % nickpass)

def restart_program():
    send_data("QUIT")
    python = sys.executable
    os.execl(python, python, * sys.argv)

def postpls():
    while(True):
        ech = raw_input()
        send_data(ech)

def ohmygoddoit(jesuschrist):
    exec(jesuschrist)

def reloadReggie():
    new = 0
    reloaded = 0
    variables.regexes = []

    for item in os.listdir("./regexes"):
        if not "pyc" in item:
            module = string.split(item, '.')[0]
        else:
            module = "INVALID"

        if not "__init__" in module and module != "INVALID":
            try:
                ohmygoddoit("%s = reload(%s)" % (module, module))
                reloaded += 1
            except:
                ohmygoddoit("import regexes.%s as %s" % (module, module))
                new += 1

            ohmygoddoit("variables.regexes.append(%s.setup())" % module)

    variables.debug(variables.regexes)

    if reloaded > 0:
        send_data("PRIVMSG %s :Reloaded %s Regex modules." % (CHANNEL, reloaded))

    if new > 0:
        send_data("PRIVMSG %s :Loaded %s new Regex modules." % (CHANNEL, new))

def execute(command, user, msgarr):
    variables.debug("Executing %s.%s" % (command, command))
    exec("commandthread = Thread(target = %s.%s, args=(send_data, msgarr, user))" % (command, command))
    commandthread.start()
    #exec("%s.%s(send_data, msgarr, user)" % (command, command))

def help(command, user, msgarr):
    variables.debug("Executing %s.help()" % command)

    try:
        exec("%s.help(send_data)" % command)
    except:
        send_data("PRIVMSG %s :No help available." % CHANNEL)

def reloader(module):
    exec("%s = reload(%s)" % (module, module))

def loader(module):
    exec("import modules.%s as %s" % (module, module)) in globals()

def pleaseDoIt(item, msg, send_data):
    exec(item)

def recvloop():
    global COMMANDS

    while (1):
        buffer = IRC.recv(1024)
        variables.buffer = buffer
        print buffer
        variables.debug(variables.buffer,0)
        variables.debug(string.split(string.split(buffer, ':')[1], '!')[0])
        for item in variables.regexes:
                #if "if" in item:
                variables.debug(item, 2)
                pleaseDoIt(item, buffer, send_data)
        if string.split(string.split(buffer, ':')[1], '!')[0] == OWNER:
            if "\x01UPDATE" in buffer:
                output = subprocess.Popen(["git", "pull", "git://github.com/NinjaTomate/UpBot.git", "testing"], stdout = subprocess.PIPE)

                for PythonIsGreat in output.stdout:
                    variables.debug(PythonIsGreat)
                    send_data("PRIVMSG %s :%s" % (OWNER, PythonIsGreat))

            if "\x01RESTART" in buffer:
                restart_program()

        if "\x01VERSION" in buffer:
            variables.debug("Version request received.")

            send_data("NOTICE %s :VERSION Funco Testing" % string.split(string.split(buffer, ':')[1], '!')[0])

        if string.split(buffer)[0] == "PING":
            send_data("PRIVMSG %s PONG" % string.split(buffer, ':')[1])

        if "INVITE" in buffer and string.split(string.split(buffer, ':')[1], '!')[0] == OWNER:
            channel = string.split(string.join(string.split(buffer)[3:])[1:])[0]

            send_data("JOIN %s" % channel)

        if "PRIVMSG" in buffer and string.split(string.split(buffer, ':')[1], '!')[0] == OWNER:
            if not ": " in buffer:
                msg = string.join(string.split(buffer)[3:])[1:]
                msg = string.split(msg)

                if msg[0] == "part":
                    if "#" in msg[1]:
                        send_data("PART %s" % msg[1])
                    else:
                        send_data("PART #%s" % msg[1])

        if "PRIVMSG" in buffer and "\x01PING" in buffer:
            msg = string.join(string.split(buffer)[3:])[1:]
            sender = string.split(string.split(buffer, ':')[1], '!')[0]

            send_data("NOTICE %s :%s" % (sender, msg))

        if "PRIVMSG" in buffer:
            user = string.split(string.split(buffer, ':')[1], '!')[0]

            if '#' in string.split(buffer.lower())[2]:
                msgChan = string.split(buffer.lower())[2]
            else:
                msgChan = user

            CHANNEL = msgChan
            variables.channel = CHANNEL
            msg = string.join(string.split(buffer)[3:])[1:]
            msgarr = string.split(msg)
            variables.debug(re.sub('\n','',msg))

            

            try:
                variables.debug(msgarr[0])
            except:
                msgarr = string.split("This string magically prevents crashing.")

            variables.user = user

            if ".commands" in msgarr[0]:
                commands = ""
                COMMANDS

                for item in COMMANDS:
                    commands = commands + item + " "

                send_data("PRIVMSG %s :Available commands: %s" % (CHANNEL, commands))

            if ".update" in msgarr[0] and user == OWNER:
                output = subprocess.Popen(["git", "pull", "git://github.com/NinjaTomate/UpBot.git", "testing"],  stdout = subprocess.PIPE)

                for PythonIsGreat in output.stdout:
                    variables.debug(PythonIsGreat)

                    send_data("PRIVMSG %s :%s" % (OWNER, PythonIsGreat))

            if ".restart" in msgarr[0] and user == OWNER:
                restart_program()

            if ".reload" in msgarr[0] and user == OWNER:
                reloadReggie()
                ncount = 0
                count = 0
                oCOMMANDS = COMMANDS
                COMMANDS = []

                for item in os.listdir("./modules"):
                    module = string.split(item, '.')[0]
                    if not any(module in item for item in COMMANDS) and module != "__init__":
                        if not any(module in item for item in oCOMMANDS) and module != "__init__":
                            COMMANDS.append(module)
                            ncount = ncount + 1
                            loader(module)
                        else:
                            COMMANDS.append(module)
                            count = count + 1
                            reloader(module)
                if ncount > 0:
                    send_data("PRIVMSG %s :Successfully loaded %s new modules." % (CHANNEL, ncount))

                send_data("PRIVMSG %s :Successfully reloaded %s modules." % (CHANNEL, count))
            elif ".help" in msgarr[0]:
                variables.debug("Help command used.")

                try:
                    for COMMAND in COMMANDS:
                        command = msgarr[1]
                        variables.debug("%s = %s?" % (command, COMMAND))

                        if command == COMMAND:
                            variables.debug("Found module %s" % command)

                            help(command, user, msgarr)

                            break;
                except:
                    send_data("PRIVMSG %s :%s" % (CHANNEL, "Please supply a module."))
            elif "." in msgarr[0]:
                variables.debug("Command detected.")

                for COMMAND in COMMANDS:
                    command = (string.split(string.split(msgarr[0], '.')[1], "\r\n"))[0]
                    variables.debug("%s = %s?" % (command, COMMAND))

                    if command == COMMAND:
                        variables.debug("Found module %s" % command)
                        execute(command, user, msgarr)
                        break;

for item in os.listdir('./modules'):
    module = string.split(item, '.')[0]

    if module != "__init__" and not any(module in item for item in COMMANDS):
        exec("import modules.%s as %s" % (module, module))
        COMMANDS.append(module)

variables.debug(COMMANDS)

irc_conn()
login()
join(CHANNEL)
for item in os.listdir('./regexes'):
    module = string.split(item, '.')[0]
    variables.debug(module, 2)

    if not "__init__" in module and not any (module in item for item in variables.regexes):
        exec("import regexes.%s as %s" % (module, module))
        exec("variables.regexes.append(%s.setup())" % module)
thread = Thread(target = recvloop)
inputthread = Thread(target = postpls)
inputthread.start()
thread.start()
