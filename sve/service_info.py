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
import re

# NAMES
services_sve = ['ftp', 'ssh']

services_actual = {
    'Arch Linux':
        {
            'ftp': 'vsftpd',
            'ssh': 'sshd',
            # 'apache': 'httpd',
            # 'nginx': 'nginx'
        },
}


# CONFIG FILES
services_configs = {
    'Arch Linux':
        {
            'ftp': '/etc/vsftpd.conf',
            'ssh': '/etc/ssh/sshd_config',
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
                'regex flags': None,
                'prereq': ['anon enable'],
                'prereq_type': ['vulnerable default']
            },
            'anon mkdir': {
                'description': 'anonymous users may create directories',
                'type': 'explicit',
                'regex': '^anon_mkdir_write_enable=YES',
                'regex flags': None,
                'prereq': ['anon enable'],
                'prereq_type': ['vulnerable default']
            },
            'anon write': {
                'description': 'anonymous users may perform write operations (e.g., deletion, renaming, etc.)',
                'type': 'explicit',
                'regex': '^anon_other_write_enable=YES',
                'regex flags': None,
                'prereq': ['anon enable'],
                'prereq_type': ['vulnerable default']
            },
            'anon upload': {
                'description': 'anonymous users may upload files',
                'type': 'explicit',
                'regex': '^anon_upload_enable=YES',
                'regex flags': None,
                'prereq': ['anon enable'],
                'prereq_type': ['vulnerable default']
            },
            'anon world read': {
                'description': 'anonymous users may download files other than those that are world readable',
                'type': 'explicit',
                'regex': '^anon_world_readable_only=NO',
                'regex flags': None,
                'prereq': ['anon enable'],
                'prereq_type': ['vulnerable default']
            },
            'anon enable': {
                'description': 'anonymous logins permitted',
                'type': 'default',
                'regex': '^anonymous_enable=NO',
                'regex flags': None,
                'prereq': [],
                'prereq_type': []
            },
            'abor requests': {
                'description': 'async ABOR requests enabled',
                'type': 'explicit',
                'regex': '^async_abor_enable=YES',
                'regex flags': None,
                'prereq': [],
                'prereq_type': []
            },
            'chroot local user': {
                'description': 'local users are chrooted in their home directory',
                'type': 'explicit',
                'regex': '^chroot_local_user=YES',
                'regex flags': None,
                'prereq': ['local enable'],
                'prereq_type': ['normal default']
            },
            'local umask': {
                'description': 'insufficient umask for local user-created files',
                'type': 'regex explicit',
                'regex': '^local_umask=0[0-6][0-6]',
                'regex flags': None,
                'prereq': ['local enable'],
                'prereq_type': ['normal default']
            },
            'ls recursive': {
                'description': 'recursive ls enabled (may consume a lot of resources)',
                'type': 'explicit',
                'regex': '^ls_recurse_enable=YES',
                'regex flags': None,
                'prereq': [],
                'prereq_type': []
            },
            'log lock': {
                'description': 'vsftpd prevented from taking a file lock when writing to a file (this should generally not be enabled)',
                'type': 'explicit',
                'regex': '^no_log_lock=YES',
                'regex flags': None,
                'prereq': [],
                'prereq_type': []
            },
            'one process model': {
                'description': 'using security model which only uses 1 process per connection',
                'type': 'explicit',
                'regex': '^one_process_model=YES',
                'regex flags': None,
                'prereq': [],
                'prereq_type': []
            },
            'pasv promisc': {
                'description': 'disabled PASV security check (which ensures data connection originates from the same IP as the control connection)',
                'type': 'explicit',
                'regex': '^pasv_promiscuous=YES',
                'regex flags': None,
                'prereq': [],
                'prereq_type': []
            },
            'port promisc': {
                'description': 'disabled PORT security check (ensures outgoing data connections can only connect to the client)',
                'type': 'explicit',
                'regex': '^port_promiscuous=YES',
                'regex flags': None,
                'prereq': [],
                'prereq_type': []
            },
            'launching user': {
                'description': 'vsftpd runs as user which launched vsftpd (this should generally not be enabled)',
                'type': 'explicit',
                'regex': '^run_as_launching_user=YES',
                'regex flags': None,
                'prereq': [],
                'prereq_type': []
            },
            'proctitle': {
                'description': 'vsftpd shows session status information in system process listing',
                'type': 'explicit',
                'regex': '^setproctitle_enable=YES',
                'regex flags': None,
                'prereq': [],
                'prereq_type': []
            },
            'ssl enable': {
                'description': 'vsftpd can make no guarantees about the security of the OpenSSL libraries',
                'type': 'explicit',
                'regex': '^ssl_enable=YES',
                'regex flags': None,
                'prereq': [],
                'prereq_type': []
            },
            'virtual privs': {
                'description': 'virtual users have local user privileges',
                'type': 'explicit',
                'regex': '^virtual_use_local_privs=YES',
                'regex flags': None,
                'prereq': [],
                'prereq_type': []
            },
            'banner': {
                'description': 'banner shows version info',
                'type': 'default',
                'regex': '(^ftpd_banner=.*)|(^banner_file=.*)',
                'regex flags': None,
                'prereq': [],
                'prereq_type': []
            },
        },
    'ssh':
        {
            'accept env': {
                'description': "some environment variables copied into the session's environment can be used to bypass restricted user environments",
                'type': 'regex explicit',
                'regex': '^AcceptEnv\s*.*',
                'regex flags': re.IGNORECASE,
                'prereq': [],
                'prereq_type': []
            },
            'password auth': {
                'description': 'password authentication is allowed. Prefer key authentication',
                'type': 'default',
                'regex': '^PasswordAuthentication\s*no',
                'regex flags': re.IGNORECASE,
                'prereq': [],
                'prereq_type': []
            },
            'empty passwords': {
                'description': 'login to accounts with empty passwords allowed',
                'type': 'regex explicit',
                'regex': '^PermitEmptyPasswords\s*yes',
                'regex flags': re.IGNORECASE,
                'prereq': ['password auth'],
                'prereq_type': ['vulnerable default'],
            },
            'root login': {
                'description': 'root login allowed',
                'type': 'regex default',
                'regex': '^PermitRootLogin\s*no',
                'regex flags': re.IGNORECASE,
                'prereq': [],
                'prereq_type': [],
            },
            'root login no pass': {
                'description': 'password authentication disabled for root',
                'type': 'regex explicit',
                'regex': '^PermitRootLogin\s*without-password',
                'regex flags': re.IGNORECASE,
                'prereq': ['root login'],
                'prereq_type': ['vulnerable default'],
            },
            'permit user env': {
                'description': 'environment processing may enable users to bypass access restrictions in some configurations using mechanisms like LD_PRELOAD',
                'type': 'regex explicit',
                'regex': '^PermitUserEnvironment\s*yes',
                'regex flags': re.IGNORECASE,
                'prereq': [],
                'prereq_type': [],
            },
            'protocol 1': {
                'description': 'using protocol version 1',
                'type': 'regex explicit',
                'regex': '^Protocol\s*1',
                'regex flags': re.IGNORECASE,
                'prereq': [],
                'prereq_type': []
            },
            'pubkey auth': {
                'description': 'public key authentication disabled',
                'type': 'regex explicit',
                'regex': '^PubkeyAuthentication\s*no',
                'regex flags': re.IGNORECASE,
                'prereq': ['protocol 2'],
                'prereq_type': ['normal default']
            },
            'strict mode': {
                'description': "checking file modes and ownership of users' files or home directory before accepting login disabled. This is desirable since novices sometimes leave their directory/files world-writable.",
                'type': 'regex explicit',
                'regex': '^StrictModes\s*no',
                'regex flags': re.IGNORECASE,
                'prereq': [],
                'prereq_type': []
            },
            'tcp keepalive': {
                'description': 'sessions may hang indefinitely, leaving "ghost" users and consuming server resources',
                'type': 'regex explicit',
                'regex': '^TCPKeepAlive\s*no',
                'regex flags': re.IGNORECASE,
                'prereq': [],
                'prereq_type': []
            },
            'use login': {
                'description': 'login(1) is used for interactive login sessions',
                'type': 'regex explicit',
                'regex': '^UseLogin\s*yes',
                'regex flags': re.IGNORECASE,
                'prereq': [],
                'prereq_type': []
            },
            'no privilege separation': {
                'description': 'privilege separation disabled',
                'type': 'regex explicit',
                'regex': '^UsePrivilegeSeparation\s*no',
                'regex flags': re.IGNORECASE,
                'prereq': [],
                'prereq_type': []
            },
            'x11 forwarding': {
                'description': "the client's X11 display server may be exposed to attack when the SSH client requests forwarding",
                'type': 'regex explicit',
                'regex': '^X11Forwarding\s*yes',
                'regex flags': re.IGNORECASE,
                'prereq': ['use login no'],
                'prereq_type': ['vulnerable explicit']
            },
        },
    # 'apache':
        # {
        # },
}


# TEMPLATES
services_vuln_templates = {
    'ftp':
        {'anon enable': '(^anonymous_enable=YES)|(^#+\w*anonymous_enable=.*)',
         'banner': '(^#+\w*ftpd_banner=.*)|(^#+\w*banner_file=.*)'
        },
    'ssh':
        {'use login no': '(^UseLogin\s*no)|(^#+\w*UseLogin\s*no)',
         'root login': '(^PermitRootLogin\s*yes)|(^#*\w*PermitRootLogin\s*.*)',
         'password auth': '(^PasswordAuthentication\s*yes)|(^#*\s*PasswordAuthentication\s*.*)'
        },
    # 'apache':
        # {
        # },
}

services_norm_templates = {
    'ftp':
        {'local enable': '(^local_enable=YES)|(^#+\w*local_enable=.*)'
        },
    'ssh':
        {'protocol 2': '(^protocol\s*(1,)?2(,1)?)|(^#*\s*protocol\s*(1,)?2(,1)?)'
        },
    # 'apache':
        # {
        # },
}

