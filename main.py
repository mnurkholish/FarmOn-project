"""Program Utama"""

import os

def clear():
    '''memmbersihkan tampilan'''
    os.system("cls")

def header():
    '''tampilan header'''
    width = 100
    print("="*width)
    print("FarmOn".center(width))
    print("="*width)

def main():
    '''program utama'''
    clear()
    header()

main()
