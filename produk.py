"""percobaan fitur produk"""

import pandas as pd
from main import header

def lihat_produk(jenis):
    '''daftar produk'''
    header("Daftar Produk")

    df = pd.read_csv("data_produk.csv")
    df = df[df["jenis"] == jenis]
    df = df.reset_index()
    df.drop(columns="index", inplace=True)

    print(jenis.upper().center(71))
    print("+" + "-"*5 + "+" + "-"*20 + "+" + "-"*10 + "+" + "-"*20 + "+" + "-"*10 + "+")
    print(f"| {"No":>2}. | {"Nama":^18} | {"Satuan":^8} | {"Harga per Satuan":^18} | {"Stok":^8} |")
    print("+" + "-"*5 + "+" + "-"*20 + "+" + "-"*10 + "+" + "-"*20 + "+" + "-"*10 + "+")
    for i in range(len(df)):
        no = i+1
        nama = df.loc[i,"nama"]
        satuan = df.loc[i,"satuan"]
        harga = df.loc[i,"harga"]
        stok = df.loc[i, "stok"]
        print(f"| {no:>2}. | {nama:<18} | {satuan:<8} | Rp{harga:<16} | {stok:<8} |")
    print("+" + "-"*5 + "+" + "-"*20 + "+" + "-"*10 + "+" + "-"*20 + "+" + "-"*10 + "+")

def tambah_produk():
    '''tambah produk'''
    while True:
        header("Tambah Produk")
        print("Pilih jenis hasil pertanian:")
        print("1. Buah\n2. Rempah\n3. Sayuran\n4. Serealia")
        opsi_jenis = input("Masukkan pilihan sesuai angka (1/2/3/4)> ")
        if opsi_jenis == "1":
            jenis = "buah"
        elif opsi_jenis == "2":
            jenis = "rempah"
        elif opsi_jenis == "3":
            jenis = "sayuran"
        elif opsi_jenis == "4":
            jenis = "serealia"
        else:
            print("Inputan tidak valid.")
            input("Tekan enter untuk mengulangi")
            continue

        header("Tambah Produk")
        lihat_produk(jenis)
        df = pd.read_csv("data_produk.csv")

        while True:
            header("Tambah Produk")
            try:
                nama = input("Masukkan nama hasil pertanian: ")
                satuan = input("Tentukan satuan yang digunakan (kg/ikat/buah): ")
                harga = int(input(f"Tentukan harga per-{satuan}: "))
                stok = int(input(f"Berapa {satuan} stok yang akan dimasukkan: "))
            except Exception as error:
                print("Inputan tidak sesuai.", error)
                input("Tekan enter untuk mengulangi")
                continue
            break

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
            input("Tekan enter untuk melanjutkan")

def hapus_produk(jenis, nama):
    '''hapus produk'''
    lihat_produk(jenis)
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
            lihat_produk(jenis)

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
