'''data produl editor manual'''

import pandas as pd

produk = {
    "jenis" : ["buah", "buah", "sayuran", "serealia", "serealia"],
    "nama" : ["apel", "nanas", "bayam", "beras", "gandum"],
    "satuan" : ["kg", "kg", "ikat", "kg", "kg"],
    "harga" : [10, 20, 2, 14, 20]
}

df = pd.DataFrame(produk)
df.to_csv("data_produk.csv", index=False)
