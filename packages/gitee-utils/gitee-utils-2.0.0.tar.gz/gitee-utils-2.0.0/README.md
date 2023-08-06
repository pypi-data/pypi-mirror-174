# gitee-utils

A command-line tool ported from [github-utils](https://github.com/he-yaowen/github-utils) to manage repositories on Gitee.

# Install

```
pip install gitee-utils
```

# Configurations

In file `~/.gitee-utils/config.ini`

```
[auth]
access_token = GITHUB_ACCESS_TOKEN
```

# Commands

## List all repositories

```
gitee-utils list-repos
```

## Create new repositories

```
gitee-utils create-repo [--private] [--description DESC] [--path PATH] [--homepage URL] [--has-issues] [--has-wiki]
                        [--can-comment] [--auto-init] [--gitignore_template LANG] [--license-template LICENSE]
                        NAME...
```

## Delete existing repositories

```
gitee-utils delete-repos [--all] [NAME...]
```


## License

Copyright (C) 2020 HE Yaowen <he.yaowen@hotmail.com>

The GNU General Public License (GPL) version 3, see [COPYING](./COPYING).