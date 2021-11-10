#!/usr/bin/env python3
import subprocess
from subprocess import run

if __name__ == '__main__':

    process = run(['id', '-u'], check=True, text=True, capture_output=True)
    uid = str(process.stdout)
    if int(uid) != 0:
        print("Unauthorized - Try running with sudo.")
        exit(1)

    run(['systemctl', 'stop', 'jar_logon.service'], check=True, text=True)

    with open('./logs/logon_server.log', 'w'):
        ...  # clear the log

    run(['git', 'stash'], check=True, text=True)
    run(['git', 'fetch'], check=True, text=True)
    run(['git', 'pull'], check=True, text=True)
    run(['chown', '-R', 'jar_user:jar_user', '*'], check=True, text=True)

    process = run("grep -rl '^#!/.*' .", text=True, capture_output=True, shell=True)
    lines = str(process.stdout).strip().split('\n')
    if lines and not lines[0].startswith('grep:'):
        for item in lines:
            if '/.git/' not in item:
                run(['chmod', '+x', item], check=True, text=True)
    run(['chmod', '0554', '-R', '*'], check=True, text=True)
    run(['chmod', '0664', './logs/logon_server.log'], check=True, text=True)
    run(['chmod', '0440', './params.json'], check=True, text=True)
    run(['systemctl', 'start', 'jar_logon.service'], check=True, text=True, capture_output=True)
    process = run(['systemctl', 'status', '-n', '100', 'jar_logon.service'], check=True, text=True,
                  stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    status_output = str(process.stdout)
    print(status_output)