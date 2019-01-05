# -*- coding: utf-8 -*-

"""
sve.utils

This module has utility functions.
"""
import sys
import subprocess as sp

def system_info():
    system_os = sys.platform
    if sys.platform.startswith("darwin"):
        distro = sp.run(['head', '-n1', '/etc/os-release'])
    elif sys.platform.startswith("darwin"):
        # MacOS
        pass
    elif sys.platform("win32"):
        #windows
        pass

system_info()