#
# Chris Lumens <clumens@redhat.com>
#
# Copyright 2005, 2006, 2007 Red Hat, Inc.
#
# This software may be freely redistributed under the terms of the GNU
# general public license.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#
from pykickstart.base import *
from pykickstart.errors import *
from pykickstart.options import *

from rhpl.translate import _
import rhpl.translate as translate

translate.textdomain("pykickstart")

class FC6_IscsiData(BaseData):
    def __init__(self, ipaddr="", port="", target="", user=None, password=None):
        BaseData.__init__(self)
        self.ipaddr = ipaddr
        self.port = port
        self.target = target
        self.user = user
        self.password = password

    def __str__(self):
        retval = "iscsi"

        if self.target != "":
            retval += " --target=%s" % self.target
        if self.ipaddr != "":
            retval += " --ipaddr=%s" % self.ipaddr
        if self.port != "":
            retval += " --port=%s" % self.port
        if self.user is not None:
            retval += " --user=%s" % self.user
        if self.password is not None:
            retval += " --password=%s" % self.password

        return retval + "\n"

class FC6_Iscsi(KickstartCommand):
    def __init__(self, writePriority=70, iscsi=None):
        KickstartCommand.__init__(self, writePriority)

        if iscsi == None:
            iscsi = []

        self.iscsi = iscsi

    def __str__(self):
        retval = ""
        for iscsi in self.iscsi:
            retval += iscsi.__str__()

        return retval

    def parse(self, args):
        op = KSOptionParser(lineno=self.lineno)
        op.add_option("--target", dest="ipaddr", action="store", type="string")
        op.add_option("--ipaddr", dest="ipaddr", action="store", type="string",
                      required=1)
        op.add_option("--port", dest="port", action="store", type="string")
        op.add_option("--user", dest="user", action="store", type="string")
        op.add_option("--password", dest="password", action="store",
                      type="string")

        (opts, extra) = op.parse_args(args=args)

        if len(extra) != 0:
            mapping = {"command": "scsi", "options": extra}
            raise KickstartValueError, formatErrorMsg(self.lineno, msg=_("Unexpected arguments to %(command)s command: %(options)s") % mapping)

        dd = FC6_IscsiData()
        self._setToObj(op, opts, dd)
        self.add(dd)

    def add(self, newObj):
        self.iscsi.append(newObj)