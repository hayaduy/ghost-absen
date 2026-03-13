import flet as ft
import requests
import random
import time
from datetime import datetime

# --- KONFIGURASI TARGET (LINK BARU) ---
# Link dari kamu: https://docs.google.com/forms/d/e/1FAIpQLSe4pgHjDzZB9OTgbq7XNw5SWTNIo0AjTnnVUukd13e9BgkNPw/viewform
BASE_URL = "https://docs.google.com/forms/d/e/1FAIpQLSe4pgHjDzZB9OTgbq7XNw5SWTNIo0AjTnnVUukd13e9BgkNPw"

def cek_hari_libur():
    """Cek hari libur nasional Indonesia"""
    try:
        tahun = datetime.now().year
        res = requests.get(f"https://dayoffapi.vercel.app/api/v1/holidays?year={tahun}", timeout=5)
        if res.status_code == 200:
            hari_ini = datetime.now().strftime("%Y-%m-%d")
            holidays = res.json().get('data', [])
            for h in holidays:
                if h['date'] == hari_ini:
                    return h['name']
        return False
    except:
        return False

def kirim_data_absen(nama, nip, jabatan):
    """Fungsi kirim data dengan Auto-URL Fix"""
    # Gunakan endpoint formResponse untuk bot
    final_url = f"{BASE_URL}/formResponse"
    
    payload = {
        "entry.960346359": nama,
        "entry.468881973": nip,
        "entry.159009649": jabatan
    }
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    try:
        response = requests.post(final_url, data=payload, headers=headers, timeout=10)
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

# --- ANTARMUKA UI (FLET) ---
def main(page: ft.Page):
    page.title = "Ghost Absen v3.5"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0A0A0A"
    page.padding = 30
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_width = 450
    page.window_height = 750

    # UI Elements
    nama_in = ft.TextField(label="Nama Lengkap", value="Abdurrahman", border_radius=12)
    nip_in = ft.TextField(label="NIP", value="198810122025211031", border_radius=12)
    jab_in = ft.TextField(label="Jabatan", value="OPERATOR LAYANAN OPERASIONAL", border_radius=12)
    
    status_text = ft.Text("System Ready", color="white54")

    def handle_test_absen(e):
        btn_test.disabled = True
        status_text.value = "Sedang mengirim..."
        page.update()
        
        success = kirim_data_absen(nama_in.value, nip_in.value, jab_in.value)
        
        if success:
            status_text.value = f"Status: Berhasil Terkirim! ✅ ({datetime.now().strftime('%H:%M')})"
            page.snack_bar = ft.SnackBar(ft.Text("✅ Berhasil!"), bgcolor="#2ecc71")
        else:
            status_text.value = "Status: Gagal ❌ (Cek Link/Koneksi)"
            page.snack_bar = ft.SnackBar(ft.Text("❌ Gagal Kirim!"), bgcolor="#e74c3c")
        
        btn_test.disabled = False
        page.snack_bar.open = True
        page.update()

    btn_test = ft.FilledButton(
        content=ft.Text("SAVE & TEST ABSEN", weight="bold"),
        on_click=handle_test_absen,
        bgcolor="#3498db",
        height=55,
        width=400
    )

    page.add(
        ft.Text("Ghost Absen", size=32, weight="bold"),
        ft.Text("Auto Attendance v3.5", color="#3498db"),
        ft.Divider(height=30, color="white10"),
        ft.Column([
            ft.Text("Pagi: 06:30 - 07:59", size=14, color="white70"),
            ft.Text("Sore: 16:30 - 23:59", size=14, color="white70"),
        ], spacing=5, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        ft.Divider(height=30, color="white10"),
        nama_in,
        nip_in,
        jab_in,
        ft.Container(height=20),
        btn_test,
        ft.Container(content=status_text, padding=20)
    )

# --- ENGINE AUTOMATION (UNTUK GITHUB) ---
def run_engine_auto():
    now = datetime.now()
    if now.weekday() >= 5: return
    if cek_hari_libur(): return

    # Logika Random Sleep
    jam = now.hour
    if jam < 12: delay = random.randint(1, 5340) # Pagi
    else: delay = random.randint(1, 27000) # Sore
    
    print(f"Waiting for {delay} seconds...")
    time.sleep(delay)
    
    success = kirim_data_absen("Abdurrahman", "198810122025211031", "OPERATOR LAYANAN OPERASIONAL")
    print("DONE" if success else "FAILED")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--auto":
        run_engine_auto()
    else:
        ft.app(target=main, view=ft.AppView.WEB_BROWSER)