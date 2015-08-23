from __future__ import print_function
import subprocess
import termios
import sys

def require_python_version(required):
    if sys.version_info.major < required:
        print("Please use Python {0} or higher.".format(required))
        sys.exit(1)

def sys_cmd(cmd, bg=False):
    try:
        rv = subprocess.Popen(cmd) # run in background
        if not bg:
            rv.wait()
    except OSError as e:
        print(cmd[0], "not installed?")

''' seems broken
'''
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

''' format a raw string that has *
'''
def fstr(raw_str):
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

''' print list items in 48 line per page fashion,
    ask user to continue once output reaches page limit
'''
def paged_print(lines, line_limit=48):
    while lines:
        print('\n'.join(lines[:line_limit]))
        lines = lines[line_limit:]
        if lines and input("More? ") not in ['Y', 'y']:
            break

''' update, append, or remove items in a list
'''
def update_list(lst, new_item_func, item_name="item"):
    if lst == []:
        print("Current content is empty.")
    else:
        print("Current content: ")
        for i in range(len(lst)):
            print("#"+str(i+1)+":", lst[i])

    print("A valid update instruction is an operator" + \
          "(a/d/r, append/delete/replace) with an optional index.")
    print(("For example, 'a' -- append {0}, 'd1' -- delete {0} #1," + \
           "'r2' -- replace {0} #2.").format(item_name))
    print("If index is not specified for d/r, the last {0} will be the target."\
          .format(item_name))
    prompt = "Input your update instruction (<Enter> to finish): "
    action = input(prompt)
    while action != "":
        try:
            op = action[0].lower()
            if op not in 'adr':
                raise ValueError("Unrecognized update operation")
            if len(action) > 1:
                idx = int(action[1:]) - 1
                if idx < 0 or idx >= len(lst):
                    raise IndexError("Index out of range")
            else:
                idx = -1
            if op == 'a' or op == 'r':
                new_item = new_item_func()
                if new_item == '':
                    raise ValueError("No {0} provided.".format(item_name))
                if op == 'a':
                    lst.append(new_item)
                else:
                    lst[idx] = new_item
            else:
                del lst[idx]
        except (ValueError, IndexError) as e:
            print("Invalid update operation:", e, end='.\n')
            return 1
        action = input(prompt)
    return 0

