#! /usr/bin/env python
#
# PyKota
#
# PyKota : Print Quotas for CUPS
#
# (c) 2003 Jerome Alet <alet@librelogiciel.com>
# You're welcome to redistribute this software under the
# terms of the GNU General Public Licence version 2.0
# or, at your option, any higher version.
#
# You can read the complete GNU GPL in the file COPYING
# which should come along with this software, or visit
# the Free Software Foundation's WEB site http://www.fsf.org
#
# $Id$
#
# $Log$
# Revision 1.5  2003/03/29 13:08:28  jalet
# Configuration is now expected to be found in /etc/pykota.conf instead of
# in /etc/cups/pykota.conf
# Installation script can move old config files to the new location if needed.
# Better error handling if configuration file is absent.
#
# Revision 1.4  2003/03/29 09:47:00  jalet
# More powerful installation script.
#
# Revision 1.3  2003/03/26 17:48:36  jalet
# First shot at trying to detect the availability of the needed software
# during the installation.
#
# Revision 1.2  2003/03/09 16:49:04  jalet
# The installation script installs the man pages too now.
#
# Revision 1.1  2003/02/05 21:28:17  jalet
# Initial import into CVS
#
#
#

import sys
import glob
import os
from distutils.core import setup

sys.path.insert(0, "pykota")
from pykota.version import __version__, __doc__

ACTION_CONTINUE = 0
ACTION_ABORT = 1

def checkModule(module) :
    """Checks if a Python module is available or not."""
    try :
        exec "import %s" % module
    except ImportError :    
        return 0
    else :    
        return 1
        
def checkCommand(command) :
    """Checks if a command is available or not."""
    input = os.popen("type %s 2>/dev/null" % command)
    result = input.read().strip()
    input.close()
    return result
    
def checkWithPrompt(prompt, module=None, command=None) :
    """Tells the user what will be checked, and asks him what to do if something is absent."""
    sys.stdout.write("Checking for %s availability : " % prompt)
    sys.stdout.flush()
    if command is not None :
        result = checkCommand(command)
    elif module is not None :    
        result = checkModule(module)
    if result :    
        sys.stdout.write("OK\n")
        return ACTION_CONTINUE
    else :    
        sys.stdout.write("NO.\n")
        sys.stderr.write("ERROR : %s not available !\n" % prompt)
        answer = raw_input("%s is missing. Do you want to continue anyway (y/N) ? " % prompt)
        if answer[0:1].upper() == 'Y' :
            return ACTION_CONTINUE
        else :
            return ACTION_ABORT
    
if "install" in sys.argv :
    # checks if Python version is correct, we need >= 2.1
    if not (sys.version > "2.1") :
        sys.stderr.write("PyKota needs at least Python v2.1 !\nYour version seems to be older than that, please update.\nAborted !\n")
        sys.exit(-1)
        
    # checks if a configuration file is present in the old location
    if os.path.isfile("/etc/cups/pykota.conf") :
        if not os.path.isfile("/etc/pykota.conf") :
            sys.stdout.write("From version 1.02 on, PyKota expects to find its configuration file in /etc instead of /etc/cups.\n")
            sys.stdout.write("It seems that you've got a configuration file in the old location, so it will not be used anymore, and no configuration file in the new location.\n")
            answer = raw_input("Do you want me to move your configuration file to the new location in /etc (y/N) ? ")
            if answer[0:1].upper() == 'Y' :
                try :
                    os.rename("/etc/cups/pykota.conf", "/etc/pykota.conf")
                except OSError :    
                    sys.stderr.write("ERROR : An error occured while moving /etc/cups/pykota.conf to /etc/pykota.conf\nAborted !\n")
                    sys.exit(-1)
            else :
                sys.stderr.write("WARNING : Configuration file /etc/cups/pykota.conf won't be used ! Move it to /etc instead.\n")
                sys.stderr.write("PyKota installation will continue anyway, but the software won't run until you put a proper configuration file in /etc\n")
        else :        
            sys.stderr.write("WARNING : Configuration file /etc/cups/pykota.conf will not be used !\nThe file /etc/pykota.conf will be used instead.\n")
    
    # checks if some needed Python modules are there or not.
    modulestocheck = [("PygreSQL", "pg"), ("mxDateTime", "mx.DateTime")]
    commandstocheck = [("SNMP Tools", "snmpget")]
    for (name, module) in modulestocheck :
        action = checkWithPrompt(name, module=module)
        if action == ACTION_ABORT :
            sys.stderr.write("Aborted !\n")
            sys.exit(-1)
            
    # checks if some software are there or not.
    for (name, command) in commandstocheck :
        action = checkWithPrompt(name, command=command)
        if action == ACTION_ABORT :
            sys.stderr.write("Aborted !\n")
            sys.exit(-1)
            
data_files = []
mofiles = glob.glob(os.sep.join(["po", "*", "*.mo"]))
for mofile in mofiles :
    lang = mofile.split(os.sep)[1]
    directory = os.sep.join(["share", "locale", lang, "LC_MESSAGES"])
    data_files.append((directory, [ mofile ]))
    
directory = os.sep.join(["share", "man", "man1"])
manpages = glob.glob(os.sep.join(["man", "*.1"]))    
data_files.append((directory, manpages))

setup(name = "pykota", version = __version__,
      license = "GNU GPL",
      description = __doc__,
      author = "Jerome Alet",
      author_email = "alet@librelogiciel.com",
      url = "http://www.librelogiciel.com/software/",
      packages = [ "pykota", "pykota.storages", "pykota.requesters", "pykota.loggers" ],
      scripts = [ "bin/pykota", "bin/edpykota", "bin/repykota", "bin/warnpykota" ],
      data_files = data_files)

