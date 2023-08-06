# ntfy-send

ntfy-send is a client application for notification service
[ntfy.sh](https://ntfy.sh).

## Configuration

ntfy-send can be configured via a configuration file. It is recommended
method of storing your credential informations, which simplifies obtaining
and sending them to ntfy server.

All configuration options can be enclosed in backticks (`). When this is the
case, the option is treated as a command whose output substitutes the
configurration option.

Configuration files are stored in _$XDG_CONFIG_HOME/ntfy-send/config.toml_.
If you don't have _$XDG_CONFIG_HOME_ environment variale set, then it is
stored in _~/.config/ntfy-send/config.toml_. Below are documented all
options:

```toml
# config.toml

# URL to the server
server = "https://ntfy.sh"

# Username and password can be automatically obtained each time they're
# required. This is done by passing commands which should echo credentials.
# For complex commands it's recommended to pot them in a separate script, due
# to problems with several levels of quote escaping

# Username and password can be passed in plain text. This isn't recommended.
username = "user"
password = "pass"

# Alternatively, ntfy-send can automatically run a command for username and
# password when they're enclosed in backticks (`):
username = """`gpg2 --decrypt pass.gpg | awk -F ":" '/user:/ { printf $2 }'`"""
password = """`gpg2 --decrypt pass.gpg | awk -F ":" '/password:/ { printf $2 }'`"""
```

