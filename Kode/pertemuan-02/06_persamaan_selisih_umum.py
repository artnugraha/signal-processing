import numpy as np


def persamaan_selisih(x, b, a, x_awal=None, y_awal=None):
    x = np.asarray(x, dtype=float)
    b = np.asarray(b, dtype=float)
    a = np.asarray(a, dtype=float)

    if x.ndim != 1 or b.ndim != 1 or a.ndim != 1:
        raise ValueError("Masukan dan koefisien harus berupa larik satu dimensi.")
    if len(a) == 0 or len(b) == 0:
        raise ValueError("Larik koefisien tidak boleh kosong.")
    if a[0] == 0:
        raise ValueError("Koefisien a[0] tidak boleh nol.")

    M = len(b) - 1
    N = len(a) - 1

    if x_awal is None:
        x_awal = np.zeros(M)
    if y_awal is None:
        y_awal = np.zeros(N)
    x_awal = np.asarray(x_awal, dtype=float)
    y_awal = np.asarray(y_awal, dtype=float)

    if x_awal.ndim != 1 or y_awal.ndim != 1:
        raise ValueError("Riwayat harus berupa larik satu dimensi.")
    if len(x_awal) != M or len(y_awal) != N:
        raise ValueError("Panjang riwayat harus sesuai dengan M dan N.")

    y = np.zeros(len(x))

    for n in range(len(x)):
        jumlah_x = 0.0
        for k in range(M + 1):
            if n - k >= 0:
                nilai_x = x[n - k]
            else:
                nilai_x = x_awal[k - n - 1]
            jumlah_x = jumlah_x + b[k] * nilai_x

        jumlah_y = 0.0
        for k in range(1, N + 1):
            if n - k >= 0:
                nilai_y = y[n - k]
            else:
                nilai_y = y_awal[k - n - 1]
            jumlah_y = jumlah_y + a[k] * nilai_y

        y[n] = (jumlah_x - jumlah_y) / a[0]

    return y


x = np.array([1, 2, 0, -1, 0, 0], dtype=float)
b = [1.0, 0.25]
a = [1.0, -0.5]
y = persamaan_selisih(x, b, a, x_awal=[0.0], y_awal=[1.0])

print(" n      x[n]       y[n]")
for n in range(len(x)):
    print(f"{n:2d}  {x[n]:8.3f}  {y[n]:9.4f}")
