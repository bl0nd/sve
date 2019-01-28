"""
sve.entries
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
                'prereq_type': ['vulnerable explicit']
            },
            'local umask': {
                'description': 'insufficient umask for local user-created files',
                'type': 'explicit',
                'regex': '^local_umask=0[0-6][0-6]',
                'regex flags': None,
                'prereq': ['local enable'],
                'prereq_type': ['vulnerable explicit']
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
                'description': 'disabled PASV security check (ensures data connection originates from the same IP as the control connection)',
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
                'type': 'explicit',
                'regex': '^AcceptEnv\s+.*',
                'regex flags': re.IGNORECASE,
                'prereq': [],
                'prereq_type': []
            },
            'password auth': {
                'description': 'password authentication is allowed; prefer key authentication',
                'type': 'default',
                'regex': '^PasswordAuthentication\s+no',
                'regex flags': re.IGNORECASE,
                'prereq': [],
                'prereq_type': []
            },
            'empty passwords': {
                'description': 'login to accounts with empty passwords allowed',
                'type': 'explicit',
                'regex': '^PermitEmptyPasswords\s+yes',
                'regex flags': re.IGNORECASE,
                'prereq': ['password auth'],
                'prereq_type': ['vulnerable default'],
            },
            'root login': {
                'description': 'root login allowed',
                'type': 'default',
                'regex': '^PermitRootLogin\s+no',
                'regex flags': re.IGNORECASE,
                'prereq': [],
                'prereq_type': [],
            },
            'root login no pass': {
                'description': 'password authentication disabled for root',
                'type': 'explicit',
                'regex': '^PermitRootLogin\s+without-password',
                'regex flags': re.IGNORECASE,
                'prereq': ['root login'],
                'prereq_type': ['vulnerable default'],
            },
            'permit user env': {
                'description': 'environment processing may enable users to bypass access restrictions in some configurations using mechanisms like LD_PRELOAD',
                'type': 'explicit',
                'regex': '^PermitUserEnvironment\s+yes',
                'regex flags': re.IGNORECASE,
                'prereq': [],
                'prereq_type': [],
            },
            'protocol 1': {
                'description': 'using protocol version 1',
                'type': 'explicit',
                'regex': '^Protocol\s+1',
                'regex flags': re.IGNORECASE,
                'prereq': [],
                'prereq_type': []
            },
            'pubkey auth': {
                'description': 'public key authentication disabled',
                'type': 'explicit',
                'regex': '^PubkeyAuthentication\s+no',
                'regex flags': re.IGNORECASE,
                'prereq': ['protocol 2'],
                'prereq_type': ['normal default']
            },
            'client alive interval': {
                'description': 'no timeout interval specified; idle sessions can be dangerous',
                'type': 'default',
                'regex': '^ClientAliveInterval\s+[1-9][0-9]*',
                'regex flags': re.IGNORECASE,
                'prereq': [],
                'prereq_type': []
            },
            'strict mode': {
                'description': "checking file modes and ownership of users' files or home directory before accepting login disabled. This is desirable since novices sometimes leave their directory/files world-writable.",
                'type': 'explicit',
                'regex': '^StrictModes\s+no',
                'regex flags': re.IGNORECASE,
                'prereq': [],
                'prereq_type': []
            },
            'tcp keepalive': {
                'description': 'sessions may hang indefinitely, leaving "ghost" users and consuming server resources',
                'type': 'explicit',
                'regex': '^TCPKeepAlive\s+no',
                'regex flags': re.IGNORECASE,
                'prereq': [],
                'prereq_type': []
            },
            'use login': {
                'description': 'login(1) is used for interactive login sessions',
                'type': 'explicit',
                'regex': '^UseLogin\s+yes',
                'regex flags': re.IGNORECASE,
                'prereq': [],
                'prereq_type': []
            },
            'no privilege separation': {
                'description': 'privilege separation disabled',
                'type': 'explicit',
                'regex': '^UsePrivilegeSeparation\s+no',
                'regex flags': re.IGNORECASE,
                'prereq': [],
                'prereq_type': []
            },
            'x11 forwarding': {
                'description': "the client's X11 display server may be exposed to attack when the SSH client requests forwarding",
                'type': 'explicit',
                'regex': '^X11Forwarding\s+yes',
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
"""
Templates are used for 2 things:

  1) Prerequisite checking for all entries.
  2) Getting error line and line numbers for default entries.

If we're doing error line or line numbers, the regex used should
  be the config option in a vulnerable state. To account for
  implicitness, the name of the config option should at least
  be in the regex so we can provide the name in the error line.

If we're doing prerequisite checking, the regex used depends on
  the prereq state and type:

  vulnerable explicit: The config option must be explicitly set for
                         it to be in a vulnerable state.
  vulnerable default:  The config option is implicitly set to a
                         vulnerable state.
  normal explicit:     The config option must be explicitly set for
                         it to be in a safe state.
  normal default:      The config option is implicitly set to a
                         safe state.
"""
services_vuln_templates = {
    'ftp':
        {'anon enable': {
            'vuln': '^anonymous_enable=YES',
            'safe': '^anonymous_enable=NO'
            },
         # not a prereq
         'banner': '^(ftpd_banner|banner_file)',  # since we only get here if ftpd_banner isn't set,
                                                  # we can just set it to ftpd_banner so it always just
                                                  # shows the config option name
         #  This is here b/c if it were an ND, local_umask would
         #    only show if local_enable=YES wasn't in the file.
         #    And it couldn't be a NE since that would look for
         #    local_enable=NO as prereq confirmation.
         'local enable': {
            'vuln': '^local_enable=YES',
            'safe': '^local_enable=NO'
            },
        },
    'ssh':
        {'use login no': {
            'vuln': '^UseLogin\s+yes',  # disables x11
            'safe': '^UseLogin\s+no',
            },
         'root login': {
             'vuln': '^PermitRootLogin\s+yes',
             'safe': '^PermitRootLogin\s+no'
             },
         'password auth': {
             'vuln': '^PasswordAuthentication\s+yes',
             'safe': '^PasswordAuthentication\s+no'
             },
         # not a prereq
         'client alive interval': '^ClientAliveInterval\s+0',
        },
    # 'apache':
        # {
        # },
}

services_norm_templates = {
    'ftp':
        {
        },
    'ssh':
        # This is here and not local_enable because if it were a VE,
        #   and Protocol 1 was set, then PubkeyAuthentication would
        #   show up. Since it's a ND, PubkeyAuthentication will only
        #   show up if there's no match for Protocol 1. We can't have
        #   it as a VD either cause that wouldn't make any sense as
        #   the key values would be flipped flopped.
        {'protocol 2': {
             'vuln': '^protocol\s+1',
             'safe': '^protocol\s+(1,)?2(1,)?'
             },
        },
    # 'apache':
        # {
        # },
}

