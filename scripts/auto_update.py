#!/usr/bin/python3

import configparser
import os
import datetime
from git import Repo

config = configparser.ConfigParser()
root_dir = os.getcwd() + '/..'
now = datetime.datetime.now()

if not os.path.exists(f"{root_dir}/.user.conf"):
    with open(f"{root_dir}.user.conf", 'w') as user_conf:
        user_conf.write('[USER]\n')
        user_conf.write('Autoupdate = True')

if not os.path.exists(f"{root_dir}/.gitignore"):
    with open(f"{root_dir}/.gitignore", 'w') as gitignore:
        gitignore.write('.user.conf')

config.read([f"{root_dir}/.global.conf", f"{root_dir}/.user.conf"])



last_update = config.get('USER', 'last_update', fallback=False)


if not config.get('USER', 'auto_update'):
    exit()

repo = Repo(root_dir)
master_branch = config.get('GLOBAL', 'master_branch', fallback='master')


print(last_update)

config.set('USER', 'last_update', now.strftime("%m/%d/%Y, %H:%M:%S"))
with open(f"{root_dir}/.user.conf", 'w') as config_file:
    config.write(config_file)