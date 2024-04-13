import subprocess
from time import sleep


with open('targets.txt', 'r', encoding='utf-8') as f:
    for line in f:
        print(line, end="")
        line = line.replace('\n', '')
        output = subprocess.call([
            './enscan',
            '-n', line,
            '-is-merge',
            '-o', 'outs',
            '-json',
            #'-oip',
            #'-proxy', "http://127.0.0.1:8080",
        ])
        sleep(5)