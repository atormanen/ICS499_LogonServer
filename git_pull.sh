#!/bin/bash
if [ $(id -u) -ne 0 ]
  then echo "Unauthorized"
  exit
fi
systemctl stop jar_logon.service
echo '' > ./logs/logon_server.log # clear log
git stash
git fetch
git pull
chown -R jar_user:jar_user *
chmod +x ./git_pull.sh
chmod +x ./controller.py
chmod 0554 -R *
chmod 0664 ./logs/logon_server.log
chmod 0440 ./params.json
systemctl start jar_logon.service
systemctl status -n 100 jar_logon.service
tail -n 100 -f ./logs/logon_server.log
