# github-utils

A command-line tool to manage repositories of GitHub.

# Install

```
pip install github-utils
```

# Configurations

In file `~/.github-utils/config.ini`

```
[auth]
access_token = GITHUB_ACCESS_TOKEN
```

# Commands

## List all repositories

```
github_utils list-repos
```

## Create new repositories

```
github-utils create-repos [--private] [--description DESC] [--homepage URL] [--has-issues] [--has-wiki]
                          [--has-downloads] [--auto-init] [--gitignore_template LANG]
                          NAME...
```

## Delete existing repositories

```
github-utils delete-repos [--all] [NAME...]
```

## License

Copyright (C) 2020 HE Yaowen <he.yaowen@hotmail.com>

The GNU General Public License (GPL) version 3, see [COPYING](./COPYING).