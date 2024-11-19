"""percobaan fitur produk"""

import os
import pandas as pd


def clear():
    '''memmbersihkan tampilan'''
    os.system("cls")

def header():
    '''tampilan header'''
    width = 100
    print("="*width)
    print("FarmOn".center(width))
    print("="*width)

def lihat_produk(jenis):
    '''daftar produk'''
    clear()
    header()

    df = pd.read_csv("data_produk.csv")
    df = df[df["jenis"] == jenis]
    df = df.reset_index()
    df.drop(columns="index", inplace=True)

    print("+---+" + "-"*19 + "+" + "-"*9 + "+" + "-"*18 + "+")
    print(f"|{"No":>2}.| {"Nama":<18}| {"Satuan":<8}| {"Harga per Satuan":<17}|")
    print("+---+" + "-"*19 + "+" + "-"*9 + "+" + "-"*18 + "+")
    for i in range(len(df)):
        nama = df.loc[i,"nama"]
        satuan = df.loc[i,"satuan"]
        harga = df.loc[i,"harga"]
        print(f"|{i+1:>2}.| {nama:<18}| {satuan:<8}| Rp{harga:<15}|")
    print("+---+" + "-"*19 + "+" + "-"*9 + "+" + "-"*18 + "+")

def main():
    '''run'''
    while True:
        clear()
        header()
        print("Daftar Jenis Hasil Tani\n>1 Buah\n>2 Sayuran\n>3 Serealia\n")
        opsi = input("Jenis hasil pertanian apa yang anda cari >")
        if opsi == "1":
            lihat_produk("buah")
            break
        elif opsi == "2":
            lihat_produk("sayuran")
            break
        elif opsi == "3":
            lihat_produk("serealia")
            break

main()
