#!/usr/bin/python3

import configparser
import os
import datetime
from git import Repo


test = "test1234"
test2 = "test2 qwexsadsdqwe"

config = configparser.ConfigParser()
root_dir = os.getcwd() + '/..'
now = datetime.datetime.now()
timeformat = "%m/%d/%Y, %H:%M:%S"

if not os.path.exists(f"{root_dir}/.user.conf"):
    with open(f"{root_dir}/.user.conf", 'w') as user_conf:
        user_conf.write('[USER]\n')
        user_conf.write('auto_update = True\n')
        user_conf.write('update_every_x_days = 1')

if not os.path.exists(f"{root_dir}/.gitignore"):
    with open(f"{root_dir}/.gitignore", 'w') as gitignore:
        gitignore.write('.user.conf')

config.read([f"{root_dir}/.global.conf", f"{root_dir}/.user.conf"])



last_update = config.get('USER', 'last_update', fallback=False)
update_every_x_days = config.get('USER', 'update_every_x_days', fallback = 1)

if not config.get('USER', 'auto_update', fallback=False) or \
    datetime.datetime.strptime(last_update,timeformat) > now - datetime.timedelta(days=int(update_every_x_days)):
    exit()

repo = Repo(root_dir)
master_branch = config.get('GLOBAL', 'master_branch', fallback='master')
current_branch = repo.active_branch

head = repo.head.commit.tree
if not not repo.git.diff(head): 
    repo.git.stash('save')

if not current_branch.name == master_branch:
    repo.git.checkout(master_branch)

repo.remotes.origin.pull() 

if not current_branch.name == master_branch:
    repo.git.checkout(current_branch.name)
    repo.git.merge(master_branch)

if not not repo.git.diff(head):
    repo.git.stash.pop()    




print( now - datetime.timedelta(days=int(update_every_x_days)))
print(last_update)











config.set('USER', 'last_update', now.strftime(timeformat))
with open(f"{root_dir}/.user.conf", 'w') as config_file:
    config.write(config_file)
