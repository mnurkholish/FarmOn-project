"""Program Utama"""

import os
import csv
import pandas as pd
from tabulate import tabulate

# =========================Fungsi Umum=========================

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

def intro():
    '''tampilan pertama aplikasi'''
    header()
    width = 100
    print("\n\n" + "Selamat Datang di aplikasi FarmOn".center(width))
    print("Tekan enter untuk memulai aplikasi".center(width) + "\n\n")
    print("-"*width + "\n" + "=" * width)
    input()

def outro():
    """Tampilan penutup aplikasi"""
    header()
    width = 100
    print("\n\n" + "Terima Kasih Telah Menggunakan Aplikasi FarmOn :)".center(width))
    print("Tekan enter untuk menutup aplikasi".center(width) + "\n\n")
    print("-"*width + "\n" + "=" * width)
    input()

# =========================Fungsi Main Menu=========================

# ===Login===

def login():
    '''Login'''
    while True:
        header("Login")

        username = input("Username: ").strip()
        password = input("Password: ").strip()

        df = pd.read_csv("akun_pengguna.csv")

        ambil_role = df[(df["username"] == username) & (df["password"] == password)]

        if ambil_role.empty:
            role = None
            print("Login gagal, pilih opsi Registrasi untuk membuat akun.")
            input("Tekan enter untuk kembali")
        else:
            role = ambil_role.iloc[0]['role']
            print(f"Login berhasil\nSelamat datang {username}.")
            input("Tekan enter untuk melanjutkan")

        return username, role

# ===Registrasi===

def registrasi():
    '''registrasi'''
    while True:
        header("Registrasi")

        username = input("username: ").strip()
        password = input("password: ").strip()
        role = "user"

        # validasi username harus ada
        if not username:
            print("Username tidak boleh kosong")
            opsi = input("Tekan enter untuk mengulang atau 0 untuk kembali> ")
            if opsi == "0":
                return
            continue
        # validasi password harus ada
        if not password:
            print("Password tidak boleh kosong")
            opsi = input("Tekan enter untuk mengulang atau 0 untuk kembali> ")
            if opsi == "0":
                return
            continue
        # validasi password harus berupa huruf dan angka
        if password:
            huruf = False
            angka = False
            for karakter in password:
                if karakter.isalpha():
                    huruf = True
                if karakter.isnumeric():
                    angka = True

            if not (huruf and angka):
                print("Password harus berupa huruf dan angka")
                opsi = input("Tekan enter untuk mengulang atau 0 untuk kembali> ")
                if opsi == "0":
                    return
                continue

        data_akun = "akun_pengguna.csv"
        df = pd.read_csv(data_akun)

        # validasi username harus berbeda dari yang sudah ada
        if username in df["username"].values:
            print("username sudah ada, buatlah username yang berbeda")
            opsi = input("tekan enter untuk mengulang atau 0 untuk kembali> ")
            if opsi == "0":
                return
            continue

        # jika syarat terpenuhi, membuat data baru
        user_baru = pd.DataFrame([[username, password, role]], columns=["username", "password", "role"])

        # mengupdate data
        df = pd.concat([df, user_baru], ignore_index=True)
        df.to_csv(data_akun, index=False)

        print("Akun berhasil dibuat. Silahkan login ulang!")
        input("Tekan enter untuk melanjutkan")
        break

# =========================Fungsi Admin=========================

# ===Gudang===

# Penentuan jenis (fungsi umum)
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

# Lihat produk/katalog (fungsi umum)
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

# Tambah produk
def tambah_produk():
    '''tambah produk'''
    jenis = input_jenis("Tambah Produk")

    while True:
        katalog("Tambah Produk", jenis)
        try:
            nama = input("Masukkan nama hasil pertanian: ").strip().lower()
            satuan = input("Tentukan satuan yang digunakan (kg/ikat/buah): ").strip().lower()
            harga = int(input(f"Tentukan harga per-{satuan}: ").strip())
            stok = int(input(f"Berapa {satuan} stok yang akan dimasukkan: ").strip())
        except:
            print("Inputan tidak sesuai.")
            opsi = input("Tekan enter untuk mengulang atau 0 untuk kembali> ")
            if opsi == "0":
                return
            continue
        break

    df = pd.read_csv("data_produk.csv")
    if (jenis in df["jenis"].values) and (nama in df["nama"].values):
        print("produk sudah ada")
        input("Tekan enter untuk kembali ke gudang")
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

        print("\nKatalog terbaru")
        lihat_produk(jenis)
        print("Berhasil ditambahkan!")
        input("Tekan enter untuk kembali")

# Hapus produk
def hapus_produk():
    '''hapus produk'''
    jenis = input_jenis("Hapus Produk")

    while True:
        katalog("Hapus Produk", jenis)
        nama = input("Masukkan nama produk: ").strip().lower()
        df = pd.read_csv("data_produk.csv")

        if (jenis in df["jenis"].values) and (nama in df["nama"].values):
            index_produk = df[(df["jenis"] == jenis) & (df["nama"] == nama)].index
            df.drop(index=index_produk, inplace=True)
            df.to_csv("data_produk.csv", index=False)
            print("\nKatalog Terbaru")
            lihat_produk(jenis)
            print("produk berhasil dihapus!")
            input("Tekan enter untuk kembali")
        else:
            print("produk tidak ada")
            opsi = input("Tekan enter untuk mengulang atau 0 untuk kembali> ")
            if opsi == "0":
                return
            continue
        break

# Edit stok (Menambah atau mengurangi)
def edit_stok(operasi):
    '''Edit Stok'''
    jenis = input_jenis("Edit Stok")

    while True:
        katalog("Edit Stok", jenis)
        nama = input("Masukkan nama produk yang akan diedit: ").strip().lower()

        df = pd.read_csv("data_produk.csv")

        if (jenis in df["jenis"].values) and (nama in df["nama"].values):

            baris_produk = df[(df["jenis"] == jenis) & (df["nama"] == nama)]
            if nama in baris_produk["nama"].values:
                index_baris_produk = baris_produk.index[0]
                stok_lama = baris_produk.loc[index_baris_produk, "stok"]
                satuan = baris_produk.loc[index_baris_produk, "satuan"]
                nama = baris_produk.loc[index_baris_produk, "nama"]
            else:
                print("Produk tidak ada, tolong masukkan nama dengan benar.")
                opsi = input("Tekan enter untuk mengulang atau 0 untuk kembali> ")
                if opsi == "0":
                    return
                continue

            try:
                if operasi == "+":
                    print(f"Stok saat ini: {stok_lama} {satuan}")
                    tambah = int(input(f"Berapa {satuan} {nama} yang akan ditambahkan: "))
                    stok_baru = stok_lama + tambah
                    df.loc[index_baris_produk, "stok"] = [stok_baru]
                elif operasi == "-":
                    print(f"Stok saat ini: {stok_lama} {satuan}")
                    while True:
                        kurang = int(input(f"Berapa {satuan} {nama} yang akan dikurangi: "))
                        if kurang > stok_lama:
                            print("Tidak bisa mengurangi lebih dari jumlah stok lama")
                            continue
                        break

                    stok_baru = stok_lama - kurang
                    df.loc[index_baris_produk, "stok"] = [stok_baru]
            except:
                print("Inputan tidak valid.")
                opsi = input("Tekan enter untuk mengulang atau 0 untuk kembali> ")
                if opsi == "0":
                    return
                continue

            df.to_csv("data_produk.csv", index=False)

            print("\nKatalog Terbaru")
            lihat_produk(jenis)
            print("Berhasil diedit!")
            input("Tekan enter untuk kembali")
        else:
            print("Produk tidak ada, tolong masukkan nama dengan benar.")
            opsi = input("Tekan enter untuk mengulang atau 0 untuk kembali> ")
            if opsi == "0":
                return
            continue
        break

# Edit harga
def edit_harga():
    '''Edit Harga'''
    jenis = input_jenis("Edit Harga")

    while True:
        katalog("Edit Harga", jenis)
        nama = input("Masukkan nama produk: ").strip().lower()

        df = pd.read_csv("data_produk.csv")

        baris_produk = df[(df["jenis"] == jenis) & (df["nama"] == nama)]

        try:
            if (jenis in df["jenis"].values) and (nama in df["nama"].values):
                harga_baru = int(input("Masukkan harga baru: "))
                index = baris_produk.index[0]
                df.at[index, 'harga'] = harga_baru
                df.to_csv("data_produk.csv", index=False)

                print("\nKatalog Terbaru")
                lihat_produk(jenis)
                print("Berhasil diedit!")
                input("Tekan enter untuk kembali")
            else:
                print("Produk tidak ada, tolong masukkan nama dengan benar.")
                opsi = input("Tekan enter untuk mengulang atau 0 untuk kembali> ")
                if opsi == "0":
                    return
                continue
        except:
            print("Inputan tidak valid.")
            opsi = input("Tekan enter untuk mengulang atau 0 untuk kembali> ")
            if opsi == "0":
                return
            continue

        break

# ===Riwayat Transaksi===

def riwayat_transaksi():
    """
    Membaca dan menampilkan data dari file riwayat_transaksi.csv
    """
    try:
        header("Riwayat Transaksi")

        # Membaca file CSV
        riwayat = pd.read_csv("riwayat_transaksi.csv")

        # Cek apakah file kosong
        if riwayat.empty:
            print("\nRiwayat transaksi kosong.")
            input("\nTekan enter untuk kembali")
            return

        # Menampilkan data riwayat transaksi
        print("\n=== Riwayat Transaksi ===")
        print(tabulate(riwayat, headers="keys", tablefmt="fancy_grid", showindex=False))

    except FileNotFoundError:
        print("File 'riwayat_transaksi.csv' tidak ditemukan.")
    except pd.errors.EmptyDataError:
        print("File 'riwayat_transaksi.csv' kosong.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

    input("Tekan enter untuk kembali")

# ===Riwayat Masukan===

def riwayat_masukan():
    """
    Fungsi untuk admin membaca semua masukan dari user
    """
    header("Riwayat Masukan")
    masukan_csv = "masukan.csv"

    # Coba membaca file CSV
    try:
        df = pd.read_csv(masukan_csv)
        if df.empty:
            print("Tidak ada masukan")
        else:
            print("\n=== Semua Masukan ===")
            print(tabulate(df, headers="keys", tablefmt="fancy_grid", maxcolwidths=[15,40], showindex=False))

    except FileNotFoundError:
        print("\nBelum ada masukan")

    input("Tekan enter untuk kembali")

# =========================Fungsi User=========================

# ===Lihat Katalog===

def katalog_user():
    '''Katalog User'''
    while True:
        jenis = input_jenis("Katalog")
        katalog("Katalog", jenis)
        opsi = input("Tekan enter untuk melihat jenis hasil pertanian lainnya atau '0' untuk kembali")
        if opsi == "0":
            break

# ===Pembelian===

def keranjang(username):
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
                nomor_produk = int(input("Masukkan nomor produk yang ingin ditambahkan di keranjang: "))
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

                opsi = input("Tekan enter untuk menambahkan ke keranjang atau ketik '0' untuk membatalkan keranjang: ")
                if opsi == "0":
                    print(f"\n{nama} sebanyak {jumlah} {satuan} batal dimasukkan ke keranjang.")
                    break

                data_keranjang.append([username, jenis, nama, jumlah, harga, total])
                print(f"\n{nama} sebanyak {jumlah} {satuan} berhasil ditambahkan ke keranjang!")

                break

            except ValueError:
                print("Inputan tidak sesuai.")
                continue

        opsi = input("\nTekan enter untuk menambahkan barang lain atau ketik 'n' untuk selesai: ").lower()
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

def cetak_nota(username, data_keranjang, total_harga, harga_ongkir, pembayaran):
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

    tabel = tabulate(nota, headers=["Nama", "Jumlah", "Harga", "Total"], tablefmt="fancy_grid")
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

def pembelian(username):
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
                    pembayaran = int(input(f"Total biaya adalah Rp{total_akhir}. Masukkan jumlah uang yang akan dibayar: Rp"))
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

# ===Masukan===

def masukan():
    """
    Fungsi untuk menambahkan masukan user ke masukan.csv
    """
    header("Masukan")

    kolom = ["Nama", "Saran"]
    masukan_csv = "masukan.csv"

    try:
        with open(masukan_csv, mode="r", newline='', encoding="utf-8") as file:
            reader = csv.DictReader(file)
            data = list(reader)
    except FileNotFoundError:
        data = []

    # Input dari user
    print("=== Masukan saran anda ===")
    nama = input("Nama anda: ").strip()
    saran = input("Tuliskan saran anda: ").strip()

    # Menambahkan masukan ke data
    new_row = {"Nama": nama, "Saran": saran}
    data.append(new_row)

    # Simpan ke CSV
    with open(masukan_csv, mode="w", newline='', encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=kolom)

        # Tulis header hanya jika file kosong
        if file.tell() == 0:
            writer.writeheader()
        writer.writerows(data)

    print("\nMasukan anda berhasil disimpan. Terima Kasih!\n")
    input("Tekan enter untuk kembali")

# =========================Navigasi=========================

def menu_admin():
    '''Menu Admin'''
    while True:
        header("Menu Admin")
        print("Pilih opsi:")
        print("1. Gudang\n2. Riwayat Transaksi\n3. Riwayat Masukan\n0. Logout")
        opsi = input("Masukkan pilihan opsi sesuai angka (1/2/3/0)> ")
        if opsi == "1":
            while True:
                header("Gudang")
                print("Pilih opsi:")
                print("1. Tambah produk\n2. Hapus Produk\n3. Edit Stok\n4. Edit Harga\n0. Kembali")
                opsi = input("Masukkan pilihan opsi sesuai angka (1/2/3/4/0)> ")
                if opsi == "1":
                    tambah_produk()
                elif opsi == "2":
                    hapus_produk()
                elif opsi == "3":
                    while True:
                        header("Edit Stok")
                        print("Pilih opsi:")
                        print("1. Tambah Stok\n2. Kurangi Stok\n0. Kembali")
                        opsi = input("Masukkan pilihan opsi sesuai angka (1/2/0)> ")
                        if opsi == "1":
                            edit_stok("+")
                        elif opsi == "2":
                            edit_stok("-")
                        elif opsi == "0":
                            break
                        else:
                            print("Opsi tidak valid. Silakan masukkan angka 1, 2, atau 0.")
                            input("Tekan enter untuk mengulang")
                elif opsi == "4":
                    edit_harga()
                elif opsi == "0":
                    break
                else:
                    print("Opsi tidak valid. Silakan masukkan angka 1, 2, 3, 4 atau 0.")
                    input("Tekan enter untuk mengulang")

        elif opsi == "2":
            riwayat_transaksi()
        elif opsi == "3":
            riwayat_masukan()
        elif opsi == "0":
            break

def menu_user(username):
    '''Menu User'''
    while True:
        header("Menu User")
        print("Pilih opsi:")
        print("1. Lihat Katalog\n2. Pembelian\n3. Masukan\n0. Kembali")
        opsi = input("Masukkan pilihan opsi sesuai angka (1/2/0)> ")
        if opsi == "1":
            katalog_user()
        elif opsi == "2":
            pembelian(username)
        elif opsi == "3":
            masukan()
        elif opsi == "0":
            break

# =========================Main Program=========================

def main():
    '''Main Menu'''
    intro()
    while True:
        header("Main Menu")
        print("Pilih opsi:")
        print("1. Login\n2. Registrasi\n0. Keluar")
        opsi = input("Masukkan pilihan opsi sesuai angka (1/2/0)> ")
        if opsi == "1":
            username, role = login()
            if role == "admin":
                menu_admin()
            elif role == "user":
                menu_user(username)
        elif opsi == "2":
            registrasi()
        elif opsi == "0":
            role = None
            outro()
            break
        else:
            print("Opsi tidak valid. Silakan masukkan angka 1, 2, atau 0.")
            input("Tekan enter untuk mengulang")

# ===START===

main()
