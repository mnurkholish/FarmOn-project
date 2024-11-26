"""Program Utama"""

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

def intro():
    '''tampilan pertama aplikasi'''
    clear()
    header()
    width = 100
    print("\n\n" + "Selamat Datang di aplikasi FarmOn".center(width))
    print("Tekan enter untuk memulai aplikasi".center(width) + "\n\n")
    input("="*width + "\n")

def registrasi():
    '''registrasi'''
    while True:
        clear()
        header()
        x = "registrasi |"
        print(x + "\n" + "-"*(len(x)-1) + "+")

        username = input("username: ")
        password = input("password: ")
        confirm_password = input("confirm password: ")
        role = "user"

        if confirm_password != password:
            print("password tidak sama silahkan coba lagi")
            input("Tekan enter untuk mengulang")
            continue

        df = pd.read_csv("akun_pengguna.csv")
        if username in df["username"].values:
            print("username sudah ada, gunakan username yang berbeda")
            input("tekan enter untuk mengulang")
            continue
        break

    user_baru = pd.DataFrame([[username, password, role]], columns=["username", "password", "role"])

    df = pd.concat([df, user_baru], ignore_index=True)
    df.to_csv("akun_pengguna.csv", index=False)

    print("Akun berhasil dibuat. Silahkan login ulang!")
    input("Tekan enter untuk melanjutkan")

def login():
    '''Login'''
    clear()
    header()
    x = "LOGIN |"
    print(x + "\n" + "-"*(len(x)-1) + "+")

    username = input("Username: ")
    password = input("Password: ")

    global user # pylint: disable=global-variable-undefined
    user = username

    df = pd.read_csv("akun_pengguna.csv")

    ambil_role = df[(df["username"] == username) & (df["password"] == password)]

    if not ambil_role.empty:
        role = ambil_role.iloc[0,2]
        return role

def main():
    '''program utama'''
    while True:
        intro()
        while True:
            clear()
            header()
            print("Pilih opsi\n1. Login\n2. registrasi\n0. Exit")
            opsi = input("Masukkan opsi pilihan sesuai angka (1/2/3) >")
            if opsi == "1":
                role = login()
                if role == "user":
                    print("kamu adalah user")
                    input()
                elif role == "admin":
                    print("kamu adalah admin")
                    input()
                else:
                    print("Login gagal, username tidak ditemukan")
                    print("Silahkan pilih opsi registrasi jika anda belum punya akun")
                    input("Tekan enter untuk melanjutkan")
                    continue

            elif opsi == "2":
                registrasi()

            elif opsi == "0":
                print("Terima kasih")
                input()
                return

main()
