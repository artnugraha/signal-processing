# Pengolahan Sinyal

Repositori ini berisi materi kuliah **Pengolahan Sinyal** untuk mahasiswa **Teknik Fisika** dengan bobot **3 SKS**. Materi inti disusun untuk 12 pertemuan dari 16 pekan perkuliahan. Tiga pekan dialokasikan untuk UTS, UAS, dan tugas besar, sedangkan satu pekan lainnya dapat digunakan untuk review, presentasi, atau penyesuaian jadwal. Setiap pertemuan kuliah berlangsung sekitar 3 jam, dengan penekanan pada pemahaman konsep, formulasi matematis, contoh hitungan tangan, visualisasi, dan implementasi komputasi menggunakan Python.

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
| 2 | ⚙️ Sistem, Sistem LTI Waktu-Diskret, dan Persamaan Selisih | Menyusul |
| 3 | 🧩 Respons Impuls, Konvolusi, dan Korelasi | Menyusul |
| 4 | 🎚️ Sampling, Kuantisasi, ADC, dan DAC | Menyusul |
| 5 | 🌊 Representasi Fourier: FS, FT, dan DTFT | Menyusul |
| 6 | ⚡ DFT, FFT, dan Analisis Spektrum Numerik | Menyusul |
| 7 | 🌀 Transformasi Z, Fungsi Sistem, dan Pole-Zero | Menyusul |
| 8 | 🧱 Filter Digital FIR | Menyusul |
| 9 | 🔄 Filter Digital IIR | Menyusul |
| 10 | 📊 Analisis Spektral Sinyal Pengukuran dan Sinyal Tidak Stasioner | Menyusul |
| 11 | 🎵 Sistem Pengolahan Sinyal Audio | Menyusul |
| 12 | 🖼️ Sistem Pengolahan Citra sebagai Sinyal Dua Dimensi | Menyusul |

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

### 2. Sistem, Sistem LTI Waktu-Diskret, dan Persamaan Selisih

- sistem sebagai transformasi dari masukan menjadi keluaran;
- sistem waktu-kontinu dan waktu-diskret;
- linearitas;
- prinsip superposisi dan homogenitas;
- sistem *time-invariant* dan *time-varying*;
- sistem dengan dan tanpa memori;
- kausalitas;
- invertibilitas;
- stabilitas BIBO;
- sistem *linear time-invariant*;
- diagram blok sistem waktu-diskret;
- penjumlah, pengali, dan *unit delay*;
- persamaan selisih;
- sistem rekursif dan nonrekursif;
- kondisi awal;
- respons masukan-nol dan respons keadaan-nol;
- implementasi persamaan selisih dengan Python.

### 3. Respons Impuls, Konvolusi, dan Korelasi

- impuls diskret sebagai komponen penyusun sinyal;
- representasi sinyal menggunakan impuls;
- respons impuls sistem LTI;
- hubungan masukan, respons impuls, dan keluaran sistem;
- definisi konvolusi waktu-diskret;
- interpretasi *flip, shift, multiply, sum*;
- sifat-sifat konvolusi;
- hubungan konvolusi dengan sistem LTI;
- interkoneksi seri dan paralel sistem LTI;
- hubungan antara persamaan selisih dan respons impuls;
- konvolusi waktu-kontinu sebagai pengayaan;
- autokorelasi;
- korelasi silang;
- estimasi pergeseran waktu menggunakan korelasi.

### 4. Sampling, Kuantisasi, ADC, dan DAC

- proses sampling;
- periode sampling dan frekuensi sampling;
- teorema sampling;
- *Nyquist rate* dan *Nyquist frequency*;
- aliasing;
- *sample-and-hold*;
- filter anti-aliasing;
- kuantisasi dan *quantization error*;
- resolusi ADC;
- SQNR;
- PCM dan pengantar *companding*;
- DAC;
- *zero-order hold*;
- rekonstruksi sinyal analog.

### 5. Representasi Fourier: FS, FT, dan DTFT

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

### 6. DFT, FFT, dan Analisis Spektrum Numerik

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

### 7. Transformasi Z, Fungsi Sistem, dan Pole-Zero

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

### 8. Filter Digital FIR

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

### 9. Filter Digital IIR

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

### 10. Analisis Spektral Sinyal Pengukuran dan Sinyal Tidak Stasioner

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

### 11. Sistem Pengolahan Sinyal Audio

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

### 12. Sistem Pengolahan Citra sebagai Sinyal Dua Dimensi

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
