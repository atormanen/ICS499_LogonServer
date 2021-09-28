#!/bin/bash
git stash
git fetch
git pull
chmod +x -R *
systemctl restart jar_logon.service
tail -f ./logs/logon_server.log
