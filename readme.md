# Instalasi

## Menggunakan pip

1. Jalankan perintah berikut di terminal:

   ```bash
   python -m pip install -r requirements.txt
   ```

2. Salin file konfigurasi contoh:

   ```bash
   cp config.example.yaml config.yml
   ```

---

# Jika Suara TTS Bahasa Indonesia Tidak Tersedia di Windows

## Cara Menambahkan Bahasa Indonesia dan Mengaktifkan Suara TTS

1. Buka **Settings** > **Time & Language** > **Language & Region**
2. Klik **Add a language** (Tambah bahasa), lalu cari dan tambahkan **Bahasa Indonesia**
3. Setelah bahasa ditambahkan, buka pengaturan **Speech**
4. Klik **Add voices** (Tambah suara)
5. Cari dan pilih **Bahasa Indonesia**, lalu klik **Install**
6. Setelah proses instalasi selesai, temukan file `clone_voices.ps1`
7. **Untuk menjalankan `clone_voices.ps1` sebagai Administrator:**

   * Klik **Start**, ketik **PowerShell**
   * Klik kanan **Windows PowerShell** atau **Windows Terminal**, lalu pilih **Run as administrator**
   * Arahkan ke folder tempat file `clone_voices.ps1` berada:

     ```powershell
     cd "C:\path\to\folder"
     ```
   * Jalankan skrip dengan perintah:

     ```powershell
     .\clone_voices.ps1
     ```

---

## Menjalankan skrip dengan Execution Policy Bypass

Jika muncul error bahwa skrip tidak boleh dijalankan karena kebijakan keamanan, kamu bisa jalankan skrip ini sementara waktu dengan melewati kebijakan tersebut menggunakan perintah ini **di PowerShell**:

```powershell
powershell -ExecutionPolicy Bypass -File .\clone_voices.ps1
```

---

Untuk pertanyaan atau bantuan lebih lanjut, silakan kunjungi:
[https://github.com/NotYusta](https://github.com/NotYusta)