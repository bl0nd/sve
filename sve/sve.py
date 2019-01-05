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


def check_prereqs(prereqs, prereq_types, srv_file,
                  vuln_templates, norm_templates):
    """Count the number of prerequisites satisfied for a configuration.

    :param prereqs: List of config prerequisites.
    :param prereq_types: Types of each config prerequisite.
    :param srv_file: The service's config file.
    :param vuln_templates: Templates (regexes) for vulnerable prerequisites.
    :param norm_templates: Templates (regexes) for normal prerequisites.
    :return: Boolean indicating if prerequisites are met.
    :rtype: bool
    """
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

            if config_type == 'default':
                if not re.findall(regex, srv_file):
                    if not prereqs or (prereqs and
                            check_prereqs(prereqs,
                                          prereq_types, srv_file,
                                          services_vuln_templates[service],
                                          services_norm_templates[service])):
                        bad_line = color(f"E   missing: {config['regex'][1:]}", "r")
            elif re.findall(regex, srv_file):
                if not prereqs or (prereqs and
                            check_prereqs(prereqs,
                                          prereq_types, srv_file,
                                          services_vuln_templates[service],
                                          services_norm_templates[service])):
                    if config_type == 'special regex':
                        matches = re.findall(regex,srv_file)
                        bad_line = color(f"E   {', '.join(matches)}", "r")
                    else:
                        bad_line = color(f"E   {config['regex'][1:]}", "r")


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
