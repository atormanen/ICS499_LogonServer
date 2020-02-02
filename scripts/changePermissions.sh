#!/bin/bash
#sudo chown -R apache:apache /var/www/html/apothecary
sudo chow -R 777 /var/logonServer/ICS499_LogonServer
python3 /var/logonServer/ICS499_LogonServer/listener.py
