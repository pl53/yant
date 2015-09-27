import subprocess
import sys

pwd = subprocess.checkout_output(['pwd']
subprocess.call(['mkdir', 'devo'])
subprocess.call(['export', 'YANT_PATH=' + sys.path.join(pwd, 'devo')])
subprocess.call(['rm', '-r', '$YANT_PATH'])
subprocess.call(['yant', 'create', '-b', 'whereIs', '--desc', \
                 'A notebook for finding my personal belongings"])
sub


