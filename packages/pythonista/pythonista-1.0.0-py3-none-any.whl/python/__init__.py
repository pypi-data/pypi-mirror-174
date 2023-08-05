from sys import argv
from os import system

def cli():
    if len(argv) > 1:
        system(f"python3 {' '.join(argv[1:])}")
    else:
        system("python3")
