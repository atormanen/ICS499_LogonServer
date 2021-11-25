#!/usr/bin/env python3
from __future__ import annotations

import shutil
import subprocess
import sys
from subprocess import run
from time import sleep
from typing import List, Optional

# Help Documentation Constants
from util.args import CommandDict
from util.const import ConstContainer

WAIT_TIME_SECONDS = 2.0

commands: CommandDict = CommandDict()


class GitOp(ConstContainer):
    PULL = 'pull'
    PUSH = 'push'
    CHECKOUT = 'checkout'


def __perform_git_op(git_op: str, parsed_args) -> None:
    is_verbose = parsed_args.verbose
    is_quiet = parsed_args.quiet
    if _SCRIPT_IS_INTERACTIVE_BY_DEFAULT:
        is_interactive = True
    else:
        is_interactive = parsed_args.interactive
    command_args = parsed_args.command_args
    width = int(shutil.get_terminal_size((80, 20)).columns * 0.8)
    should_monitor_log = is_interactive
    should_show_service_status = not is_quiet
    operation = git_op.strip().lower()

    def s_print(s, *args, **kwargs):
        print(f"*{str(s).strip().center(width - 2)}*", *args, **kwargs)

    def quiet_print(*args, **kwargs):
        if any(args) or any(kwargs):
            print(*args, **kwargs)

    def verbose_print(*args, **kwargs):
        if is_verbose:
            if any(args) or any(kwargs):
                print(*args, **kwargs)

    def verbose_or_normal_print(*args, **kwargs):
        if not is_quiet:
            if any(args) or any(kwargs):
                print(*args, **kwargs)

    def normal_print(*args, **kwargs):
        if not is_verbose and not is_quiet:
            if any(args) or any(kwargs):
                print(*args, **kwargs)

    try:

        print('start')
        process = run(['id', '-u'], check=True, text=True, capture_output=True)
        uid = str(process.stdout)
        if int(uid) != 0:
            quiet_print("Unauthorized - Try running with sudo.")
            exit(1)

        # --------------------------------------------
        #               Stopping Service
        verbose_or_normal_print('-' * width)
        verbose_or_normal_print('Stopping Service'.center(width), end='\r')
        process = run(['systemctl', 'stop', 'jar_logon.service'], check=True, text=True, capture_output=True)
        verbose_or_normal_print('Stopped Service'.center(width))
        verbose_print(process.stdout)
        verbose_or_normal_print(process.stderr, file=sys.stderr)
        normal_print('')

        # --------------------------------------------
        #                  Clearing Logs
        verbose_or_normal_print('-' * width)
        verbose_or_normal_print('Clearing Logs'.center(width), end='\r')
        with open('./logs/logon_server.log', 'w'):
            ...  # clear the log
        verbose_or_normal_print('Cleared Logs'.center(width))

        # --------------------------------------------
        #               Performing Git Add All
        verbose_or_normal_print('-' * width)
        verbose_or_normal_print('Performing Git Add All'.center(width), end='\r')
        process = run(['git', 'add', '--all'], check=True, text=True, capture_output=True)
        verbose_or_normal_print('Performed Git Add Add'.center(width))
        verbose_print(process.stdout)
        verbose_or_normal_print(process.stderr, file=sys.stderr)

        # --------------------------------------------
        #               Performing Git Stash
        verbose_or_normal_print('-' * width)
        verbose_or_normal_print('Performing Git Stash'.center(width), end='\r')
        process = run(['git', 'stash'], check=True, text=True, capture_output=True)
        verbose_or_normal_print('Performed Git Stash'.center(width))
        verbose_print(process.stdout)
        verbose_or_normal_print(process.stderr, file=sys.stderr)

        # --------------------------------------------
        #               Performing Git Fetch
        verbose_or_normal_print('-' * width)
        verbose_or_normal_print('Performing Git Fetch'.center(width), end='\r')
        process = run(['git', 'fetch'], check=True, text=True, capture_output=True)
        verbose_or_normal_print('Performed Git Fetch'.center(width))
        verbose_print(process.stdout)
        verbose_or_normal_print(process.stderr, file=sys.stderr)

        # --------------------------------------------
        #               Performing Git <op>
        verbose_or_normal_print('-' * width)
        verbose_or_normal_print(f'Performing Git {operation.capitalize()}'.center(width), end='\r')
        process = run(['git',
                       str(operation),
                       *[str(arg) for arg in command_args]],
                      check=True,
                      text=True,
                      capture_output=True)
        verbose_or_normal_print(f'Performed Git {operation.capitalize()}'.center(width))
        verbose_print(process.stdout)
        verbose_or_normal_print(process.stderr, file=sys.stderr)

        # --------------------------------------------
        #               Changing Ownership
        verbose_or_normal_print('-' * width)
        verbose_or_normal_print('Changing Ownership'.center(width), end='\r')
        process = run(['chown', '-R', 'jar_user:jar_user', '.'], text=True, capture_output=True)
        verbose_or_normal_print('Changed Ownership'.center(width))
        verbose_print(process.stdout)
        verbose_or_normal_print(process.stderr, file=sys.stderr)

        # --------------------------------------------
        #           Changing Mode Bits
        verbose_or_normal_print('-' * width)
        verbose_or_normal_print('Changing Mode Bits'.center(width), end='\r')
        processes = [None, None, None]
        processes[0] = run('chmod 0554 -R .', check=True, text=True, shell=True, capture_output=True)
        processes[1] = run(['chmod', '0664', './logs/logon_server.log'], check=True, text=True, capture_output=True)
        processes[2] = run(['chmod', '0440', './params.json'], check=True, text=True, capture_output=True)
        verbose_or_normal_print('Changed Mode Bits'.center(width))
        for process in processes:
            verbose_print(process.stdout)
            verbose_or_normal_print(process.stderr, file=sys.stderr)

        # --------------------------------------------
        #           Making Scripts Executable
        verbose_or_normal_print('-' * width)
        verbose_or_normal_print('Making Scripts Executable'.center(width), end='\r')
        processes = [None, None]
        processes[0] = run("grep -rl '^#!/.*' .", text=True, shell=True, capture_output=True)
        lines = str(process.stdout).strip().split('\n')
        if lines and not lines[0].startswith('grep:'):
            for item in lines:
                if item and '/.git/' not in item:
                    processes[1] = run(['chmod', '+x', item], check=True, text=True, capture_output=True)

        verbose_or_normal_print('Made Scripts Executable'.center(width))

        for process in processes:
            if process:
                verbose_print(process.stdout)
                verbose_or_normal_print(process.stderr, file=sys.stderr)

        # --------------------------------------------
        #           Restarting Service
        verbose_or_normal_print('-' * width)
        verbose_or_normal_print('Restarting Service'.center(width), end='\r')
        process = run(['systemctl', 'restart', 'jar_logon.service'], check=True, text=True, capture_output=True)
        verbose_or_normal_print('Restarted Service'.center(width))
        verbose_print(process.stdout)
        verbose_or_normal_print(process.stderr, file=sys.stderr)

        if (should_show_service_status):
            # --------------------------------------------
            #           Service Status
            # to see if the server false to get started
            verbose_or_normal_print('-' * width)
            verbose_or_normal_print('Waiting on Service Status'.center(width), end='\r')
            sleep(WAIT_TIME_SECONDS)
            try:
                process = run(['systemctl', 'status', '-n', '100', 'jar_logon.service'], check=True, text=True,
                              capture_output=True)
            except subprocess.CalledProcessError as e:
                verbose_or_normal_print('Service Status'.center(width))
                print(e.output)
                # print(e.stderr.decode('utf8', 'ignore'), sys.stderr)
                print('-' * width)
                print('Log'.center(width))
                t = run(['tail', '-n', '100', './logs/logon_server.log'], text=True)
                print('-' * width)
                print('-' * width)
                exit(2)
            verbose_or_normal_print('Service Status'.center(width))
            verbose_or_normal_print(process.stdout)
            verbose_or_normal_print(process.stderr, file=sys.stderr)

        if (should_monitor_log):
            # --------------------------------------------
            #           Log Monitor
            verbose_or_normal_print('-' * width)
            verbose_or_normal_print('=Log Monitor'.center(width))

            t = run(['tail', '-n', '100', '-f', './logs/logon_server.log'], text=True)
        else:
            verbose_or_normal_print('-' * width)
            verbose_or_normal_print('-' * width)
    except subprocess.CalledProcessError as e:

        print('*' * width)
        s_print('CalledProcessError')
        print('*' * width)
        print('cmd'.center(width))
        print(e.cmd)
        print('-' * width)
        print('args'.center(width))
        print(e.args)
        print('-' * width)
        print('stdout'.center(width))
        print(e.stdout)
        print('-' * width)
        print('stderr'.center(width))
        print(e.stderr, sys.stderr)
        raise e


@commands.add(description='pull changes and restart service.')
def pull(parsed_args) -> None:
    __perform_git_op(GitOp.PULL, parsed_args)


@commands.add(description='push changes and restart service.')
def push(parsed_args) -> None:
    __perform_git_op(GitOp.PUSH, parsed_args)


@commands.add(description='change current branch.', args=('<branch>',))
def checkout(parsed_args) -> None:
    __perform_git_op(GitOp.CHECKOUT, parsed_args)


_SCRIPT_NAME: Optional[str] = None
_SCRIPT_USAGE: Optional[str] = '\n'.join(('jargit.py command [command_args ...] [-h] [-v | -q] [--interactive]',
                                          '',
                                          'commands:',
                                          *[f'  {c.get_help_msg()}' for c in commands.values()]))
_SCRIPT_DESCRIPTION: Optional[str] = None
_SCRIPT_EPILOG: Optional[str] = None

# Script Default Constants
_SCRIPT_IS_INTERACTIVE_BY_DEFAULT = False

def main(args: Optional[List[str]]):
    """Executes the script. Use '-h' argument to see help info."""

    if not args:  # Default operation if no arguments are received.

        # show help
        main(['-h'])

    else:  # Operation when processing arguments.
        import argparse

        # List of variables to be set by arguments and their default values
        is_verbose: bool = False
        is_quiet: bool = False
        is_interactive: bool = _SCRIPT_IS_INTERACTIVE_BY_DEFAULT

        # Setup the argument parser
        ap: argparse.ArgumentParser = argparse.ArgumentParser(prog=_SCRIPT_NAME,
                                                              usage=_SCRIPT_USAGE,
                                                              description=_SCRIPT_DESCRIPTION,
                                                              epilog=_SCRIPT_EPILOG)
        ap.add_argument('command', action='store', help='Command to run.')
        ap.add_argument('command_args', action='store', nargs='*', help='arguments for command.')

        # Setup output group
        ap.output_group = ap.add_mutually_exclusive_group()
        ap.output_group.add_argument('-v', '--verbose', action='store_true', help='Outputs more information.')
        ap.output_group.add_argument('-q', '--quiet', action='store_true', help='Suppresses outputs.')

        if not _SCRIPT_IS_INTERACTIVE_BY_DEFAULT:
            ap.add_argument('--interactive', action='store_true', help='Allow user interaction during execution')

        # Parse the args
        args = ap.parse_args(args)

        # Use the parsed args to set variables
        is_verbose = args.verbose
        is_quiet = args.quiet
        if not _SCRIPT_IS_INTERACTIVE_BY_DEFAULT:
            is_interactive = args.interactive

        command_str = args.command
        if command_str in commands:
            command = commands[command_str]
            command.action(args)


if __name__ == '__main__':
    from sys import argv

    main(argv[1:])

#     process = run(['id', '-u'], check=True, text=True, capture_output=True)
#     uid = str(process.stdout)
#     if int(uid) != 0:
#         print("Unauthorized - Try running with sudo.")
#         exit(1)
#
#     run(['systemctl', 'stop', 'jar_logon.service'], check=True, text=True)
#
#     with open('./logs/logon_server.log', 'w'):
#         ...  # clear the log
#
#     run(['git', 'stash'], check=True, text=True)
#     run(['git', 'fetch'], check=True, text=True)
#     run(['git', 'pull'], check=True, text=True)
#     run(['chown', '-R', 'jar_user:jar_user', '*'], check=True, text=True)
#
#     process = run("grep -rl '^#!/.*' .", text=True, capture_output=True, shell=True)
#     lines = str(process.stdout).strip().split('\n')
#     if lines and not lines[0].startswith('grep:'):
#         for item in lines:
#             if '/.git/' not in item:
#                 run(['chmod', '+x', item], check=True, text=True)
#     run(['chmod', '0554', '-R', '*'], check=True, text=True)
#     run(['chmod', '0664', './logs/logon_server.log'], check=True, text=True)
#     run(['chmod', '0440', './params.json'], check=True, text=True)
#     run(['systemctl', 'start', 'jar_logon.service'], check=True, text=True, capture_output=True)
#     process = run(['systemctl', 'status', '-n', '100', 'jar_logon.service'], check=True, text=True,
#                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
#     status_output = str(process.stdout)
#     print(status_output)
#     t = run(['tail', '-n', '100', '-f', './logs/logon_server.log'], text=True)
#     print("done")
