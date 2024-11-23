'''coba flowchart'''

from main import * # pylint: disable=W0401, W0614
from produk import * # pylint: disable=W0401, W0614

def main():
    '''program utama'''
    intro()
    while True:
        header("Main Menu")
        print("Opsi pilihan\n1. Login\n2. Registrasi\n0. Keluar")
        opsi = input("Masukkan opsi (1/2/0) >")
        if opsi == "1":
            username, role = login()
            if role:
                print(f"Selamat datang, {username}")
                input("Tekan enter untuk beralih ke menu utama")
                if role == "admin":
                    menu_admin(username)
                elif role == "user":
                    menu_user(username)
            else:
                print("Akun tidak ditemukan. Silahkan registrasi untuk membuat akun baru.")
                input("Tekan enter untuk melanjutkan")
                continue
        elif opsi == "2":
            registrasi()
        elif opsi == "0":
            break
    outro()

main()
