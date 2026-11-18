import os
import sys


def clean_screen():
    if sys.stdout.isatty():
        os.system("cls" if os.name == "nt" else "clear")


def pause_and_clean():
    input("\nPresione Enter para continuar...")
    clean_screen()