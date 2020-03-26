# _*_ coding:utf-8 _*_
# ----------------------------------------- #
# @author  Robert Carlos                    #
# email robert.carlos@linuxmail.org         #
# 2020-Mar (CC BY 3.0 BR)                   #

import errno
from os import path
from sys import exit


def get_host(file_name):

    if path.isfile(file_name):
        try:
            dict_hosts = {}
            list_unique = set()
            with open(file_name, 'r', encoding='utf8') as target:
                list_unique = {line.lower() for line in target if not line.startswith(
                    '#') if '=>' in line}
                for line in list_unique:
                    dict_hosts[line.split('=>')[0].strip()] = line.split('=>')[
                        1].strip()
            return dict_hosts
        except Exception:
            print(f'Error ao tentar manipular {file_name}.')
            exit(errno.EPERM)
    else:
        print(f'Arquivo {file_name} não foi encontrado.')
        exit(errno.EPERM)


if __name__ == "__main__":
    file_name = '/home/oi412237/bob/garbage/confiles/list_hosts.properties'
    dict_hosts = get_host(file_name)
    for host, directory in dict_hosts.items():
        print(host, directory)
