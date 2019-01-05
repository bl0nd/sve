# -*- coding: utf-8 -*-

"""
sve.utils

This module has utility functions.
"""
import os
import re
import sys
import subprocess as sp

def get_distro():
    """Get name of OS/distribution.

    If the OS is macOS or Windows, then the OS name is returned
      instead of a distribution name.
    """
    system_os = sys.platform
    if sys.platform.startswith("linux"):
        with open('/etc/os-release', 'r') as f:
            distro = f.readline().rstrip()[6:-1]
    # elif sys.platform.startswith("darwin"):
    # elif sys.platform.startswith("win32"):
    return distro

def get_configs(distro):
    """Get locations of service config files.

    :param distro: Name of Linux distribution.
    :return configs: Dictionary of services and their config files.
    :rtype: dict
    """
    if distro == 'Arch Linux':
        configs = {'ftp': '/etc/vsftpd.conf',
                   'ssh': '/etc/ssh/sshd_config',
                   'apache': '/etc/https/conf/httpd.conf',
                   'nginx': '/etc/nginx/nginx.conf',
                   }
    # elif distro == 'darwin':
    # elif distro == 'win32':
    else:
        sys.exit('error: unknown Linux distribution')

    return configs

def get_ftp_version(distro):
    """Get version number of FTP.

    :param distro: Name of Linux distribution.
    :return ftp_ver: Version number of FTP.
    :rtype: str
    """
    if distro == 'Arch Linux':
        ftp_ver_cmd = sp.run(['pacman', '-Q', 'vsftpd'], capture_output=True)
        ftp_ver = ftp_ver_cmd.stdout.decode().rstrip().split(' ')[1]
    # elif distro == 'darwin':
    # elif distro == 'win32':
    else:
        sys.exit('error: unknown Linux distribution')

    return ftp_ver

def get_ssh_version(distro, ssh_config):
    """Get version number of SSH.

    :param distro: Name of Linux distribution.
    :param ssh_config: Location of SSH configuration file.
    :return ssh_ver: Version number of SSH.
    :rtype: str

    TODO:
        1. May want to stay away from relying on config files.
             They can be changed, depend on commands instead.
    """
    if distro == 'Arch Linux':
        with open(ssh_config, 'r') as f:
            ssh_ver_line = f.readline()
        ssh_ver = ssh_ver_line.split('v ')[1].split(' ')[0]
    # elif distro == 'darwin':
    # elif distro == 'win32':
    else:
        sys.exit('error: unknown Linux distribution')

    return ssh_ver

def get_apache_version(distro):
    """Get version number of Apache.

    :param distro: Name of Linux distribution.
    :return apache_ver: Version number of Apache.
    :rtype: str
    """
    if distro == 'Arch Linux':
        apache_ver_cmd = sp.run(['httpd', '-v'], capture_output=True)
        apache_ver = re.search(r'\d*\.\d*\.\d*', apache_ver_cmd.stdout.decode()).group(0)
    # elif distro == 'darwin':
    # elif distro == 'win32':
    else:
        sys.exit('error: unknown Linux distribution')

    return apache_ver

def header(title, color='n', border_type='='):
    """Draw a header.

    ================= for example =================

    :param title: The header title.
    :param color: The first letter of the header's color (n is none).
    :param border_type: The character with which to compose the header.
    :rtype: None

    TODO:
        1. Bold
    """
    term_width = int(os.popen('stty size', 'r').read().split()[1])

    if term_width < len(title):
        sys.exit('error: terminal is too small')

    border_len = (term_width - len(title) - 2) // 2
    border = border_type * border_len

    if term_width % 2 == 0:
        extra = '' if len(title) % 2 == 0 else border_type
    else:
        extra = '' if len(title) % 2 != 0 else border_type

    print(f'{border} {title} {border}{extra}')

