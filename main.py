"""Program Utama"""

import os
import pandas as pd

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

        if not ambil_role.empty:
            role = ambil_role.iloc[0]['role']
        else:
            role = None

        return username, role
