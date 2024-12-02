'''transaksi'''

import os
import pandas as pd
from tabulate import tabulate

def header(judul=None):
    '''tampilan header'''
    # clear terminal
    os.system("cls")

    # header
    width = 100
    print("=" * width)
    print("FarmOn".center(width))
    print("=" * width)
    if judul is not None:
        print(judul.center(width))
    print("-" * width)

def input_jenis(nama_header):
    '''Menentukan jenis'''
    while True:
        header(nama_header)
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
        return jenis

def lihat_produk(jenis):
    '''daftar produk'''
    df = pd.read_csv("data_produk.csv")
    df = df[df["jenis"] == jenis]
    df = df.reset_index(drop=True)

    data = []
    for i in range(len(df)):
        no = i + 1
        nama = str(df.loc[i, "nama"]).title()
        satuan = df.loc[i, "satuan"]
        harga = df.loc[i, "harga"]
        stok = df.loc[i, "stok"]
        data.append([no, nama, satuan, f'Rp{harga}', stok])

    tabel = tabulate(data, headers=["No.", "Nama", "Satuan", "Harga per Satuan", "Stok"],
                     tablefmt='fancy_grid', numalign='left')
    panjang_tabel = max(len(baris) for baris in tabel.splitlines())
    print(jenis.upper().center(panjang_tabel))
    print(tabel)

def katalog(nama_header, jenis):
    '''Katalog Produk'''
    header(nama_header)
    lihat_produk(jenis)

def keranjang(username): # pylint:disable=redefined-outer-name
    '''Keranjang'''
    kolom_keranjang = ["username", "jenis", "nama", "jumlah", "harga", "total"]
    data_keranjang = []
    total_harga = 0

    while True:
        jenis = input_jenis("Keranjang")

        try:
            df_produk = pd.read_csv("data_produk.csv")
        except FileNotFoundError:
            df_produk = pd.DataFrame(columns=kolom_keranjang)

        df_produk = df_produk[df_produk["jenis"] == jenis].reset_index(drop=True)

        while True:
            katalog("Keranjang", jenis)

            try:
                nomor_produk = int(input("Masukkan nomor produk yang ingin ditambahkan di keranjang: ")) #pylint:disable=line-too-long
                if nomor_produk < 1 or nomor_produk > len(df_produk):
                    print(f"Pilih nomor produk antara 1 dan {len(df_produk)}.")
                    input("Tekan enter untuk mengulang")
                    continue

                index_produk = df_produk.index[nomor_produk - 1]
                nama = df_produk.loc[index_produk, 'nama']
                satuan = df_produk.loc[index_produk, "satuan"]
                harga = df_produk.loc[index_produk, "harga"]
                stok = df_produk.loc[index_produk, "stok"]

                jumlah = int(input(f'berapa {satuan} {nama} yang ingin Anda beli: '))
                if jumlah < 1 or jumlah > stok:
                    print("Jumlah tidak valid atau stok tidak mencukupi")
                    input("Tekan enter untuk mengulang")
                    continue

                total = harga * jumlah
                total_harga += total

                opsi = input("Tekan enter untuk menambahkan ke keranjang atau ketik '0' untuk membatalkan keranjang: ") #pylint:disable=line-too-long
                if opsi == "0":
                    print(f"\n{nama} sebanyak {jumlah} {satuan} batal dimasukkan ke keranjang.")
                    break

                data_keranjang.append([username, jenis, nama, jumlah, harga, total])
                print(f"\n{nama} sebanyak {jumlah} {satuan} berhasil ditambahkan ke keranjang!")

                break

            except ValueError:
                print("Inputan tidak sesuai.")
                continue

        opsi = input("\nTekan enter untuk menambahkan barang lain atau ketik 'n' untuk selesai: ").lower() #pylint:disable=line-too-long
        if opsi == 'n':
            while True:
                checkout = input("Apakah anda ingin melanjutkan transaksi? (y/n) ")
                if checkout == "y":
                    return data_keranjang, total_harga
                elif checkout == "n":
                    return [], 0
                else:
                    print("Inputan salah. Ketik 'y' untuk melanjutkan atau 'n' jika tidak.")

def tentukan_ongkir():
    '''menentukan harga ongkir'''
    while True:
        header("Ongkos Kirim")
        print("Pilih jarak pengiriman: ")
        print("1. Jarak <2 km")
        print("2. Jarak 2 km - 7km")
        print("3. Jarak 7 km - 15 km")
        print("4. Jarak 15 km - 20 km")

        try:
            pilihan_ongkir = int(input("Masukkan pilihan ongkir (1/2/3/4): "))
            if pilihan_ongkir == 1:
                ongkir = 3000
            elif pilihan_ongkir == 2:
                ongkir = 6000
            elif pilihan_ongkir == 3:
                ongkir = 11000
            elif pilihan_ongkir == 4:
                ongkir = 15000
            else:
                print("Masukkan angka 1, 2, 3, atau 4")
                input("Tekan enter untuk mengulang")
                continue
            break
        except ValueError:
            print("Input harus berupa angka. Silahkan coba lagi")
            input("Tekan enter untuk mengulang")

    print(f"\nBiaya ongkos kirim adalah {ongkir}")

    return ongkir

def cetak_nota(username, data_keranjang, total_harga, harga_ongkir, pembayaran): # pylint:disable=redefined-outer-name
    '''Nota'''
    header("Nota Pembayaran")
    print(f"Nama Pembeli: {username}\n")

    nota = []

    for item in data_keranjang:
        nama = item[3]
        jumlah = item[4]
        harga = item[5]
        total = item[6]
        nota.append([nama, jumlah, f"Rp{harga}", f"Rp{total}"])

    tabel = tabulate(nota, headers=["Nama", "Jumlah", "Harga", "Total"], tablefmt="rounded_grid")
    print(tabel)

    print(f"\nTotal: Rp{total_harga}")
    print(f"Ongkir: Rp{harga_ongkir}")
    total_harga_akhir = total_harga + harga_ongkir
    print(f"Total akhir: Rp{total_harga_akhir}")

    if pembayaran >= total_harga_akhir:
        change = pembayaran - total_harga_akhir
        print(f"Uang yang dibayarkan: Rp{pembayaran}")
        print(f"Kembalian: Rp{change}")
    else:
        print("Uang yang dibayarkan tidak cukup.")

def simpan_transaksi(data_keranjang):
    '''Simpan Transaksi ke Riwayat'''
    nama_kolom = ["no", "username", "jenis", "nama", "jumlah", "harga", "total"]

    if os.path.exists("riwayat_transaksi.csv"):
        df_transaksi = pd.read_csv("riwayat_transaksi.csv")
    else:
        df_transaksi = pd.DataFrame(columns=nama_kolom)

    if not df_transaksi.empty:
        no = df_transaksi.iloc[-1,0] + 1
    else:
        no = 1

    for i in data_keranjang:
        i.insert(0,no)

    df_baru = pd.DataFrame(data_keranjang, columns=nama_kolom)
    df_transaksi = pd.concat([df_transaksi, df_baru], ignore_index=True)
    df_transaksi.to_csv("riwayat_transaksi.csv", index=False)

    # Kurangi stok
    data_produk = pd.read_csv("data_produk.csv")
    for item in data_keranjang:
        nama = item[3]
        jumlah = item[4]
        index_produk = data_produk[data_produk["nama"] == nama].index[0]
        stok_baru = data_produk.loc[index_produk, "stok"] - jumlah
        data_produk.at[index_produk, "stok"] = stok_baru

    data_produk.to_csv("data_produk.csv", index=False)



def pembelian(username): # pylint:disable=redefined-outer-name
    '''Alur Pembelian'''
    data_keranjang, total_harga = keranjang(username)

    if not data_keranjang:
        print("\nKeranjang kosong. Transaksi dibatalkan.")
        return

    ongkir = tentukan_ongkir()
    total_akhir = total_harga + ongkir
    while True:
        konfirmasi = input("\nApakah Anda yakin ingin menyelesaikan transaksi? (y/n): ").lower()
        if konfirmasi == 'y':
            while True:
                header("Pembayaran")
                try:
                    pembayaran = int(input(f"Total biaya adalah Rp{total_akhir}. Masukkan jumlah uang yang akan dibayar: Rp")) # pylint:disable=line-too-long
                    if pembayaran < total_akhir:
                        print("Uang yang dibayarkan tidak cukup.")
                        input("Tekan enter untuk coba lagi")
                        continue
                    break
                except ValueError:
                    print("Input tidak valid. Harap masukkan angka yang benar.")

            # Simpan transaksi
            simpan_transaksi(data_keranjang)

            # Cetak nota
            print("Pembayaran berhasil.")
            input("Tekan enter untuk melihat nota transaksi anda")
            cetak_nota(username, data_keranjang, total_harga, ongkir, pembayaran)
            print("\nTransaksi berhasil.")
            input("Tekan enter untuk melanjutkan")
            break
        elif konfirmasi == "n":
            print("\nTransaksi dibatalkan.")
            input("Tekan enter untuk kembali")
            break
        else:
            print("Ketik 'y' untuk ya atau 'n' untuk tidak")
            continue
