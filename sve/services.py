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
services_sve = ['ftp', 'ssh', 'apache', 'nginx']

# Actual service name
services_actual = {'Arch Linux':
                    {
                       'ftp': 'vsftpd',
                       'ssh': 'sshd',
                       'apache': 'httpd',
                       'nginx': 'nginx'
                    },
                  }

# Service config file locations
services_configs = {'Arch Linux':
                     {
                       'ftp': '/etc/vsftpd.conf',
                       'ssh': '/etc/ssh/sshd_config',
                       'apache': '/etc/httpd/conf/httpd.conf',
                       'nginx': '/etc/nginx/nginx.conf'
                     },
                   }

