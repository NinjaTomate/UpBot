import socket, string, os, sys, commands, variables, subprocess

SERVER = 'irc.rizon.net'
PORT = 6667
NICKNAME = sys.argv[2] #Uncomment me for deployment
#NICKNAME = "TomatoTestBot" #Remove me for deployment
CHANNEL = '#' + sys.argv[1]
COMMANDS = []
variables.channel = CHANNEL

IRC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def irc_conn():
    IRC.connect((SERVER, PORT))

def send_data(command):
    IRC.send(command + '\n')

def join(channel):
    send_data("JOIN %s" % channel)

def login(nickname, username='Tomate', password = None, realname='Tomate', hostname='Spurdo', servername='Server'):
    send_data("USER %s %s %s %s" % (username, hostname, servername, realname))
    send_data("NICK " + nickname)
    send_data("MODE %s +irx" % nickname)
def restart_program():
    """Restarts the current program.
    Note: this function does not return. Any cleanup action (like
    saving data) must be done before calling this function."""
    python = sys.executable
    os.execl(python, python, * sys.argv)
def execute(command, user, msgarr):
    print "Executing vsquare.%s" % command
    exec("%s.%s(send_data, msgarr, user)" % (command, command))
def reloader(module):
    exec("%s = reload(%s)" % (module, module))
def loader(module):
    exec("import modules.%s as %s" % (module, module)) in globals()
def recvloop():
    while (1):
        buffer = IRC.recv(1024)
        variables.buffer = buffer
        print variables.buffer
        if string.split(buffer)[0] == "PING":
            send_data("PRIVMSG %s PONG" % string.split(buffer, ':')[1])
        if "PRIVMSG" in buffer and CHANNEL in buffer:
            msg = string.split(buffer, ':')[2]
            msgarr = string.split(msg)
            user = string.split(string.split(buffer, ':')[1], '!')[0]
            variables.user=user
            if msg == "syntax test\r\n":
                send_data("PRIVMSG %s :User: %s" % (CHANNEL, user))
            if ".commands" in msgarr[0]:
                commands = ""
                for item in COMMANDS:
                    commands = commands + item + " "
                send_data("PRIVMSG %s :Available commands: %s" % (CHANNEL, commands))

            if ".update" in msgarr[0] and user == "TomatoGuy":
                #output=subprocess.Popen(["svn", "update", "http://localhost/svn/ircbot/trunk", \
                #    "/home/tomate/Python/Moddable_IRC_Bot/"], stdout=subprocess.PIPE)
                output=subprocess.Popen(["git", "pull", "git://github.com/NinjaTomate/UpBot.git", "testing"],  stdout=subprocess.PIPE)
                for PythonIsGreat in output.stdout:
                    print PythonIsGreat
                    send_data("PRIVMSG %s :%s" % (CHANNEL, PythonIsGreat))
            if ".restart" in msgarr[0] and user == "TomatoGuy":
                restart_program()
            if ".reload" in msgarr[0] and user == "TomatoGuy":
                ncount = 0
                count = 0
                global COMMANDS
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

            elif "." in msgarr[0]:
                print "Command detected."
                for COMMAND in COMMANDS:
                    command = (string.split(string.split(msgarr[0], '.')[1], "\r\n"))[0]
                    print "%s = %s?" % (command, COMMAND)
                    if command == COMMAND:
                        print "Found module %s" % command
                        execute(command, user, msgarr)
                        break;

#commands.initial()
#COMMANDS = commands.COMMANDS
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