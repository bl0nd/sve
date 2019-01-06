"""
sve.service_info
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

# NAMES
services_sve = ['ftp']

services_actual = {
    'Arch Linux':
        {
            'ftp': 'vsftpd',
            # 'ssh': 'sshd',
            # 'apache': 'httpd',
            # 'nginx': 'nginx'
        },
}


# CONFIG FILES
services_configs = {
    'Arch Linux':
        {
            'ftp': '/etc/vsftpd.conf',
            # 'ssh': '/etc/ssh/sshd_config',
            # 'apache': '/etc/httpd/conf/httpd.conf',
            # 'nginx': '/etc/nginx/nginx.conf'
        },
}


# ENTRIES
services_entries = {
    'ftp':
        {
            'anon ssl': {
                'description': 'anonymous users may connect using SSL connections',
                'type': 'explicit',
                'regex': '^allow_anon_ssl=YES',
                'prereq': ['anon FTP'],
                'prereq_type': ['vulnerable default']
            },
            'anon mkdir': {
                'description': 'anonymous users may create directories',
                'type': 'explicit',
                'regex': '^anon_mkdir_write_enable=YES',
                'prereq': ['anon FTP'],
                'prereq_type': ['vulnerable default']
            },
            'anon write': {
                'description': 'anonymous users may perform write operations (e.g., deletion, renaming, etc.)',
                'type': 'explicit',
                'regex': '^anon_other_write_enable=YES',
                'prereq': ['anon FTP'],
                'prereq_type': ['vulnerable default']
            },
            'anon upload': {
                'description': 'anonymous users may upload files',
                'type': 'explicit',
                'regex': '^anon_upload_enable=YES',
                'prereq': ['anon FTP'],
                'prereq_type': ['vulnerable default']
            },
            'anon world read': {
                'description': 'anonymous users may download files other than those that are world readable',
                'type': 'explicit',
                'regex': '^anon_world_readable_only=NO',
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
            'abor requests': {
                'description': 'async ABOR requests enabled',
                'type': 'explicit',
                'regex': '^async_abor_enable=YES',
                'prereq': [],
                'prereq_type': []
            },
            'chroot local user': {
                'description': 'local users are chrooted in their home directory',
                'type': 'explicit',
                'regex': '^chroot_local_user=YES',
                'prereq': ['local enable'],
                'prereq_type': ['normal default']
            },
            'local umask': {
                'description': 'insufficient umask for local user-created files',
                'type': 'special regex',
                'regex': '^local_umask=0[0-6][0-6]',
                'prereq': ['local enable'],
                'prereq_type': ['normal default']
            },
            'ls recursive': {
                'description': 'recursive ls enabled (may consume a lot of resources)',
                'type': 'explicit',
                'regex': '^ls_recurse_enable=YES',
                'prereq': [],
                'prereq_type': []
            },
            'log lock': {
                'description': 'vsftpd prevented from taking a file lock when writing to a file (this should generally not be enabled)',
                'type': 'explicit',
                'regex': '^no_log_lock=YES',
                'prereq': [],
                'prereq_type': []
            },
            'one process model': {
                'description': 'using security model which only uses 1 process per connection',
                'type': 'explicit',
                'regex': '^one_process_model=YES',
                'prereq': [],
                'prereq_type': []
            },
            'pasv promisc': {
                'description': 'disabled PASV security check (which ensures data connection originates from the same IP as the control connection)',
                'type': 'explicit',
                'regex': '^pasv_promiscuous=YES',
                'prereq': [],
                'prereq_type': []
            },
            'port promisc': {
                'description': 'disabled PORT security check (ensures outgoing data connections can only connect to the client)',
                'type': 'explicit',
                'regex': '^port_promiscuous=YES',
                'prereq': [],
                'prereq_type': []
            },
            'launching user': {
                'description': 'vsftpd runs as user which launched vsftpd (this should generally not be enabled)',
                'type': 'explicit',
                'regex': '^run_as_launching_user=YES',
                'prereq': [],
                'prereq_type': []
            },
            'proctitle': {
                'description': 'vsftpd shows session status information in system process listing',
                'type': 'explicit',
                'regex': '^setproctitle_enable=YES',
                'prereq': [],
                'prereq_type': []
            },
            'ssl enable': {
                'description': 'vsftpd can make no guarantees about the security of the OpenSSL libraries',
                'type': 'explicit',
                'regex': '^ssl_enable=YES',
                'prereq': [],
                'prereq_type': []
            },
            'virtual privs': {
                'description': 'virtual users have local user privileges',
                'type': 'explicit',
                'regex': '^virtual_use_local_privs=YES',
                'prereq': [],
                'prereq_type': []
            },
            # 'banner': {
                # 'description': 'banner shows version info',
                # 'type': 'default',
                # 'regex': '(^ftpd_banner=.*)|(^banner_file=.*)',
                # 'prereq': [],
                # 'prereq_type': []
            # },
        },
    # 'ssh':
        # {
        # },
    # 'apache':
        # {
        # },
}


# TEMPLATES
services_vuln_templates = {
    'ftp':
        {'anon FTP': '(^anonymous_enable=YES)|(^#+\w*anonymous_enable=.*)',
         'FTP banner': '(^#+\w*ftpd_banner=.*)|(^#+\w*banner_file=.*)'
        },
    # 'ssh':
        # {
        # },
    # 'apache':
        # {
        # },
}

services_norm_templates = {
    'ftp':
        {'local enable':'(^local_enable=YES)|(^#+\w*local_enable=.*)'
        },
    # 'ssh':
        # {
        # },
    # 'apache':
        # {
        # },
}
                                         
