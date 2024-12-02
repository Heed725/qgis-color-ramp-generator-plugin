# -*- coding: utf-8 -*-

# Resource object code
#
# Created by: The Resource Compiler for PyQt5 (pyrcc5)
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore

qt_resource_data = b"\
\x00\x00\x00\x00\
"

qt_resource_name = b"\
\x00\x04\
\x00\x00\x00\x00\
\x00\x69\
\x00\x63\x00\x6f\x00\x6e\
"

qt_resource_struct = b"\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x01\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x02\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x03\
"

def qInitResources():
    QtCore.qRegisterResourceData(0x01, qt_resource_struct, qt_resource_name, qt_resource_data)

def qCleanupResources():
    QtCore.qUnregisterResourceData(0x01, qt_resource_struct, qt_resource_name, qt_resource_data)

qInitResources()
