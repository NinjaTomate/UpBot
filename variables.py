debuglevel = 0

def debug(text, level = 1):
    if (level <= debuglevel):
        print(text)
