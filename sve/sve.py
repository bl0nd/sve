# -*- coding: utf-8 -*-

"""
sve.sve
~~~~~~~

This module does something.
"""

import re
import sys
import time
import argparse

from __version__ import __version__
from output import color, header
from utils import (
        get_os, get_existing, get_active, get_configs, get_versions,
        show_collection_count, show_service_info, config_exists, check_prereqs,
        get_error, show_test_status, show_percentage
)
from service_info import (
        services_sve, services_entries, services_vuln_templates
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


def get_failures(services, configs, versions):
    """Get service test failure information.

    :param services: List of existing services or user-specified services.
    :param configs: Dictionary of config file locations for each OS.
    :param versions: Dictionary of each service and their version.
    :return failure_msgs, passed: A dictionary of each failed entry and
                                    its error message, and the number of
                                    passed tests.
    :rtype: dict, int

    TODO:
        1. Multiple regex flags.

    FIXME:
        1. Having anonymous_enable=NO before anonymous_enable=YES.
    """
    failure_msgs = {}
    tests_passed = 0

    for service in services:
        failure_msgs[service] = []  # empty failure message list for `service`
        service_test_stats = {'passed': 0, 'failed': 0}  # for percentage output

        # Grab vulnerable templates and service file contents
        #   for default entries and regex matching
        vuln_templates = services_vuln_templates[service]
        with open(configs[service], 'r') as f:
            srv_file = f.read()

        # Skip if no actual entries exist for a listed service
        if not services_entries[service]:
            continue

        show_service_info(service, versions[service])

        # Test each configuration
        for name, config in services_entries[service].items():
            flags = re.M | config['regex flags'] if config['regex flags'] else re.M
            regex = re.compile(config['regex'], flags=flags)

            if config_exists(regex, config['type'], srv_file):
                if (not config['prereq'] or
                        (config['prereq'] and check_prereqs(service,
                                                            config['prereq'],
                                                            config['prereq_type'],
                                                            srv_file,
                                                            flags))):
                    test_status = 'failed'

                    if config['type'] == 'default':
                        # For defaults, use templates which'll give us either:
                        #   1) The config option in a vulnerable state.
                        #   2) The config option's name (in the case of
                        #        implicit defaults).
                        regex = re.compile(vuln_templates[name], flags=flags)
                        match = re.findall(regex, srv_file)

                        # If template matches, use the match
                        if match:
                            match = match[0]
                            bad_line = color(f"E   {match}", "r")
                        # Otherwise, use the config option name
                        else:
                            match = re.findall(r'[a-zA-Z_]+', vuln_templates[name])[0]
                            bad_line = color(f"E   implicit: {match}", "r")
                    elif config['type'] == 'explicit':
                        match = re.findall(regex, srv_file)[0]
                        bad_line = color(f"E   {match}", "r")

                    error_line = get_error(service,
                                           name,
                                           config['description'],
                                           regex,
                                           configs[service],
                                           bad_line)
                    failure_msgs[service].append(error_line)
            else:
                test_status = 'passed'
                tests_passed += 1

            # Print test status and increment the current service's test status
            show_test_status(test_status)
            service_test_stats[test_status] += 1

        show_percentage(service, versions[service], services_entries[service], service_test_stats)

    return failure_msgs, tests_passed


def show_failures(services, configs, versions, total_services):
    """Get failures and display results.

    :param services: List of existing services or user-specified services.
    :param configs: Dictionary of config file locations for each OS.
    :param versions: Dictionary of each service and their version.
    :param total_services: Number of services that sve has tests for.
    :return: None
    """
    start = time.time()
    failure_msgs, passed = get_failures(services, configs, versions)
    total_time = round(time.time() - start, 3)

    # no tests
    if total_services == 0:
        print(header(f'no tests ran in {total_time} seconds', 'y'))
    else:
        failed = sum([len(fails) for fails in failure_msgs.values()])

        # failed some tests
        if any([fails for fails in failure_msgs.values()]):
            print(f"\n{header('FAILURES')}")
            for service, fails in failure_msgs.items():
                print(f"{header(f'test_{service}', clr='r', border_type='_')}\n")
                for error in fails:
                    print(f'{error}\n')
            print(header(f'{failed} tests failed, {passed} passed in {total_time} seconds', 'r'))
        # passed all tests
        else:
            print(header(f'{passed} tests passed in {total_time} seconds', 'g'))


def main():
    args = create_parser()

    if args.version:
        sys.exit(f'sve version {__version__}')

    services = parse_services(args.services) if args.services else []

    # Gather facts
    distro = get_os()
    existing_srvs = get_existing(distro, services)
    active_srvs = get_active(distro, services)
    configs = get_configs(distro, services)
    versions = get_versions(distro, services)

    # Start tests
    print(header('sve session starts'))
    total_services = show_collection_count(services_entries)
    show_failures(existing_srvs, configs, versions, total_services)


if __name__ == '__main__':
    main()
