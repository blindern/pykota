#! /bin/sh
#
# PyKota - Print Quotas for CUPS and LPRng
#
# (c) 2003-2004 Jerome Alet <alet@librelogiciel.com>
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
for prog in pkmail pkbanner autopykota dumpykota edpykota pykotme repykota warnpykota pkprinters pkhint pykosd ; do 
    echo $prog ;
    help2man --no-info --section=1 --manual "User Commands" --source="C@LL - Conseil Internet & Logiciels Libres" --output=$prog.1 $prog ; 
    for loc in *_* ; do
        echo "  $loc" ;
        cd $loc ;
        help2man --no-info --locale=$loc --section=1 --manual "User Commands" --source="C@LL - Conseil Internet & Logiciels Libres" --output=$prog.1 $prog ; 
        cd .. ;
    done ;
    echo ;
done
