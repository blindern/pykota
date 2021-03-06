# -*- coding: utf-8 -*-
#
# PyKota : Print Quotas for CUPS
#
# (c) 2003-2013 Jerome Alet <alet@librelogiciel.com>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# $Id$
#
#

"""This module handles all the data dumping facilities for PyKota."""

import sys
import os
import pwd
from xml.sax import saxutils

from mx import DateTime

try :
    import jaxml
except ImportError :
    sys.stderr.write("The jaxml Python module is not installed. XML output is disabled.\n")
    sys.stderr.write("Download jaxml from http://www.librelogiciel.com/software/ or from your Debian archive of choice\n")
    hasJAXML = False
else :
    hasJAXML = True

from pykota.utils import *

from pykota import version
from pykota.tool import PyKotaTool
from pykota.errors import PyKotaToolError, PyKotaCommandLineError

class DumPyKota(PyKotaTool) :
    """A class for dumpykota."""
    validdatatypes = { u"history" : N_("History"),
                       u"users" : N_("Users"),
                       u"groups" : N_("Groups"),
                       u"printers" : N_("Printers"),
                       u"upquotas" : N_("Users Print Quotas"),
                       u"gpquotas" : N_("Users Groups Print Quotas"),
                       u"payments" : N_("History of Payments"),
                       u"pmembers" : N_("Printers Groups Membership"),
                       u"umembers" : N_("Users Groups Membership"),
                       u"billingcodes" : N_("Billing Codes"),
                       u"all": N_("All"),
                     }
    validformats = { u"csv" : N_("Comma Separated Values"),
                     u"ssv" : N_("Semicolon Separated Values"),
                     u"tsv" : N_("Tabulation Separated Values"),
                     u"xml" : N_("eXtensible Markup Language"),
                     u"cups" : N_("CUPS' page_log"),
                   }
    validfilterkeys = [ "username",
                        "groupname",
                        "printername",
                        "pgroupname",
                        "hostname",
                        "billingcode",
                        "jobid",
                        "start",
                        "end",
                      ]
    def main(self, arguments, options, restricted=True) :
        """Print Quota Data Dumper."""
        self.adminOnly(restricted)

        datatype = options.data
        if datatype not in self.validdatatypes.keys() :
            raise PyKotaCommandLineError, _("Invalid data type '%(datatype)s', see help.") % locals()

        orderby = options.orderby or []
        if orderby :
            fields = [f.strip() for f in orderby.split(",")]
            orderby = []
            for field in fields :
                if field.isalpha() \
                   or ((field[0] in ("+", "-")) and field[1:].isalpha()) :
                    orderby.append(field)
                else :
                    logerr(_("Skipping invalid ordering statement '%(field)s'") % locals())

        extractonly = {}
        if datatype == u"all" :
            if (options.format != u"xml") or options.sum or arguments :
                self.printInfo(_("Dumping all PyKota's datas forces format to XML, and disables --sum and filters."), "warn")
            options.format = u"xml"
            options.sum = None
        else :
            for filterexp in arguments :
                if filterexp.strip() :
                    try :
                        (filterkey, filtervalue) = [part.strip() for part in filterexp.split("=")]
                        filterkey = filterkey.encode("ASCII", "replace").lower()
                        if filterkey not in self.validfilterkeys :
                            raise ValueError
                    except ValueError :
                        raise PyKotaCommandLineError, _("Invalid filter value '%(filterexp)s', see help.") % locals()
                    else :
                        extractonly.update({ filterkey : filtervalue })

        format = options.format
        if (format not in self.validformats.keys()) \
           or ((format == u"cups") \
              and ((datatype != u"history") or options.sum)) :
            raise PyKotaCommandLineError, _("Invalid format '%(format)s', see help.") % locals()

        if (format == u"xml") and not hasJAXML :
            raise PyKotaToolError, _("XML output is disabled because the jaxml module is not available.")

        if datatype not in (u"payments", u"history") :
            if options.sum :
                raise PyKotaCommandLineError, _("Invalid data type '%(datatype)s' for --sum command line option, see help.") % locals()
            if extractonly.has_key(u"start") or extractonly.has_key(u"end") :
                self.printInfo(_("Invalid filter for the '%(datatype)s' data type.") % locals(), "warn")
                try :
                    del extractonly[u"start"]
                except KeyError :
                    pass
                try :
                    del extractonly[u"end"]
                except KeyError :
                    pass

        retcode = 0
        nbentries = 0
        mustclose = False
        outfname = options.output.strip().encode(sys.getfilesystemencoding())
        if outfname == "-" :
            self.outfile = sys.stdout
        else :
            self.outfile = open(outfname, "w")
            mustclose = True

        if datatype == u"all" :
            # NB : order does matter to allow easier or faster restore
            allentries = []
            datatypes = [ "printers", "pmembers", "users", "groups", \
                          "billingcodes", "umembers", "upquotas", \
                          "gpquotas", "payments", "history" ]
            neededdatatypes = datatypes[:]
            for datatype in datatypes :
                entries = getattr(self.storage, "extract%s" % datatype.title())(extractonly) # We don't care about ordering here
                if entries :
                    nbentries += len(entries)
                    allentries.append(entries)
                else :
                    neededdatatypes.remove(datatype)
            retcode = self.dumpXml(allentries, neededdatatypes)
        else :
            datatype = datatype.encode("ASCII")
            format = format.encode("ASCII")
            entries = getattr(self.storage, "extract%s" % datatype.title())(extractonly, orderby)
            if entries :
                nbentries = len(entries)
                retcode = getattr(self, "dump%s" % format.title())([self.summarizeDatas(entries, datatype, extractonly, options.sum)], [datatype])

        if mustclose :
            self.outfile.close()
            if not nbentries :
                os.remove(options.output)

        return retcode

    def summarizeDatas(self, entries, datatype, extractonly, sum=0) :
        """Transforms the datas into a summarized view (with totals).

           If sum is false, returns the entries unchanged.
        """
        if not sum :
            return entries
        else :
            headers = entries[0]
            nbheaders = len(headers)
            fieldnumber = {}
            fieldname = {}
            for i in range(nbheaders) :
                fieldnumber[headers[i]] = i

            if datatype == "payments" :
                totalize = [ ("amount", float) ]
                keys = [ "username" ]
            else : # elif datatype == "history"
                totalize = [ ("jobsize", int),
                             ("jobprice", float),
                             ("jobsizebytes", int),
                             ("precomputedjobsize", int),
                             ("precomputedjobprice", float),
                           ]
                keys = [ k for k in ("username", "printername", "hostname", "billingcode") if k in extractonly.keys() ]

            newentries = [ headers ]
            sortedentries = entries[1:]
            if keys :
                # If we have several keys, we can sort only on the first one, because they
                # will vary the same way.
                sortedentries.sort(lambda x, y, fnum=fieldnumber[keys[0]] : cmp(x[fnum], y[fnum]))
            totals = {}
            for (k, t) in totalize :
                totals[k] = { "convert" : t, "value" : 0.0 }
            prevkeys = {}
            for k in keys :
                prevkeys[k] = sortedentries[0][fieldnumber[k]]
            for entry in sortedentries :
                curval = '-'.join([str(entry[fieldnumber[k]]) for k in keys])
                prevval = '-'.join([str(prevkeys[k]) for k in keys])
                if curval != prevval :
                    summary = [ "*" ] * nbheaders
                    for k in keys :
                        summary[fieldnumber[k]] = prevkeys[k]
                    for k in totals.keys() :
                        summary[fieldnumber[k]] = totals[k]["convert"](totals[k]["value"])
                    newentries.append(summary)
                    for k in totals.keys() :
                        totals[k]["value"] = totals[k]["convert"](entry[fieldnumber[k]])
                else :
                    for k in totals.keys() :
                        totals[k]["value"] += totals[k]["convert"](entry[fieldnumber[k]] or 0.0)
                for k in keys :
                    prevkeys[k] = entry[fieldnumber[k]]
            summary = [ "*" ] * nbheaders
            for k in keys :
                summary[fieldnumber[k]] = prevkeys[k]
            for k in totals.keys() :
                summary[fieldnumber[k]] = totals[k]["convert"](totals[k]["value"])
            newentries.append(summary)
            return newentries

    def dumpWithSeparator(self, separator, allentries) :
        """Dumps datas with a separator."""
        try :
            for entries in allentries :
                for entry in entries :
                    line = []
                    for value in entry :
                        try :
                            strvalue = '"%s"' % value.encode(self.charset, \
                                                             "replace").replace(separator,
                                                                                "\\%s" % separator).replace('"', '\\"')
                        except AttributeError :
                            if value is None :
                                strvalue = '"None"' # Double quotes around None to prevent spreadsheet from failing
                            else :
                                strvalue = str(value)
                        line.append(strvalue)

                    self.outfile.write("%s\n" % separator.join(line))
        except IOError, msg :
            pass # We used to return an error, not really needed
        return 0

    def dumpCsv(self, allentries, dummy) :
        """Dumps datas with a comma as the separator."""
        return self.dumpWithSeparator(",", allentries)

    def dumpSsv(self, allentries, dummy) :
        """Dumps datas with a comma as the separator."""
        return self.dumpWithSeparator(";", allentries)

    def dumpTsv(self, allentries, dummy) :
        """Dumps datas with a comma as the separator."""
        return self.dumpWithSeparator("\t", allentries)

    def dumpCups(self, allentries, dummy) :
        """Dumps history datas as CUPS' page_log format."""
        months = [ "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec" ]
        entries = allentries[0]
        fieldnames = entries[0]
        fields = {}
        for i in range(len(fieldnames)) :
            fields[fieldnames[i]] = i
        sortindex = fields["jobdate"]
        entries = entries[1:]
        entries.sort(lambda m, n, si=sortindex : cmp(m[si], n[si]))
        for entry in entries :
            printername = entry[fields["printername"]]
            username = entry[fields["username"]]
            jobid = entry[fields["jobid"]]
            jobdate = DateTime.ISO.ParseDateTime(str(entry[fields["jobdate"]])[:19])
            gmtoffset = jobdate.gmtoffset()
            jobdate = "%02i/%s/%04i:%02i:%02i:%02i %+03i%02i" % (jobdate.day,
                                                                 months[jobdate.month - 1],
                                                                 jobdate.year,
                                                                 jobdate.hour,
                                                                 jobdate.minute,
                                                                 jobdate.second,
                                                                 gmtoffset.hour,
                                                                 gmtoffset.minute)
            jobsize = entry[fields["jobsize"]] or 0
            copies = entry[fields["copies"]] or 1
            hostname = entry[fields["hostname"]] or ""
            billingcode = entry[fields["billingcode"]] or "-"
            for pagenum in range(1, jobsize+1) :
                line = "%s %s %s [%s] %s %s %s %s" % (printername, username, jobid, jobdate, pagenum, copies, billingcode, hostname)
                self.outfile.write("%s\n" % line.encode(self.charset,
                                                        "replace"))
        return 0

    def dumpXml(self, allentries, datatypes) :
        """Dumps datas as XML."""
        x = jaxml.XML_document(encoding="UTF-8")
        x.pykota(version=version.__version__, author=version.__author__)
        for (entries, datatype) in zip(allentries, datatypes) :
            x._push()
            x.dump(storage=self.config.getStorageBackend()["storagebackend"], type=datatype)
            headers = entries[0]
            for entry in entries[1:] :
                x._push()
                x.entry()
                for (header, value) in zip(headers, entry) :
                    try :
                        strvalue = saxutils.escape(value.encode("UTF-8", \
                                                                "replace"), \
                                                   { "'" : "&apos;", \
                                                     '"' : "&quot;" })
                    except AttributeError :
                        strvalue = str(value)
                    # We use 'str' instead of 'unicode' below to be compatible
                    # with older releases of PyKota.
                    # The XML dump will contain UTF-8 encoded strings,
                    # not unicode strings anyway.
                    x.attribute(strvalue, \
                                type=type(value).__name__.replace("unicode", "str"), \
                                name=header)
                x._pop()
            x._pop()
        x._output(self.outfile)
        return 0
