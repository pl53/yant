import subprocess
import sys

pwd = subprocess.checkout_output(['pwd']
subprocess.call(['mkdir', 'devo'])
# set data dir
subprocess.call(['export', 'YANT_PATH=' + sys.path.join(pwd, 'devo')])

# clean up existing books
subprocess.call(['cd', '$YANT_PATH'])
subprocess.call(['rm', '*'])

subprocess.call(['yant', 'create', '-b', 'whereIs', '--desc', \
                 'A notebook for finding my personal belongings'])
subprocess.call


