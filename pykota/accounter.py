# PyKota
# -*- coding: ISO-8859-15 -*-
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
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# $Id$
#
#

import sys

class PyKotaAccounterError(Exception):
    """An exception for Accounter related stuff."""
    def __init__(self, message = ""):
        self.message = message
        Exception.__init__(self, message)
    def __repr__(self):
        return self.message
    __str__ = __repr__
    
class AccounterBase :    
    """A class to account print usage by querying printers."""
    def __init__(self, kotafilter, arguments) :
        """Sets instance vars depending on the current printer."""
        self.filter = kotafilter
        self.arguments = arguments
        self.onerror = self.filter.config.getPrinterOnAccounterError(self.filter.PrinterName)
        self.isSoftware = 1 # by default software accounting
        
    def getLastPageCounter(self) :    
        """Returns last internal page counter value (possibly faked)."""
        try :
            return self.LastPageCounter or 0
        except :    
            return 0
            
    def beginJob(self, printer) :    
        """Saves the computed job size."""
        # computes job's size
        self.JobSize = self.computeJobSize()
        if self.filter.InputFile is not None :
            self.JobSize *= self.filter.Copies
        
        # get last job information for this printer
        if not printer.LastJob.Exists :
            # The printer hasn't been used yet, from PyKota's point of view
            self.LastPageCounter = 0
        else :    
            # get last job size and page counter from Quota Storage
            # Last lifetime page counter before actual job is 
            # last page counter + last job size
            self.LastPageCounter = int(printer.LastJob.PrinterPageCounter or 0) + int(printer.LastJob.JobSize or 0)
        
    def fakeBeginJob(self) :    
        """Do nothing."""
        pass
        
    def endJob(self, printer) :    
        """Do nothing."""
        pass
        
    def getJobSize(self, printer) :    
        """Returns the actual job size."""
        try :
            return self.JobSize
        except AttributeError :    
            return 0
        
    def computeJobSize(self) :    
        """Must be overriden in children classes."""
        raise RuntimeError, "AccounterBase.computeJobSize() must be overriden !"
        
def openAccounter(kotafilter) :
    """Returns a connection handle to the appropriate accounter."""
    (backend, args) = kotafilter.config.getAccounterBackend(kotafilter.PrinterName)
    try :
        exec "from pykota.accounters import %s as accounterbackend" % backend.lower()
    except ImportError :
        raise PyKotaAccounterError, _("Unsupported accounter backend %s") % backend
    else :    
        return accounterbackend.Accounter(kotafilter, args)
