# PyKota
#
# PyKota - Print Quotas for CUPS and LPRng
#
# (c) 2003 Jerome Alet <alet@librelogiciel.com>
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
# Revision 1.1  2003/04/29 18:37:54  jalet
# Pluggable accounting methods (actually doesn't support external scripts)
#
#
#

from pykota.accounter import AccounterBase, PyKotaAccounterError
from pykota.requester import openRequester, PyKotaRequesterError

MAXTRIES = 6     # maximum number of tries to get the printer's internal page counter
TIMETOSLEEP = 10 # number of seconds to sleep between two tries to get the printer's internal page counter

class Accounter(AccounterBase) :
    def doAccounting(self, printerid, userid) :
        """Does print accounting and returns if the job status is ALLOW or DENY."""
        # Get the page counter directly from the printer itself
        # Tries MAXTRIES times, sleeping two seconds each time, in case the printer is sleeping.
        # This was seen with my Apple LaserWriter 16/600 PS which doesn't answer before having warmed up.
        global MAXTRIES, TIMETOSLEEP
        requester = openRequester(self.filter.config, self.filter.printername)
        for i in range(MAXTRIES) :
            try :
                counterbeforejob = requester.getPrinterPageCounter(self.filter.printerhostname)
            except PyKotaRequesterError, msg :
                # can't get actual page counter, assume printer is off or warming up
                # log the message anyway.
                self.filter.logger.log_message("%s" % msg, "warn")
                counterbeforejob = None
                printerIsOff = 1
            else :    
                # printer answered, it is on so we can exit the loop
                printerIsOff = 0
                break
            time.sleep(TIMETOSLEEP)    
        
        # get last job information for this printer
        pgc = self.filter.storage.getPrinterPageCounter(printerid)    
        if pgc is None :
            # The printer hasn't been used yet, from PyKota's point of view
            lasthistoryid = None
            lastjobid = self.filter.jobid
            lastuserid = userid
            lastusername = self.filter.username
            lastpagecounter = counterbeforejob
        else :    
            # get last values from Quota Storage
            (lasthistoryid, lastjobid, lastuserid, lastusername, lastpagecounter) = (pgc["id"], pgc["jobid"], pgc["userid"], pgc["username"], pgc["pagecounter"])
            
        # if printer is off then we assume the correct counter value is the last one
        if printerIsOff :
            counterbeforejob = lastpagecounter
            
        # if the internal lifetime page counter for this printer is 0    
        # then this may be a printer with a volatile counter (never
        # saved to NVRAM) which has just been switched off and then on
        # so we use the last page counter from the Quota Storage instead
        # explanation at : http://web.mit.edu/source/third/lprng/doc/LPRng-HOWTO-15.html
        if counterbeforejob == 0 :
            counterbeforejob = lastpagecounter
            
        # Computes the last job size as the difference between internal page
        # counter in the printer and last page counter taken from the Quota
        # Storage database for this particular printer
        try :
            jobsize = (counterbeforejob - lastpagecounter)    
        except TypeError :    
            # never used, and internal page counter not accessible
            jobsize = 0
            
        if jobsize < 0 :
            # Probably an HP printer which was switched off and back on, 
            # its primary counter is only saved in a 10 increment, so
            # it may be lower than the last page counter saved in the
            # Quota Storage. 
            # We unconditionnally set the last job's size to 
            # abs(int((10 - abs(lastcounter(snmp) - lastcounter(storage)) / 2))
            # For more accurate accounting, don't switch off your HP printers !
            # explanation at : http://web.mit.edu/source/third/lprng/doc/LPRng-HOWTO-15.html
            self.filter.logger.log_message(_("Error in page count value %i for user %s on printer %s") % (jobsize, lastusername, self.filter.printername), "error")
            jobsize = abs(int((10 - abs(jobsize)) / 2))     # Workaround for HP printers' feature !
            
        # update the quota for the previous user on this printer 
        self.filter.storage.updateUserPQuota(lastuserid, printerid, jobsize)
        
        # update the last job size in the history
        self.filter.storage.updateJobSizeInHistory(lasthistoryid, jobsize)
        
        # warns the last user if he is over quota
        self.filter.warnUserPQuota(lastusername, self.filter.printername)
            
        # Is the current user allowed to print at all ?
        action = self.filter.warnUserPQuota(self.filter.username, self.filter.printername)
        
        # adds the current job to history    
        self.filter.storage.addJobToHistory(self.filter.jobid, self.filter.storage.getUserId(self.filter.username), printerid, counterbeforejob, action)
            
        return action
