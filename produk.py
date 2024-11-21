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

def tambah_produk_baru(jenis, nama, satuan, harga, stok):
    '''tambah produk'''
    df = pd.read_csv("data_produk.csv")

    if (jenis in df["jenis"].values) and (nama in df["nama"].values):
        print("produk sudah ada")
    else:
        data = {
            "jenis" : [jenis],
            "nama" : [nama],
            "satuan" : [satuan],
            "harga" : [harga],
            "stok" : [stok]
        }
        produk_baru = pd.DataFrame(data)
        df = pd.concat([df, produk_baru], ignore_index=True)
        df = df.sort_values(by=["jenis", "nama"])
        df.to_csv("data_produk.csv", index=False)
        print("Berhasil ditambahkan")

def hapus_produk(jenis, nama):
    '''hapus produk'''
    df = pd.read_csv("data_produk.csv")

    if (jenis in df["jenis"].values) and (nama in df["nama"].values):
        index_produk = df[(df["jenis"] == jenis) & (df["nama"] == nama)].index
        df.drop(index=index_produk, inplace=True)
        df.to_csv("data_produk.csv", index=False)
        print("produk berhasil dihapus")
    else:
        print("produk tidak ada")

def edit_stok(operasi):
    '''Tambah stok'''
    while True:

        jenis = input("jenis")
        nama = input("nama")

        df = pd.read_csv("data_produk.csv")

        if (jenis in df["jenis"].values) and (nama in df["nama"].values):
            baris_produk = df[(df["jenis"] == jenis) & (df["nama"] == nama)]
            index_baris_produk = baris_produk.index[0]
            stok_lama = baris_produk.loc[index_baris_produk, "stok"]
            satuan = baris_produk.loc[index_baris_produk, "satuan"]
            nama = baris_produk.loc[index_baris_produk, "nama"]

            print("-"*20)

            if operasi == "+":
                print(f"Stok saat ini: {stok_lama} {satuan}")
                tambah = int(input(f"Berapa {satuan} {nama} yang akan ditambahkan: "))
                stok_baru = stok_lama + tambah
                df.loc[index_baris_produk, "stok"] = [stok_baru]
            elif operasi == "-":
                print(f"Stok saat ini: {stok_lama} {satuan}")
                kurang = int(input(f"Berapa {satuan} {nama} yang akan dikurangi: "))
                stok_baru = stok_lama - kurang
                df.loc[index_baris_produk, "stok"] = [stok_baru]

            df.to_csv("data_produk.csv", index=False)
            break
        else:
            print("Produk tidak ada")
            input("Tolong masukkan nama dengan benar")

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

tambah_produk_baru("buah", "jeruk", "buah", 1, 100)
