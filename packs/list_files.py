# _*_ coding:utf-8 _*_
# 2020-Mar (CC BY 3.0 BR)                   #
# ----------------------------------------- #
# Contate o @author, Robert Carlos, para    #
# solicitar alterações                      #
# email robert.carlos@linuxmail.org         #

from datetime import datetime
from glob import glob
from os import path

# data de hoje
today = datetime.today()

files = glob('/tmp/*')

# organiza a lista por tempo
files.sort(key=path.getmtime)

# verifica arquivos por data

for file_ in files:
    file_date = datetime.fromtimestamp(path.getmtime(file_))
    if file_date.day > 5:
        print(f'mover {file_} para QUARENTENA')
    else:
        print(f'manter {file_}')


def list_files(indir, dirout, time_expurgo):
    file_list = []
    files = glob(indir)
    for file_ in files:
        file_date = datetime.fromtimestamp(path.getmtime(file_))
        if file_date.day > 30:
            print('mover')
        else:
            print('não mover')