#!/bin/bash
systemctl stop jar_logon.service
git stash
git fetch
git pull
chown -R jar_user:jar_user *
chmod 0554 -R *
systemctl restart jar_logon.service
tail -n 100 -f ./logs/logon_server.log
