# Pengolahan Sinyal

Repositori ini berisi materi kuliah **Pengolahan Sinyal** untuk mahasiswa **Teknik Fisika** dengan bobot **3 SKS**. Materi inti disusun untuk 11 pertemuan dalam satu semester. Pekan lainnya dapat dialokasikan untuk UTS, UAS, tugas besar, serta kegiatan akademik lain sesuai kalender perkuliahan. Setiap pertemuan kuliah berlangsung sekitar 3 jam, dengan penekanan pada pemahaman konsep, formulasi matematis, contoh hitungan tangan, visualisasi, dan implementasi komputasi menggunakan Python.

Implementasi komputasi diupayakan menggunakan pustaka Python sesedikit mungkin. Sebagian besar contoh program dalam kuliah ini hanya memanggil dua pustaka utama untuk komputasi dengan Python.

```python
import numpy as np
import matplotlib.pyplot as plt
```

Pustaka `scipy` hanya digunakan pada beberapa bagian tertentu ketika diperlukan.

---

## Daftar materi

| No. | Topik | Link Catatan Kuliah |
|---:|---|---|
| 1 | 📈 Pengantar Pengolahan Sinyal dan Representasi Sinyal | [Materi 1](Catatan-Kuliah/pertemuan-01.md) |
| 2 | ⚙️ Sifat dan Klasifikasi Sistem, Komponen Dasar Sistem, Persamaan Selisih, Sampling dan Kuantisasi | Menyusul |
| 3 | 🧩 Konvolusi, Korelasi, dan Interkoneksi Sistem LTI | Menyusul |
| 4 | 🌊 Representasi Fourier: FS, FT, dan DTFT | Menyusul |
| 5 | ⚡ DFT, FFT, dan Analisis Spektrum Numerik | Menyusul |
| 6 | 🌀 Transformasi Z, Fungsi Sistem, dan Pole-Zero | Menyusul |
| 7 | 🧱 Filter Digital FIR | Menyusul |
| 8 | 🔄 Filter Digital IIR | Menyusul |
| 9 | 📊 Analisis Spektral Sinyal Pengukuran dan Sinyal Tidak Stasioner | Menyusul |
| 10 | 🎵 Sistem Pengolahan Sinyal Audio | Menyusul |
| 11 | 🖼️ Sistem Pengolahan Citra sebagai Sinyal Dua Dimensi | Menyusul |

---

## Media pembelajaran

Media utama yang digunakan dalam mata kuliah ini adalah:

- catatan kuliah dalam format Markdown yang dapat dibaca langsung melalui GitHub;
- ilustrasi konseptual dalam format SVG atau PNG;
- skrip Python pendukung untuk simulasi dan visualisasi;
- NumPy untuk komputasi numerik;
- Matplotlib untuk visualisasi;
- SciPy secara terbatas untuk beberapa metode yang tidak efisien jika diimplementasikan seluruhnya dari awal;
- Jupyter Notebook atau Google Colab sebagai lingkungan eksekusi interaktif jika diperlukan;
- latihan hitungan tangan untuk memperkuat pemahaman matematis;
- latihan pemrograman untuk menghubungkan formulasi matematis dengan implementasi komputasional.

Prinsip utama dalam penggunaan kode adalah memahami algoritma terlebih dahulu sebelum menggunakan fungsi pustaka tingkat tinggi. Sebagai contoh, konvolusi, DFT, dan persamaan selisih akan dipelajari dari definisinya sebelum dibandingkan dengan implementasi pustaka.

---

## Silabus kuliah

### 1. Pengantar Pengolahan Sinyal dan Representasi Sinyal

- pengertian sinyal dan pengolahan sinyal;
- sinyal waktu-kontinu dan waktu-diskret;
- sinyal analog, data-tercacah, terkuantisasi, dan digital;
- sinyal deterministik dan acak;
- sinyal periodik dan aperiodik;
- sinyal genap dan ganjil;
- sinyal energi dan sinyal daya;
- sinyal eksponensial, sinusoidal, *unit step*, impuls, *ramp*, dan sinc;
- operasi dasar pada sinyal;
- pengantar akuisisi dan pengolahan sinyal digital.

### 2. Sifat dan Klasifikasi Sistem, Komponen Dasar Sistem, Persamaan Selisih, Sampling dan Kuantisasi

- sifat dan klasifikasi sistem;
- komponen dasar sistem;
- persamaan selisih;
- konversi sinyal analog ke digital;
- sampling;
- kuantisasi.

Pokok bahasan yang dicakup meliputi linearitas, invariansi waktu, sistem dengan dan tanpa memori, kausalitas, invertibilitas, stabilitas, penjumlah, pengali, *unit delay*, diagram blok sistem, sistem rekursif dan nonrekursif, kondisi awal, periode dan frekuensi sampling, teorema sampling, aliasing, *sample-and-hold*, tingkat kuantisasi, galat kuantisasi, dan pengkodean digital.

### 3. Konvolusi, Korelasi, dan Interkoneksi Sistem LTI

- konvolusi dan korelasi;
- interkoneksi sistem LTI;
- rangkuman operasi sinyal dan notasinya;
- konvolusi sinyal kontinu.

Pokok bahasan yang dicakup meliputi konvolusi waktu-diskret, respons impuls dan hubungan masukan-keluaran sistem LTI, interpretasi operasi konvolusi, sifat-sifat konvolusi, autokorelasi, korelasi silang, hubungan seri dan paralel sistem LTI, serta konvolusi pada sinyal waktu-kontinu.

### 4. Representasi Fourier: FS, FT, dan DTFT

- motivasi analisis domain frekuensi;
- sinusoid kompleks;
- Fourier Series;
- Fourier Transform;
- Discrete-Time Fourier Transform;
- magnitudo dan fase;
- periodisitas spektrum sinyal waktu-diskret;
- sifat linearitas dan pergeseran;
- modulasi;
- konvolusi dalam domain frekuensi;
- respons frekuensi sistem LTI.

### 5. DFT, FFT, dan Analisis Spektrum Numerik

- Discrete Fourier Transform;
- invers DFT;
- hubungan DFT dengan DTFT;
- *frequency bin*;
- resolusi frekuensi;
- Fast Fourier Transform;
- kompleksitas komputasi;
- spektrum satu sisi;
- *spectral leakage*;
- fungsi *window*;
- *zero padding*;
- konvolusi linear dan konvolusi sirkular.

### 6. Transformasi Z, Fungsi Sistem, dan Pole-Zero

- definisi transformasi Z;
- *region of convergence*;
- hubungan transformasi Z dengan DTFT;
- sifat-sifat transformasi Z;
- invers transformasi Z sederhana;
- fungsi sistem;
- hubungan fungsi sistem dengan persamaan selisih;
- representasi pole-zero;
- kausalitas;
- stabilitas;
- lingkaran satuan;
- transformasi Z satu sisi sebagai pengayaan.

### 7. Filter Digital FIR

- pengertian filter digital;
- low-pass, high-pass, band-pass, dan band-stop;
- spesifikasi filter;
- passband, stopband, dan transition band;
- Finite Impulse Response;
- fase linear;
- simetri respons impuls;
- tipe-tipe FIR;
- metode window;
- rectangular, Hann, Hamming, Blackman, dan Kaiser;
- metode sampling frekuensi;
- pengantar metode Parks-McClellan.

### 8. Filter Digital IIR

- Infinite Impulse Response;
- perbandingan FIR dan IIR;
- sistem rekursif;
- pole placement;
- filter analog sebagai prototipe;
- Butterworth dan Chebyshev;
- metode impulse invariance;
- matched-Z transform;
- bilinear transform;
- frequency warping;
- prewarping;
- stabilitas filter IIR;
- implementasi filter orde satu dan orde dua.

### 9. Analisis Spektral Sinyal Pengukuran dan Sinyal Tidak Stasioner

- sinyal pengukuran dan derau;
- mean, variance, RMS, dan SNR;
- autokorelasi;
- power spectral density;
- periodogram;
- averaging spektrum;
- metode Welch secara konseptual;
- sinyal stasioner dan tidak stasioner;
- Short-Time Fourier Transform;
- resolusi waktu dan frekuensi;
- spectrogram.

### 10. Sistem Pengolahan Sinyal Audio

- audio sebagai sinyal tekanan;
- sampling rate dan bit depth;
- sinyal mono dan stereo;
- frekuensi fundamental dan harmonik;
- timbre;
- waveform, spectrum, dan spectrogram;
- filtering audio;
- equalization sederhana;
- penghilangan hum;
- clipping;
- dynamic range;
- resampling sederhana;
- alur pengolahan berkas WAV.

### 11. Sistem Pengolahan Citra sebagai Sinyal Dua Dimensi

- citra sebagai sinyal dua dimensi;
- citra grayscale dan RGB;
- sampling spasial;
- kuantisasi citra;
- impuls dua dimensi;
- kernel;
- konvolusi dua dimensi;
- smoothing;
- sharpening;
- deteksi tepi;
- separability;
- 2-D DFT;
- frekuensi spasial;
- filtering dalam domain spasial dan frekuensi;
- aliasing spasial.

---

## Daftar pustaka

1. D. Gunawan dan F. H. Juwono, *Pengolahan Sinyal Digital*.
2. A. V. Oppenheim dan R. W. Schafer, *Discrete-Time Signal Processing*.
3. S. W. Smith, *The Scientist and Engineer's Guide to Digital Signal Processing*.
