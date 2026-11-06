# Pantau Kuota Dosen & Topik Skripsi JTI Polinema 2026 (Live Crowdsourced)

Web crowdsource real-time untuk memantau status kuota bimbingan riil **81 Dosen JTI Polinema** dan daftar topik skripsi yang sedang dikerjakan mahasiswa. Dirancang khusus untuk mengatasi masalah **false-positive** di sistem SIMTA resmi tanpa perlu login.

---

## 🚀 Fitur Unggulan

1. **Bebas Login (Zero-Friction Access):**
   * Semua mahasiswa dan perwakilan kelas bisa langsung melihat, memfilter, mengupdate status dosen, atau mendaftarkan topik skripsi tanpa perlu akun/password.
2. **Koreksi Riil Lapangan (Anti False-Positive):**
   * Mengatasi kasus di mana SIMTA tampak masih ada sisa kuota, padahal secara riil (chat WA / tatap muka) dosen sudah penuh (misal: Pak Yuri, Pak Yan, dll.).
3. **Pendaftaran Topik Mahasiswa Berjalan:**
   * Mahasiswa yang sudah di-ACC bimbingan bisa mencantumkan judul skripsinya agar teman-teman lain tahu topik apa saja yang sudah mengisi kuota dosen tersebut.
4. **Sistem Konfirmasi Komunitas (Peer Verification):**
   * Tombol `👍 Konfirmasi` untuk menambah skor kepercayaan laporan status dosen.
5. **Anti Race-Condition & Skalabilitas Tinggi:**
   * Menggunakan arsitektur **Append-Only Event Sourcing** dan **PostgreSQL Atomic Stored Procedure** di Supabase sehingga ribuan update simultan tidak akan pernah konflik atau *deadlock*.
6. **One-Click Share ke WhatsApp Kelas:**
   * Siap dibagikan ke grup WhatsApp kelas atau angkatan lengkap dengan tautan web.

---

## 🗄️ Arsitektur Database & Solusi Race Condition

### Mengapa Supabase (PostgreSQL) adalah Pilihan Terbaik?
1. **100% Gratis & Serverless:** Free tier mencakup 500 MB database, 50.000 Monthly Active Users, dan Realtime WebSockets.
2. **Koneksi Langsung dari GitHub Pages:** Tidak butuh server backend Node.js/Python terpisah. Frontend di GitHub Pages bisa langsung membaca dan menulis data ke Supabase menggunakan Public Anon Key dengan aman melalui **Row Level Security (RLS)**.
3. **Pencegahan Race Condition (ACID Concurrency):**
   * Setiap update dari mahasiswa tidak langsung me-overwrite baris secara serentak, melainkan dicatat sebagai *immutable audit log* di tabel `crowdsource_reports`.
   * Stored procedure `submit_crowdsource_report()` mengeksekusi operasi insert log, insert topik, dan update status master dosen dalam **satu transaksi atomik PostgreSQL dengan row-level lock**.

---

## 🛠️ Cara Deploy ke GitHub Pages (Hanya 2 Menit)

### Langkah 1: Buat Repository di GitHub
1. Buka [GitHub New Repository](https://github.com/new).
2. Beri nama repository, misalnya: `pantau-kuota-dosen-jti`.
3. Pilih **Public**.
4. Upload file `index.html` dari folder ini ke branch `main`.

### Langkah 2: Aktifkan GitHub Pages
1. Di repository GitHub Anda, buka tab **Settings** &rarr; **Pages**.
2. Pada bagian **Build and deployment** &rarr; **Branch**, pilih `main` dan folder `/ (root)`.
3. Klik **Save**.
4. Website Anda akan langsung aktif di URL: `https://<username-anda>.github.io/pantau-kuota-dosen-jti/`.

---

## ⚡ Cara Menghubungkan Supabase Cloud (Live Real-Time Sync)

*(Opsional — Tanpa Supabase pun web sudah langsung berfungsi dengan LocalStorage)*

1. Buat project baru gratis di [supabase.com](https://supabase.com).
2. Buka menu **SQL Editor** di dashboard Supabase Anda.
3. Buka file `supabase_schema.sql` di repository ini, salin seluruh kodenya, lalu klik **Run** di Supabase SQL Editor.
   * Ini akan otomatis membuat tabel, stored procedure anti-race condition, RLS policy, dan mengisi awal seluruh data 81 Dosen JTI.
4. Buka menu **Project Settings** &rarr; **API** di Supabase, lalu salin:
   * **Project URL**
   * **Project API Anon Key**
5. Buka web Anda di browser, klik tombol **Database Cloud** di navbar kanan atas, masukkan URL dan Anon Key Anda, lalu klik **Simpan & Hubungkan**.
6. Selesai! Web Anda sekarang terhubung ke database cloud realtime!
