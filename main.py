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

def register():
    '''register'''
    clear()
    header()
    x = "REGISTER |"
    print(x + "\n" + "-"*(len(x)-1) + "+")
    username = input("username: ")
    password = input("password: ")

    df = pd.read_csv("akun_pengguna.csv")

    user_baru = pd.DataFrame({
    "username": [username],
    "password": [password],
    "role": ["user"]
    })

    df = pd.concat([df, user_baru], ignore_index=True)
    df.to_csv("akun_pengguna.csv", index=False)

    print("Akun Berhasil dibuat. Silahkan login ulang!")
    input("Tekan enter untuk melanjutkan")
    return login()

def login():
    '''Login'''
    clear()
    header()
    x = "LOGIN |"
    print(x + "\n" + "-"*(len(x)-1) + "+")
    username = input("Username: ")
    password = input("Password: ")

    df = pd.read_csv("akun_pengguna.csv")

    ambil_role = df[(df["username"] == username) & (df["password"] == password)]

    if not ambil_role.empty:
        role = ambil_role.iloc[0,2]
        return role
    else:
        print("Login gagal.\nApakah anda belum punya aku?")
        konfirmasi_registrasi = input("Masuk ke halaman registrasi! (y/n)" )
        if konfirmasi_registrasi == "y":
            return register()

def main():
    '''program utama'''
    while True:
        intro()
        while True:
            clear()
            header()
            print("Pilih opsi\n1. Login\n2. Register\n3. Exit")
            opsi = input("Masukkan opsi pilihan sesuai angka (1/2/3) >")
            if opsi == "1":
                role = login()
                if role is None:
                    print("Login gagal")
                    continue
                break
            elif opsi == "2":
                role = register()
                break
            elif opsi == "3": # kembali ke perulangan intro
                print("Terima kasih")
                input()
                return

        print(role)
        input()

main()
