# Contributing

All sve entries are stored right here on Github in [*service_info.py*](https://github.com/bl0nd/sve/blob/master/sve/service_info.py). Just open an issue or send a pull request and we'll add it in as soon as possible!


## Style
For information on the style of sve entries, please refer to the [Style Guide](https://github.com/bl0nd/sve/blob/master/contributing-guides/style-guide.md).


## Pull Requests
Most people submit pull requests to the sve project using GitHub's web interface.

If you prefer, you can do most of the process using the command line instead.
The overall process should look somewhat like this:

1. Fork the tldr repository on the github web interface.

2. Clone your fork locally:  
  `git clone https://github.com/<your_username>/sve.git && cd sve`

3. Create a feature branch (e.g., named after the entry you plan to create):  
  `git checkout -b <branch_name>`

4. Make your changes (edit existing files or create new ones)

5. Commit the changes (following the [commit message guidelines](#commit-msg)):  
  `git commit --all -m "<commit_message>"`

6. Push the commit(s) to your fork:  
  `git push origin <branch_name>`

7. Go to the github page for your fork and click the green "pull request" button.

Please only send related changes in the same pull request.
Typically a pull request will include changes in a single file.

<a name="commit-msg"></a>
## Commits
For the commit message, use the following format:
```
<name>: type of change
```

Examples:
* New entry for existing service: `anon FTP: add ftp entry`
* New service: `ssh: add service`
* New OS: `macOS: add OS`
* Revised entry regex: `local umask: revised ftp regex`
* New templates: `FTP banner: add ftp template`
