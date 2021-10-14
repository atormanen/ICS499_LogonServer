#!/bin/bash
systemctl stop jar_logon.service
git stash
git fetch
git pull
chown -R jar_user:jar_user *
chmod +x ./git_pull.sh
chmod +x ./controller.py
chmod 0554 -R *
chmod 0664 ./logs/logon_server.log
chmod 0440 ./params.json
systemctl restart jar_logon.service
tail -n 100 -f ./logs/logon_server.log
