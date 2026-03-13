import requests
import random
import time
from datetime import datetime, timedelta

# URL HASIL MODIFIKASI
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSe4pgHjDzZB9OTgbq7XNw5SWTNIo0AjTnnVUukd13e9BgkNPw/formResponse"

def cek_hari_libur(tanggal_str):
    try:
        tahun = datetime.now().year
        res = requests.get(f"https://dayoffapi.vercel.app/api/v1/holidays?year={tahun}", timeout=10)
        if res.status_code == 200:
            holidays = res.json().get('data', [])
            for h in holidays:
                if h['date'] == tanggal_str:
                    return True
        return False
    except:
        return False

def kirim_absen():
    payload = {
        "entry.960346359": "Abdurrahman",
        "entry.468881973": "198810122025211031",
        "entry.159009649": "OPERATOR LAYANAN OPERASIONAL"
    }
    # Tambahkan User-Agent agar terlihat seperti browser asli
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        res = requests.post(FORM_URL, data=payload, headers=headers)
        if res.status_code == 200:
            print(f"[{datetime.now()}] Status: SUKSES Mengirim Absen")
        else:
            print(f"[{datetime.now()}] Status: GAGAL (Code: {res.status_code})")
    except Exception as e:
        print(f"Error saat kirim_absen: {e}")

if __name__ == "__main__":
    # Menyesuaikan waktu ke WITA (UTC + 8)
    wita_now = datetime.utcnow() + timedelta(hours=8)
    hari_ini_str = wita_now.strftime("%Y-%m-%d")
    
    print(f"Menjalankan skrip pada: {wita_now} (WITA)")

    if wita_now.weekday() >= 5: 
        print("Hari Libur Akhir Pekan (Weekend). Skrip Berhenti.")
    elif cek_hari_libur(hari_ini_str):
        print(f"Hari ini ({hari_ini_str}) adalah Hari Libur Nasional. Skrip Berhenti.")
    else:
        # Tambahkan jeda acak 1-5 menit agar tidak terlalu kaku/robotik
        delay = random.randint(1, 300)
        print(f"Menunggu jeda acak selama {delay} detik...")
        time.sleep(delay)
        
        kirim_absen()
