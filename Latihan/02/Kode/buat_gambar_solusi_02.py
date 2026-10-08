"""Hitungan numerik dan tujuh gambar untuk solusi kuliah Pengolahan Sinyal 2.
Jalankan: python Kode/buat_gambar_solusi_02.py
Memerlukan Python 3, NumPy, dan Matplotlib. Semua PNG disimpan di ../Gambar.
"""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle

OUT = Path(__file__).resolve().parents[1] / 'Gambar'
OUT.mkdir(parents=True, exist_ok=True)
plt.rcParams.update({'font.size': 11, 'axes.grid': True, 'grid.alpha': 0.25})


def simpan(fig, nama):
    fig.tight_layout()
    fig.savefig(OUT / nama, dpi=170)
    plt.close(fig)


def kuantisasi_midrise(x, bit, vmin, vmax):
    """Batas bawah termasuk interval; indeks di luar rentang disaturasi."""
    x = np.asarray(x, dtype=float)
    delta = (vmax - vmin) / 2**bit
    mentah = np.floor((x - vmin) / delta).astype(int)
    kode = np.clip(mentah, 0, 2**bit - 1)
    xq = vmin + (kode + 0.5)*delta
    return mentah, kode, xq, delta


def kotak(ax, x, y, teks, warna):
    ax.add_patch(Rectangle((x-.45, y-.27), .9, .54,
                           facecolor=warna, edgecolor='#203040', lw=1.4))
    ax.text(x, y, teks, ha='center', va='center')


def panah(ax, titik):
    for a, b in zip(titik[:-2], titik[1:-1]):
        ax.plot([a[0], b[0]], [a[1], b[1]], color='#203040', lw=1.5)
    ax.annotate('', xy=titik[-1], xytext=titik[-2],
                arrowprops={'arrowstyle': '->', 'lw': 1.5, 'color': '#203040'})


# Soal 2: rekonstruksi dengan nilai awal yang diketahui.
y_selisih = np.array([2, -1, 0, 3])
x_rekonstruksi = 4 + np.cumsum(y_selisih)
assert np.array_equal(x_rekonstruksi, [6, 5, 5, 8])
print('Soal 2, masukan:', x_rekonstruksi)

# Soal 4: hitung menggunakan keadaan lama, baru perbarui penunda.
x = np.array([1, 2, 0, -1, 0], dtype=float)
y = np.zeros(len(x))
x_lama, y_lama = 0.0, 2.0
print('\nSoal 4: n, x, y, penunda x sesudah, penunda y sesudah')
for n, nilai in enumerate(x):
    y[n] = .5*y_lama + nilai - .25*x_lama
    x_lama, y_lama = nilai, y[n]
    print(n, nilai, y[n], x_lama, y_lama)
assert np.allclose(y, [2, 2.75, .875, -.5625, -.03125])

fig, ax = plt.subplots(2, 1, figsize=(10, 8),
                        gridspec_kw={'height_ratios': [1.45, 1]})
a = ax[0]
a.set(xlim=(0, 10.3), ylim=(0, 4.6))
a.axis('off')
a.text(.3, 3.45, r'$x[n]$', ha='center', va='bottom')
a.text(9.7, 3.45, r'$y[n]$', ha='center', va='bottom')
a.add_patch(Circle((6.7, 3.25), .3, facecolor='#fff1bf',
                   edgecolor='#203040', lw=1.5))
a.text(6.7, 3.25, '+', ha='center', va='center', fontsize=17)
panah(a, [(.45, 3.25), (6.38, 3.25)])
panah(a, [(7.02, 3.25), (9.55, 3.25)])
a.plot(1.2, 3.25, 'ko', ms=4)
panah(a, [(1.2, 3.25), (1.2, 2.05), (2.15, 2.05)])
kotak(a, 2.6, 2.05, 'D', '#d9eaff')
panah(a, [(3.05, 2.05), (4.05, 2.05)])
kotak(a, 4.5, 2.05, '−0.25', '#daf3df')
panah(a, [(4.95, 2.05), (5.8, 2.05), (5.8, 2.7), (6.48, 3.02)])
a.plot(8.7, 3.25, 'ko', ms=4)
panah(a, [(8.7, 3.25), (8.7, .7), (7.65, .7)])
kotak(a, 7.2, .7, 'D', '#d9eaff')
panah(a, [(6.75, .7), (5.55, .7)])
kotak(a, 5.1, .7, '0.5', '#daf3df')
panah(a, [(4.65, .7), (3.75, .7), (3.75, 1.25),
          (6.7, 1.25), (6.7, 2.92)])
a.text(2.6, 1.57, r'$x[n-1]$; awal 0', ha='center', fontsize=10)
a.text(7.2, .21, r'$y[n-1]$; awal 2', ha='center', fontsize=10)
a.text(5.15, 4.08, 'Realisasi menggunakan dua penunda (D = unit delay)', ha='center')
ax[1].stem(np.arange(len(y)), y)
ax[1].set(xlabel='Indeks n', ylabel='y[n]', title='Soal 4: keluaran dengan kondisi awal y[−1] = 2')
simpan(fig, 'soal-04-diagram-dan-respons.png')

# Soal 5: perbandingan iterasi dan solusi analitik.
n = np.arange(18)
y_iter = np.zeros(len(n))
y_satu = y_dua = 0.0
for i in n:
    nilai = 1 + y_satu - .25*y_dua
    y_iter[i] = nilai
    y_dua, y_satu = y_satu, nilai
homogen = -(n+3)*2.0**(-n)
y_analitik = 4 + homogen
assert np.allclose(y_iter, y_analitik, atol=1e-13)
assert np.allclose(y_iter[:3], [1, 2, 2.75])
print('\nSoal 5, tiga keluaran:', y_iter[:3])
fig, ax = plt.subplots(2, 1, figsize=(9, 6.5), sharex=True)
ax[0].plot(n, y_analitik, label='Solusi total analitik')
ax[0].plot(n, y_iter, 'o', ms=4, label='Iterasi')
ax[0].axhline(4, color='gray', ls='--', label='Partikular = 4')
ax[0].set(ylabel='y[n]', title='Soal 5: akar karakteristik berulang 0.5')
ax[0].legend()
ax[1].stem(n, homogen)
ax[1].set(xlabel='Indeks n', ylabel='Bagian homogen')
simpan(fig, 'soal-05-solusi-analitik.png')

# Soal 6: dua bentuk analog berbeda memberikan sampel yang sama.
fs = 500.0
t = np.linspace(0, .02, 5001)
ts = np.arange(11)/fs
asli = lambda z: 2*np.cos(2*np.pi*120*z) + np.sin(2*np.pi*380*z)
alias = lambda z: 2*np.cos(2*np.pi*120*z) - np.sin(2*np.pi*120*z)
assert np.allclose(asli(ts), alias(ts), atol=1e-13)
fig, ax = plt.subplots(2, 1, figsize=(10, 7), sharex=True)
ax[0].plot(1000*t, np.sin(2*np.pi*380*t), label='Sinus 380 Hz asli')
ax[0].plot(1000*t, -np.sin(2*np.pi*120*t), '--', label='Alias: −sinus 120 Hz')
ax[0].plot(1000*ts, np.sin(2*np.pi*380*ts), 'ko', label='Sampel fs = 500 Hz')
ax[0].set(ylabel='Amplitudo', title='Soal 6: pelipatan membalik tanda sinus')
ax[1].plot(1000*t, asli(t), label='Sinyal analog semula')
ax[1].plot(1000*t, alias(t), '--', label='Sinyal analog dengan komponen alias')
ax[1].plot(1000*ts, asli(ts), 'ko', label='Sampel identik')
ax[1].set(xlabel='Waktu (ms)', ylabel='Amplitudo')
for a in ax: a.legend(fontsize=9)
simpan(fig, 'soal-06-aliasing.png')
print('\nSoal 6, galat identitas alias:', np.max(np.abs(asli(ts)-alias(ts))))

# Soal 7: lima interval penahanan dan sampel berikutnya di titik ujung.
fs = 80.0
Ts = 1/fs
ns = np.arange(6)
tsample = ns*Ts
sampel = 2*np.sin(np.pi*ns/4)
sampel[np.abs(sampel) < 1e-14] = 0
pengamatan = np.array([.018, .044])
indeks = np.floor(pengamatan/Ts).astype(int)
assert np.array_equal(indeks, [1, 3])
assert np.allclose(sampel[indeks], np.sqrt(2))
fig, ax = plt.subplots(figsize=(10, 5))
t = np.linspace(0, 5*Ts, 2001)
ax.plot(t*1000, 2*np.sin(2*np.pi*10*t), label='Analog')
ax.stairs(sampel[:5], tsample*1000, baseline=None, lw=2, label='Penahanan orde nol')
ax.plot(tsample[:5]*1000, sampel[:5], 'ko', label='Lima sampel pertama')
ax.plot(tsample[5]*1000, sampel[5], 's', color='tab:red', label='Sampel baru tepat 5Ts')
ax.plot([62.5], [0], 'o', mfc='white', mec='tab:orange')
for tm, nilai in zip(pengamatan*1000, sampel[indeks]):
    ax.axvline(tm, color='gray', ls=':', alpha=.7)
    ax.annotate(f'{tm:g} ms: √2', (tm, nilai), xytext=(tm-4, 2.3),
                arrowprops={'arrowstyle': '->'}, fontsize=10)
ax.set(xlabel='Waktu (ms)', ylabel='Amplitudo', ylim=(-1.8, 2.65),
       title='Soal 7: penahanan lima interval hingga 62.5 ms')
ax.legend(loc='lower left', fontsize=9)
simpan(fig, 'soal-07-sample-hold.png')
print('\nSoal 7, lima sampel:', sampel[:5], 'nilai pengamatan:', sampel[indeks])

# Soal 8: tabel sampel, karakteristik, dan galat saturasi.
x8 = np.array([-4, -3.2, -.1, 0, 1.9, 3.9, 4.8])
mentah, kode, xq8, delta8 = kuantisasi_midrise(x8, 3, -4, 4)
e8 = xq8-x8
assert np.array_equal(kode, [0, 0, 3, 4, 5, 7, 7])
assert np.allclose(e8, [.5, -.3, -.4, .5, -.4, -.4, -1.3])
dalam = (x8 >= -4) & (x8 < 4)
assert np.all(np.abs(e8[dalam]) <= delta8/2 + 1e-14)
assert np.abs(e8[-1]) > delta8/2
print('\nSoal 8: x, indeks mentah, kode, xq, galat, biner')
for a, b, c, d, e in zip(x8, mentah, kode, xq8, e8):
    print(a, b, c, d, f'{e:.1f}', format(c, '03b'))
v = np.linspace(-4.5, 5, 4001)
_, _, qv, _ = kuantisasi_midrise(v, 3, -4, 4)
fig, ax = plt.subplots(2, 1, figsize=(10, 7), sharex=True)
ax[0].plot(v, qv, label='Keluaran mid-rise')
ax[0].plot(v, v, '--', color='gray', label='Tanpa kuantisasi')
ax[0].scatter(x8[dalam], xq8[dalam], color='tab:green', zorder=3, label='Sampel dalam rentang')
ax[0].scatter(x8[~dalam], xq8[~dalam], color='tab:red', marker='x', s=70, zorder=4, label='Kelebihan rentang')
ax[0].set(ylabel='xq (V)', title='Soal 8: kuantisator mid-rise 3 bit')
ax[1].plot(v, qv-v, color='tab:orange', label='Galat xq − x')
ax[1].scatter(x8, e8, color=np.where(dalam, 'tab:green', 'tab:red'), zorder=3)
ax[1].axhline(.5, color='gray', ls='--', label='Batas ±Δ/2 dalam rentang')
ax[1].axhline(-.5, color='gray', ls='--')
ax[1].set(xlabel='Masukan x (V)', ylabel='Galat (V)')
for a in ax:
    a.axvspan(4, 5, color='tab:red', alpha=.08)
    a.axvline(-4, color='gray', ls=':')
    a.axvline(4, color='gray', ls=':')
    a.legend(fontsize=9)
simpan(fig, 'soal-08-kuantisasi.png')

# Soal 9: SQNR model galat seragam dan dua cara penyimpanan.
delta9 = 10/4096
Pq = delta9**2/12
SQNR = 10*np.log10((2.5**2/2)/Pq)
jumlah_sampel = 2*16000*10
byte12 = jumlah_sampel*12//8
byte16 = jumlah_sampel*16//8
assert np.isclose(SQNR, 67.98751163663268)
assert (byte12, byte16) == (480000, 640000)
print('\nSoal 9: Δ (mV), batas galat (mV), SQNR (dB), byte12, byte16')
print(delta9*1000, delta9*500, SQNR, byte12, byte16)
A = np.linspace(.5, 5, 300)
model = 10*np.log10((A**2/2)/Pq)
fig, ax = plt.subplots(1, 2, figsize=(11, 4.7))
ax[0].plot(A, model, label='Model galat seragam')
ax[0].plot([2.5], [SQNR], 'o', label=f'2.5 V: {SQNR:.2f} dB')
ax[0].set(xlabel='Amplitudo puncak sinusoid (V)', ylabel='SQNR (dB)',
          title='Soal 9: ADC 12 bit, rentang ±5 V')
ax[0].legend(fontsize=9)
bars = ax[1].bar(['12 bit rapat', 'Wadah 16 bit'], [byte12/1000, byte16/1000],
                 color=['tab:blue', 'tab:orange'])
for b in bars:
    ax[1].text(b.get_x()+b.get_width()/2, b.get_height()+12,
               f'{b.get_height():.0f} kB', ha='center')
ax[1].set(ylabel='Ukuran (kB desimal)', ylim=(0, 750),
          title='Dua kanal, 16 kHz/kanal, durasi 10 s')
simpan(fig, 'soal-09-sqnr-penyimpanan.png')

# Soal 10: pilih semua pasangan sah dan periksa respons penghalus.
opsi = []
for fs in [2000, 4000, 8000]:
    for bit in [8, 10, 12]:
        if fs > 2*1500 and 5/(2**bit)/2 <= .003:
            opsi.append((fs*bit, fs, bit))
minimum = min(opsi)
assert minimum == (40000, 4000, 10)
print('\nSoal 10, laju minimum, fs, bit:', minimum)
n = np.arange(24)
h = .4*.6**n
ystep = 1-.6**(n+1)
y_iter = np.zeros(len(n))
lama = 0.0
for i in n:
    lama = .6*lama + .4
    y_iter[i] = lama
assert np.allclose(y_iter, ystep)
assert np.all(ystep <= 1)
fig, ax = plt.subplots(2, 1, figsize=(9, 6.5), sharex=True)
ax[0].stem(n, h)
ax[0].set(ylabel='h[n]', title='Soal 10: bobot respons impuls meluruh')
ax[1].plot(n, ystep, 'o-', label='Respons untuk xq[n] = 1, n ≥ 0')
ax[1].axhline(1, color='gray', ls='--', label='Batas / nilai akhir = 1')
ax[1].set(xlabel='Indeks n', ylabel='y[n]')
ax[1].legend(fontsize=9)
simpan(fig, 'soal-10-penghalus-stabil.png')
print('\nSemua pemeriksaan numerik selesai. Tujuh PNG disimpan di:', OUT)
