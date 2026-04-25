# DScanner - Network Security Vulnerability Scanner

DScanner adalah alat keamanan jaringan komprehensif yang dirancang untuk memindai jaringan mencari kerentanan, port terbuka, layanan lemah, dan konfigurasi keamanan yang salah.

## 📋 Daftar Isi
- [Fitur](#fitur)
- [Persyaratan](#persyaratan)
- [Instalasi](#instalasi)
- [Cara Penggunaan](#cara-penggunaan)
- [Contoh Penggunaan](#contoh-penggunaan)
- [Basis Data Kerentanan](#basis-data-kerentanan)
- [Keluaran Laporan](#keluaran-laporan)
- [Pertimbangan Keamanan](#pertimbangan-keamanan)

## ✨ Fitur

✅ **Pemindaian Port** - Mengidentifikasi port terbuka dan layanan yang berjalan
✅ **Deteksi Layanan** - Mendeteksi layanan yang sedang berjalan dan versinya
✅ **Analisis SSL/TLS** - Memeriksa validitas sertifikat SSL dan kerentanan
✅ **Pemeriksaan Kerentanan Umum** - Mendeteksi kerentanan yang diketahui
✅ **Pemetaan Jaringan** - Menemukan host yang aktif di jaringan
✅ **Analisis Header Keamanan** - Memeriksa header keamanan HTTP yang hilang
✅ **Keamanan DNS** - Memverifikasi konfigurasi dan keamanan DNS
✅ **Pelaporan Terperinci** - Menghasilkan laporan kerentanan yang komprehensif

## 🔧 Persyaratan

- Python 3.8 atau lebih baru
- Hak akses administratif/Root (untuk beberapa fitur)
- Linux, macOS, atau Windows

## 📥 Instalasi

### Langkah 1: Clone Repository
```bash
git clone https://github.com/D1-nimous/DScanner.git
cd DScanner
```

### Langkah 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Langkah 3: Jalankan Scanner
```bash
python dscanner.py -h
```

## 🎯 Cara Penggunaan

### Syntax Dasar
```
python dscanner.py -t TARGET [OPSI]
```

### Daftar Opsi
```
-t, --target TARGET           IP address target atau range CIDR (WAJIB)
-p, --ports PORTS            Port spesifik untuk dipindai (dipisahkan koma)
--timeout TIMEOUT            Timeout pemindaian dalam detik (default: 5)
--full                       Melakukan pemindaian komprehensif penuh
--report REPORT              Menghasilkan laporan HTML
-v, --verbose                Output verbose/detail
-h, --help                   Tampilkan bantuan
```

## 📖 Contoh Penggunaan

### 1. Pemindaian Host Tunggal Dasar
**Deskripsi:** Memindai satu host untuk port terbuka

```bash
python dscanner.py -t 192.168.1.1
```

**Output:**
```
[*] Scanning host: 192.168.1.1
[+] Port 22 (ssh) is OPEN on 192.168.1.1
[+] Port 80 (http) is OPEN on 192.168.1.1
```

---

### 2. Pemindaian Host dengan Mode Verbose (Detail)
**Deskripsi:** Memindai dengan output yang lebih rinci

```bash
python dscanner.py -t 192.168.1.1 -v
```

**Output:**
```
[*] Scanning host: 192.168.1.1
[+] Port 22 (ssh) is OPEN on 192.168.1.1
[+] Port 80 (http) is OPEN on 192.168.1.1
[+] Port 443 (https) is OPEN on 192.168.1.1
[!] VULNERABILITY: MySQL on port 3306 - MySQL exposed to network
```

---

### 3. Pemindaian Port Spesifik
**Deskripsi:** Memindai hanya port yang ditentukan

```bash
python dscanner.py -t 192.168.1.1 -p 22,80,443,3306
```

**Penjelasan:**
- `-p 22,80,443,3306` = Hanya periksa port 22 (SSH), 80 (HTTP), 443 (HTTPS), dan 3306 (MySQL)

**Output:**
```
[*] Scanning host: 192.168.1.1
[+] Port 22 (ssh) is OPEN on 192.168.1.1
[+] Port 80 (http) is OPEN on 192.168.1.1
[+] Port 443 (https) is OPEN on 192.168.1.1
[!] VULNERABILITY: MySQL on port 3306 - MySQL exposed to network
```

---

### 4. Pemindaian Jaringan Lengkap (Network Range)
**Deskripsi:** Memindai seluruh subnet jaringan

```bash
python dscanner.py -t 192.168.1.0/24
```

**Penjelasan:**
- `192.168.1.0/24` = Memindai jaringan dari 192.168.1.1 hingga 192.168.1.254

**Output:**
```
[*] Scanning network: 192.168.1.0/24 (254 hosts)
[*] Scanning host: 192.168.1.1
[+] Port 22 (ssh) is OPEN on 192.168.1.1
[*] Scanning host: 192.168.1.2
[+] Port 80 (http) is OPEN on 192.168.1.2
```

---

### 5. Pemindaian Komprehensif Penuh
**Deskripsi:** Melakukan pemindaian mendalam dengan analisis SSL dan header keamanan

```bash
python dscanner.py -t 192.168.1.1 --full -v
```

**Penjelasan:**
- `--full` = Analisis SSL/TLS, header keamanan, dan layanan web
- `-v` = Tampilkan detail lengkap

**Output:**
```
[*] Scanning host: 192.168.1.1
[+] Port 22 (ssh) is OPEN on 192.168.1.1
[+] Port 80 (http) is OPEN on 192.168.1.1
[+] Port 443 (https) is OPEN on 192.168.1.1
[!] VULNERABILITY: Missing security headers: X-Frame-Options, X-XSS-Protection
[+] SSL Certificate found - Valid
```

---

### 6. Menghasilkan Laporan HTML
**Deskripsi:** Membuat laporan kerentanan dalam format HTML

```bash
python dscanner.py -t 192.168.1.1 --full --report laporan_kerentanan.html -v
```

**Penjelasan:**
- `--report laporan_kerentanan.html` = Simpan laporan ke file HTML
- File akan berisi ringkasan lengkap semua kerentanan

**Output:**
```
[+] Report generated: laporan_kerentanan.html
[+] Scan completed successfully
```

---

### 7. Pemindaian Jaringan dengan Laporan HTML
**Deskripsi:** Memindai seluruh subnet dan buat laporan detail

```bash
python dscanner.py -t 192.168.1.0/24 --full --report laporan_subnet.html -v
```

---

### 8. Pemindaian dengan Timeout Kustom
**Deskripsi:** Mengatur waktu tunggu koneksi lebih lama

```bash
python dscanner.py -t 192.168.1.1 --timeout 10 -v
```

**Penjelasan:**
- `--timeout 10` = Tunggu maksimal 10 detik per port

---

### 9. Kombinasi Opsi Lengkap
**Deskripsi:** Pemindaian komprehensif dengan semua fitur

```bash
python dscanner.py -t 192.168.1.1 -p 22,80,443,3306,5432 --full --timeout 10 --report scan_result.html -v
```

---

### 10. Pemindaian dengan Script Bash
**Jalankan dari contoh yang sudah disiapkan:**

```bash
# Pemindaian dasar
bash examples/basic_scan.sh

# Pemindaian jaringan penuh
bash examples/full_network_scan.sh

# Pemindaian port spesifik
bash examples/specific_ports_scan.sh
```

---

## 🗄️ Basis Data Kerentanan

DScanner mencakup database kerentanan yang diketahui:

| Port | Layanan | Severity | Masalah |
|------|---------|----------|--------|
| 21 | FTP | HIGH | Layanan FTP tanpa enkripsi |
| 23 | Telnet | CRITICAL | Layanan Telnet tidak aman |
| 80 | HTTP | MEDIUM | HTTP tanpa enkripsi |
| 135 | RPC | HIGH | RPC service terekspos |
| 139 | NetBIOS | HIGH | NetBIOS terekspos |
| 445 | SMB | HIGH | SMB terekspos |
| 3306 | MySQL | CRITICAL | MySQL terbuka ke jaringan |
| 5432 | PostgreSQL | CRITICAL | PostgreSQL terbuka ke jaringan |
| 5984 | CouchDB | CRITICAL | CouchDB tanpa autentikasi |
| 6379 | Redis | CRITICAL | Redis tanpa autentikasi |
| 27017 | MongoDB | CRITICAL | MongoDB tanpa autentikasi |

---

## 📊 Keluaran Laporan

### Format Hasil Scan di Terminal

```
============================================================
SCAN RESULTS
============================================================

[+] Open Ports Found: 3
    - 192.168.1.1:22 (ssh)
    - 192.168.1.1:80 (http)
    - 192.168.1.1:443 (https)

[!] Vulnerabilities Found: 2
    - [HIGH] Unencrypted HTTP detected
      Recommendation: Use HTTPS (port 443) instead of HTTP
    - [MEDIUM] Missing security headers: X-Frame-Options, X-XSS-Protection
      Recommendation: Add security headers to HTTP responses

[+] Scan completed successfully
[+] Report generated: laporan_kerentanan.html
```

### Format Laporan HTML

Laporan HTML mencakup:
- 📅 Tanggal dan waktu pemindaian
- 🎯 Target yang dipindai
- 📋 Daftar port terbuka
- ⚠️ Daftar kerentanan dengan tingkat keparahan
- 💡 Rekomendasi perbaikan untuk setiap kerentanan
- 📈 Ringkasan statistik keamanan

---

## 🔒 Pertimbangan Keamanan

⚠️ **PENTING**: Gunakan alat ini hanya pada jaringan dan sistem yang Anda miliki atau memiliki izin eksplisit untuk menguji. Pemindaian jaringan tanpa izin dapat melanggar hukum.

### Praktik Terbaik:
1. ✅ Dapatkan izin tertulis sebelum memindai
2. ✅ Dokumentasikan semua pemindaian yang dilakukan
3. ✅ Laporkan kerentanan ke administrator sistem
4. ✅ Ikuti proses responsible disclosure

---

## 📝 Contoh Skenario Penggunaan

### Skenario 1: Audit Keamanan Internal
```bash
# Pemindai seluruh infrastruktur internal
python dscanner.py -t 10.0.0.0/24 --full --report audit_internal.html -v
```

### Skenario 2: Pemeriksaan Server Produksi
```bash
# Periksa server produksi spesifik
python dscanner.py -t 192.168.100.50 -p 22,80,443,3306 --full --report server_prod.html -v
```

### Skenario 3: Monitoring Rutin
```bash
# Pemindaian harian dengan laporan
python dscanner.py -t 192.168.1.0/25 --report daily_$(date +%Y%m%d).html -v
```

### Skenario 4: Identifikasi Host yang Terinfeksi
```bash
# Cari port aneh yang mungkin menunjukkan infeksi malware
python dscanner.py -t 192.168.1.0/24 -v | grep -i "port"
```

---

## ❓ Troubleshooting

### Masalah: "Permission denied"
**Solusi:**
```bash
# Linux/macOS
sudo python dscanner.py -t 192.168.1.1

# Atau gunakan chmod
chmod +x dscanner.py
```

### Masalah: "Module not found"
**Solusi:**
```bash
pip install --upgrade -r requirements.txt
```

### Masalah: "Connection timeout"
**Solusi:**
```bash
# Tingkatkan timeout
python dscanner.py -t 192.168.1.1 --timeout 15
```

---

## 🤝 Kontribusi

Kontribusi sangat diterima! Silakan kirim pull request untuk:
- Penambahan kerentanan baru ke database
- Perbaikan deteksi layanan
- Peningkatan performa
- Dokumentasi yang lebih baik

---

## 📄 Lisensi

MIT License - Lihat LICENSE untuk detail

---

## ⚖️ Disclaimer

Alat ini disediakan sebagai-adanya untuk tujuan pengujian keamanan yang sah dan pendidikan saja. Para penulis tidak bertanggung jawab atas penyalahgunaan atau kerusakan yang disebabkan oleh alat ini. Selalu dapatkan izin sebelum melakukan pengujian keamanan pada sistem atau jaringan apa pun.

---

**Dibuat dengan ❤️ untuk keamanan jaringan yang lebih baik**
