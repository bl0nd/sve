# -*- coding: utf-8 -*-

"""
sve.sve
~~~~~~~

This module does something.
"""

import os
import re
import sys
import argparse

from __version__ import __version__
from drawing import color, header
from utils import (
        get_os, get_existing, get_active, get_versions, get_configs,
        get_time, get_longest_version
)
from service_info import (
        services_sve, services_regex, services_vuln_templates,
        services_norm_templates
)

TERM_WIDTH = int(os.popen('stty size', 'r').read().split()[1])

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


def show_service_info(service, version):
    """Show current service and its version."""
    print(f"{service} ({version})", end=' ')


def get_test_status(service, version, uh_oh):
    """Show test status of the current service."""
    if not uh_oh:
        print(color('.', 'g'), end='')
        return 'passed'
    else:
        print(color('F', 'r'), end='')
        return 'failed'


def show_collection_count(items_total):
    """Display the number of services collected."""
    if items_total == 0:
        print(color(f"collected 0 items\n\n{header('no tests performed', 'y')}"))
    elif items_total == 1:
        print(color(f"collected 1 item\n"))
    else:
        print(color(f"collected {items_total} items\n"))


def get_test_stats(pass_count, fail_count):
    """Show test pass/fail percentage."""
    if fail_count == 0:
        percent = 100
    else:
        percent = int(pass_count / (pass_count + fail_count) * 100)

    return str(percent)


def show_percentage(service, version, configurations, test_stats):
    # 7: ()[]% and the 2 spaces around ()
    percentage = get_test_stats(test_stats['passed'], test_stats['failed'])
    spacing = ' ' * (TERM_WIDTH - (len(service) + len(version) + 7 + len(configurations) + len(percentage)))
    print(color(f'{spacing}[{percentage}%]', 'b'))


def get_failures(services, configs, versions):
    """Get service test failure information.

    FIXME:
        1. Having anonymous_enable=NO before anonymous_enable=YES.
    """
    failures = {}

    # Collection count
    show_collection_count(len(services))

    # Test each service
    for service in services:
        # Initialize failure dict
        failures[service] = []

        # Show service version
        show_service_info(service, versions[service])

        # Gather config file, configurations, and templates
        with open(configs[service], 'r') as f:
            srv_file = f.read()
        configurations = services_regex[service]
        vuln_templates = services_vuln_templates[service]
        norm_templates = services_norm_templates[service]
        test_stats = {'passed': 0, 'failed': 0}

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
                        config_type, srv_file, configs[service],
                        bad_line)
                    failures[service].append(error_line)
                    uh_oh = True

            # Print test status and increment the aggregate
            test_status = get_test_status(service, versions[service], uh_oh)
            test_stats[test_status] += 1

        # Show service test percentage
        show_percentage(service, versions[service], configurations, test_stats)

    return failures

def show_failures(failures):
    print(f"\n{header('FAILURES')}")
    for service, failures in failures.items():
        print(f"{header(f'test_{service}', clr='r', border_type='_')}\n")
        for error in failures:
            print(f'{error}\n')


def main():
    args = create_parser()

    if args.version:
        sys.exit(f'sve version {__version__}')

    services = parse_services(args.services) if args.services else []

    print(header('sve session starts'))
    distro = get_os()
    existing_srvs = get_existing(distro, services)
    active_srvs = get_active(distro, services)
    configs = get_configs(distro, services)
    versions = get_versions(distro, services)

    failures = get_failures(existing_srvs, configs, versions)
    show_failures(failures)


if __name__ == '__main__':
    main()
