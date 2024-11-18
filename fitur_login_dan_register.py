'''Fitur Login dan Registrasi'''

import pandas as pd

# Register
def register():
    '''register'''
    username = input("username: ")
    password = input("password: ")
    
    df = pd.read_csv("akun_pengguna.csv")

    user_baru = pd.DataFrame({
    "username": [username],
    "password": [password],
    "role": ["user"]
    })
    
    df = pd.concat([df, user_baru], ignore_index=True)
    df.to_csv("akun_pengguna", index=False)

    print("Akun Berhasil dibuat. Silahkan login ulang!")
    input("Tekan enter untuk melanjutkan")

# Login
def login():
    '''Login'''
    username = input("Username: ")
    password = input("Password: ")

    df = pd.read_csv("akun_pengguna.csv")

    ambil_role = df[(df["username"] == username) & (df["password"] == password)]

    if not ambil_role.empty:
        role = ambil_role.iloc[0,2]
        return role
    else:
        return "Login gagal"
