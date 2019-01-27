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

from .output import color, header
from .service_info import (
        services_sve, services_actual, services_configs,
        services_vuln_templates, services_norm_templates
)

TERM_WIDTH = int(os.popen('stty size', 'r').read().split()[1])

def get_os():
    """Get name of OS/distribution.

    If the OS is macOS or Windows, then the OS name is returned
      instead of a distribution name.

    :return distro: Name of operating system or Linux distribution.
    :rtype: str
    """
    if sys.platform.startswith("linux"):
        with open('/etc/os-release', 'r') as f:
            distro = f.readline().rstrip()[6:-1]
    elif sys.platform.startswith("darwin"):
        distro = "darwin"
    elif sys.platform.startswith("win32"):
        distro = "windows"

    return distro


def get_existing(distro, services=None):
    """Determine installed services.

    :param distro: Name of OS/Linux distribution.
    :param services: (optional) List of existing services to check for.
    :return existing_srvs: List of existing services (actual names).
    :rtype: list

    TODO:
        1. Systems without systemd.
        2. Mac/Windows
    """
    existing_srvs = []

    if sys.platform.startswith("linux"):
        unit_files = sp.run(['systemctl', 'list-unit-files'],
                capture_output=True).stdout.decode()

        for srv_e, srv_a in services_actual[distro].items():
            if (((services and srv_e in services) or not services) and
                    f'{srv_a}.service' in unit_files):
                existing_srvs.append(srv_e)

    return existing_srvs


def get_active(distro, services=None):
    """Determine active services.

    :param distro: Name of OS/Linux distribution.
    :param services: (optional) List of active services to check for.
    :return active_srvs: Dictionary of services and their activity status.
    :rtype: dict
    """
    active_services = dict()

    if sys.platform.startswith("linux"):
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
            # 'apache': get_apache_version(distro)
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


def parse_services(services):
    """Parse provided services into a list.

    :param services: String of comma-delimited services.
    :return services: List of services.
    :rtype: list
    """
    services = services.split(',')

    unknown_services = set(services) - set(services_sve)
    if unknown_services:
        sys.exit(f"unknown services: {', '.join(unknown_services)}")

    return services


def config_exists(regex, config_type, srv_file):
    """Determine if a config exists.

    :param regex: The regex of the config to look for.
    :param config_type: The config's type.
    :param srv_file: The config file.
    :return: Boolean indicating if the config exists.
    :rtype: bool
    """
    if config_type == 'default' or config_type == 'regex default':
        if not re.findall(regex, srv_file):
            return True
    elif re.findall(regex, srv_file):
        return True

    return False


def get_error(service, name, desc, regex, srv_file, bad_line):
    """Get line number of vulnerable config.

    :param service: Name of the current service.
    :param name: Name of the current configuration.
    :param desc: The current configuration's description.
    :param regex: The current configuration's regex pattern.
    :param srv_file: The config file name.
    :param bad_line: The offending configuration in an error message.
    :return: An error line including :param: `bad_line`, the file and
               line number where the configuration was found, and a
               brief description.
    :rtype: str
    """
    # It's always going to be a vulnerable default
    vuln_templates = services_vuln_templates[service]

    # Get line numbers
    line_nums = []
    with open(srv_file, 'r') as f:
        for line_num, line in enumerate(f, 1):
            if regex.search(line):
                line_nums.append(f'{line_num}:')

    line_nums = f"{','.join(line_nums).replace(':', '')}:" if line_nums else ''
    return f"{bad_line}\n{srv_file}:{line_nums} {desc}"


def check_prereqs(service, prereqs, prereq_types, srv_file, flags):
    """Count the number of prerequisites satisfied for a configuration.

    :param service: Name of current service.
    :param prereqs: List of config prerequisites.
    :param prereq_types: Types of each config prerequisite.
    :param srv_file: The service's config file.
    :return: Boolean indicating if prerequisites are met.
    :rtype: bool
    """
    satisfied = 0
    vuln_templates = services_vuln_templates[service]
    norm_templates = services_norm_templates[service]

    if not prereqs:
        return

    for prereq, prereq_type in zip(prereqs, prereq_types):
        state, re_type = prereq_type.split()
        templates = vuln_templates if state == 'vulnerable' else norm_templates
        if prereq_type == 'vulnerable explicit' or prereq_type == 'normal default':
            regex = re.compile(templates[prereq]['vuln'], flags=flags)
        elif prereq_type == 'vulnerable default' or prereq_type == 'normal explicit':
            regex = re.compile(templates[prereq]['safe'], flags=flags)

        if config_exists(regex, re_type, srv_file):
            satisfied += 1

    if satisfied != len(prereqs):
        return False

    return True


def show_service_info(service, version):
    """Show current service and its version.

    :param service: Name of the current service.
    :param versions: The version of the current service.
    :return: None
    """
    print(f"{service} ({version})", end=' ')


def show_test_status(test_status):
    """Show test status of the current service.

    :param test_status: Status of the current test (True or False).
    :return: A string indicating whether the test passed or failed.
    :rtype: str
    """
    if test_status == 'passed':
        print(color('.', 'g'), end='')
    elif test_status == 'failed':
        print(color('F', 'r'), end='')


def show_collection_count(entries):
    """Display the number of services collected.

    :param entries: Dictionary of configuration entries for all services.
    :return count: Number of services with tests.
    :rtype: int
    """
    count = 0

    if not all(entries):
        print(color(f"collected 0 items\n\n{header('no tests performed', 'y')}"))
    else:
        for entry in entries.values():
            count += 1 if any(entry) else 0

        if count == 1:
            print(color(f"collected 1 item\n"))
        else:
            print(color(f"collected {count} items\n"))

    return count


def get_test_stats(pass_count, fail_count):
    """Show test pass/fail percentage.

    :param pass_count: The number of tests passed.
    :param fail_count: The number of tests failed.
    :return: Pass/fail percentage.
    :rtype: str
    """
    if fail_count == 0:
        percent = 100
    else:
        percent = int(pass_count / (pass_count + fail_count) * 100)

    return str(percent)


def show_percentage(service, version, configurations, test_stats):
    """

    :param services: List of existing services or user-specified services.
    :param versions: Dictionary of each service and their version.
    :param configurations:
    :param test_stats: Dictionary containing the number of passed and failed tests.
    """
    # 7: ()[]% and the 2 spaces around ()
    percentage = get_test_stats(test_stats['passed'], test_stats['failed'])
    spacing = ' ' * (TERM_WIDTH - (len(service) + len(version) + 7 + len(configurations) + len(percentage)))
    print(color(f'{spacing}[{percentage}%]', 'b'))
