# -*- coding: utf-8 -*-

"""
sve.sve
~~~~~~~

This module does something.
"""

import sys
import argparse

from __version__ import __version__
from drawing import header
from utils import (
        get_os, get_existing, get_active, get_versions, get_configs,
        show_service_info,
)
from service_info import services_sve

class ArgumentParser(argparse.ArgumentParser):
    """Overriding class for custom help/message."""
    def error(self, message):
        """Custom error messages.

        :param message: The default argparse error message raised.
        """

    # def print_help(self):
        # """Print custom help menu."""
        # print('''\
# usage: sve [--help] [--services <SERVICES>]

# sve enumerates vulnerable service configurations that probably
# shouldn't be set on your servers.

    # -h, --help                           Show this help message and exit
    # --version                            Show this program version and exit
    # --services SERVICE1[,SERVICE2,...]   Specify services to enumerate
# ''')


def create_parser():
    """Create command-line parser.

    For a custom usage message and error handling, uses an
      overridden ArgumentParser instance.

    :return: A Namespace object containing the command-line flags
               and their state.
    :rtype: Namespace

    TODO:
        1. Handle bogus arguments passed (e.g., asdf). Right now it
             just acts like you ran with no arguments.
    """
    parser = ArgumentParser()


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

    show_service_info(existing_srvs, versions)


if __name__ == '__main__':
    main()
