from __future__ import print_function
import subprocess
import termios
import sys

def SysCall(cmd, bg=False):
    try:
        rv = subprocess.Popen(cmd) # run in background
        if not bg:
            rv.wait()
    except OSError as e:
        print(cmd[0], "not installed?")

def my_input(prompt):
    import tty
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    print(prompt, end=' ')
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def fstr(raw_str):
    '''format a raw string that has *'''
    # states: raw, esp (escape), hl (highlight)
    state = 'raw' 
    HC, RS = "\033[1m\033[32m", "\033[0m"
    fm_str = ''
    for c in raw_str:
        if state == 'raw':
            if c == '*':
                state = 'hl'
                fm_str += HC
            elif c == '\\':
                prev_state = state
                state = 'esp'
            else:
                fm_str += c
        elif state == 'hl':
            if c == '*':
                state = 'raw'
                fm_str += RS
            elif c == '\\':
                prev_state = state
                state = 'esp'
            else:
                fm_str += c 
        elif state == 'esp':
                state = prev_state
                fm_str += c

    if state == 'hl':
        fm_str += RS # in case of unmatched *

    return fm_str # in case of unmatched *

def paged_print(s, line_limit=48):
    ''' print s in a 48 line per page fashion,
        ask user to continue once output reaches page limit
    '''
    lines = s.splitlines()
    while lines:
        print('\n'.join(lines[:line_limit]))
        lines = lines[line_limit:]
        if lines and input("More? ") not in ['Y', 'y']:
            break

