import pytest
import subprocess as sp

from sve.utils import (
        get_distro, get_configs, get_ftp_version, get_ssh_version,
        get_apache_version,
        parse_services
)
