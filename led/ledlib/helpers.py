#!/usr/bin/env python -t
# -t issues warnings when mixing tabs and spaces (Python 2 - 3 errors out on those.)
#
# library of little helper functions written for python 2.6.4 (local lowest common denominator)
#
# Aliza R. Panitz
# 2014-10-22

from ledlib import globalconfig

def fileappend (filename, texttoappend):
    # not very efficient if the same file is appended to multiple times.
    if globalconfig.noop:
        # print "noop flag set, not appending %s to file %s" % (texttoappend, filename)
        print ("noop flag set, not appending", texttoappend, "to file", filename) 
    else:
        filehandle = open (filename, 'a')
        filehandle.write (texttoappend + "\n")
        filehandle.close()
        verboseprint ("appended line(s)\n%s\nto file %s" % (texttoappend, filename) )

def debugprint(infostring):
    if globalconfig.debugflag:
        print ("DEBUG:", infostring)

def warnprint(infostring):
    globalconfig.warningflag = True
    print ("WARNING:", infostring)

def verboseprint(infostring):
    if globalconfig.verboseflag:
        print (infostring)

# No die as per http://stackoverflow.com/questions/6722210/or-die-in-python
# use sys.exit[arg] or assert

def prompt_if_empty(variable,promptstring):
    while not variable:
        if globalconfig.batchmode:
            raise Exception('Required variable missing.')
        print (promptstring, end=" ")
        variable = raw_input(globalconfig.prompt)
    return variable

def prompt_yn(question="OK? ", default="yes"):
    # modified from http://stackoverflow.com/questions/3041986/python-command-line-yes-no-input
    # there's also a nice alternative using strtobool at http://mattoc.com/python-yes-no-prompt-cli.html
    if globalconfig.batchmode:
        return True
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        response = raw_input(question + prompt + globalconfig.prompt)
        response = response.lower()
        if globalconfig.batchmode or (default is not None and response == ''):
            return valid[default]
        elif response in valid:
            return valid[response]
        else:
            print("Please respond with 'yes' or 'no' (or 'y' or 'n').\n")

def pressenter():
  response = raw_input ("Press enter when ready. " +  globalconfig.prompt)
  return True

def getfqdn():
  from os import uname
  if not globalconfig.fqdn:
    globalconfig.fqdn = uname()[1]
    debugprint ("Host name set to %s" % globalconfig.fqdn )
  return globalconfig.fqdn

def getshorthostname():
  if not globalconfig.hostname:
      fqdn = getfqdn()
      globalconfig.hostname = fqdn.split(".",1)[0]
      debugprint ("Short host name set to %s" % globalconfig.hostname )
  return globalconfig.hostname

def get_human_user():
    from getpass import getuser
    if not globalconfig.humanuser:
        globalconfig.humanuser = getuser()
        debugprint ("Human user is %s" % globalconfig.humanuser )
    return globalconfig.humanuser

def get_effective_user():
    from os import getlogin
    if not globalconfig.effectiveuser:
        globalconfig.effectiveuser = getlogin()
        debugprint ("Effective user is %s" % globalconfig.effectiveuser )
    return globalconfig.effectiveuser

