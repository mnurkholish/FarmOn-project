import pandas as pd

def daftar_produk(jenis):
    '''daftar produk'''
    df = pd.read_csv("data_produk.csv")
    df = df[df["jenis"] == jenis]
    df = df.reset_index()
    for i in range(len(df)):
        nama = df.iloc[i,2]
        satuan = df.iloc[i,3]
        harga = df.iloc[i,4]
        print(f"{nama} harganya Rp{harga} per {satuan}")

opsi = input("jenis:" )
daftar_produk(opsi)
