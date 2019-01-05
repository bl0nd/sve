# -*- coding: utf-8 -*-

"""
sve.utils

This module contains utility functions related to services.

If adding a service, please try to use the subprocess
  library as little as possible.
"""
import os
import re
import sys
import subprocess as sp

from service_info import (
        services_sve, services_actual, services_configs
)
from drawing import header

def get_os():
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


def get_existing(distro, services=None):
    """Determine installed services.

    :param distro: Name of OS/Linux distribution.
    :param services: (optional) List of existing services to check for.
    :return existing_srvs: List of existing services (actual names).
    :rtype: list

    TODO:
        1. Maybe return srv_e instead of srv_a?
    """
    unit_files = sp.run(['systemctl', 'list-unit-files'],
            capture_output=True).stdout.decode()
    existing_srvs = []

    for srv_e, srv_a in services_actual[distro].items():
        if (((services and srv_e in services) or not services) and
                f'{srv_a}.service' in unit_files):
            existing_srvs.append(srv_a)

    return existing_srvs


def get_active(distro, services=None):
    """Determine active services.

    :param distro: Name of OS/Linux distribution.
    :param services: (optional) List of active services to check for.
    :return active_srvs: Dictionary of services and their activity status.
    :rtype: dict
    """
    active_services = dict()

    for srv_e, srv_a in services_actual[distro].items():
        if (services and srv_e in services) or not services:
            status = sp.run(['systemctl', 'status', srv_a],
                    capture_output=True).stdout.decode()
            active_services[srv_a] = 'g' if "Active: active" in status else 'r'

    return active_services


def get_configs(distro, services=None):
    """Get locations of service config files.

    :param distro: Name of OS/Linux distribution.
    :param services: (optional) List of services to grab configs for.
    :return configs: Dictionary of services and their config files.
    :rtype: dict
    """
    configs = dict()
    try:
        if services:
            unknown_services = set(services) - set(services_configs[distro].keys())
            if unknown_services:
                sys.exit(f"error: unknown service: {', '.join(unknown_services)}")
            return {srv:cnf for srv,cnf in services_configs[distro].items() if srv in services}
        else:
            return services_configs[distro]
    except KeyError:
        sys.exit(f'error: unknown OS: {distro}')


def get_ftp_version(distro):
    """Get version number of FTP.

    :param distro: Name of OS/Linux distribution.
    :return ftp_ver: Version number of FTP.
    :rtype: str
    """
    if distro == 'Arch Linux':
        ftp_ver_cmd = sp.run(['pacman', '-Q', services_actual[distro]['ftp']],
                capture_output=True)
        ftp_ver = ftp_ver_cmd.stdout.decode().rstrip().split(' ')[1]
    # elif distro == 'darwin':
    # elif distro == 'win32':
    else:
        sys.exit('error: unknown Linux distribution')

    return ftp_ver


def get_ssh_version(distro, ssh_config):
    """Get version number of SSH.

    :param distro: Name of OS/Linux distribution.
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

    :param distro: Name of OS/Linux distribution.
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


def get_versions(distro, services=None):
    """Get service versions.

    :param distro: Name of OS/Linux distribution.
    :param services: (optional) List of services to get versions for.
    :return versions: Dictionary of services and their version numbers.
    :rtype: dict
    """
    versions = {
            'ftp': get_ftp_version(distro),
            'ssh': get_ssh_version(distro, services_configs[distro]['ssh']),
            'apache': get_apache_version(distro)
    }

    if services:
        versions = {srv: ver for srv,ver in versions.items() if srv in services}

    return versions


def get_longest_version(versions):
    """Calculate the longest version length.

    :param versions: Dictionary of services and their version numbers.
    :return srv_longest, ver_longest: Tuple containing length of longest
                                      service and version.
    :rtype: tuple
    """
    srv_longest = 0
    ver_longest = 0

    for service, version in versions.items():
        srv_longest = len(service) if len(service) > srv_longest else srv_longest
        ver_longest = len(version) if len(version) > ver_longest else ver_longest

    return (srv_longest, ver_longest)


def show_service_info(existing_srvs, versions):
    """Show installed services, their version, activity, and test status."""
    if len(existing_srvs) == 0:
        print(f"collected 0 items\n\n{header('no tests performed', 'y')}")
    elif len(existing_srvs) == 1:
        print(f"collected 1 item\n")
    else:
        print(f"collected {len(existing_srvs)} items\n")

    srv_longest, ver_longest = get_longest_version(versions)

    # TODO: must do actual tests before printing

