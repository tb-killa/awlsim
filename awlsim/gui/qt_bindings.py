# -*- coding: utf-8 -*-
#
# AWL simulator - QT bindings wrapper
#
# Copyright 2015 Michael Buesch <m@bues.ch>
#
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
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

from __future__ import division, absolute_import, print_function, unicode_literals
from awlsim.common.compat import *

from awlsim.common import *

import sys
import os


def __frameworkError(msg):
	printError("Awlsim-GUI: " + msg)
	input("Press enter to exit.")
	sys.exit(1)

def __autodetectGuiFramework():
	urls = {
		"pyside" : "http://www.pyside.org/",
		"pyqt4" : "http://www.riverbankcomputing.com/software/pyqt/download",
		"pyqt5" : "http://www.riverbankcomputing.com/software/pyqt/download5",
	}
	try:
		import PySide as __unused
		return "pyside4"
	except ImportError:
		pass
#FIXME	try:
#		import PyQt5 as __unused
#		return "pyqt5"
#	except ImportError:
#		pass
	try:
		import PyQt4 as __unused
		return "pyqt4"
	except ImportError:
		pass
	__frameworkError("Neither PySide nor PyQt found.\n"
			 "PLEASE INSTALL PySide (%s)\n"
			 "            or PyQt4 (%s)\n"
			 "            or PyQt5 (%s)" %\
			 (urls["pyside"],
			  urls["pyqt4"],
			  urls["pyqt5"]))

__guiFramework = os.getenv("AWLSIMGUI", "auto").lower()

if __guiFramework == "auto":
	__guiFramework = __autodetectGuiFramework()

if __guiFramework in ("pyside", "pyside4"):
	printInfo("Awlsim-GUI: Using PySide4 GUI framework")
	try:
		from PySide.QtCore import *
		from PySide.QtGui import *
	except ImportError as e:
		__frameworkError("Failed to import PySide modules:\n" + str(e))
elif __guiFramework == "pyqt4":
	printInfo("Awlsim-GUI: Using PyQt4 GUI framework")
	try:
		from PyQt4.QtCore import *
		from PyQt4.QtGui import *
	except ImportError as e:
		__frameworkError("Failed to import PyQt4 modules:\n" + str(e))
	# Compatibility
	Signal = pyqtSignal
elif __guiFramework in ("pyqt", "pyqt5"):
	printInfo("Awlsim-GUI: Using PyQt5 GUI framework")
	try:
		from PyQt5.QtCore import *
		from PyQt5.QtGui import *
		from PyQt5.QtWidgets import *
	except ImportError as e:
		__frameworkError("Failed to import PyQt5 modules:\n" + str(e))
	# Compatibility
	Signal = pyqtSignal
else:
	__frameworkError("Unknown GUI framework '%s' requested. "
			 "Please fix AWLSIMGUI environment variable." %\
			 __guiFramework)
