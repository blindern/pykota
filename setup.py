#! /usr/bin/env python
# -*- coding: ISO-8859-15 -*-
#
# PyKota
#
# PyKota : Print Quotas for CUPS and LPRng
#
# (c) 2003-2004 Jerome Alet <alet@librelogiciel.com>
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.
#
# $Id$
#
# $Log$
# Revision 1.54  2004/10/13 07:45:01  jalet
# Modified installation script to please both me and the Debian packagers
#
# Revision 1.53  2004/10/04 21:25:29  jalet
# dumpykota can now output datas in the XML format
#
# Revision 1.52  2004/09/30 09:52:45  jalet
# Initial release of autopykota. Reading help or manpage is greatly
# encouraged !
#
# Revision 1.51  2004/09/21 21:31:35  jalet
# Installation script now checks for availability of Python-SNMP (http://pysnmp.sf.net)
#
# Revision 1.50  2004/09/14 22:29:12  jalet
# First version of dumpykota. Works fine but only with PostgreSQL backend
# for now.
#
# Revision 1.49  2004/07/28 13:00:02  jalet
# Now takes care of .sxi and .sxc files if any
#
# Revision 1.48  2004/07/27 07:14:24  jalet
# Now warns the user if pyosd is not present
#
# Revision 1.47  2004/07/16 12:22:45  jalet
# LPRng support early version
#
# Revision 1.46  2004/07/07 13:21:26  jalet
# Introduction of the pykosd command
#
# Revision 1.45  2004/07/06 09:37:01  jalet
# Integrated most of the Debian packaging work made by Sergio Gonz�lez Gonz�lez
#
# Revision 1.44  2004/06/05 22:03:49  jalet
# Payments history is now stored in database
#
# Revision 1.43  2004/05/25 09:49:41  jalet
# The old pykota filter has been removed. LPRng support disabled for now.
#
# Revision 1.42  2004/05/18 14:48:46  jalet
# Big code changes to completely remove the need for "requester" directives,
# jsut use "hardware(... your previous requester directive's content ...)"
#
# Revision 1.41  2004/05/13 14:17:32  jalet
# Warning about changed accounter and requester directives
#
# Revision 1.40  2004/05/13 13:59:27  jalet
# Code simplifications
#
# Revision 1.39  2004/04/08 17:07:41  jalet
# pkpgcounter added
#
# Revision 1.38  2004/03/18 09:18:09  jalet
# Installation now checks for old scripts
#
# Revision 1.37  2004/03/03 19:35:36  jalet
# Spelling problem. Thanks to Jurandy Martins
#
# Revision 1.36  2004/02/25 15:10:38  jalet
# Preliminary snmpprinterstatus command added.
#
# Revision 1.35  2004/02/12 22:43:58  jalet
# Better integration in Debian and more LSB compliance, thanks to
# Peter Hawkins.
#
# Revision 1.34  2004/02/07 13:45:51  jalet
# Preliminary work on the pkhint command
#
# Revision 1.33  2004/02/04 11:16:59  jalet
# pkprinters command line tool added.
#
# Revision 1.32  2004/01/18 20:52:50  jalet
# Portuguese portuguese translation replaces brasilian portuguese one, which
# moves in its own directory.
# Installation script modified to reorganise installed documentation and include
# the documentation on OpenOffice.org + ODBC
#
# Revision 1.31  2004/01/15 12:50:41  jalet
# Installation scripts now tells where the documentation was installed.
#
# Revision 1.30  2004/01/12 15:45:03  jalet
# Now installs documentation in /usr/share/doc/pykota too.
#
# Revision 1.29  2004/01/08 14:10:32  jalet
# Copyright year changed.
#
# Revision 1.28  2003/12/27 16:49:25  uid67467
# Should be ok now.
#
# Revision 1.28  2003/12/06 09:03:43  jalet
# Added Perl script to retrieve printer's internal page counter via PJL,
# contributed by Ren� Lund Jensen.
#
# Revision 1.27  2003/11/28 08:31:28  jalet
# Shell script to wait for AppleTalk enabled printers being idle was added.
#
# Revision 1.26  2003/11/08 16:05:31  jalet
# CUPS backend added for people to experiment.
#
# Revision 1.25  2003/10/08 07:01:19  jalet
# Job history can be disabled.
# Some typos in README.
# More messages in setup script.
#
# Revision 1.24  2003/10/07 09:07:27  jalet
# Character encoding added to please latest version of Python
#
# Revision 1.23  2003/07/29 20:55:17  jalet
# 1.14 is out !
#
# Revision 1.22  2003/07/29 09:54:03  jalet
# Added configurable LDAP mail attribute support
#
# Revision 1.21  2003/07/28 09:11:12  jalet
# PyKota now tries to add its attributes intelligently in existing LDAP
# directories.
#
# Revision 1.20  2003/07/23 16:51:32  jalet
# waitprinter.sh is now included to prevent PyKota from asking the
# printer's internal page counter while a job is still being printer.
#
# Revision 1.19  2003/07/16 21:53:07  jalet
# Really big modifications wrt new configuration file's location and content.
#
# Revision 1.18  2003/07/03 09:44:00  jalet
# Now includes the pykotme utility
#
# Revision 1.17  2003/06/30 12:46:15  jalet
# Extracted reporting code.
#
# Revision 1.16  2003/06/06 20:49:15  jalet
# Very latest schema. UNTESTED.
#
# Revision 1.15  2003/05/17 16:32:30  jalet
# Also outputs the original import error message.
#
# Revision 1.14  2003/05/17 16:31:38  jalet
# Dies gracefully if DistUtils is not present.
#
# Revision 1.13  2003/04/29 18:37:54  jalet
# Pluggable accounting methods (actually doesn't support external scripts)
#
# Revision 1.12  2003/04/23 22:13:56  jalet
# Preliminary support for LPRng added BUT STILL UNTESTED.
#
# Revision 1.11  2003/04/17 13:49:29  jalet
# Typo
#
# Revision 1.10  2003/04/17 13:48:39  jalet
# Better help
#
# Revision 1.9  2003/04/17 13:47:28  jalet
# Help added during installation.
#
# Revision 1.8  2003/04/15 17:49:29  jalet
# Installation script now checks the presence of Netatalk
#
# Revision 1.7  2003/04/03 20:03:37  jalet
# Installation script now allows to install the sample configuration file.
#
# Revision 1.6  2003/03/29 13:45:26  jalet
# GPL paragraphs were incorrectly (from memory) copied into the sources.
# Two README files were added.
# Upgrade script for PostgreSQL pre 1.01 schema was added.
#
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

#########################################################

#
# IMPORTANT : Modify the variable below if needed 
#
# 0 - You're NOT trying to build a Debian package 
#
# 1 - You ARE trying to build a Debian package
#
DEBIAN_BUILD_PACKAGE = 0

#########################################################


import sys
import glob
import os
import shutil
try :
    from distutils.core import setup
except ImportError, msg :    
    sys.stderr.write("%s\n" % msg)
    sys.stderr.write("You need the DistUtils Python module.\nunder Debian, you may have to install the python-dev package.\nOf course, YMMV.\n")
    sys.exit(-1)

from distutils import sysconfig
sys.path.insert(0, "pykota")
from pykota.version import __version__, __doc__

ACTION_CONTINUE = 0
ACTION_ABORT = 1

if DEBIAN_BUILD_PACKAGE :
    ETC_DIR = "./debian/tmp/etc/pykota/"
else :    
    ETC_DIR = "/etc/pykota/"

def checkOldModule(path) :
    """Checks if an old PyKota module is still in the destination (in case of upgrade)."""
    fname = os.path.join(sysconfig.get_python_lib(), "pykota", path)
    for ext in ["py", "pyc", "pyo"] :
        fullname = "%s.%s" % (fname, ext)
        if os.path.isfile(fullname) and not DEBIAN_BUILD_PACKAGE :
            sys.stderr.write("ERROR : old module %s still exists. Remove it and restart installation.\n" % fullname)
            sys.stderr.write("INSTALLATION ABORTED !\n")
            sys.exit(-1)
    
def checkOldScript(cmd) :
    """Checks if an old shell script is still around in /usr/bin."""
    return os.path.isfile(os.path.join("/usr/bin", cmd))

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
    
def checkWithPrompt(prompt, module=None, command=None, helper=None) :
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
        if helper is not None and not DEBIAN_BUILD_PACKAGE :
            sys.stdout.write("%s\n" % helper)
            sys.stdout.write("You may continue safely if you don't need this functionnality.\n")
        answer = raw_input("%s is missing. Do you want to continue anyway (y/N) ? " % prompt)
        if DEBIAN_BUILD_PACKAGE :
            return ACTION_CONTINUE
        elif answer[0:1].upper() == 'Y' :
            return ACTION_CONTINUE
        else :
            return ACTION_ABORT
    
if ("install" in sys.argv) and not ("help" in sys.argv) :
    # checks if Python version is correct, we need >= 2.1
    if not (sys.version > "2.1") :
        sys.stderr.write("PyKota needs at least Python v2.1 !\nYour version seems to be older than that, please update.\nAborted !\n")
        sys.exit(-1)
        
    # checks if a configuration file is present in the new location
    if not os.path.isfile(os.path.join(ETC_DIR,"pykota.conf")) :
        if not os.path.isdir(ETC_DIR) :
            try :
                os.mkdir(ETC_DIR)
            except OSError, msg :    
                sys.stderr.write("An error occured while creating the etc/pykota directory.\n%s\n" % msg)
                sys.exit(-1)
                
        if os.path.isfile("/etc/pykota.conf") and not DEBIAN_BUILD_PACKAGE :
            # upgrade from pre-1.14 to 1.14 and above
            sys.stdout.write("From version 1.14 on, PyKota expects to find its configuration\nfile in /etc/pykota/ instead of /etc/\n")
            sys.stdout.write("It seems that you've got a configuration file in the old location,\nso it will not be used anymore,\nand there's no configuration file in the new location.\n")
            answer = raw_input("Do you want to move /etc/pykota.conf to /etc/pykota/pykota.conf (y/N) ? ")
            if answer[0:1].upper() == 'Y' :
                try :
                    os.rename("/etc/pykota.conf", os.path.join(ETC_DIR,"pykota.conf"))
                except OSError :    
                    sys.stderr.write("ERROR : An error occured while moving /etc/pykota.conf to /etc/pykota/pykota.conf\nAborted !\n")
                    sys.exit(-1)
                else :    
                    sys.stdout.write("Configuration file /etc/pykota.conf moved to /etc/pykota/pykota.conf.\n")
            else :
                sys.stderr.write("WARNING : Configuration file /etc/pykota.conf won't be used ! Move it to /etc/pykota/ instead.\n")
                sys.stderr.write("PyKota installation will continue anyway,\nbut the software won't run until you put a proper configuration file in /etc/pykota/\n")
            dummy = raw_input("Please press ENTER when you have read the message above. ")
        else :
            # first installation
            if DEBIAN_BUILD_PACKAGE :
                try :
                    shutil.copy("conf/pykota.conf.sample", os.path.join(ETC_DIR,"pykota.conf"))
                    shutil.copy("conf/pykotadmin.conf.sample", os.path.join(ETC_DIR,"pykotadmin.conf"))
                except IOError, msg :
                    sys.stderr.write("WARNING : Problem while installing sample configuration files in /etc/pykota/, please do it manually.\n%s\n" % msg)
            else :
                if os.path.isfile("conf/pykota.conf.sample") :
                    answer = raw_input("Do you want to install\n\tconf/pykota.conf.sample as /etc/pykota/pykota.conf (y/N) ? ")
                    if answer[0:1].upper() == 'Y' :
                        try :
                            shutil.copy("conf/pykota.conf.sample", os.path.join(ETC_DIR,"pykota.conf"))        
                            shutil.copy("conf/pykotadmin.conf.sample", os.path.join(ETC_DIR,"pykotadmin.conf"))        
                        except IOError, msg :    
                            sys.stderr.write("WARNING : Problem while installing sample configuration files in /etc/pykota/, please do it manually.\n%s\n" % msg)
                        else :    
                            sys.stdout.write("Configuration file /etc/pykota/pykota.conf and /etc/pykota/pykotadmin.conf installed.\nDon't forget to adapt these files to your needs.\n")
                    else :        
                        sys.stderr.write("WARNING : PyKota won't run without a configuration file !\n")
                else :        
                    # Problem ?
                    sys.stderr.write("WARNING : PyKota's sample configuration file cannot be found.\nWhat you have downloaded seems to be incomplete,\nor you are not in the pykota directory.\nPlease double check, and restart the installation procedure.\n")
                dummy = raw_input("Please press ENTER when you have read the message above. ")
    else :    
        # already at 1.14 or above.
        # Now check if old scripts are still in /usr/bin
        for script in ["cupspykota", "pykota", "waitprinter.sh", "papwaitprinter.sh", "mailandpopup.sh", "pagecount.pl"] :
            if checkOldScript(script) and not DEBIAN_BUILD_PACKAGE :
                sys.stderr.write("WARNING : the %s script is still present in /usr/bin, but the new version will be installed in /usr/share/pykota, please remove the %s script from /usr/bin and double check that your configuration is correct.\n" % (script, script))
                if script == "cupspykota" :
                    sys.stderr.write("\nBe sure to also remove the old symbolic link from /usr/lib/cups/backend/cupspykota to /usr/bin/cupspykota. You'll have to recreate it once the installation has finished successfully.\n")
                sys.stderr.write("\nINSTALLATION ABORTED !\nPlease correct the problem and restart installation.\n")
                sys.exit(-1)
                
        # now checks if pre-1.19alpha8 code is still there       
        for module in ["accounters/querying", "accounters/external", "requesters/snmp", "requesters/external"] :
            checkOldModule(module)
        
    # Second stage, we will fail if onfiguration is incorrect for security reasons
    from pykota.config import PyKotaConfig,PyKotaConfigError
    try :
        conf = PyKotaConfig(ETC_DIR)
    except PyKotaConfigError, msg :    
        sys.stedrr.write("%s\nINSTALLATION ABORTED !\nPlease restart installation.\n" % msg)
        sys.exit(-1)
    else :
        hasadmin = conf.getGlobalOption("storageadmin", ignore=1)
        hasadminpw = conf.getGlobalOption("storageadminpw", ignore=1)
        hasuser = conf.getGlobalOption("storageuser", ignore=1)
        if hasadmin or hasadminpw : 
            sys.stderr.write("From version 1.14 on, PyKota expects that /etc/pykota/pykota.conf doesn't contain the Quota Storage Administrator's name and optional password.\n")
            sys.stderr.write("Please put these in a [global] section in /etc/pykota/pykotadmin.conf\n")
            sys.stderr.write("Then replace these values with 'storageuser' and 'storageuserpw' in /etc/pykota/pykota.conf\n")
            sys.stderr.write("These two fields were re-introduced to allow any user to read to his own quota, without allowing them to modify it.\n")
            sys.stderr.write("You can look at the conf/pykota.conf.sample and conf/pykotadmin.conf.sample files for examples.\n")
            sys.stderr.write("YOU HAVE TO DO THESE MODIFICATIONS MANUALLY, AND RESTART THE INSTALLATION.\n")
            sys.stderr.write("INSTALLATION ABORTED FOR SECURITY REASONS.\n")
            sys.exit(-1)
        if not hasuser :
            sys.stderr.write("From version 1.14 on, PyKota expects that /etc/pykota/pykota.conf contains the Quota Storage Normal User's name and optional password.\n")
            sys.stderr.write("Please put these in a [global] section in /etc/pykota/pykota.conf\n")
            sys.stderr.write("These fields are respectively named 'storageuser' and 'storageuserpw'.\n")
            sys.stderr.write("These two fields were re-introduced to allow any user to read to his own quota, without allowing them to modify it.\n")
            sys.stderr.write("You can look at the conf/pykota.conf.sample and conf/pykotadmin.conf.sample files for examples.\n")
            sys.stderr.write("YOU HAVE TO DO THESE MODIFICATIONS MANUALLY, AND RESTART THE INSTALLATION.\n")
            sys.stderr.write("INSTALLATION ABORTED FOR SECURITY REASONS.\n")
            sys.exit(-1)
            
        sb = conf.getStorageBackend()
        if (sb.get("storageadmin") is None) or (sb.get("storageuser") is None) :
            sys.stderr.write("From version 1.14 on, PyKota expects that /etc/pykota/pykota.conf contains the Quota Storage Normal User's name and optional password which gives READONLY access to the Print Quota DataBase,")
            sys.stderr.write("and that /etc/pykota/pykotadmin.conf contains the Quota Storage Administrator's name and optional password which gives READ/WRITE access to the Print Quota DataBase.\n")
            sys.stderr.write("Your configuration doesn't seem to be OK, please modify your configuration files in /etc/pykota/\n")
            sys.stderr.write("AND RESTART THE INSTALLATION.\n")
            sys.stderr.write("INSTALLATION ABORTED FOR SECURITY REASONS.\n")
            sys.exit(-1)
            
        # warns for new LDAP fields    
        if sb.get("storagebackend") == "ldapstorage" :    
            usermail = conf.getGlobalOption("usermail", ignore=1)
            newuser = conf.getGlobalOption("newuser", ignore=1)
            newgroup = conf.getGlobalOption("newgroup", ignore=1)
            if not (usermail and newuser and newgroup) :
                sys.stderr.write("From version 1.14 on, PyKota LDAP Support needs three additional configuration fields.\n")
                sys.stderr.write("Please put the 'usermail', 'newuser' and 'newgroup' configuration fields in a\n[global] section in /etc/pykota/pykota.conf\n")
                sys.stderr.write("You can look at the conf/pykota.conf.sample file for examples.\n")
                sys.stderr.write("YOU HAVE TO DO THESE MODIFICATIONS MANUALLY, AND RESTART THE INSTALLATION.\n")
                sys.stderr.write("INSTALLATION ABORTED BECAUSE CONFIGURATION INCOMPLETE.\n")
                sys.exit(-1)

#### INFO ####
                
        # Say something about caching mechanism and disabling job history
        if not DEBIAN_BUILD_PACKAGE :
            sys.stdout.write("You can now activate the database caching mechanism\nwhich is disabled by default.\nIt is especially recommended with the LDAP backend.\n")
            sys.stdout.write("You can now disable the preservation of the complete\njob history which is enabled by default.\nIt is probably more useful with the LDAP backend.\n")
            sys.stdout.write("PLEASE LOOK AT THE SAMPLE CONFIGURATION FILE conf/pykota.conf.sample\n")
            sys.stdout.write("TO LEARN HOW TO DO\n")
            dummy = raw_input("Please press ENTER when you have read the message above. ")
            sys.stdout.write("\n")
            
    # change files permissions    
    os.chmod(os.path.join(ETC_DIR,"pykota.conf"), 0644)
    os.chmod(os.path.join(ETC_DIR,"pykotadmin.conf"), 0640)
    
#### INFO ####

    # WARNING MESSAGE    
    if not DEBIAN_BUILD_PACKAGE :
        sys.stdout.write("WARNING : IF YOU ARE UPGRADING FROM A PRE-1.19alpha17 TO 1.19alpha17 OR ABOVE\n")
        sys.stdout.write("AND USE THE POSTGRESQL BACKEND, THEN YOU HAVE TO MODIFY YOUR\n")
        sys.stdout.write("DATABASE SCHEMA USING initscripts/postgresql/upgrade-to-1.19.sql\n")
        sys.stdout.write("PLEASE READ DOCUMENTATION IN initscripts/postgresql/ TO LEARN HOW TO DO.\n")
        sys.stdout.write("YOU CAN DO THAT AFTER THE INSTALLATION IS FINISHED, OR PRESS CTRL+C NOW.\n")
        sys.stdout.write("\n\nYOU DON'T HAVE ANYTHING SPECIAL TO DO IF THIS IS YOUR FIRST INSTALLATION\nOR IF YOU ARE ALREADY RUNNING VERSION 1.19alpha17 OR ABOVE.\n\n")
        dummy = raw_input("Please press ENTER when you have read the message above. ")
        
        sys.stdout.write("\n\nWARNING : IF YOU ARE UPGRADING FROM A PRE-1.19alpha10 TO 1.19alpha10 OR ABOVE\n")
        sys.stdout.write("YOU **MUST** MODIFY YOUR /etc/pykota/pykota.conf FILE BECAUSE accounter\n")
        sys.stdout.write("AND requester DIRECTIVES SUPPORTED VALUES HAVE CHANGED.\n\n")
        sys.stdout.write("YOU CAN DO THAT AFTER THE INSTALLATION IS FINISHED, OR PRESS CTRL+C NOW.\n")
        sys.stdout.write("\n\nYOU DON'T HAVE ANYTHING SPECIAL TO DO IF THIS IS YOUR FIRST INSTALLATION\nOR IF YOU ARE ALREADY RUNNING VERSION 1.19alpha10 OR ABOVE.\n\n")
        dummy = raw_input("Please press ENTER when you have read the message above. ")
    
    # checks if some needed Python modules are there or not.
    if not DEBIAN_BUILD_PACKAGE :
        modulestocheck = [ ("PygreSQL", "pg", "PygreSQL is mandatory if you want to use PostgreSQL as the quota storage backend.\nSee http://www.pygresql.org"),                                            
                           ("mxDateTime", "mx.DateTime", "eGenix' mxDateTime is mandatory for PyKota to work.\nSee http://www.egenix.com"), 
                           ("Python-LDAP", "ldap", "Python-LDAP is mandatory if you plan to use an LDAP\ndirectory as the quota storage backend.\nSee http://python-ldap.sf.net"),
                           ("Python-OSD", "pyosd", "Python-OSD is recommended if you plan to use the X Window On Screen Display\nprint quota reminder named pykosd."),
                           ("Python-SNMP", "pysnmp", "Python-SNMP is recommended if you plan to use hardware\naccounting with printers which support SNMP.\nSee http://pysnmp.sf.net"),
                           ("Python-JAXML", "jaxml", "Python-JAXML is recommended if you plan to dump datas in the XML format.\nSee http://www.librelogiciel.com/software/"),
                         ]
        commandstocheck = [("SNMP Tools", "snmpget", "SNMP Tools are needed if you want to use SNMP enabled printers."), ("Netatalk", "pap", "Netatalk is needed if you want to use AppleTalk enabled printers.")]
        for (name, module, helper) in modulestocheck :
            action = checkWithPrompt(name, module=module, helper=helper)
            if action == ACTION_ABORT :
                sys.stderr.write("Aborted !\n")
                sys.exit(-1)
                
        # checks if some software are there or not.
        for (name, command, helper) in commandstocheck :
            action = checkWithPrompt(name, command=command, helper=helper)
            if action == ACTION_ABORT :
                sys.stderr.write("Aborted !\n")
                sys.exit(-1)
            
data_files = []
mofiles = glob.glob(os.sep.join(["po", "*", "*.mo"]))
for mofile in mofiles :
    lang = mofile.split(os.sep)[1]
    directory = os.sep.join(["share", "locale", lang, "LC_MESSAGES"])
    data_files.append((directory, [ mofile ]))
    
docdir = "share/doc/pykota"    
docfiles = ["README", "FAQ", "SECURITY", "COPYING", "LICENSE", "CREDITS", "TODO", "NEWS"]
data_files.append((docdir, docfiles))

docfiles = glob.glob(os.sep.join(["docs", "*.pdf"]))
docfiles += glob.glob(os.sep.join(["docs", "*.sx?"]))
data_files.append((docdir, docfiles))

docfiles = glob.glob(os.sep.join(["docs", "spanish", "*.pdf"]))
docfiles += glob.glob(os.sep.join(["docs", "spanish", "*.sxw"]))
data_files.append((os.path.join(docdir, "spanish"), docfiles))

docfiles = glob.glob(os.sep.join(["docs", "pykota", "*.html"]))
data_files.append((os.path.join(docdir, "html"), docfiles))

docfiles = glob.glob(os.sep.join(["openoffice", "*.sx?"]))
docfiles += glob.glob(os.sep.join(["openoffice", "*.png"]))
docfiles += glob.glob(os.sep.join(["openoffice", "README"]))
data_files.append((os.path.join(docdir, "openoffice"), docfiles))

directory = os.sep.join(["share", "man", "man1"])
manpages = glob.glob(os.sep.join(["man", "*.1"]))    
data_files.append((directory, manpages))

directory = os.sep.join(["share", "pykota"])
data_files.append((directory, ["bin/cupspykota", "bin/lprngpykota", "bin/waitprinter.sh", "bin/papwaitprinter.sh", "bin/mailandpopup.sh", "contributed/pagecount.pl", "untested/pjl/pagecount.pjl", "untested/pjl/status.pjl", "untested/netatalk/netatalk.sh", "untested/netatalk/pagecount.ps"]))

setup(name = "pykota", version = __version__,
      license = "GNU GPL",
      description = __doc__,
      author = "Jerome Alet",
      author_email = "alet@librelogiciel.com",
      url = "http://www.librelogiciel.com/software/",
      packages = [ "pykota", "pykota.storages", "pykota.loggers", "pykota.accounters", "pykota.reporters" ],
      scripts = [ "bin/autopykota", "bin/dumpykota", "bin/pkpgcounter", "bin/snmpprinterstatus", "bin/pykosd", "bin/edpykota", "bin/repykota", "bin/warnpykota", "bin/pykotme", "bin/pkprinters", "bin/pkhint" ],
      data_files = data_files)

if ("install" in sys.argv) and not ("help" in sys.argv) :
    sys.stdout.write("\n\nYou can give a look at PyKota's documentation in:\n%s\n\n" % docdir)
