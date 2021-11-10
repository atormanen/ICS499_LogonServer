#!/usr/bin/env python3
import subprocess
import sys
from subprocess import run

if __name__ == '__main__':

    width = 40
    verbose = True
    quiet = False
    should_monitor_log = True
    should_show_service_status = True
    operation = 'pull'

    c_operation = operation.strip().lower()


    def qprint(*args, **kwargs):
        print(*args, **kwargs)


    def vprint(*args, **kwargs):
        if verbose:
            print(*args, **kwargs)


    def vnprint(*args, **kwargs):
        if not quiet:
            print(*args, **kwargs)


    def nprint(*args, **kwargs):
        if not verbose and not quiet:
            print(*args, **kwargs)


    print('start')
    process = run(['id', '-u'], check=True, text=True, capture_output=True)
    uid = str(process.stdout)
    if int(uid) != 0:
        qprint("Unauthorized - Try running with sudo.")
        exit(1)

    # --------------------------------------------
    #               Stopping Service
    vnprint('-' * width)
    vnprint('Stopping Service'.center(width))
    process = run(['systemctl', 'stop', 'jar_logon.service'], check=True, text=True, capture_output=True)
    vprint(process.stdout)
    vnprint(process.stderr, file=sys.stderr)
    nprint('')

    # --------------------------------------------
    #                  Clearing Logs
    vnprint('-' * width)
    vnprint('Clearing Logs'.center(width))
    with open('./logs/logon_server.log', 'w'):
        ...  # clear the log

    # --------------------------------------------
    #               Performing Git Stash
    vnprint('-' * width)
    vnprint('Performing Git Stash'.center(width))
    process = run(['git', 'stash'], check=True, text=True, capture_output=True)
    vprint(process.stdout)
    vnprint(process.stderr, file=sys.stderr)

    # --------------------------------------------
    #               Performing Git Fetch
    vnprint('-' * width)
    vnprint('Performing Git Fetch'.center(width))
    process = run(['git', 'fetch'], check=True, text=True, capture_output=True)
    vprint(process.stdout)
    vnprint(process.stderr, file=sys.stderr)

    # --------------------------------------------
    #               Performing Git <op>
    vnprint('-' * width)
    vnprint(f'Performing Git {operation.capitalize()}'.center(width))
    process = run(['git', str(operation)], check=True, text=True, capture_output=True)
    vprint(process.stdout)
    vnprint(process.stderr, file=sys.stderr)

    # --------------------------------------------
    #               Changing Ownership
    vnprint('-' * width)
    vnprint('Changing Ownership'.center(width))
    process = run(['chown', '-R', 'jar_user:jar_user', '.'], text=True,capture_output=True)
    vprint(process.stdout)
    vnprint(process.stderr, file=sys.stderr)

    # --------------------------------------------
    #           Making Scripts Executable
    vnprint('-' * width)
    vnprint('Making Scripts Executable'.center(width))
    process =  run("grep -rl '^#!/.*' .", text=True,  shell=True, capture_output=True)
    vprint(process.stdout)
    vnprint(process.stderr, file=sys.stderr)
    lines = str(process.stdout).strip().split('\n')
    if lines and not lines[0].startswith('grep:'):
        for item in lines:
            if '/.git/' not in item:
                process = run(['chmod', '+x', item], check=True, text=True, capture_output=True)
                vprint(process.stdout)
                vnprint(process.stderr, file=sys.stderr)

    # --------------------------------------------
    #           Changing Mode Bits
    vnprint('-' * width)
    vnprint('Changing Mode Bits'.center(width))
    process = run('chmod 0554 -R .', check=True, text=True, shell=True, capture_output=True)
    vprint(process.stdout)
    vnprint(process.stderr, file=sys.stderr)
    process = run(['chmod', '0664', './logs/logon_server.log'], check=True, text=True, capture_output=True)
    vprint(process.stdout)
    vnprint(process.stderr, file=sys.stderr)
    process = run(['chmod', '0440', './params.json'], check=True, text=True, capture_output=True)
    vprint(process.stdout)
    vnprint(process.stderr, file=sys.stderr)

    # --------------------------------------------
    #           Restarting Service
    vnprint('-' * width)
    vnprint('Restarting Service'.center(width))
    process = run(['systemctl', 'restart', 'jar_logon.service'], check=True, text=True, capture_output=True)
    vprint(process.stdout)
    vnprint(process.stderr, file=sys.stderr)
    
    if(should_show_service_status):
        # --------------------------------------------
        #           Service Status
        vnprint('-' * width)
        vnprint('Starting Log Monitor'.center(width))
        process = run(['systemctl', 'status', '-n', '100', 'jar_logon.service'], check=True, text=True)

    if(should_monitor_log):
        # --------------------------------------------
        #           Starting Log Monitor
        vnprint('-' * width)
        vnprint('Starting Log Monitor'.center(width))

        t = run(['tail', '-n', '100', '-f', './logs/logon_server.log'], text=True)
    else:
        vnprint('-' * width)
        vnprint('-' * width)
        
        

