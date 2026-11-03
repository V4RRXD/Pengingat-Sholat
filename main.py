import requests
import datetime
import time
import schedule
import threading
import sys
import subprocess
import os
import winreg
import signal
import ctypes
from plyer import notification
import pystray
from PIL import Image, ImageDraw
import tkinter as tk
from tkinter import messagebox

# ================= DAFTAR KOTA DI INDONESIA =================
KOTA_INDONESIA = [
    "Banda Aceh", "Langsa", "Lhokseumawe", "Sabang", "Subulussalam",
    "Binjai", "Gunungsitoli", "Medan", "Padang Sidempuan", "Pematangsiantar", "Sibolga", "Tanjungbalai", "Tebing Tinggi",
    "Bukittinggi", "Padang", "Padangpanjang", "Pariaman", "Payakumbuh", "Sawahlunto", "Solok",
    "Dumai", "Pekanbaru", "Batam", "Tanjungpinang", "Jambi", "Sungai Penuh",
    "Lubuklinggau", "Pagar Alam", "Palembang", "Prabumulih", "Pangkalpinang", "Bengkulu",
    "Bandar Lampung", "Metro",
    "Jakarta Barat", "Jakarta Pusat", "Jakarta Selatan", "Jakarta Timur", "Jakarta Utara",
    "Bandung", "Bekasi", "Bogor", "Cimahi", "Cirebon", "Depok", "Sukabumi", "Tasikmalaya", "Banjar",
    "Cilegon", "Serang", "Tangerang", "Tangerang Selatan",
    "Magelang", "Pekalongan", "Salatiga", "Semarang", "Surakarta", "Tegal", "Yogyakarta",
    "Batu", "Blitar", "Kediri", "Madiun", "Malang", "Mojokerto", "Pasuruan", "Probolinggo", "Surabaya",
    "Denpasar", "Bima", "Mataram", "Kupang",
    "Pontianak", "Singkawang", "Banjarbaru", "Banjarmasin", "Palangka Raya", "Balikpapan", "Bontang", "Samarinda", "Tarakan",
    "Bitung", "Kotamobagu", "Manado", "Tomohon", "Gorontalo", "Palu", "Mamuju",
    "Makassar", "Palopo", "Parepare", "Baubau", "Kendari",
    "Ambon", "Tual", "Ternate", "Tidore Kepulauan", "Jayapura", "Sorong"
]

# ================= KONFIGURASI =================
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
    EXE_PATH = sys.executable
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    EXE_PATH = sys.executable 

FILE_KONFIG = os.path.join(BASE_DIR, "konfigurasi_kota.txt")
NAMA_FILE_IKON = os.path.join(BASE_DIR, "icon.ico")
REG_PATH = r"Software\Microsoft\Windows\CurrentVersion\Run"
APP_NAME = "PengingatSholat"

def baca_kota_tersimpan():
    if os.path.exists(FILE_KONFIG):
        with open(FILE_KONFIG, "r") as f:
            kota = f.read().strip()
            if kota in KOTA_INDONESIA:
                return kota
    return "Jakarta Selatan"

KOTA_USER = baca_kota_tersimpan()

def simpan_kota_baru(kota_baru):
    global KOTA_USER
    KOTA_USER = kota_baru
    with open(FILE_KONFIG, "w") as f:
        f.write(KOTA_USER)

def get_url_api():
    return f"https://api.aladhan.com/v1/timingsByCity?city={KOTA_USER}&country=Indonesia&method=11"

APLIKASI_BERJALAN = True
ICON_TRAY = None

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# ================= FUNGSI ANTI DOBEL (WINDOWS MUTEX) =================
def cek_dan_kunci_aplikasi():
    mutex_name = "Global\\PengingatSholatMutex_12345"
    mutex = ctypes.windll.kernel32.CreateMutexW(None, False, mutex_name)
    last_error = ctypes.windll.kernel32.GetLastError()
    if last_error == 183: # ERROR_ALREADY_EXISTS
        return False
    return True

# ================= FUNGSI STARTUP WINDOWS (FIXED) =================
def cek_status_startup():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_READ)
        try:
            value, _ = winreg.QueryValueEx(key, APP_NAME)
            winreg.CloseKey(key)
            return value
        except FileNotFoundError:
            winreg.CloseKey(key)
            return None
    except Exception:
        return None

def set_startup(mode):
    """Mode: 'tray', 'menu', atau 'off'"""
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_SET_VALUE)
        
        if mode == 'off':
            try:
                winreg.DeleteValue(key, APP_NAME)
                print("\n[SUKSES] Startup berhasil dimatikan.")
            except FileNotFoundError:
                print("\n[INFO] Startup memang sudah mati.")
        else:
            # DAPETIN PATH LENGKAP PYTHON.EXE / PYTHONW.EXE
            python_exe = sys.executable
            if mode == 'tray':
                # Ganti python.exe jadi pythonw.exe biar silent
                python_exe = python_exe.replace("python.exe", "pythonw.exe")
                if not os.path.exists(python_exe):
                    python_exe = sys.executable # Fallback kalau pythonw gak ada
            
            script_path = os.path.abspath(__file__)
            
            # COMMAND LENGKAP: "C:\path\python.exe" "C:\path\main.py" --arg
            if mode == 'tray':
                cmd = f'"{python_exe}" "{script_path}" --background'
            else:
                cmd = f'"{python_exe}" "{script_path}" --menu'
                
            winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, cmd)
            print(f"\n[SUKSES] Startup diaktifkan (Mode: {mode.upper()}).")
            print(f"Command: {cmd}")
            
        winreg.CloseKey(key)
    except Exception as e:
        print(f"\n[ERROR] Gagal mengatur startup: {e}")
    time.sleep(2)

def menu_startup():
    while True:
        clear_screen()
        status = cek_status_startup()
        print("="*40)
        print("        PENGATURAN STARTUP")
        print("="*40)
        
        if status:
            if "--background" in status:
                print("Status saat ini: AKTIF (Langsung ke Tray)")
            else:
                print("Status saat ini: AKTIF (Buka Menu CMD)")
            print(f"Path: {status[:60]}...") # Tampilin dikit buat debug
        else:
            print("Status saat ini: MATI")
            
        print("-" * 40)
        print("1. Aktifkan Startup (Langsung ke Tray)")
        print("2. Aktifkan Startup (Buka Menu CMD)")
        print("3. Matikan Startup")
        print("4. Kembali ke Menu Utama")
        print("="*40)
        
        pilihan = input("Pilih (1/2/3/4): ").strip()
        if pilihan == '1':
            set_startup('tray')
        elif pilihan == '2':
            set_startup('menu')
        elif pilihan == '3':
            set_startup('off')
        elif pilihan == '4':
            break

# ================= FUNGSI JADWAL & NOTIFIKASI =================
def ambil_jadwal_sholat():
    try:
        response = requests.get(get_url_api(), timeout=10)
        data = response.json()
        if data['code'] == 200:
            timings = data['data']['timings']
            return {
                "Subuh": timings['Fajr'].split(' ')[0],
                "Dzuhur": timings['Dhuhr'].split(' ')[0],
                "Ashar": timings['Asr'].split(' ')[0],
                "Maghrib": timings['Maghrib'].split(' ')[0],
                "Isya": timings['Isha'].split(' ')[0]
            }
    except Exception:
        return None

def tampilkan_notifikasi(nama_sholat):
    judul = f"Waktu Sholat {nama_sholat} - {KOTA_USER}"
    pesan = f"Jangan lupa solat ya! Sekarang udah masuk waktu {nama_sholat} untuk wilayah {KOTA_USER} dan sekitarnya. Yuk tinggalin kerjaan sebentar, ambil wudhu, dan solat."
    
    notification.notify(title=judul, message=pesan, app_name='Pengingat Sholat', timeout=30)

    def show_popup():
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        full_msg = f"Jangan lupa solat ya!\nSekarang udah masuk waktu {nama_sholat} untuk wilayah {KOTA_USER} dan sekitarnya."
        messagebox.showwarning(title="Pengingat Sholat", message=full_msg, parent=root)
        root.destroy()

    threading.Thread(target=show_popup, daemon=True).start()

def test_notifikasi(icon, item):
    tampilkan_notifikasi("TEST")

def cek_dan_set_jadwal_harian():
    jadwal = ambil_jadwal_sholat()
    if jadwal:
        schedule.clear('sholat')
        for sholat, waktu in jadwal.items():
            schedule.every().day.at(waktu).do(tampilkan_notifikasi, nama_sholat=sholat).tag('sholat')

# ================= FUNGSI MENU CMD =================
def menu_ganti_kota():
    clear_screen()
    print("="*40)
    print("          MENU GANTI KOTA")
    print("="*40)
    print("Ketik nama kota untuk mencari (contoh: 'Medan', 'Jakarta')")
    print("Atau ketik 'batal' untuk kembali ke menu utama.\n")
    
    while True:
        try:
            keyword = input("Cari kota: ").strip().lower()
        except EOFError:
            return
        if keyword == 'batal' or keyword == 'cancel':
            return
        hasil_pencarian = [k for k in KOTA_INDONESIA if keyword in k.lower()]
        if not hasil_pencarian:
            print("Kota tidak ditemukan. Coba kata kunci lain.\n")
            continue
        print(f"\nDitemukan {len(hasil_pencarian)} kota:")
        for i, kota in enumerate(hasil_pencarian, 1):
            print(f"{i}. {kota}")
        print("\nMasukkan NOMOR kota yang ingin dipilih (atau '0' untuk batal):")
        try:
            pilihan = input("Pilihan: ").strip()
        except EOFError:
            return
        if pilihan == '0':
            return
        if pilihan.isdigit():
            idx = int(pilihan) - 1
            if 0 <= idx < len(hasil_pencarian):
                kota_terpilih = hasil_pencarian[idx]
                simpan_kota_baru(kota_terpilih)
                print(f"\n[SUKSES] Kota berhasil diubah menjadi: {kota_terpilih}")
                print("Memperbarui jadwal sholat...")
                cek_dan_set_jadwal_harian()
                input("\nTekan Enter untuk kembali ke menu utama...")
                return
            else:
                print("Nomor tidak valid.\n")
        else:
            print("Input harus berupa angka.\n")

def menu_lihat_jadwal():
    clear_screen()
    print("="*40)
    print(f"   JADWAL SHOLAT HARI INI - {KOTA_USER.upper()}")
    print("="*40)
    jadwal = ambil_jadwal_sholat()
    if jadwal:
        for sholat, waktu in jadwal.items():
            print(f"- {sholat:<8}: {waktu}")
    else:
        print("Gagal mengambil jadwal. Periksa koneksi internet.")
    print("="*40)
    input("\nTekan Enter untuk kembali...")

def keluar_dari_menu():
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    jawab = messagebox.askyesnocancel(
        "Konfirmasi Pengingat Sholat", 
        "Apakah Anda ingin meminimize aplikasi ke System Tray?\n\nPilih 'Yes' untuk Minimize ke Tray.\nPilih 'No' untuk Keluar Total.",
        parent=root
    )
    root.destroy()
    if jawab is True:
        script_path = os.path.abspath(__file__)
        pythonw_exe = sys.executable.replace("python.exe", "pythonw.exe")
        if not os.path.exists(pythonw_exe):
            pythonw_exe = sys.executable 
        subprocess.Popen([pythonw_exe, script_path, "--background"])
        os._exit(0)
    elif jawab is False:
        os._exit(0)
    else:
        return False
    return True

def buka_menu_cli():
    def signal_handler(sig, frame):
        if keluar_dari_menu():
            sys.exit(0)
        print("\nKembali ke menu...")
        time.sleep(1)
        buka_menu_cli()
    signal.signal(signal.SIGINT, signal_handler)
    
    while True:
        clear_screen()
        print("="*40)
        print("       PENGINGAT SHOLAT - MENU UTAMA")
        print("="*40)
        print(f"Kota aktif saat ini: [{KOTA_USER}]")
        print("-" * 40)
        print("1. Ganti Kota / Cari Kota")
        print("2. Lihat Jadwal Sholat Hari Ini")
        print("3. Pengaturan Startup (Nyala Otomatis)")
        print("4. Tutup Menu (Background / Tray)")
        print("="*40)
        print("         Made By V4RRXD")
        print("="*40)
        
        try:
            pilihan = input("Pilih menu (1/2/3/4): ").strip()
        except EOFError:
            if keluar_dari_menu():
                sys.exit(0)
            continue
        if pilihan == '1':
            menu_ganti_kota()
        elif pilihan == '2':
            menu_lihat_jadwal()
        elif pilihan == '3':
            menu_startup()
        elif pilihan == '4':
            if keluar_dari_menu():
                sys.exit(0)
        else:
            print("Pilihan tidak valid.")
            time.sleep(1)

# ================= FUNGSI SYSTEM TRAY =================
def buat_ikon_tray():
    try:
        if os.path.exists(NAMA_FILE_IKON):
            img = Image.open(NAMA_FILE_IKON).convert("RGBA")
            return img.resize((64, 64), Image.Resampling.LANCZOS)
        elif os.path.exists(os.path.join(BASE_DIR, "icon.jpg")):
            img = Image.open(os.path.join(BASE_DIR, "icon.jpg")).convert("RGBA")
            return img.resize((64, 64), Image.Resampling.LANCZOS)
    except Exception as e:
        print(f"Gagal load gambar: {e}")
    image = Image.new('RGB', (64, 64), color=(255, 255, 255))
    d = ImageDraw.Draw(image)
    d.ellipse((10, 10, 54, 54), fill=(0, 128, 0)) 
    d.ellipse((25, 10, 69, 54), fill=(255, 255, 255))
    return image

def keluar_aplikasi(icon, item):
    global APLIKASI_BERJALAN
    APLIKASI_BERJALAN = False
    icon.stop()
    os._exit(0)

def jalankan_scheduler():
    global APLIKASI_BERJALAN
    while APLIKASI_BERJALAN:
        schedule.run_pending()
        time.sleep(1)

def buka_menu_dari_tray(icon, item):
    script_path = os.path.abspath(__file__)
    subprocess.Popen(f'start "Pengingat Sholat" cmd /c python "{script_path}" --menu', shell=True)

def restart_aplikasi(icon, item):
    icon.stop()
    script_path = os.path.abspath(__file__)
    subprocess.Popen(f'start "Pengingat Sholat" cmd /c python "{script_path}"', shell=True)
    os._exit(0)

def jalankan_tray():
    global ICON_TRAY
    icon_image = buat_ikon_tray()
    menu = pystray.Menu(
        pystray.MenuItem('Buka Pengingat', buka_menu_dari_tray, default=True),
        pystray.MenuItem('Test Notifikasi', test_notifikasi),
        pystray.MenuItem('Restart Aplikasi', restart_aplikasi), 
        pystray.MenuItem('Keluar', keluar_aplikasi)
    )
    ICON_TRAY = pystray.Icon("Pengingat Sholat", icon_image, "Pengingat Sholat", menu)
    ICON_TRAY.run()

# ================= FUNGSI UTAMA =================
def main():
    global APLIKASI_BERJALAN
    
    if len(sys.argv) > 1 and sys.argv[1] == '--background':
        if not cek_dan_kunci_aplikasi():
            print("Aplikasi sudah berjalan di background!")
            time.sleep(2)
            os._exit(0)
        schedule.every().day.at("00:01").do(cek_dan_set_jadwal_harian)
        cek_dan_set_jadwal_harian()
        threading.Thread(target=jalankan_scheduler, daemon=True).start()
        jalankan_tray()
        return

    if len(sys.argv) > 1 and sys.argv[1] == '--menu':
        buka_menu_cli()
        return 

    buka_menu_cli()

if __name__ == "__main__":
    main()