# -*- coding: utf-8 -*-

"""
sve.sve
~~~~~~~

This module does something.
"""

import re
import sys
import argparse

from __version__ import __version__
from drawing import color, header
from utils import (
        get_os, get_existing, get_active, get_versions, get_configs,
        show_service_info, get_time
)
from service_info import (
        services_sve, services_regex, services_vuln_templates,
        services_norm_templates
)

def create_parser():
    """Create command-line parser.

    :return: A Namespace object containing the command-line flags
               and their state.
    :rtype: Namespace

    TODO:
        1. Handle bogus arguments passed. Right now it
             just acts like you ran with no arguments.
    """
    parser = argparse.ArgumentParser()


    parser.add_argument('--version', action='store_true', help='Show program version and exit')
    parser.add_argument('--services', help='Specifies services to enumerate')

    return parser.parse_args()


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
    if config_type == 'default':
        if not re.findall(regex, srv_file):
            return True
    elif re.findall(regex, srv_file):
        return True

    return False


def get_error(service, name, desc, regex, config_type, srv_file_text, srv_file, bad_line):
    """Get line number of vulnerable config."""
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


def check_prereqs(service, prereqs, prereq_types, srv_file):
    """Count the number of prerequisites satisfied for a configuration.

    :param service: Name of current service.
    :param prereqs: List of config prerequisites.
    :param prereq_types: Types of each config prerequisite.
    :param srv_file: The service's config file.
    :return: Boolean indicating if prerequisites are met.
    :rtype: bool
    """
    vuln_templates = services_vuln_templates[service]
    norm_templates = services_norm_templates[service]

    if not prereqs:
        return

    satisfied = 0
    for prereq, prereq_type in zip(prereqs, prereq_types):
        templates = vuln_templates if prereq_type.startswith('vulnerable') else norm_templates
        regex = re.compile(templates[prereq], flags=re.MULTILINE)  # re.MULTILINE is so ^ works
        if re.findall(regex, srv_file):
            satisfied += 1
            break

    if satisfied != len(prereqs):
        return False

    return True


def get_failures(services, configs):
    """Get service test failure information."""
    for service in services:
        with open(configs[service], 'r') as f:
            srv_file = f.read()
        configurations = services_regex[service]
        vuln_templates = services_vuln_templates[service]
        norm_templates = services_norm_templates[service]

        for name, config in configurations.items():
            regex = re.compile(config['regex'], flags=re.MULTILINE)
            config_type = config['type']
            prereqs = config['prereq']
            prereq_types = config['prereq_type']

            if config_exists(regex, config_type, srv_file):
                if not prereqs or (prereqs and
                        check_prereqs(service, prereqs, prereq_types, srv_file)):
                    if config_type == 'default':
                        bad_line = color(f"E   missing: {config['regex'][1:]}", "r")
                        print(bad_line)
                        regex = re.compile(vuln_templates[name], flags=re.MULTILINE)
                    elif config_type == 'special regex':
                        matches = re.findall(regex,srv_file)
                        bad_line = color(f"E   {', '.join(matches)}", "r")
                        # print(bad_line)
                    else:
                        bad_line = color(f"E   {config['regex'][1:]}", "r")
                        # print(bad_line)
                    error_line = get_error(service, name,
                        config['description'], regex,
                        config_type, srv_file, configs[service],
                        bad_line)


def main():
    args = create_parser()

    if args.version:
        sys.exit(f'sve version {__version__}')

    services = parse_services(args.services) if args.services else []

    print(header('sve session started'))
    distro = get_os()
    existing_srvs = get_existing(distro, services)
    active_srvs = get_active(distro, services)
    configs = get_configs(distro, services)
    versions = get_versions(distro, services)

    # print('existing:', existing_srvs)
    # print('active:', active_srvs)
    # print('configs:', configs)
    # print('versions:', versions)

    # show_service_info(existing_srvs, versions)
    get_failures(existing_srvs, configs)


if __name__ == '__main__':
    main()
