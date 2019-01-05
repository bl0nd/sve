# -*- coding: utf-8 -*-

"""
sve.sve
~~~~~~~

This module does something.
"""

from __version__ import __version__
from drawing import header
from utils import (
        get_os, get_existing, get_active, get_versions, get_configs
)

def main():
    header('sve session started')
    distro = get_os()
    existing_srvs = get_existing(distro)
    active_srvs = get_active(distro)
    configs = get_configs(distro, services=['ftp', 'ssh', 'asdf', 'fdas'])
    print(configs)
    versions = get_versions(distro)


if __name__ == '__main__':
    main()
