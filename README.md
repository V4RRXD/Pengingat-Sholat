# 🕌 Pengingat Sholat (Prayer Reminder)

![Made with Python](https://img.shields.io/badge/Made%20with-Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Platform Windows](https://img.shields.io/badge/Platform-Windows-0078D4?style=for-the-badge&logo=windows&logoColor=white)
![Status Active](https://img.shields.io/badge/Status-Active-4CAF50?style=for-the-badge)

**Pengingat Sholat** adalah aplikasi desktop Windows berbasis Python yang berfungsi sebagai pengingat waktu sholat otomatis untuk seluruh wilayah Indonesia. Aplikasi ini berjalan secara efisien di latar belakang (*background*) melalui System Tray, memastikan Anda tetap beribadah tepat waktu tanpa mengganggu produktivitas kerja.

---

## 🌟 Fitur Utama

*   **📍 Cakupan Seluruh Indonesia:** Mendukung pencarian jadwal sholat untuk seluruh kota dan kabupaten di Indonesia melalui integrasi [API Aladhan](https://aladhan.com/prayer-times-api).
*   **🔔 Notifikasi Ganda (Dual Notification):**
    *   *Toast Notification:* Pemberitahuan halus di pojok kanan bawah layar Windows.
    *   *Pop-up Warning:* Jendela peringatan di tengah layar untuk memastikan Anda tidak melewatkan waktu sholat.
*   **📥 System Tray Integration:** Aplikasi dapat di-*minimize* ke System Tray agar *taskbar* tetap rapi.
*   **🚀 Auto Start (Windows Startup):** Fitur otomatis berjalan saat Windows menyala via Registry Windows, dengan pilihan opsi *Mode Tray* atau *Mode Menu*.
*   **🔒 Anti-Double Instance:** Menggunakan sistem *Windows Mutex* untuk mencegah aplikasi berjalan ganda di waktu yang sama.

---

## 📋 Prasyarat & Instalasi

Sebelum menjalankan aplikasi, pastikan Anda telah menginstal Python di Windows Anda. Aplikasi ini memerlukan beberapa dependencies tambahan.

### 1. Clone atau Unduh Project
Unduh *source code* aplikasi ini ke komputer Anda.

### 2. Instal Dependencies
Buka Command Prompt (CMD) di dalam folder project, lalu jalankan perintah berikut:
```bash
pip install requests schedule plyer pystray Pillow
```

---

## 🧑‍💻 Cara Menjalankan

Anda memiliki dua opsi mudah untuk menjalankan aplikasi ini:

### Metode 1: Menggunakan File Batch (Rekomendasi)
Cukup klik dua kali (*double click*) pada file **`Jalankan Sholat.bat`** yang tersedia di folder utama project. Metode ini sangat praktis karena Anda tidak perlu membuka terminal secara manual.

### Metode 2: Menggunakan Terminal / CMD
Buka Command Prompt (CMD), arahkan ke folder project, lalu ketik perintah:
```bash
python main.py
```

---

## 🛠️ Cara Menggunakan

### 1. Menu Awal
Saat pertama kali dijalankan, aplikasi akan menampilkan menu interaktif di CMD untuk:
*   Memasukkan lokasi kota/kabupaten Anda.
*   Mengaktifkan atau menonaktifkan fitur *Auto Start (Startup)*.
*   Memilih mode peluncuran saat Windows *booting* (langsung ke Tray atau masuk ke Menu).

### 2. Menu System Tray
Setelah konfigurasi selesai, aplikasi akan bersembunyi di System Tray. Klik kanan pada ikon aplikasi untuk memunculkan menu:
*   **Buka Menu:** Menampilkan kembali jendela CMD pengaturan.
*   **Keluar / Exit:** Menutup aplikasi secara total.

---

## 📁 Struktur Folder Project

```text
📁 Pengingat-Sholat/
├── 📄 main.py               # Kode utama aplikasi Python
├── 📄 Jalankan Sholat.bat   # Script batch untuk menjalankan aplikasi sekali klik
├── 📄 icon.jpg              # Ikon aplikasi
└── 📄 README.md             # Dokumentasi project ini
```

---

## ⚠️ Catatan Penting

*   **Mengapa Tidak Menggunakan `.exe`?** Aplikasi ini **sengaja tidak di-compile** menjadi file executable (`.exe`) menggunakan PyInstaller. Hal ini dikarenakan adanya batasan teknis terkait interaksi `sys.stdin` pada mode latar belakang (*background loop*) di PyInstaller yang dapat menyebabkan aplikasi *crash*. Aplikasi ini berjalan murni dan jauh lebih stabil menggunakan interpreter Python `.py` asli dibantu script `.bat`.
*   **Koneksi Internet:** Diperlukan koneksi internet saat pertama kali menentukan kota atau saat menyinkronkan jadwal sholat harian via API.

---

## ✍️ Footer

Made with ❤️ by V4RRXD.
