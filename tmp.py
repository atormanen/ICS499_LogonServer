#!/usr/bin/env python3
import subprocess
import sys
from time import sleep
from subprocess import run

if __name__ == '__main__':

    width = 40
    try:
        verbose = True
        quiet = False
        should_monitor_log = True
        should_show_service_status = True
        operation = 'pull'

        c_operation = operation.strip().lower()


        def qprint(*args, **kwargs):
            if any(args) or any(kwargs):
                print(*args, **kwargs)


        def vprint(*args, **kwargs):
            if verbose:
                if any(args) or any(kwargs):
                    print(*args, **kwargs)


        def vnprint(*args, **kwargs):
            if not quiet:
                if any(args) or any(kwargs):
                    print(*args, **kwargs)


        def nprint(*args, **kwargs):
            if not verbose and not quiet:
                if any(args) or any(kwargs):
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
        vnprint('Stopping Service'.center(width), end='\r')
        process = run(['systemctl', 'stop', 'jar_logon.service'], check=True, text=True, capture_output=True)
        vnprint('Stopped Service'.center(width))
        vprint(process.stdout)
        vnprint(process.stderr, file=sys.stderr)
        nprint('')

        # --------------------------------------------
        #                  Clearing Logs
        vnprint('-' * width)
        vnprint('Clearing Logs'.center(width), end='\r')
        with open('./logs/logon_server.log', 'w'):
            ...  # clear the log
        vnprint('Cleared Logs'.center(width))

        # --------------------------------------------
        #               Performing Git Add All
        vnprint('-' * width)
        vnprint('Performing Git Add All'.center(width), end='\r')
        process = run(['git', 'add', '--all'], check=True, text=True, capture_output=True)
        vnprint('Performed Git Add Add'.center(width))
        vprint(process.stdout)
        vnprint(process.stderr, file=sys.stderr)

        # --------------------------------------------
        #               Performing Git Stash
        vnprint('-' * width)
        vnprint('Performing Git Stash'.center(width), end='\r')
        process = run(['git', 'stash'], check=True, text=True, capture_output=True)
        vnprint('Performed Git Stash'.center(width))
        vprint(process.stdout)
        vnprint(process.stderr, file=sys.stderr)

        # --------------------------------------------
        #               Performing Git Fetch
        vnprint('-' * width)
        vnprint('Performing Git Fetch'.center(width), end='\r')
        process = run(['git', 'fetch'], check=True, text=True, capture_output=True)
        vnprint('Performed Git Fetch'.center(width))
        vprint(process.stdout)
        vnprint(process.stderr, file=sys.stderr)

        # --------------------------------------------
        #               Performing Git <op>
        vnprint('-' * width)
        vnprint(f'Performing Git {operation.capitalize()}'.center(width), end='\r')
        process = run(['git', str(operation)], check=True, text=True, capture_output=True)
        vnprint(f'Performed Git {operation.capitalize()}'.center(width))
        vprint(process.stdout)
        vnprint(process.stderr, file=sys.stderr)

        # --------------------------------------------
        #               Changing Ownership
        vnprint('-' * width)
        vnprint('Changing Ownership'.center(width), end='\r')
        process = run(['chown', '-R', 'jar_user:jar_user', '.'], text=True, capture_output=True)
        vnprint('Changed Ownership'.center(width))
        vprint(process.stdout)
        vnprint(process.stderr, file=sys.stderr)

        # --------------------------------------------
        #           Changing Mode Bits
        vnprint('-' * width)
        vnprint('Changing Mode Bits'.center(width), end='\r')
        processes = [None, None, None]
        processes[0] = run('chmod 0554 -R .', check=True, text=True, shell=True, capture_output=True)
        processes[1] = run(['chmod', '0664', './logs/logon_server.log'], check=True, text=True, capture_output=True)
        processes[2] = run(['chmod', '0440', './params.json'], check=True, text=True, capture_output=True)
        vnprint('Changed Mode Bits'.center(width))
        for process in processes:
            vprint(process.stdout)
            vnprint(process.stderr, file=sys.stderr)

        # --------------------------------------------
        #           Making Scripts Executable
        vnprint('-' * width)
        vnprint('Making Scripts Executable'.center(width), end='\r')
        processes = [None, None]
        processes[0] = run("grep -rl '^#!/.*' .", text=True, shell=True, capture_output=True)
        lines = str(process.stdout).strip().split('\n')
        if lines and not lines[0].startswith('grep:'):
            for item in lines:
                if item and '/.git/' not in item:
                    processes[1] = run(['chmod', '+x', item], check=True, text=True, capture_output=True)

        vnprint('Made Scripts Executable'.center(width))

        for process in processes:
            if process:
                vprint(process.stdout)
                vnprint(process.stderr, file=sys.stderr)

        # --------------------------------------------
        #           Restarting Service
        vnprint('-' * width)
        vnprint('Restarting Service'.center(width), end='\r')
        process = run(['systemctl', 'restart', 'jar_logon.service'], check=True, text=True, capture_output=True)
        vnprint('Restarted Service'.center(width))
        vprint(process.stdout)
        vnprint(process.stderr, file=sys.stderr)

        if (should_show_service_status):
            # --------------------------------------------
            #           Service Status
              # to see if the server false to get started
            vnprint('-' * width)
            vnprint('Waiting on Service Status'.center(width), end='\r')
            sleep(5.0)
            process = run(['systemctl', 'status', '-n', '100', 'jar_logon.service'], check=True, text=True, capture_output=True)
            vnprint('Service Status'.center(width))
            vprint(process.stdout)
            vnprint(process.stderr, file=sys.stderr)

        if (should_monitor_log):
            # --------------------------------------------
            #           Log Monitor
            vnprint('-' * width)
            vnprint('=Log Monitor'.center(width))

            t = run(['tail', '-n', '100', '-f', './logs/logon_server.log'], text=True)
        else:
            vnprint('-' * width)
            vnprint('-' * width)
    except subprocess.CalledProcessError as e:
        def sprint(s, *args, **kwargs):
            print(f"*{str(s).strip().center(width-2)}*", *args, **kwargs)
        print('*' * width)
        sprint('Stopping Service')
        print('*' * width)
        print(e.cmd)
        print(e.args)
        print(e.stdout)
        print(e.stderr, sys.stderr)
        raise e
