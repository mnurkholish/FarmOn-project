'''data produl editor manual'''

import pandas as pd

produk = {
    "jenis" : ["buah", "buah", "sayuran", "serealia", "serealia"],
    "nama" : ["apel", "nanas", "bayam", "beras", "gandum"],
    "satuan" : ["kg", "kg", "ikat", "kg", "kg"],
    "harga" : [10, 20, 2, 14, 20],
    "stok" : [100, 89, 87, 28, 77]
}

df = pd.read_csv("data_produk.csv")
baris = df[(df["jenis"] == "buah") & (df["nama"] == "nanas")]
index_baris = baris.index[0]
print(index_baris)
stok = baris.loc[index_baris, "stok"]
print(baris.loc[index_baris, "satuan"])
print(baris.loc[index_baris, "stok"])
print(df)
