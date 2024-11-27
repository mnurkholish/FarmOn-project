'''coba keranjang'''

import pandas as pd
from main import input_jenis, katalog

def keranjang_transaski(username):
    '''keranjang'''
    kolom = ["no", "username", "jenis", "nama", "jumlah", "harga", "total"]
    keranjang = pd.read_csv("riwayat_transaksi.csv")
    if keranjang.empty:
        no = 1
    else:
        no = (keranjang.iloc[-1,0]) + 1
    total_harga = 0
    while True:
        jenis = input_jenis("Keranjang")
        katalog("Keranjang", jenis)

        df = pd.read_csv("data_produk.csv")
        df_jenis = df[df["jenis"] == jenis].reset_index()
        while True:
            try:
                nomor = int(input("Masukkan nomor produk: "))
                if nomor < 1 or nomor > len(df):
                    print(f"Pilih angka 1 sampai {len(df)}")
                    input("Tekan enter untuk mengulang")
                    continue
                index_produk = df.index[nomor-1]

                nama = df_jenis.loc[index_produk, "nama"]
                satuan = df_jenis.loc[index_produk, "satuan"]
                harga = df_jenis.loc[index_produk, "harga"]
                stok = df_jenis.loc[index_produk, "stok"]

                jumlah = int(input(f"Berapa {satuan} {nama} yang ingin di beli: "))
                if jumlah < 1 or jumlah > stok:
                    print("jumlah tidak valid atau stok tidak mencukupi")
                    opsi = input("Tekan enter untuk mengulang atau 0 untuk kembali> ")
                    if opsi == "0":
                        return
                    continue

                baris_produk = df[(df["jenis"] == jenis) & (df["nama"] == nama)]
                index_baris = baris_produk.index[0]
                stok_baru = stok - jumlah
                df.at[index_baris, "stok"] = stok_baru
                df.to_csv("data_produk.csv", index=False)

                total = harga * jumlah
                total_harga += total

                opsi = input("Tekan enter untuk menambahkan ke keranjang atau 0 untuk ")

                break

            except: # pylint:disable=bare-except
                print("Inputan tidak sesuai.")
                opsi = input("Tekan enter untuk mengulang atau 0 untuk kembali> ")
                if opsi == "0":
                    return
                continue

        data = [[no, username, jenis, nama, jumlah, harga, total]]
        data_keranjang = pd.DataFrame(data, columns=kolom)

        keranjang = pd.concat([keranjang, data_keranjang], ignore_index=True)
        keranjang.to_csv("riwayat_transaksi.csv", index=False)

        opsi = input("Tekan enter jika ingin menambahkan barang ke keranjang lagi atau ketik 'n' jika tidak").lower() #pylint:disable=line-too-long
        if opsi == "n":
            break

# keranjang_transaski("User")
