'''coba keranjang'''

import pandas as pd
from main import input_jenis, katalog

def keranjang_transaski(username):
    '''keranjang'''
    kolom = ["username", "jenis", "nama", "jumlah", "harga", "total"]
    keranjang = pd.read_csv("riwayat_transaksi.csv")
    while True:
        jenis = input_jenis("Keranjang")
        katalog("Keranjang", jenis)

        df = pd.read_csv("data_produk.csv")
        df = df[df["jenis"] == jenis]
        print(len(df))
        input("ENTER")
        while True:
            try:
                nomor = int(input("Masukkan nomor produk: "))
                if nomor < 1 or nomor > len(df):
                    print(f"Pilih angka 1 sampai {len(df)}")
                    input("Tekan enter untuk mengulang")
                    continue
                index_produk = df.index[nomor-1]

                nama = df.loc[index_produk, "nama"]
                satuan = df.loc[index_produk, "satuan"]
                harga = df.loc[index_produk, "harga"]
                stok = df.loc[index_produk, "stok"]

                jumlah = int(input(f"Berapa {satuan} {nama} yang ingin di beli: "))
                if jumlah < 1 or jumlah > stok:
                    print("jumlah tidak valid atau stok tidak mencukupi")
                    opsi = input("Tekan enter untuk mengulang atau 0 untuk kembali> ")
                    if opsi == "0":
                        break
                    continue

                total = harga * jumlah

                input("enter")
                break
            except: # pylint:disable=bare-except
                print("Inputan tidak sesuai.")
                opsi = input("Tekan enter untuk mengulang atau 0 untuk kembali> ")
                if opsi == "0":
                    return
                continue
        
        data = [[username, jenis, nama, jumlah, harga, total]]
        data_keranjang = pd.DataFrame(data, columns=kolom)

        keranjang = pd.concat([keranjang, data_keranjang], ignore_index=True)
        keranjang.to_csv("riwayat_transaksi.csv", index=False)


keranjang_transaski("User")
