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
for dir in br en es fr it pt sv th ; do 
    cd $dir ;
    chmod 644 *.?o ;
    msgmerge -N pykota.po ../pykota.pot >pykota.po.new ;
    mv pykota.po.new pykota.po ;
    rm pykota.mo ;
    msgfmt -o pykota.mo pykota.po ;
    cd .. ;
done
