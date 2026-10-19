# 📊 Projek Dashboard Manufaktur (Sales BI Dashboard)

[![Streamlit](https://img.shields.io/badge/Streamlit-1.23.1-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=Python&logoColor=white)](https://www.python.org/)
[![Plotly](https://img.shields.io/badge/Plotly-5.18.0-3F4F75?style=for-the-badge&logo=Plotly&logoColor=white)](https://plotly.com/)
[![Pandas](https://img.shields.io/badge/Pandas-1.3.5-150458?style=for-the-badge&logo=Pandas&logoColor=white)](https://pandas.pydata.org/)

Dashboard Business Intelligence & Analisis Performa Manufaktur/Sales interaktif berbasis web yang dibangun dengan **Streamlit** dan **Plotly**. Aplikasi ini menyajikan visualisasi data penjualan secara *real-time* yang terhubung langsung dengan **Google Sheets**, dilengkapi sistem filter multi-dimensi, pelacakan status proyek, analisis aging, serta antarmuka modern bertema *dark minimalist*.

---

## 🌟 Fitur Utama

- **⚡ Real-time Data Sync & Caching**: Mengambil data langsung dari Google Sheets via CSV export dengan mekanisme *retry* otomatis dan *smart caching* (TTL 5 menit) untuk efisiensi performa.
- **📈 Executive KPI Metric Cards**:
  - **Total Proyek (PA)**: Jumlah Proyek Aktif unik.
  - **Total Pendapatan**: Akumulasi nilai pendapatan dalam format mata uang Rupiah.
  - **Active Projects**: Jumlah proyek berstatus aktif/OPEN.
  - **Conversion Rate**: Rasio keberhasilan penyelesaian proyek (CLOSE vs Total PA).
- **📌 Project Status Tracking**: Pemantauan distribusi status proyek (OPEN, CLOSE, CANCEL) secara independen tanpa terdistorsi oleh filter status aktif.
- **📊 Interactive Charts (Plotly)**:
  - **Tren Rilis Proyek Bulanan**: Smooth area chart yang interaktif dengan hover informasi detail.
  - **Top 10 Pelanggan**: Tersedia dalam 2 mode (Tab *By Revenue* dengan horizontal bar chart & Tab *By PA* dalam bentuk tabel ringkasan).
- **📦 Analisis Layanan & Produk**:
  - **Ringkasan Produk**: Menampilkan total transaksi, jumlah pembeli unik, dan top customer per produk.
  - **Detail Pembeli**: Breakdown komprehensif pasangan produk dan pelanggan.
- **📝 Pelacakan Detail Progress**: Tabel monitoring catatan update terakhir setiap proyek beserta IDPA, Revenue, dan status, dilengkapi tombol **Download CSV**.
- **⏳ Analisis Aging Proyek**:
  - Pengelompokan umur proyek ke dalam 4 bracket: `0-14 Hari`, `15-30 Hari`, `31-365 Hari`, dan `> 365 Hari`.
  - Format durasi otomatis ramah baca (*human-readable*, contoh: *"1 Tahun 2 Bulan 5 Hari"*).
  - Ekspor data aging ke format CSV.
- **🎛️ Multi-Dimensional Filter**: Panel sidebar untuk menyaring data berdasarkan **Tahun**, **Sales**, **SBU**, **Pelanggan**, dan **Status Proyek**.
- **🎨 Dark Minimalist Interface**: Desain elegan dengan palet warna netral, glassmorphism cards, tipografi modern (*Outfit* & *Inter*), transisi halus, dan kontras ergonomis.

---

## 🏗️ Struktur Direktori

```text
dashboardsales-streamlit/
├── .streamlit/
│   └── config.toml          # Konfigurasi tema gelap & server Streamlit
├── app.py                   # Script aplikasi utama (UI, data pipeline, styling)
├── code_documentation.md    # Dokumentasi teknis komprehensif kode & arsitektur
├── README.md                # Dokumentasi ringkas proyek
└── requirements.txt         # Daftar pustaka & dependensi Python
```

---

## 🚀 Panduan Memulai

### 1. Prasyarat
Pastikan Anda telah menginstal:
- **Python 3.8** atau versi yang lebih baru
- Manajer paket **pip**

### 2. Kloning / Unduh Repositori
```bash
git clone https://github.com/username/dashboardsales-streamlit.git
cd dashboardsales-streamlit
```

### 3. Buat Virtual Environment (Disarankan)
- **Windows (PowerShell):**
  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```
- **macOS / Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 4. Instalasi Dependensi
```bash
pip install -r requirements.txt
```

### 5. Menjalankan Dashboard
Jalankan perintah Streamlit:
```bash
streamlit run app.py
```
Aplikasi akan otomatis berjalan pada peramban default Anda di alamat:
```
http://localhost:8501
```

---

## ⚙️ Konfigurasi Sumber Data

Secara default, aplikasi telah terhubung ke spreadsheet rujukan. Jika ingin menghubungkan ke Google Sheets Anda sendiri:

1. Pastikan Google Sheet Anda diatur ke akses publik (*"Anyone with the link can view"*).
2. Salin URL ekspor CSV sheet tersebut, contoh:
   ```text
   https://docs.google.com/spreadsheets/d/<SPREADSHEET_ID>/export?format=csv
   ```
3. Atur variabel lingkungan (*Environment Variable*) `GOOGLE_SHEETS_URL` sebelum menjalankan aplikasi:
   - **Windows (PowerShell):**
     ```powershell
     $env:GOOGLE_SHEETS_URL="https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/export?format=csv"
     streamlit run app.py
     ```
   - **Windows (CMD):**
     ```cmd
     set GOOGLE_SHEETS_URL=https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/export?format=csv
     streamlit run app.py
     ```
   - **macOS / Linux:**
     ```bash
     export GOOGLE_SHEETS_URL="https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/export?format=csv"
     streamlit run app.py
     ```

### Mekanisme Column Fallback
Aplikasi dilengkapi fungsi pra-pemrosesan (`preprocess_dataframe`) yang secara cerdas mendeteksi variasi nama kolom dari Google Sheets, antara lain:
- **ID Proyek**: `IDPA`
- **Pendapatan**: `Revenue`, `revenue`, `REVENUE`, `hargaPelanggan`, `Harga`
- **Status Proyek**: `STATUS SO`, `statusPA`
- **Tanggal Rilis**: `CREATEDON`, `Date`, `Tanggal`
- **Nama Pelanggan**: `CUSTOMERNAME`, `Pelanggan`
- **Tenaga Sales**: `namaSales`, `Sales`
- **Unit Bisnis**: `SBUNODE`, `SBU`

---

## 🛠️ Tech Stack & Pustaka

| Paket | Versi | Peran |
|---|---|---|
| [`streamlit`](https://streamlit.io/) | `1.23.1` | Kerangka kerja web UI interaktif utama |
| [`pandas`](https://pandas.pydata.org/) | `1.3.5` | Manipulasi, pembersihan, dan agregasi data |
| [`plotly`](https://plotly.com/python/) | `5.18.0` | Pembuatan visualisasi grafik responsif |
| [`requests`](https://requests.readthedocs.io/) | `2.31.0` | Pengambilan data ekspor CSV dari Google Sheets |
| [`openpyxl`](https://openpyxl.readthedocs.io/) | `3.1.3` | Pendukung pemrosesan spreadsheet berbasis Excel |

---

## 📖 Dokumentasi Teknis

Untuk penjelasan mendalam mengenai arsitektur logika, alur data (*pipeline*), referensi fungsi internal, serta detail desain CSS, silakan baca dokumentasi lengkap di:
👉 **[code_documentation.md](file:///d:/Projek%20Coding/dashboardsales-streamlit/code_documentation.md)**

---

## 📄 Lisensi
Proyek ini dibuat untuk keperluan monitoring bisnis dan analisis internal. Silakan sesuaikan penggunaan sesuai kebutuhan organisasi Anda.
