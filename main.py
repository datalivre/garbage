# _*_ coding:utf-8 _*_
# ----------------------------------------- #
# @author Robert Carlos                     #
# email robert.carlos@linuxmail.org         #
# 2020-Mar (CC BY 3.0 BR)                   #

import argparse
import errno
import logging
import socket
from datetime import date, datetime, timedelta
from getpass import getpass
from os import path
from sys import exit

from paramiko import AuthenticationException, AutoAddPolicy, SSHClient

from packs.list_args import get_args
from packs.list_hosts import get_host


def garbage(func_get_host, properties):

    try:
        client = SSHClient()
        client.set_missing_host_key_policy(AutoAddPolicy())
        client.load_system_host_keys()

        dict_hosts = func_get_host(properties['list_hosts'])

        for host, destiny in dict_hosts.items():
            file_name = datetime.today() - \
                timedelta(days=int(properties['expurgo']))
            destiny_file_name = path.join(destiny, str(
                file_name.strftime('%d-%m-%Y') + '+.zip'))

            command_list = [
                f'find {properties["origem"]} -type f \\( -iname {" -o -iname ".join(properties["file_type"].split())} \\) 2>/dev/null -exec zip -m {destiny_file_name} {{}} +',
                f'find {destiny} -type f -iname "*+.zip" -mtime +{properties["expurgo"]} 2>/dev/null -exec rm -f {{}} +"']
            try:
                logging.info(str(f'Estabelecendo conexão com {host.upper()}'))
                client.connect(
                    host, properties['port'], properties['username'], getpass())
            except IOError as e:
                logging.error(str(f'Erro: IOError {host.upper()}. {e}'))
                continue
            except AuthenticationException as e:
                logging.error(f'Erro de autenticação {host.upper()}. {e}')
                continue
            except Exception as e:
                logging.error(f'Error inesperado. {e}')
                continue
            for sublist in command_list:
                try:
                    stdin, stdout, stderr = client.exec_command(
                        sublist, timeout=2.0)
                    if stdout:
                        for line in stdout:
                            logging.info(
                                f"Arquivo {line.split('/')[-1].strip()} >> {destiny}")
                    if stdin or stderr:
                        logging.warning("Não foi possível realizar a operação")
                except socket.timeout as e:
                    logging.error(f'Erro ao executar comando. {e}')
                    continue
                except Exception as e:
                    logging.error(f'Erro inesperado. {e}')
                    continue
        client.close()
    finally:
        if client:
            client.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="""Script que mediante a sua execução, move e compacta arquivos expecíficos 
        de um diretório de origem para um diretório de destino, para que, dentro de um prazo 
        pré determinado sejam expurgados.""")
    parser.add_argument('-P', action='store', dest='properties_file',
                        default='confiles/garbage.properties',
                        required=False, help='Caminho para o arquivo de propriedades.')

    log = logging.getLogger(__name__)
    arguments = parser.parse_args()
    properties = get_args(arguments.properties_file)

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s: %(message)s',
                        datefmt='%d/%m/%Y %I:%M:%S %p',
                        filename=properties['logfile'], level=logging.INFO)

    if path.isfile(properties['list_hosts']):
        try:
            garbage(get_host, properties)
        except KeyboardInterrupt:
            print('Bye!')
            exit(errno.EPERM)
    else:
        print(f"O {properties['list_hosts']} não existe.")
        exit(errno.EPERM)
