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
from drawing import color, header
from utils import (
        get_os, get_existing, get_active, get_configs, get_versions,
        show_collection_count, show_service_info, config_exists, check_prereqs,
        get_error, get_test_status, show_percentage
)
from service_info import (
        services_sve, services_entries, services_vuln_templates,
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


def get_failures(services, configs, versions):
    """Get service test failure information.

    FIXME:
        1. Having anonymous_enable=NO before anonymous_enable=YES.
    """
    failures = {}
    passed = 0

    # Test each service
    for service in services:
        # Initialize failure dict
        failures[service] = []

        # Gather config file, configurations, and templates
        configurations = services_entries[service]
        vuln_templates = services_vuln_templates[service]
        norm_templates = services_norm_templates[service]
        test_stats = {'passed': 0, 'failed': 0}
        with open(configs[service], 'r') as f:
            srv_file = f.read()

        if not configurations:
            continue

        # Show service version
        show_service_info(service, versions[service])

        # Test each configuration
        for name, config in configurations.items():
            regex = re.compile(config['regex'], flags=re.MULTILINE)
            config_type = config['type']
            prereqs = config['prereq']
            prereq_types = config['prereq_type']
            found_config = config_exists(regex, config_type, srv_file)
            uh_oh = False

            # Found a bad config
            if found_config:
                if not prereqs or (prereqs and
                        check_prereqs(service, prereqs, prereq_types, srv_file)):
                    if config_type == 'default':
                        bad_line = color(f"E   missing: {config['regex'][1:]}", "r")
                        regex = re.compile(vuln_templates[name], flags=re.MULTILINE)
                    elif config_type == 'special regex':
                        matches = re.findall(regex,srv_file)
                        bad_line = color(f"E   {', '.join(matches)}", "r")
                    else:
                        bad_line = color(f"E   {config['regex'][1:]}", "r")
                    error_line = get_error(service, name,
                        config['description'], regex,
                        configs[service], bad_line)
                    failures[service].append(error_line)
                    uh_oh = True
            else:
                passed += 1

            # Print test status and increment the aggregate
            test_status = get_test_status(service, versions[service], uh_oh)
            test_stats[test_status] += 1

        # Show service test percentage
        show_percentage(service, versions[service], configurations, test_stats)

    return failures, passed


def show_failures(services, configs, versions, total_services):
    start = time.time()
    failures, passed = get_failures(services, configs, versions)
    total_time = round(time.time() - start, 3)

    if total_services == 0:
        print(header(f'no tests ran in {total_time} seconds', 'y'))
    else:
        failed = sum([len(fails) for fails in failures.values()])

        if any([fails for fails in failures.values()]):
            print(f"\n{header('FAILURES')}")
            for service, fails in failures.items():
                print(f"{header(f'test_{service}', clr='r', border_type='_')}\n")
                for error in fails:
                    print(f'{error}\n')

            print(header(f'{failed} tests failed, {passed} passed in {total_time} seconds', 'r'))
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
