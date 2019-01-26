# Style Guide
This page lists specific formatting instructions for sve entries.


## Layout
*service_info.py* is divided into 4 sections.

If you simply want to add a configuration entry for a service already covered by sve, [Entries](#entries) and [Templates](#templates) will be what you want to look at.

If you're looking to add entries for a brand new service, [Names](#names) and [Configuration Files](#configs) will also be of interest.

<a name="names"></a>
### Names
This section holds the common and actual names of services processed by sve. Actual names are the ones used by `systemctl`, `service`, or some other system manager; they can often be found in the service's configuration filename. For example, SSH's common name is **ssh** while it's actual name would be **sshd**.

*Note*: The common name in any service structure should be all lowercase.

When adding a new service or operating system:

1. Append the service's common name to `services_sve`.
2. Update each operating system's service dictionary in `services_actual`. As a quick reference, the format of a `services_actual` entry is:

```
'Operating System or Linux distribution':
    {
        'common service name 1': 'actual service name 1',
        'common service name 2': 'actual service name 2',
        ...
    },
    ...
```


<a name="configs"></a>
### Configuration Files
This section holds the configuration file locations of the services processed by `sve`. The locations may differ between operating systems so each OS has it's own dictionary that needs to be updated when adding a new service.

The format of `services_configs` is:
```
'Operating System or Linux distribution':
    {
        'common service name 1': 'config file 1',
        'common service name 2': 'config file 2',
        ...
    },
    ...
```

<a name="entries"></a>
### Entries
This section holds information about configuration options processed by sve. The format of `services_entries` is:

```
'common service name':
    {
        'short entry name (preferably 2 or 3 words)': {
            'description': 'brief description of the vulnerability',
            'type': 'the entry's type',
            'regex': 'a regex pattern for determining if the config option is set',
            'prereq': 'a list of prerequisite config options',
            'prereq_type': 'a list of types for each prerequisite'
        },
        ...
    }
    ...
```

#### `type`
Config options can be in 1 of 2 states: vulnerable or safe.

For example, `anonymous_enable` can only be set to `YES` (vulnerable) or `NO` (safe). Consequently, config options can have the following `type` values:

* **explicit**: Indicates that the config option is only in a vulnerable state if explicitly set.
  * For example, `anon_upload_enable` must be explicitly set to `YES`.
* **default**: Indicates that the config option is in a vulnerable state by default.
  * For example, `anonymous_enable` is automatically set to `YES`.
* **special regex**: Indicates the config option type is explicit, but matching it relies on some regex magic and thus requires some special output processing on sve's side.
  * For example, `^local_umask=0[0-6][0-6]` is a special regex since in our test output we don't want to show `[0-6]` but the actual number matched.


#### `regex`
The `regex` field is a pattern allowing sve to determine if a vulnerable config option is set or not. How the pattern is constructed depends on your `type` specification:

* If an entry is considered `explicit`, then the regex pattern  will probably be more or less an exact copy of the config option when it's set (e.g., `^anon_upload_enable=YES` is an explicit regex since `anon_upload_enable` must be set to `YES` explicitly for it to be in a vulnerable state).

* If an entry is considered a `default`, the pattern should match the config option when it's not set. (e.g., `^anonymous_enable=NO` is a default regex since `anonymous_enable` is automatically set to `YES`). This way, if we don't find a match, we know that the config option must be set, either explicitly or automatically.

* If an entry is considered a `special regex`, follow the rules for `explicit` regexes.


#### `prereq`, `prereq_type`
The `prereq` field is a list of config options required by an entry, denoted by their short entry name. For example, `allow_anon_ssl` requires `anonymous_enable` and so you would put `anon FTP` in `prereq`.

Prerequisites also have their own types, reflected in the `prereq_type` field. Its value is a list of corresponding types for each prerequisite listed in `prereq`. Valid prerequisite types include:
* **normal explicit**: The prerequisite is a safe config option that must be explicitly set.
  * For example, `local_umask` is a potentially vulnerable config option that requires `local_enable`, a safe config option, to be set).
* **normal default**: The prerequisite is a safe config option that is automatically set.
* **vulnerable explicit**: The prerequisite is a vulnerable config option that must be explicitly set.
* **vulnerable default**: The prerequisite is a vulnerable config option that is automatically set.
  * For example, `anon_upload_enable` is a potentially vulnerable config option that requires `anonymous_enable`, a vulnerable config option that's automatically set to `YES`.

<a name="templates"></a>
### Templates
This section contains templates for default entries. Templates have 3 main uses:
1. Getting the line number of explicitly set default vulnerable config options.
2. Getting the config option name of implicitly set default vulnerable config options.
3. Prerequisite checking for all config options.

Use cases 1 and 2 can be thought of as the same thing when submitting a new entry. The regex for either situation should match the config option in a vulnerable state.

Note: To account for implicitly set options, the entire config option should be in the regex so that we can provide the name in the error line. For example, `^anonymous_enable=YES` is fine since we would be able to match `anonymous_enable` if the option's not explicitly set.

As for using templates to check if prequisite config options are satisfied, the regex depends on its type. valid prerequisite types are shown below:

* **vulnerable explicit**: The config option must be explicitly set for it to be in a vulnerable state.
* **vulnerable default**:  The config option is implicitly set to a vulnerable state.
* **normal explicit**:     The config option must be explicitly set for it to be in a safe state.
* **normal default**:      The config option is implicitly set to a safe state.

But isn't `vulnerable explicit` the same thing as `normal default`? And `vulnerable default` the same as `normal explicit`? Logically, they are. However, the reason for the distinction is that sve's regex processing is very simple. If the regex type has `explicit` in the name, sve will only say the vulnerable config option exists if the regex provided has a match. Likewise, if the regex type has `default` in the name, sve will say the option exists only if there's no match.

Given that, consider the `PubkeyAuthentication` option for SSH. It requires the `Protocol` option to be set to `2` (since only SSHv2 supports public key authentication), which it automatically is in most SSH clients. In our heads, it would make sense to label `Protocol` as a `vulnerable explicit` since you have to explicitly set it to `1` for it to be in a vulnerable state right? Well, if you set and provide `Protocol 1` as the prerequisite regex to sve with a type of `vulnerable explicit`, sve would say that `PubkeyAuthentication`'s prerequisites are satisfied, which we know isn't to be true so `PubkeyAuthentication` requires `Protocol 2`. We also can't just switch the regex provided to `Protocol 2` as that would mean the `vuln` key would have a value of the config option in a safe state and the `safe` key would have a value of the config option in a vulnerable state, which is even more confusing. So that's why we have 4 prereq types.

There are 2 template structures, `services_vuln_templates` which holds patterns for vulnerable config options, and `services_norm_templates` which holds patterns for safe config options (**that actually doesn't hold true anymore this needs a better name**).

Both of their formats are:
```
'common service name':
    {'short entry name (non-prereq)': 'regex pattern',
     'short entry name (prereq)': {
         'vuln': 'regex pattern',
         'safe': 'regex pattern'
         },
     ...
    },
    ...
```

As a general rule, the regex patterns tend to follow the following formats:
```
^{ENTRY NAME}={ENTRY VALUE}
^{ENTRY NAME}\s+{ENTRY VALUE}

# Examples
^anonymous_enable=YES
^PasswordAuthentication\s+yes
```
