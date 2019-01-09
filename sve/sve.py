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
    :return failures, passed: A dictionary of each failed entry and its error message,
                                and the number of passed tests.
    :rtype: dict, int

    FIXME:
        1. Having anonymous_enable=NO before anonymous_enable=YES.
    """
    total_passed = 0

    # Initialize failure dict to hold failure messages
    failures = {}

    # Test each service
    for service in services:
        # Initialize empty failure message list for each service
        failures[service] = []

        # Initialize stats dict for percentage output
        service_test_stats = {'passed': 0, 'failed': 0}

        # Grab templates and srv_file for default entries and regex matching, respectively
        vuln_templates = services_vuln_templates[service]  # no norm_templates since that's just for prereqs
        with open(configs[service], 'r') as f:
            srv_file = f.read()

        # If a service is listed in services_entries but no actual entries exist, skip it
        if not services_entries[service]:
            continue

        # Show service version
        show_service_info(service, versions[service])

        # Test each configuration
        for name, config in services_entries[service].items():
            flags = re.M|config['regex flags'] if config['regex flags'] else re.M
            regex = re.compile(config['regex'], flags=flags)

            # Found a bad config
            if config_exists(regex, config['type'], srv_file):
                if not config['prereq'] or (config['prereq'] and check_prereqs(service, config['prereq'], config['prereq_type'], srv_file, flags)):
                    test_status = 'failed'

                    # This if/else block is really just for getting the line numbers
                    if config['type'] == 'default':
                        regex = re.compile(vuln_templates[name], flags=flags)
                        matches = re.findall(regex, srv_file)
                        if not matches:
                            matches = re.findall(r'[a-zA-Z_]+', vuln_templates[name])[0]
                            bad_line = color(f"E   implicit: {matches}", "r")
                        else:
                            matches = matches[0]
                            bad_line = color(f"E   {matches}", "r")
                    elif config['type'] == 'explicit':
                        matches = re.findall(regex, srv_file)
                        bad_line = color(f"E   {', '.join(matches)}", "r")
                    # else:
                        # bad_line = color(f"E   {config['regex'][1:]}", "r")

                    error_line = get_error(service, name,
                        config['description'], regex,
                        configs[service], bad_line)
                    failures[service].append(error_line)
            # Didn't find a bad config
            else:
                test_status = 'passed'
                total_passed += 1

            # Print test status and increment the current service's aggregate
            show_test_status(test_status)
            service_test_stats[test_status] += 1

        # Show service test percentage
        show_percentage(service, versions[service], services_entries[service], service_test_stats)

    return failures, total_passed


def show_failures(services, configs, versions, total_services):
    """Get failures and display results.

    :param services: List of existing services or user-specified services.
    :param configs: Dictionary of config file locations for each OS.
    :param versions: Dictionary of each service and their version.
    :param total_services: Number of services that sve has tests for.
    :return: None
    """
    start = time.time()
    failures, passed = get_failures(services, configs, versions)
    total_time = round(time.time() - start, 3)

    # no tests
    if total_services == 0:
        print(header(f'no tests ran in {total_time} seconds', 'y'))
    else:
        failed = sum([len(fails) for fails in failures.values()])

        # failed some tests
        if any([fails for fails in failures.values()]):
            print(f"\n{header('FAILURES')}")
            for service, fails in failures.items():
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
