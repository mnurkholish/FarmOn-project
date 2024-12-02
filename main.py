"""Program Utama"""

import os
import pandas as pd
import csv
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
        user_baru = pd.DataFrame([[username, password, role]], columns=["username", "password", "role"]) #pylint:disable=line-too-long

        # mengupdate data
        df = pd.concat([df, user_baru], ignore_index=True)
        df.to_csv(data_akun, index=False)

        print("Akun berhasil dibuat. Silahkan login ulang!")
        input("Tekan enter untuk melanjutkan")
        break

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

# =========================Fungsi Admin=========================

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

def katalog(nama_header, jenis):
    '''Katalog Produk'''
    header(nama_header)
    lihat_produk(jenis)

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
        except: # pylint:disable=bare-except
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
            except: # pylint:disable=bare-except
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
        except: # pylint:disable=bare-except
            print("Inputan tidak valid.")
            opsi = input("Tekan enter untuk mengulang atau 0 untuk kembali> ")
            if opsi == "0":
                return
            continue

        break
    
def keranjang(username, jenis):
    """
    Fungsi untuk menambahkan barang ke keranjang.
    Data barang diambil dari file data_produk.csv.
    """
    try:
        kolom_keranjang = ["username", "jenis", "nama", "jumlah", "harga", "total"]
        
        # Memuat file keranjang jika sudah ada, atau membuat baru
        try:
            keranjang_df = pd.read_csv("keranjang.csv")
        except FileNotFoundError:
            keranjang_df = pd.DataFrame(columns=kolom_keranjang)
        
        total_harga = 0

        while True:
            # jenis = input("Masukkan jenis produk yang ingin Anda lihat (contoh: Makanan, Minuman): ").strip()
            katalog("Keranjang", jenis)  # Menampilkan katalog barang berdasarkan jenis
            
            df_produk = pd.read_csv("data_produk.csv")
            df_produk = df_produk[df_produk["jenis"] == jenis].reset_index()
            
            try:
                nomor_produk = int(input("Masukkan nomor produk yang ingin ditambahkan ke keranjang: "))
                if nomor_produk < 1 or nomor_produk > len(df_produk):
                    print(f"Pilih nomor produk antara 1 dan {len(df_produk)}.")
                    continue
                
                # Mengambil informasi produk yang dipilih
                index_produk = nomor_produk - 1
                nama = df_produk.loc[index_produk, "nama"]
                satuan = df_produk.loc[index_produk, "satuan"]
                harga = df_produk.loc[index_produk, "harga"]
                stok = df_produk.loc[index_produk, "stok"]
                
                jumlah = int(input(f"Berapa {satuan} {nama} yang ingin Anda beli? "))
                if jumlah < 1 or jumlah > stok:
                    print("Jumlah tidak valid atau stok tidak mencukupi.")
                    continue
                
                # Menambahkan barang ke keranjang
                total = harga * jumlah
                total_harga += total
                # Membuat DataFrame baru untuk baris tambahan
                data_keranjang = pd.DataFrame([{
                    "username": username,
                    "jenis": jenis,
                    "nama": nama,
                    "jumlah": jumlah,
                    "harga": harga,
                    "total": total,
                }])
                
                keranjang_df = pd.concat([keranjang_df, data_keranjang], ignore_index=True)
                keranjang_df.to_csv("keranjang.csv", index=False)
                
                print(f"\n{nama} sebanyak {jumlah} {satuan} berhasil ditambahkan ke keranjang!")
            
            except ValueError:
                print("Input tidak valid. Masukkan nomor produk atau jumlah yang benar.")
                continue

            # Menanyakan apakah pengguna ingin menambahkan barang lagi
            opsi = input("Tekan ENTER untuk menambahkan barang lain atau ketik 'n' untuk selesai: ").lower()
            if opsi == 'n':
                break

        print("\nPilih jarak pengiriman: ")
        print("1. Jarak <2 km")
        print("2. Jarak 2 km - 7km")
        print("3. Jarak 7 km - 15 km")
        print("4. Jarak 15 km - 20 km")

        while True:
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
                    continue
                break
            except ValueError:
                print("Input harus berupa angka. Silahkan coba lagi")

        total_harga_akhir = total_harga + ongkir

        print("\n=== Ringkasan Keranjang Anda ===")
        print(keranjang_df[keranjang_df["username"] == username].to_string(index=False))
        print(f"\nTotal harga barang: Rp{total_harga}")
        print(f"Biaya ongkir: Rp{ongkir}")
        print(f"Total yang harus dibayar: Rp{total_harga_akhir}")

    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

# =============================Masukan=================================

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

def riwayat_masukan():
    """
    Fungsi untuk admin membaca semua masukan dari user
    """
    header("Riwayat Masukan")
    masukan_csv = "masukan.csv"

    # Coba membaca file CSV
    try:
        df = pd.read_csv(masukan_csv)
        print("\n=== Semua masukan ===")
        if df.empty:
            print("Tidak ada masukan")
        else:
            print(df.to_string(index=False))
    except FileNotFoundError:
        print("\nBelum ada masukan")


# ========================Riwayat Transaksi============================
def riwayat_transaksi():
    """
    Membaca dan menampilkan data dari file riwayat_transaksi.csv
    """
    try:
        # Membaca file CSV
        riwayat = pd.read_csv("riwayat_transaksi.csv")

        # Cek apakah file kosong
        if riwayat.empty:
            print("Riwayat transaksi kosong.")
            return

        # Menampilkan data riwayat transaksi
        print("\n=== Riwayat Transaksi ===\n")
        print(tabulate(riwayat, headers="keys", tablefmt="grid", showindex=False)) #menampilkan data dengan tampilan tabel
        
    except FileNotFoundError:
        print("File 'riwayat_transaksi.csv' tidak ditemukan.")
    except pd.errors.EmptyDataError:
        print("File 'riwayat_transaksi.csv' kosong.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

# =========================Fungsi User=========================

def katalog_user(username):
    '''Katalog User'''
    jenis = input_jenis("Katalog")
    keranjang(username, jenis)
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
                        header("Gudang")
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
            input()
        elif opsi == "3":
            riwayat_masukan()
            input()
        elif opsi == "0":
            break

def menu_user():
    '''Menu User'''
    while True:
        header("Menu User")
        print("Pilih opsi:")
        print("1. Pembelian\n2. Masukan\n0. Kembali")
        opsi = input("Masukkan pilihan opsi sesuai angka (1/2/0)> ")
        if opsi == "1":
            input()
        elif opsi == "2":
            masukan()
        elif opsi == "0":
            break

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
                menu_user()
        elif opsi == "2":
            registrasi()
        elif opsi == "0":
            role = None
            outro()
            break
        else:
            print("Opsi tidak valid. Silakan masukkan angka 1, 2, atau 0.")
            input("Tekan enter untuk mengulang")

# =========================Mai Program=========================

main()
# # keranjang('surya')
# katalog_user()