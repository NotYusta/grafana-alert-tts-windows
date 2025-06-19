# Instalasi

## Menggunakan pip

1. Jalankan perintah berikut di terminal:

   ```bash
   python -m pip install -r requirements.txt
   ```

2. Salin file konfigurasi contoh dengan perintah:

   ```bash
   cp config.example.yaml config.yml
   ```

---

# Jika Suara TTS Bahasa Indonesia Tidak Tersedia di Windows

## Cara Menambahkan Bahasa Indonesia dan Mengaktifkan Suara TTS:

1. Buka **Settings** > **Time & Language** > **Language & Region**
2. Klik **Add a language** (Tambah bahasa), cari dan tambahkan **Bahasa Indonesia** atau **Indonesian**
3. Setelah bahasa ditambahkan, buka pengaturan **Speech**
4. Klik **Add voices** (Tambah suara)
5. Cari dan pilih **Bahasa Indonesia**, lalu klik **Install**
6. Setelah selesai instalasi, cari file `clone_voices.ps1`
7. **Menjalankan `clone_voices.ps1` dengan hak Administrator**:

   * Klik **Start**, ketik **PowerShell**
   * Klik kanan **Windows PowerShell** atau **Windows Terminal**, pilih **Run as administrator**
   * Arahkan ke folder tempat file `clone_voices.ps1` berada:

     ```powershell
     cd "C:\path\ke\folder"
     ```
   * Jalankan skrip dengan perintah:

     ```powershell
     .\clone_voices.ps1
     ```

---

Untuk pertanyaan atau bantuan lebih lanjut, silakan kunjungi:
[https://github.com/NotYusta](https://github.com/NotYusta)

---