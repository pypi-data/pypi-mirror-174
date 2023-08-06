# Insert your code here.
#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
    In order to solve the problem of python's permission to modify file, the _replace function is separated into this script, and then called in core.py.
"""



import os
import click

GATEWAY_FILE_PATH = "/etc/network/interfaces"


def _replace():
    a, b = "192.168.137.100", "192.168.137.1"
    with open(GATEWAY_FILE_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()
    with open(GATEWAY_FILE_PATH, "w", encoding="utf-8") as f_w:
        for line in lines:
            if "gateway" in line:
                if a in line:
                    pass
                else:
                    a, b = b, a
                line = line.replace(a, b)

            f_w.write(line)
    click.secho("Network restarting".format(a, b),fg='red')
    os.system("systemctl restart networking")
    click.secho("Gateway has changed from {} to {}".format(a, b),fg='green')
    
if __name__ == '__main__':
    _replace()