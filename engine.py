import requests
import random
import time
from datetime import datetime

# URL HASIL MODIFIKASI (Pastikan sudah benar)
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSe4pgHjDzZB9OTgbq7XNw5SWTNIo0AjTnnVUukd13e9BgkNPw/formResponse"

def cek_hari_libur():
    try:
        tahun = datetime.now().year
        res = requests.get(f"https://dayoffapi.vercel.app/api/v1/holidays?year={tahun}", timeout=5)
        if res.status_code == 200:
            hari_ini = datetime.now().strftime("%Y-%m-%d")
            holidays = res.json().get('data', [])
            for h in holidays:
                if h['date'] == hari_ini:
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
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    try:
        res = requests.post(FORM_URL, data=payload, headers=headers)
        print(f"Status: {res.status_code} - {'SUKSES' if res.status_code == 200 else 'GAGAL'}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    now = datetime.now()
    if now.weekday() >= 5: 
        print("Weekend. Skip.")
    elif cek_hari_libur():
        print("Hari Libur. Skip.")
    else:
        # Jalankan absen
        kirim_absen()
