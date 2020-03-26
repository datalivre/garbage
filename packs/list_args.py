# _*_ coding:utf-8 _*_
# ----------------------------------------- #
# @author Robert Carlos                     #
# email robert.carlos@linuxmail.org         #
# 2020-Mar (CC BY 3.0 BR)                   #

import errno
from os import path
from sys import exit


def get_args(filename):

        if path.isfile(filename):
            list_properties = [
                'username', 'port', 'expurgo', 'origem',
                'file_type', 'fs_destiny', 'logfile',
                'list_hosts', 'list_commands', 'password'
            ]
            dict_properties = {}
            try:
                with open(filename, 'r', encoding='utf8') as f:
                    for line in f:
                        for properties in list_properties:
                            if '#' not in line and len(line) > 2:
                                if properties in line.lower():
                                    dict_properties[properties] = line.split('=>')[
                                        1].strip()
                return dict_properties
            except IOError as e:
                print(f'Error ao tentar manipular {filename}\n{e}')
                exit(errno.EPERM)
        else:
            print(f'Arquivo {filename} não encontrado')
            exit(errno.EPERM)


if __name__ == "__main__":
    filename = "/home/oi412237/bob/garbage/confiles/garbage.properties"
    destiny_file_name = '/data5/dump_tmp/out.zip'
    properties = get_args(filename)
    print(f'find {properties["origem"]} -type f \\( -iname {" -o -iname ".join(properties["file_type"].split())} \\) 2>/dev/null -exec zip -m {destiny_file_name} {{}} +')
    #f'find {properties["origem"]} -type f -iname "{properties["file_type"]}" 2>/dev/null -exec zip -m {destiny_file_name} {{}} +',
