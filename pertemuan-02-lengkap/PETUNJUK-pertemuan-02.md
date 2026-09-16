# Berkas Pendukung Kuliah 2

Paket ini melengkapi repositori `artnugraha/signal-processing` dengan catatan tentang sistem, sistem LTI waktu-diskret, dan persamaan selisih. Struktur direktori mengikuti catatan pertemuan pertama serta silabus 12 pertemuan pada README yang dibaca pada 16 September 2026.

## Isi paket

Catatan dapat dibaca melalui berkas Markdown di bawah ini. Gambar dan kode disediakan pada direktori terpisah agar tautan relatif bekerja ketika ketiga direktori ditempatkan bersama di akar repositori.

| Lokasi | Isi |
|---|---|
| `Catatan-Kuliah/pertemuan-02.md` | Naskah lengkap, demo tertanam, contoh hitungan, dan latihan |
| `Gambar/pertemuan-02/` | Sepuluh ilustrasi, masing-masing dalam SVG dan PNG |
| `Kode/pertemuan-02/01_superposisi.py` | Uji superposisi pada sistem linear dan nonlinear |
| `Kode/pertemuan-02/02_invariansi_waktu.py` | Uji pergeseran melalui dua jalur |
| `Kode/pertemuan-02/03_nonrekursif.py` | Rata-rata tiga sampel dengan riwayat nol |
| `Kode/pertemuan-02/04_respons_dan_kondisi_awal.py` | Respons masukan-nol dan keadaan-nol |
| `Kode/pertemuan-02/05_stabilitas_orde_satu.py` | Perbandingan respons dengan beberapa koefisien umpan balik |
| `Kode/pertemuan-02/06_persamaan_selisih_umum.py` | Implementasi beberapa koefisien dan riwayat eksplisit |
| `Kode/pertemuan-02/07_sensor_temperatur.py` | Studi kasus penghalusan pembacaan temperatur |
| `Kode/pertemuan-02/00_buat_ilustrasi.py` | Pembuatan ulang seluruh ilustrasi |

## Menggunakan catatan

Ekstrak isi paket ke akar salinan lokal repositori agar direktori `Catatan-Kuliah`, `Gambar`, dan `Kode` berada pada tingkat yang sama. Berkas yang disertakan menggunakan nama pertemuan kedua, sehingga dapat ditambahkan bersama materi pertemuan pertama.

Tautan gambar di Markdown menggunakan berkas SVG. Berkas PNG dengan nama dasar yang sama disertakan untuk aplikasi yang belum mendukung SVG dengan baik.

Jika catatan sudah ditambahkan ke repositori, ubah tautan pada baris pertemuan kedua di tabel README menjadi `[Materi 2](Catatan-Kuliah/pertemuan-02.md)`. Silabus dan berkas README yang ada tidak disertakan dalam paket ini.

## Menjalankan demo

Setiap demo dapat dijalankan sendiri menggunakan Python dengan NumPy dan Matplotlib. Kode yang sama juga tersedia di dalam catatan agar dapat disalin ke Jupyter Notebook atau Google Colab.

```bash
python Kode/pertemuan-02/01_superposisi.py
python Kode/pertemuan-02/02_invariansi_waktu.py
python Kode/pertemuan-02/03_nonrekursif.py
python Kode/pertemuan-02/04_respons_dan_kondisi_awal.py
python Kode/pertemuan-02/05_stabilitas_orde_satu.py
python Kode/pertemuan-02/06_persamaan_selisih_umum.py
python Kode/pertemuan-02/07_sensor_temperatur.py
```

Untuk membuat ulang seluruh ilustrasi, jalankan perintah berikut dari akar repositori. Skrip menggunakan pustaka standar Python, NumPy, dan Matplotlib, lalu menyimpan keluaran ke `Gambar/pertemuan-02`.

```bash
python Kode/pertemuan-02/00_buat_ilustrasi.py
```

Skrip pembuatan ilustrasi menjalankan ketujuh demo dan menyimpan gambar tanpa membuka jendela grafik. Menjalankan demo secara terpisah tetap menampilkan grafik melalui `plt.show()` seperti yang tertulis dalam catatan.
