"""Program Utama"""

import os
import pandas as pd

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
            input("Tekan enter untuk melanjutkan")
            continue
        # validasi password harus ada
        if not password:
            print("Password tidak boleh kosong")
            input("Tekan enter untuk melanjutkan")
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
                input("Tekan untuk melanjutkan")
                continue

        data_akun = "akun_pengguna.csv"
        df = pd.read_csv(data_akun)

        # validasi username harus berbeda dari yang sudah ada
        if username in df["username"].values:
            print("username sudah ada, gunakan username yang berbeda")
            input("tekan enter untuk mengulang")
            continue

        # jika syarat terpenuhi, membuat data baru
        user_baru = pd.DataFrame([[username, password, role]], columns=["username", "password", "role"])

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
            print("Login gagal, pilih opsi registrasi untuk membuat akun.")
            input("Tekan enter untuk melanjutkan")
        else:
            role = ambil_role.iloc[0]['role']
            print(f"Login berhasil\nSelamat datang {username}.")

        return username, role

# =========================Fungsi Main Menu=========================

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
        
        while True:
            header("Tambah Produk")
            lihat_produk(jenis)
            try:
                nama = input("Masukkan nama hasil pertanian: ").strip()
                satuan = input("Tentukan satuan yang digunakan (kg/ikat/buah): ").strip()
                harga = int(input(f"Tentukan harga per-{satuan}: ").strip())
                stok = int(input(f"Berapa {satuan} stok yang akan dimasukkan: ").strip())
            except:
                print("Inputan tidak sesuai.")
                input("Tekan enter untuk mengulangi")
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
            print("Berhasil ditambahkan")
            input("Tekan enter untuk melanjutkan")
        break

# =========================Navigasi=========================

def menu_admin():
    '''Menu Admin'''
    while True:
        header("Menu Admin")
        print("Pilih opsi:")
        print("1. Gudang\n2. Riwayat Transaksi\n3. Riwayat Masukan\n0. Kembali")
        opsi = input("Masukkan pilihan opsi sesuai angka (1/2/0)> ")
        if opsi == "1":
            while True:
                header("Gudang")
                print("Pilih opsi:")
                print("1. Tambah produk\n2. Hapus Produk\n3. Edit Stok\n4. Edit Harga\n0. Kembali")
                opsi = input("Masukkan pilihan opsi sesuai angka (1/2/0)> ")
                if opsi == "1":
                    tambah_produk()
                elif opsi == "2":
                    input()

        elif opsi == "2":
            # riwayat_transaksi()
            input()
        elif opsi == "3":
            # riwayat_masukan()
            input()
        elif opsi == "0":
            break

def main_menu():
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
            else:
                continue
        elif opsi == "2":
            registrasi()
        elif opsi == "0":
            role = None
            outro()
            break
        else:
            print("Opsi tidak valid. Silakan masukkan angka 1, 2, atau 0.")
            input("Tekan enter untuk melanjutkan")

# =========================Mai Program=========================

main_menu()