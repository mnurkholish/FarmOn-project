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
            print("Login gagal, pilih opsi registrasi untuk membuat akun.")
            input("Tekan enter untuk melanjutkan")
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

def katalog(jenis):
    '''Katalog Produk'''
    header("Katalog")
    lihat_produk(jenis)

def tambah_produk():
    '''tambah produk'''
    jenis = input_jenis("Tambah Produk")

    while True:
        header("Tambah Produk")
        lihat_produk(jenis)
        try:
            nama = input("Masukkan nama hasil pertanian: ").strip()
            satuan = input("Tentukan satuan yang digunakan (kg/ikat/buah): ").strip()
            harga = int(input(f"Tentukan harga per-{satuan}: ").strip())
            stok = int(input(f"Berapa {satuan} stok yang akan dimasukkan: ").strip())
        except: # pylint:disable=bare-except
            print("Inputan tidak sesuai.")
            input("Tekan enter untuk mengulang")
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

        print("\nKatalog terbaru")
        lihat_produk(jenis)
        input("Tekan enter untuk kembali")

def hapus_produk():
    '''hapus produk'''
    jenis = input_jenis("Hapus Produk")

    lihat_produk(jenis)
    nama = input("Masukkan nama produk: ").strip()
    df = pd.read_csv("data_produk.csv")

    if (jenis in df["jenis"].values) and (nama in df["nama"].values):
        index_produk = df[(df["jenis"] == jenis) & (df["nama"] == nama)].index
        df.drop(index=index_produk, inplace=True)
        df.to_csv("data_produk.csv", index=False)
        print("produk berhasil dihapus")
        print("\nKatalog Terbaru")
        lihat_produk(jenis)
    else:
        print("produk tidak ada")
    input("Tekan enter untuk kembali")

def edit_stok(operasi):
    '''Tambah stok'''
    jenis = input_jenis("Tambah Produk")

    while True:
        header("Tambah Produk")
        lihat_produk(jenis)
        nama = input("Masukkan nama produk yang akan diedit: ").strip()

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
                input("Tekan enter untuk mengulang")
                continue

            try:
                if operasi == "+":
                    print(f"Stok saat ini: {stok_lama} {satuan}")
                    tambah = int(input(f"Berapa {satuan} {nama} yang akan ditambahkan: "))
                    stok_baru = stok_lama + tambah
                    df.loc[index_baris_produk, "stok"] = [stok_baru]
                elif operasi == "-":
                    print(f"Stok saat ini: {stok_lama} {satuan}")
                    kurang = int(input(f"Berapa {satuan} {nama} yang akan dikurangi: "))
                    stok_baru = stok_lama - kurang
                    df.loc[index_baris_produk, "stok"] = [stok_baru]
            except:
                print("Inputan tidak valid.")
                input("Tekan enter untuk mengulang")
                continue

            df.to_csv("data_produk.csv", index=False)

            print("Berhasil diedit.")
            print("\nKatalog Terbaru")
            lihat_produk(jenis)
            input("Tekan enter untuk kembali")
        else:
            print("Produk tidak ada, tolong masukkan nama dengan benar.")
            input("Tekan enter untuk mengulang")
            continue
        break

def edit_harga():
    '''Edit Harga'''
    jenis = input_jenis("Edit Harga")

    while True:
        header("Edit Harga")
        lihat_produk(jenis)
        nama = input("Masukkan nama produk: ").strip()

        df = pd.read_csv("data_produk.csv")

        baris_produk = df[(df["jenis"] == jenis) & (df["nama"] == nama)]

        try:
            if (jenis in df["jenis"].values) and (nama in df["nama"].values):
                harga_baru = int(input("Masukkan harga baru: "))
                index = baris_produk.index[0]
                df.at[index, 'harga'] = harga_baru
                df.to_csv("data_produk.csv", index=False)

                print("Berhasil diedit.")
                print("\nKatalog Terbaru")
                lihat_produk(jenis)
                input("Tekan enter untuk kembali")
            else:
                print("Produk tidak ada, tolong masukkan nama dengan benar.")
                input("Tekan enter untuk mengulang")
                continue
        except:
            print("Inputan tidak valid.")
            input("Tekan enter untuk mengulang")
            continue

        break

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
            # riwayat_transaksi()
            input()
        elif opsi == "3":
            # riwayat_masukan()
            input()
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
                # menu_user(username)
                input()
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
            input("Tekan enter untuk mengulang")

# =========================Mai Program=========================

main()

# coba coba


# halo