"""
sve.services
~~~~~~~~~~~~

This module contains service information.

Only service names and their configuration files
  may go here. OS-specific commands must be placed
  accordingly in utils.py.

When adding another OS, please use the name given in
  /etc/os-release for Linux distributions, "darwin"
  for macOS and "winXX" for Windows, replacing XX
  with the version number (prefixed with 0 if
  necessary; e.g., 07 for Windows 7).
"""

# Services sve processes by their common names
services_sve = ['ftp', 'ssh', 'apache']

# Actual service name
services_actual = {'Arch Linux':
                    {
                       'ftp': 'vsftpd',
                       'ssh': 'sshd',
                       'apache': 'httpd',
                       # 'nginx': 'nginx'
                    },
                  }

# Service config file locations
services_configs = {'Arch Linux':
                     {
                       'ftp': '/etc/vsftpd.conf',
                       'ssh': '/etc/ssh/sshd_config',
                       'apache': '/etc/httpd/conf/httpd.conf',
                       # 'nginx': '/etc/nginx/nginx.conf'
                     },
                   }

# types: explicit, default, special regex
# prereq_type: explicit, default, special regex, normal
services_regex = {
    'ftp':
        {
            'anon ssl': {
                'description': 'anonymous users may connect using SSL connections',
                'type': 'explicit',
                'regex': '^allow_anon_ssl=YES',
                'prereq': ['anon FTP'],
                'prereq_type': ['vulnerable default']
            },
            'anon FTP': {
                'description': 'anonymous logins permitted',
                'type': 'default',
                'regex': '^anonymous_enable=NO',
                'prereq': [],
                'prereq_type': [] 
            },
            'local umask': {
                'description': 'insufficient umask for local user-created files',
                'type': 'special regex',
                'regex': '^local_umask=0[0-6][0-6]',
                'prereq': ['local enable'],
                'prereq_type': ['normal default']
            },
        },
    'ssh':
        {
        },
    'apache':
        {
        },
}

services_vuln_templates = {
    'ftp':
        {'anon FTP': '(^anonymous_enable=YES)|(^#+\w*anonymous_enable=.*)',
         'FTP banner': '(^#+\w*ftpd_banner=.*)|(^#+\w*banner_file=.*)'
        },
    'ssh':
        {
        },
    'apache':
        {
        },
}

# These are for options that aren't considered vulnerable.
#   For example, local_enable is fine to have but is a
#   prereq for options that are considered vulnerable.
#   So we have a template for it here.
services_norm_templates = {
    'ftp':
        {'local enable':'(^local_enable=YES)|(^#+\w*local_enable=.*)'
        },
    'ssh':
        {
        },
    'apache':
        {
        },
}
                     
