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

def register():
    '''register'''
    clear()
    header()
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

# Login
def login():
    '''Login'''
    clear()
    header()
    username = input("Username: ")
    password = input("Password: ")

    df = pd.read_csv("akun_pengguna.csv")

    ambil_role = df[(df["username"] == username) & (df["password"] == password)]

    if not ambil_role.empty:
        role = ambil_role.iloc[0,2]
        return role
    else:
        print("Login gagal.\nApakah anda belum punya aku?")
        konfirmasi_registrasi = input("Ketik [1] untuk register!" )
        if konfirmasi_registrasi == "1":
            return register()

def main():
    '''program utama'''
    clear()
    header()
    user = login()
    print(user)

main()
print("hello world")
