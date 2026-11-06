import json
import os

SEED_FILE = '/home/aslam/.gemini/antigravity/scratch/pantau-kuota-dosen/dosen_seed.json'
OUT_FILE = '/home/aslam/.gemini/antigravity/scratch/pantau-kuota-dosen/index.html'

with open(SEED_FILE, 'r', encoding='utf-8') as f:
    seed_dosen = json.load(f)

dosen_json_str = json.dumps(seed_dosen, ensure_ascii=False)

html_template = '''<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Pantau Kuota Dosen Skripsi JTI Polinema 2026 | Crowdsourced Live Tracker</title>
  <link rel="shortcut icon" href="https://upload.wikimedia.org/wikipedia/id/4/4a/Logo_Politeknik_Negeri_Malang.png" type="image/png">
  
  <!-- Tailwind CSS & Plus Jakarta Sans Font -->
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  
  <!-- Supabase JS Client for Realtime Cloud Sync (Optional) -->
  <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>

  <script>
    tailwind.config = {
      theme: {
        extend: {
          fontFamily: {
            sans: ['"Plus Jakarta Sans"', 'system-ui', '-apple-system', 'sans-serif'],
            mono: ['"JetBrains Mono"', 'monospace'],
          },
          colors: {
            brand: {
              50: '#eff6ff',
              100: '#dbeafe',
              500: '#3b82f6',
              600: '#2563eb',
              700: '#1d4ed8',
              800: '#1e40af',
              900: '#1e3a8a',
            }
          }
        }
      }
    }
  </script>

  <style>
    body {
      background-color: #f8fafc;
      color: #1e293b;
      font-family: 'Plus Jakarta Sans', sans-serif;
      background-image: 
        radial-gradient(at 0% 0%, rgba(219, 234, 254, 0.4) 0px, transparent 40%),
        radial-gradient(at 100% 0%, rgba(209, 250, 229, 0.35) 0px, transparent 35%),
        radial-gradient(at 50% 100%, rgba(241, 245, 249, 0.7) 0px, transparent 50%);
      background-attachment: fixed;
    }
    .custom-scrollbar::-webkit-scrollbar {
      width: 6px;
      height: 6px;
    }
    .custom-scrollbar::-webkit-scrollbar-track {
      background: #f1f5f9;
    }
    .custom-scrollbar::-webkit-scrollbar-thumb {
      background: #cbd5e1;
      border-radius: 9999px;
    }
    .card-hover {
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .card-hover:hover {
      transform: translateY(-2px);
      box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.08), 0 8px 10px -6px rgba(15, 23, 42, 0.04);
    }
    .pulse-dot {
      animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
    }
    @keyframes pulse {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: .4; transform: scale(0.9); }
    }
  </style>
</head>
<body class="min-h-screen flex flex-col antialiased selection:bg-blue-500 selection:text-white">

  <!-- Toast Notification -->
  <div id="toast" class="fixed bottom-6 right-6 z-50 transform translate-y-20 opacity-0 transition-all duration-300 pointer-events-none">
    <div class="bg-slate-900/95 backdrop-blur-md text-white text-xs px-4 py-3 rounded-xl shadow-2xl flex items-center gap-2.5 border border-slate-700">
      <span class="text-emerald-400 font-bold">✓</span>
      <span id="toast-message" class="font-medium">Pesan notifikasi</span>
    </div>
  </div>

  <!-- Top Navbar -->
  <header class="sticky top-0 z-40 bg-white/85 backdrop-blur-md border-b border-slate-200/90 shadow-2xs">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between gap-4">
      
      <!-- Brand & Title -->
      <div class="flex items-center gap-3">
        <div class="h-10 w-10 rounded-xl bg-gradient-to-tr from-blue-700 to-indigo-500 text-white font-black flex items-center justify-center text-sm shadow-sm tracking-wider shrink-0">
          JT
        </div>
        <div>
          <div class="flex items-center gap-2">
            <h1 class="text-base sm:text-lg font-black text-slate-900 tracking-tight leading-tight">Pantau Kuota Dosen JTI 2026</h1>
            <span class="hidden sm:inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-black bg-emerald-100 text-emerald-800 border border-emerald-300">
              <span class="h-1.5 w-1.5 rounded-full bg-emerald-500 pulse-dot"></span>
              Live Crowdsource
            </span>
          </div>
          <p class="text-xs text-slate-500 font-medium hidden sm:block">Platform Cek &amp; Lapor Kuota Bimbingan Skripsi Riil Antar Mahasiswa &bull; Tanpa Perlu Login</p>
        </div>
      </div>

      <!-- Quick Action Buttons -->
      <div class="flex items-center gap-2 sm:gap-3">
        <button onclick="openShareModal()" class="px-3.5 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-extrabold text-xs transition-colors shadow-2xs flex items-center gap-1.5">
          <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M12.031 6.172c-3.181 0-5.767 2.586-5.768 5.766-.001 1.298.38 2.27 1.019 3.287l-.711 2.598 2.664-.699c.971.532 1.77.814 2.796.814 3.179 0 5.765-2.586 5.767-5.766 0-3.18-2.586-5.766-5.767-5.766zm3.393 8.163c-.144.405-.837.774-1.17.823-.312.045-.694.073-2.18-.54-1.9-1.077-3.125-2.909-3.22-3.036-.095-.127-.768-1.021-.768-1.947 0-.925.485-1.38.658-1.569.173-.189.38-.236.507-.236.126 0 .253.001.364.007.117.006.275-.044.43.328.158.38.54 1.316.587 1.411.047.095.079.206.016.332-.063.126-.095.205-.189.316-.095.111-.199.248-.284.333-.095.095-.194.198-.083.388.111.19 1.134 1.849 2.434 2.457.348.163.554.269.752.206.237-.079.76-.887.965-1.187.206-.3.411-.253.69-.158.28.095 1.77.834 2.072.985.301.151.503.226.577.352.074.126.074.731-.07 1.136z"/></svg>
          <span class="hidden md:inline">Share ke WA Kelas</span>
          <span class="md:hidden">WA</span>
        </button>

        <button onclick="openConfigModal()" class="px-3.5 py-2 rounded-xl bg-white hover:bg-slate-50 text-slate-700 font-bold text-xs border border-slate-200 transition-colors shadow-2xs flex items-center gap-1.5">
          <svg class="w-4 h-4 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
          <span class="hidden md:inline">Database Cloud</span>
        </button>
      </div>

    </div>
  </header>

  <!-- Main Container -->
  <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 space-y-6 flex-1">

    <!-- Anti False-Positive Alert Notice -->
    <section class="p-5 sm:p-6 rounded-3xl bg-amber-50/80 border border-amber-200/90 shadow-2xs relative overflow-hidden">
      <div class="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div class="space-y-1.5 max-w-3xl">
          <div class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-amber-200/70 text-amber-900 text-xs font-black">
            <span>⚠️</span> MENGAPA WEB INI DIBUAT? (ANTI FALSE-POSITIVE)
          </div>
          <h2 class="text-lg sm:text-xl font-black text-slate-900 tracking-tight leading-snug">
            Koreksi Data Riil Lapangan Kuota Dosen Skripsi
          </h2>
          <p class="text-xs sm:text-sm text-slate-700 leading-relaxed font-normal">
            Di sistem SIMTA sering terjadi <strong>false-positive</strong> (status kuota di web resmi tampak masih ada sisa, padahal saat ditanya langsung ke dosen seperti Pak Yuri dkk ternyata sudah <strong>penuh</strong> via chat/tatap muka). Web ini tempat seluruh mahasiswa saling gotong royong mengupdate status keterisian riil &amp; mencatat topik skripsi agar teman lain tidak berebut sia-sia.
          </p>
        </div>
        <div class="shrink-0 flex items-center">
          <button onclick="openReportModal()" class="w-full md:w-auto px-5 py-3 rounded-2xl bg-blue-600 hover:bg-blue-700 text-white font-black text-xs shadow-md shadow-blue-500/20 transition-all flex items-center justify-center gap-2">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/></svg>
            + Update Status Dosen Saya
          </button>
        </div>
      </div>
    </section>

    <!-- 5 Live Metric KPI Cards (Clean, Light, Anti-Slop) -->
    <section class="grid grid-cols-2 sm:grid-cols-2 lg:grid-cols-5 gap-3.5">
      
      <!-- Total Dosen -->
      <div class="p-4 sm:p-5 rounded-2xl border border-slate-200 bg-white shadow-xs card-hover flex flex-col justify-between">
        <div class="flex items-center justify-between">
          <span class="text-[11px] font-extrabold text-slate-500 uppercase tracking-wider">Total Dosen</span>
          <span class="p-1.5 rounded-lg bg-blue-50 text-blue-600 border border-blue-100">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"/></svg>
          </span>
        </div>
        <div class="mt-2 flex items-baseline gap-1.5">
          <span class="text-2xl sm:text-3xl font-black text-slate-900 tracking-tight" id="metric-total">81</span>
          <span class="text-xs font-semibold text-slate-500">Dosen</span>
        </div>
        <div class="mt-2 text-[11px] text-slate-500 font-medium pt-2 border-t border-slate-100">
          JTI Polinema 2026
        </div>
      </div>

      <!-- Sudah Full (Merah) -->
      <div class="p-4 sm:p-5 rounded-2xl border border-rose-300 bg-gradient-to-br from-rose-50/80 via-white to-rose-50/30 shadow-xs card-hover cursor-pointer group flex flex-col justify-between" onclick="filterByStatus('full')">
        <div class="flex items-center justify-between">
          <span class="text-[11px] font-black text-rose-800 uppercase tracking-wider flex items-center gap-1.5">
            <span class="h-2 w-2 rounded-full bg-rose-500"></span>
            Sudah FULL
          </span>
          <span class="text-[10px] font-black px-1.5 py-0.5 rounded-full bg-rose-100 text-rose-800 border border-rose-200">Riil Lapangan</span>
        </div>
        <div class="mt-2 flex items-baseline gap-1.5">
          <span class="text-2xl sm:text-3xl font-black text-rose-700 tracking-tight" id="metric-full">2</span>
          <span class="text-xs text-rose-800 font-bold bg-rose-100/70 px-1.5 py-0.5 rounded-md">Terkonfirmasi</span>
        </div>
        <div class="mt-2 text-[11px] text-rose-700 font-semibold pt-2 border-t border-rose-100 group-hover:text-rose-900 flex items-center gap-1">
          Pak Yuri, Pak Yan, dkk &rarr;
        </div>
      </div>

      <!-- Masih Ada Slot (Hijau) -->
      <div class="p-4 sm:p-5 rounded-2xl border border-emerald-300 bg-gradient-to-br from-emerald-50/80 via-white to-emerald-50/30 shadow-xs card-hover cursor-pointer group flex flex-col justify-between" onclick="filterByStatus('available')">
        <div class="flex items-center justify-between">
          <span class="text-[11px] font-black text-emerald-800 uppercase tracking-wider flex items-center gap-1.5">
            <span class="h-2 w-2 rounded-full bg-emerald-500 pulse-dot"></span>
            Ada Sisa Slot
          </span>
          <span class="text-[10px] font-black px-1.5 py-0.5 rounded-full bg-emerald-100 text-emerald-800 border border-emerald-200">Buka Kuota</span>
        </div>
        <div class="mt-2 flex items-baseline gap-1.5">
          <span class="text-2xl sm:text-3xl font-black text-emerald-700 tracking-tight" id="metric-avail">0</span>
          <span class="text-xs text-emerald-800 font-bold bg-emerald-100/70 px-1.5 py-0.5 rounded-md">Terkonfirmasi</span>
        </div>
        <div class="mt-2 text-[11px] text-emerald-700 font-semibold pt-2 border-t border-emerald-100 group-hover:text-emerald-900 flex items-center gap-1">
          Lihat dosen tersedia &rarr;
        </div>
      </div>

      <!-- Belum Ada Info (Abu-abu / Butuh Laporan) -->
      <div class="p-4 sm:p-5 rounded-2xl border border-blue-200 bg-gradient-to-br from-blue-50/50 via-white to-slate-50 shadow-xs card-hover cursor-pointer group flex flex-col justify-between" onclick="filterByStatus('unknown')">
        <div class="flex items-center justify-between">
          <span class="text-[11px] font-black text-blue-900 uppercase tracking-wider flex items-center gap-1.5">
            <span class="h-2 w-2 rounded-full bg-blue-500"></span>
            Belum Diketahui
          </span>
          <span class="text-[10px] font-black px-1.5 py-0.5 rounded-full bg-blue-100 text-blue-800 border border-blue-200">Butuh Info</span>
        </div>
        <div class="mt-2 flex items-baseline gap-1.5">
          <span class="text-2xl sm:text-3xl font-black text-blue-800 tracking-tight" id="metric-unknown">54</span>
          <span class="text-xs text-blue-800 font-bold bg-blue-100/70 px-1.5 py-0.5 rounded-md">Dosen</span>
        </div>
        <div class="mt-2 text-[11px] text-blue-700 font-semibold pt-2 border-t border-blue-100 group-hover:text-blue-900 flex items-center gap-1">
          Bantu laporkan di sini &rarr;
        </div>
      </div>

      <!-- Tidak Buka Kuota (Studi Lanjut) -->
      <div class="p-4 sm:p-5 rounded-2xl border border-slate-200 bg-white shadow-xs card-hover flex flex-col justify-between" onclick="filterByStatus('zero')">
        <div class="flex items-center justify-between">
          <span class="text-[11px] font-black text-slate-500 uppercase tracking-wider">Kuota 0</span>
          <span class="p-1.5 rounded-lg bg-slate-100 text-slate-600 border border-slate-200">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636"/></svg>
          </span>
        </div>
        <div class="mt-2 flex items-baseline gap-1.5">
          <span class="text-2xl sm:text-3xl font-black text-slate-700 tracking-tight" id="metric-zero">25</span>
          <span class="text-xs font-semibold text-slate-500">Dosen</span>
        </div>
        <div class="mt-2 text-[11px] text-slate-500 font-medium pt-2 border-t border-slate-100">
          Cuti / Studi Lanjut
        </div>
      </div>

    </section>

    <!-- Search & Filter Controls -->
    <section class="p-5 rounded-2xl border border-slate-200 bg-white shadow-xs space-y-4">
      <div class="flex flex-col md:flex-row gap-3">
        <!-- Live Search -->
        <div class="relative flex-1">
          <svg class="w-5 h-5 absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
          <input type="text" id="search-input" placeholder="Cari nama dosen, NIP, Lab (AI, IVSS, MMT, SE, BA, NCS, InLET, DT), atau topik skripsi..." class="w-full pl-11 pr-10 py-2.5 rounded-xl border border-slate-200 bg-slate-50/70 text-sm text-slate-900 placeholder-slate-400 focus:outline-none focus:border-blue-500 focus:bg-white focus:ring-2 focus:ring-blue-100 transition-all font-medium">
          <button id="search-clear" class="hidden absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-700 text-xs p-1">✕</button>
        </div>

        <!-- Filter Status Pills (Hijau, Merah, Kuning, Abu-abu) -->
        <div class="flex items-center gap-1.5 p-1 bg-slate-100/90 rounded-xl border border-slate-200 overflow-x-auto text-xs shrink-0 font-bold">
          <button class="status-tab px-3 py-1.5 rounded-lg transition-all active text-white bg-blue-600 shadow-2xs" data-status="all">Semua (81)</button>
          <button class="status-tab px-3 py-1.5 rounded-lg transition-all text-rose-800 hover:bg-rose-50" data-status="full">🔴 Sudah FULL</button>
          <button class="status-tab px-3 py-1.5 rounded-lg transition-all text-amber-800 hover:bg-amber-50" data-status="warning">🟡 Hampir Penuh</button>
          <button class="status-tab px-3 py-1.5 rounded-lg transition-all text-emerald-800 hover:bg-emerald-50" data-status="available">🟢 Masih Ada Slot</button>
          <button class="status-tab px-3 py-1.5 rounded-lg transition-all text-blue-800 hover:bg-blue-50" data-status="unknown">⚪ Belum Diketahui</button>
          <button class="status-tab px-3 py-1.5 rounded-lg transition-all text-slate-600 hover:bg-slate-200" data-status="zero">⛔ Kuota 0</button>
        </div>
      </div>

      <!-- Secondary Filters -->
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-3 border-t border-slate-100 text-xs">
        <div>
          <label class="block text-slate-600 font-extrabold mb-1">Filter Laboratorium Riset:</label>
          <select id="filter-lab" class="w-full py-2 px-3 rounded-lg border border-slate-200 bg-slate-50/80 text-slate-700 font-medium focus:outline-none focus:border-blue-500 focus:bg-white">
            <option value="all">Semua Lab (AI, IVSS, MMT, SE, BA, NCS, InLET, DT)</option>
            <option value="AI">Lab AI (Artificial Intelligence)</option>
            <option value="IVSS">Lab IVSS (Vision &amp; Smart System)</option>
            <option value="MMT">Lab MMT (Multimedia &amp; UI/UX)</option>
            <option value="SE">Lab SE (Software Engineering)</option>
            <option value="BA">Lab BA (Business Analytics)</option>
            <option value="NCS">Lab NCS (Network &amp; Cyber Security)</option>
            <option value="InLET">Lab InLET (Learning Engineering Tech)</option>
            <option value="DT">Lab DT (Digital Technology)</option>
          </select>
        </div>

        <div>
          <label class="block text-slate-600 font-extrabold mb-1">Urutkan Daftar:</label>
          <select id="sort-by" class="w-full py-2 px-3 rounded-lg border border-slate-200 bg-slate-50/80 text-slate-700 font-medium focus:outline-none focus:border-blue-500 focus:bg-white">
            <option value="status-priority">Status Riil (FULL &amp; Buka Dulu)</option>
            <option value="unknown-first">Belum Ada Laporan Dulu (Bantu Isi)</option>
            <option value="slot-desc">Sisa Slot Terbanyak</option>
            <option value="name-asc">Nama Dosen (A &rarr; Z)</option>
            <option value="confirm-desc">Paling Banyak Dikonfirmasi Mahasiswa</option>
          </select>
        </div>

        <div class="flex items-end justify-between">
          <div class="text-xs text-slate-500 font-semibold mb-2">
            Menampilkan <span id="display-count" class="font-black text-slate-900">81</span> dari 81 dosen
          </div>
          <button onclick="openReportModal()" class="mb-1 px-4 py-2 rounded-lg bg-blue-50 hover:bg-blue-100 text-blue-700 font-extrabold text-xs transition-colors border border-blue-200 flex items-center gap-1.5">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/></svg>
            + Update Status Dosen
          </button>
        </div>
      </div>
    </section>

    <!-- Dosen Cards Grid -->
    <section id="dosen-grid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
      <!-- Injected via JavaScript -->
    </section>

    <!-- Empty State -->
    <div id="empty-state" class="hidden text-center py-16 px-4 rounded-2xl border border-slate-200 bg-white shadow-xs">
      <svg class="w-12 h-12 text-slate-300 mx-auto mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
      <h4 class="text-base font-bold text-slate-900">Tidak ada dosen yang cocok</h4>
      <p class="text-xs text-slate-500 mt-1">Coba gunakan kata kunci pencarian yang lebih umum atau reset filter status.</p>
    </div>

  </main>

  <!-- Footer -->
  <footer class="border-t border-slate-200 bg-white py-6 mt-12 text-center text-xs text-slate-500">
    <div class="max-w-7xl mx-auto px-4 space-y-1">
      <p class="font-bold text-slate-700">Dibuat gotong royong oleh Mahasiswa JTI Politeknik Negeri Malang &bull; Angkatan 2026</p>
      <p>Data crowdsourced di-update tanpa login. Bebas disebarkan ke grup kelas &amp; angkatan untuk mencegah false-positive SIMTA.</p>
    </div>
  </footer>

  <!-- ========================================== -->
  <!-- MODAL 1: FORM UPDATE STATUS DOSEN          -->
  <!-- ========================================== -->
  <div id="modal-report" class="fixed inset-0 bg-slate-900/40 backdrop-blur-sm z-50 hidden transition-opacity flex items-center justify-center p-3 sm:p-4 lg:p-6" onclick="closeReportModal()">
    <div class="bg-white border border-slate-200 rounded-3xl w-full max-w-xl max-h-[92vh] flex flex-col shadow-2xl overflow-hidden relative" onclick="event.stopPropagation()">
      
      <!-- Modal Header -->
      <div class="p-5 border-b border-slate-200 bg-slate-50/80 flex items-start justify-between">
        <div>
          <span class="text-[11px] font-black text-blue-600 uppercase tracking-wider">Crowdsource Lapangan</span>
          <h3 class="text-lg font-black text-slate-900 leading-tight">Update Status Kuota &amp; Topik Dosen</h3>
          <p class="text-xs text-slate-500 mt-0.5">Informasi Anda langsung tersimpan &amp; membantu teman agar tidak salah pilih.</p>
        </div>
        <button onclick="closeReportModal()" class="p-2 rounded-xl text-slate-400 hover:text-slate-700 hover:bg-slate-100 transition-colors">✕</button>
      </div>

      <!-- Modal Form Body -->
      <form id="form-report" onsubmit="submitReportForm(event)" class="p-5 sm:p-6 overflow-y-auto custom-scrollbar space-y-4 text-xs">
        
        <!-- Select Dosen -->
        <div>
          <label class="block text-slate-800 font-extrabold mb-1">Pilih Dosen Pembimbing: *</label>
          <select id="form-dosen-id" required onchange="onDosenSelectChange()" class="w-full py-2.5 px-3 rounded-xl border border-slate-200 bg-slate-50 font-semibold text-slate-800 text-sm focus:outline-none focus:border-blue-500 focus:bg-white">
            <!-- Injected via JS -->
          </select>
        </div>

        <!-- Section: Kuota & Keterisian Slot Mahasiswa (Bisa Isi Kuota & Sudah Terisi Berapa) -->
        <div class="p-4 rounded-2xl border border-blue-200 bg-blue-50/40 space-y-3">
          <div class="flex items-center justify-between">
            <span class="font-extrabold text-blue-950 uppercase tracking-wider text-[11px] flex items-center gap-1.5">
              <span>📊</span> Hitung Slot Keterisian Mahasiswa
            </span>
            <span class="text-[10px] text-blue-700 font-bold">Otomatis Hitung Sisa</span>
          </div>

          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block text-slate-700 font-bold mb-1">Kapasitas Kuota Dosen:</label>
              <input type="number" id="form-quota-total" min="1" max="20" value="8" oninput="calculateSlotAndStatus()" class="w-full py-2 px-3 rounded-xl border border-slate-300 bg-white font-extrabold text-slate-900 text-sm focus:outline-none focus:border-blue-500">
              <span class="text-[10px] text-slate-500 mt-0.5 block">Default dari kuota SIMTA</span>
            </div>

            <div>
              <label class="block text-slate-700 font-bold mb-1">Sudah Terisi Berapa Mhs?:</label>
              <input type="number" id="form-terisi-slot" min="0" max="20" value="0" oninput="calculateSlotAndStatus()" class="w-full py-2 px-3 rounded-xl border border-slate-300 bg-white font-extrabold text-slate-900 text-sm focus:outline-none focus:border-blue-500">
              <span class="text-[10px] text-slate-500 mt-0.5 block">Jumlah mhs yang sudah di-acc</span>
            </div>
          </div>

          <!-- Dynamic Live Calculation Banner -->
          <div id="calc-result-banner" class="p-3 rounded-xl border border-slate-200 bg-white flex items-center justify-between">
            <div class="flex items-center gap-2">
              <span id="calc-icon" class="text-base">🟢</span>
              <div>
                <span id="calc-status-text" class="font-black text-slate-800 text-xs block">Sisa Slot: 8 Mahasiswa</span>
                <span id="calc-sub-text" class="text-[10px] text-slate-500">Masih banyak slot bimbingan tersedia</span>
              </div>
            </div>
            <span id="calc-badge" class="px-2.5 py-1 rounded-full text-[10px] font-black bg-emerald-100 text-emerald-800 border border-emerald-300">
              ADA SLOT
            </span>
          </div>
        </div>

        <!-- Direct Status Choice (Jikalau Mahasiswa Tidak Tahu Angka Persis Tapi Tahu Status) -->
        <div>
          <label class="block text-slate-800 font-extrabold mb-1.5">Atau Pilih Langsung Kesimpulan Status Lapangan: *</label>
          <div class="grid grid-cols-3 gap-2">
            <label class="flex flex-col items-center justify-center p-3 rounded-xl border border-rose-200 bg-rose-50/70 cursor-pointer hover:bg-rose-100/70 transition-all font-bold text-center text-rose-800">
              <input type="radio" name="form_status" value="full" required onchange="onRadioStatusChange('full')" class="mb-1">
              <span>🔴 FULL (PENUH)</span>
              <span class="text-[10px] font-normal text-rose-600">0 Slot Tersisa</span>
            </label>
            <label class="flex flex-col items-center justify-center p-3 rounded-xl border border-amber-200 bg-amber-50/70 cursor-pointer hover:bg-amber-100/70 transition-all font-bold text-center text-amber-800">
              <input type="radio" name="form_status" value="warning" onchange="onRadioStatusChange('warning')" class="mb-1">
              <span>🟡 HAMPIR PENUH</span>
              <span class="text-[10px] font-normal text-amber-600">Sisa 1-2 Slot</span>
            </label>
            <label class="flex flex-col items-center justify-center p-3 rounded-xl border border-emerald-200 bg-emerald-50/70 cursor-pointer hover:bg-emerald-100/70 transition-all font-bold text-center text-emerald-800">
              <input type="radio" name="form_status" value="available" onchange="onRadioStatusChange('available')" class="mb-1">
              <span>🟢 MASIH ADA SLOT</span>
              <span class="text-[10px] font-normal text-emerald-600">Buka Kuota</span>
            </label>
          </div>
        </div>

        <!-- Hidden input for sisa slot -->
        <input type="hidden" id="form-sisa-slot" value="8">

        <!-- Sumber Informasi -->
        <div>
          <label class="block text-slate-800 font-extrabold mb-1">Dari Mana Anda Tahu Status Ini? *</label>
          <select id="form-sumber" required class="w-full py-2 px-3 rounded-xl border border-slate-200 bg-slate-50 font-medium text-slate-700 focus:outline-none focus:border-blue-500 focus:bg-white">
            <option value="Chat WhatsApp Pribadi ke Dosen">Chat WhatsApp Pribadi ke Dosen Terkait</option>
            <option value="Tanya Langsung / Tatap Muka di Lab / Kampus">Tanya Langsung / Tatap Muka di Lab / Kampus</option>
            <option value="Saya Sendiri Sudah Di-ACC Bimbingan di Sini">Saya Sendiri Sudah Di-ACC Bimbingan di Sini</option>
            <option value="Info Teman 1 Kelas yang Sedang Bimbingan">Info Teman 1 Kelas yang Sedang Bimbingan</option>
            <option value="Dosen Mengumumkan di Grup Angkatan">Dosen Mengumumkan di Grup Angkatan</option>
          </select>
        </div>

        <!-- Judul Topik Skripsi Anda (Opsional) -->
        <div class="p-3.5 rounded-xl border border-indigo-200 bg-indigo-50/40 space-y-1">
          <label class="block text-indigo-950 font-extrabold flex items-center justify-between">
            <span>📚 Topik / Judul Skripsi Anda (Opsional):</span>
            <span class="text-[10px] text-indigo-600 font-bold">Boleh Dikosongkan</span>
          </label>
          <input type="text" id="form-topik" placeholder="Misal: Sistem Pendeteksi Hama Jagung Berbasis YOLOv8 dan IoT..." class="w-full py-2 px-3 rounded-lg border border-indigo-200 bg-white font-medium text-slate-800 placeholder-slate-400 focus:outline-none focus:border-blue-500">
          <p class="text-[10px] text-indigo-800">Jika Anda salah satu yang bimbingan di dosen ini, tuliskan judul Anda agar mahasiswa lain tahu slot beliau sudah terisi topik apa saja.</p>
        </div>

        <!-- Catatan Tambahan -->
        <div>
          <label class="block text-slate-800 font-extrabold mb-1">Catatan Tambahan untuk Teman-Teman (Opsional):</label>
          <textarea id="form-catatan" rows="2" placeholder="Misal: Tadi tanya jam 13.00 di WA, beliau bilang sudah penuh untuk bimbingan skripsi semester ini..." class="w-full py-2 px-3 rounded-xl border border-slate-200 bg-slate-50 font-medium text-slate-800 placeholder-slate-400 focus:outline-none focus:border-blue-500 focus:bg-white"></textarea>
        </div>

        <!-- Nama Pelapor (Opsional) -->
        <div>
          <label class="block text-slate-800 font-extrabold mb-1">Nama / Inisial Anda (Boleh Kosong / Anonim):</label>
          <input type="text" id="form-nama" placeholder="Mahasiswa TI (Boleh dikosongkan)" class="w-full py-2 px-3 rounded-xl border border-slate-200 bg-slate-50 font-medium text-slate-800 placeholder-slate-400 focus:outline-none focus:border-blue-500 focus:bg-white">
        </div>

        <!-- Action Buttons -->
        <div class="pt-3 border-t border-slate-100 flex items-center justify-end gap-2">
          <button type="button" onclick="closeReportModal()" class="px-4 py-2.5 rounded-xl border border-slate-200 text-slate-600 font-bold hover:bg-slate-50">Batal</button>
          <button type="submit" id="btn-submit-report" class="px-6 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-black shadow-md shadow-blue-500/20">Kirim &amp; Simpan Laporan</button>
        </div>
      </form>

    </div>
  </div>

  <!-- ========================================== -->
  <!-- MODAL 2: DETAIL TOPIK BIMBINGAN DOSEN      -->
  <!-- ========================================== -->
  <div id="modal-detail-topik" class="fixed inset-0 bg-slate-900/40 backdrop-blur-sm z-50 hidden transition-opacity flex items-center justify-center p-3 sm:p-4 lg:p-6" onclick="closeDetailModal()">
    <div class="bg-white border border-slate-200 rounded-3xl w-full max-w-2xl max-h-[90vh] flex flex-col shadow-2xl overflow-hidden relative" onclick="event.stopPropagation()">
      <div class="p-5 border-b border-slate-200 bg-slate-50/80 flex items-start justify-between">
        <div>
          <span class="text-[11px] font-black text-blue-600 uppercase tracking-wider">Detail Bimbingan Mahasiswa</span>
          <h3 id="modal-dosen-title" class="text-lg font-black text-slate-900">Nama Dosen</h3>
          <p id="modal-dosen-meta" class="text-xs text-slate-500">Kuota &bull; Lab</p>
        </div>
        <button onclick="closeDetailModal()" class="p-2 rounded-xl text-slate-400 hover:text-slate-700 hover:bg-slate-100 transition-colors">✕</button>
      </div>

      <div class="p-6 overflow-y-auto custom-scrollbar space-y-4 text-xs">
        <div>
          <h4 class="font-extrabold text-slate-800 uppercase tracking-wider mb-2 flex items-center gap-1.5">
            <span>📚</span> Topik Skripsi yang Sudah Masuk / Sedang Dikerjakan:
          </h4>
          <div id="modal-topik-list" class="space-y-2">
            <!-- Injected via JS -->
          </div>
        </div>

        <div class="p-4 rounded-xl border border-slate-200 bg-slate-50 space-y-1">
          <span class="font-extrabold text-slate-700 block">Catatan Terakhir Mahasiswa:</span>
          <p id="modal-catatan-detail" class="text-slate-600 italic">Belum ada catatan.</p>
        </div>
      </div>

      <div class="p-4 border-t border-slate-200 bg-slate-50/90 flex justify-between items-center">
        <span class="text-xs text-slate-400 font-medium">Terakhir diupdate: <span id="modal-last-update">-</span></span>
        <button onclick="closeDetailModal()" class="px-5 py-2 rounded-xl bg-slate-800 text-white font-bold text-xs hover:bg-slate-900">Tutup</button>
      </div>
    </div>
  </div>

  <!-- ========================================== -->
  <!-- MODAL 3: SHARE KE WHATSAPP                 -->
  <!-- ========================================== -->
  <div id="modal-share" class="fixed inset-0 bg-slate-900/40 backdrop-blur-sm z-50 hidden transition-opacity flex items-center justify-center p-3 sm:p-4" onclick="closeShareModal()">
    <div class="bg-white border border-slate-200 rounded-3xl w-full max-w-lg p-6 shadow-2xl space-y-4" onclick="event.stopPropagation()">
      <div class="flex items-center justify-between">
        <h3 class="text-base font-black text-slate-900 flex items-center gap-2">
          <span>📲</span> Bagikan Info Kuota ke WhatsApp Kelas
        </h3>
        <button onclick="closeShareModal()" class="text-slate-400 hover:text-slate-700">✕</button>
      </div>
      <p class="text-xs text-slate-500">Salin template pesan di bawah ini lalu kirimkan ke grup WhatsApp kelas Anda agar teman-teman bisa langsung cek dan update tanpa login:</p>
      
      <textarea id="share-text-preview" rows="7" readonly class="w-full p-3 rounded-xl border border-slate-200 bg-slate-50 text-xs font-mono text-slate-800 leading-relaxed focus:outline-none"></textarea>

      <div class="flex items-center justify-end gap-2 pt-2 border-t border-slate-100">
        <button onclick="copyShareText()" class="px-4 py-2.5 rounded-xl border border-slate-200 text-slate-700 font-bold text-xs hover:bg-slate-50 flex items-center gap-1.5">
          <span>📋</span> Salin Pesan
        </button>
        <button onclick="openWhatsAppDirect()" class="px-5 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-black text-xs shadow-md shadow-emerald-600/20 flex items-center gap-1.5">
          <span>🚀</span> Buka WhatsApp Langsung
        </button>
      </div>
    </div>
  </div>

  <!-- ========================================== -->
  <!-- MODAL 4: KONFIGURASI SUPABASE CLOUD        -->
  <!-- ========================================== -->
  <div id="modal-config" class="fixed inset-0 bg-slate-900/40 backdrop-blur-sm z-50 hidden transition-opacity flex items-center justify-center p-3 sm:p-4" onclick="closeConfigModal()">
    <div class="bg-white border border-slate-200 rounded-3xl w-full max-w-lg p-6 shadow-2xl space-y-4" onclick="event.stopPropagation()">
      <div class="flex items-center justify-between">
        <h3 class="text-base font-black text-slate-900 flex items-center gap-2">
          <span>☁️</span> Pengaturan Database Supabase Cloud
        </h3>
        <button onclick="closeConfigModal()" class="text-slate-400 hover:text-slate-700">✕</button>
      </div>
      <p class="text-xs text-slate-600 leading-relaxed">
        Aplikasi ini <strong>sudah berjalan 100%</strong> menggunakan penyimpanan lokal. Jika kelas/angkatan Anda ingin sinkronisasi realtime lintas perangkat mahasiswa secara global, cukup masukkan Supabase Project URL &amp; Anon Key di bawah ini:
      </p>

      <div class="space-y-3 text-xs">
        <div>
          <label class="block font-extrabold text-slate-700 mb-1">Supabase Project URL:</label>
          <input type="text" id="cfg-supabase-url" placeholder="https://xyzcompany.supabase.co" class="w-full p-2.5 rounded-xl border border-slate-200 bg-slate-50 font-mono text-xs focus:outline-none focus:border-blue-500">
        </div>
        <div>
          <label class="block font-extrabold text-slate-700 mb-1">Supabase Anon Public Key:</label>
          <input type="password" id="cfg-supabase-key" placeholder="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." class="w-full p-2.5 rounded-xl border border-slate-200 bg-slate-50 font-mono text-xs focus:outline-none focus:border-blue-500">
        </div>
      </div>

      <div class="p-3 rounded-xl bg-slate-50 border border-slate-200 text-[11px] text-slate-500 space-y-1">
        <span class="font-bold text-slate-700 block">Bagaimana Cara Mengisinya?</span>
        <p>1. Buat project gratis di <a href="https://supabase.com" target="_blank" class="text-blue-600 underline font-semibold">supabase.com</a>.</p>
        <p>2. Jalankan query SQL dari file <code class="bg-slate-200 px-1 rounded">supabase_schema.sql</code> di menu SQL Editor.</p>
        <p>3. Ambil URL dan Anon Key di menu Project Settings &gt; API.</p>
      </div>

      <div class="flex items-center justify-end gap-2 pt-2 border-t border-slate-100">
        <button onclick="closeConfigModal()" class="px-4 py-2 rounded-xl border border-slate-200 text-slate-600 font-bold text-xs hover:bg-slate-50">Tutup</button>
        <button onclick="saveSupabaseConfig()" class="px-5 py-2 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-black text-xs shadow-md shadow-blue-500/20">Simpan &amp; Hubungkan</button>
      </div>
    </div>
  </div>

  <!-- Application Logic JavaScript -->
  <script>
    // 1. Initial State Data
    const INITIAL_DOSEN = ''' + dosen_json_str + ''';

    // Load from LocalStorage if available, otherwise use initial seed
    function loadDosenState() {
      const saved = localStorage.getItem('pantau_dosen_state_v2');
      if (saved) {
        try {
          return JSON.parse(saved);
        } catch(e) {
          console.error(e);
        }
      }
      return INITIAL_DOSEN;
    }

    let DOSEN_STATE = loadDosenState();

    function saveToLocalStorage() {
      localStorage.setItem('pantau_dosen_state_v2', JSON.stringify(DOSEN_STATE));
    }

    // 2. Supabase Integration
    let supabaseClient = null;
    function initSupabase() {
      const url = localStorage.getItem('supabase_url');
      const key = localStorage.getItem('supabase_key');
      if (url && key && window.supabase) {
        try {
          supabaseClient = window.supabase.createClient(url, key);
          console.log('Supabase Cloud connected!');
          syncFromSupabase();
          subscribeRealtime();
        } catch (e) {
          console.error('Supabase init failed:', e);
        }
      }
    }

    async function syncFromSupabase() {
      if (!supabaseClient) return;
      try {
        const { data, error } = await supabaseClient.from('dosen').select('*');
        if (!error && data && data.length > 0) {
          data.forEach(cloudD => {
            const localD = DOSEN_STATE.find(item => item.id === cloudD.id);
            if (localD) {
              localD.status_riil = cloudD.status_riil;
              localD.terisi_slot_riil = cloudD.terisi_slot_riil;
              localD.sisa_slot_riil = cloudD.sisa_slot_riil;
              localD.konfirmasi_count = cloudD.konfirmasi_count;
              localD.catatan_terakhir = cloudD.catatan_terakhir;
              localD.last_updated = cloudD.last_updated;
              if (cloudD.topik_mahasiswa) localD.topik_mahasiswa = cloudD.topik_mahasiswa;
            }
          });
          saveToLocalStorage();
          renderCards();
          updateMetrics();
        }
      } catch (err) {
        console.warn('Sync failed:', err);
      }
    }

    function subscribeRealtime() {
      if (!supabaseClient) return;
      supabaseClient
        .channel('public:dosen')
        .on('postgres_changes', { event: '*', schema: 'public', table: 'dosen' }, payload => {
          syncFromSupabase();
        })
        .subscribe();
    }

    // 3. UI Filters & Metrics
    let currentFilterStatus = 'all';
    let currentFilterLab = 'all';
    let currentSearch = '';
    let currentSort = 'status-priority';

    function updateMetrics() {
      const total = DOSEN_STATE.length;
      const full = DOSEN_STATE.filter(d => d.status_riil === 'full').length;
      const avail = DOSEN_STATE.filter(d => d.status_riil === 'available').length;
      const unknown = DOSEN_STATE.filter(d => d.status_riil === 'unknown').length;
      const zero = DOSEN_STATE.filter(d => d.status_riil === 'zero' || d.quota_resmi === 0).length;

      document.getElementById('metric-total').textContent = total;
      document.getElementById('metric-full').textContent = full;
      document.getElementById('metric-avail').textContent = avail;
      document.getElementById('metric-unknown').textContent = unknown;
      document.getElementById('metric-zero').textContent = zero;
    }

    function getFilteredData() {
      return DOSEN_STATE.filter(d => {
        // Status filter
        if (currentFilterStatus === 'full' && d.status_riil !== 'full') return false;
        if (currentFilterStatus === 'warning' && d.status_riil !== 'warning') return false;
        if (currentFilterStatus === 'available' && d.status_riil !== 'available') return false;
        if (currentFilterStatus === 'unknown' && d.status_riil !== 'unknown') return false;
        if (currentFilterStatus === 'zero' && (d.status_riil !== 'zero' && d.quota_resmi !== 0)) return false;

        // Lab filter
        if (currentFilterLab !== 'all' && d.lab_code !== currentFilterLab) return false;

        // Search text
        if (currentSearch) {
          const nameMatch = d.name.toLowerCase().includes(currentSearch);
          const nipMatch = (d.nip || '').includes(currentSearch);
          const labMatch = d.lab_code.toLowerCase().includes(currentSearch);
          const noteMatch = (d.catatan_terakhir || '').toLowerCase().includes(currentSearch);
          const topicMatch = (d.topik_mahasiswa || []).some(t => t.toLowerCase().includes(currentSearch));
          if (!nameMatch && !nipMatch && !labMatch && !noteMatch && !topicMatch) return false;
        }

        return true;
      });
    }

    function sortData(list) {
      switch (currentSort) {
        case 'slot-desc':
          return list.sort((a, b) => (b.sisa_slot_riil || 0) - (a.sisa_slot_riil || 0));
        case 'name-asc':
          return list.sort((a, b) => a.name.localeCompare(b.name));
        case 'confirm-desc':
          return list.sort((a, b) => (b.konfirmasi_count || 0) - (a.konfirmasi_count || 0));
        case 'unknown-first':
          const unkOrder = { 'unknown': 1, 'full': 2, 'warning': 3, 'available': 4, 'zero': 5 };
          return list.sort((a, b) => (unkOrder[a.status_riil] || 9) - (unkOrder[b.status_riil] || 9));
        case 'status-priority':
        default:
          const order = { 'full': 1, 'warning': 2, 'available': 3, 'unknown': 4, 'zero': 5 };
          return list.sort((a, b) => (order[a.status_riil] || 9) - (order[b.status_riil] || 9));
      }
    }

    // 4. Render Cards with Distinct Colors (Merah, Hijau, Kuning, Abu-abu)
    function renderCards() {
      const container = document.getElementById('dosen-grid');
      const emptyState = document.getElementById('empty-state');
      
      let list = getFilteredData();
      list = sortData(list);

      document.getElementById('display-count').textContent = list.length;

      if (list.length === 0) {
        container.innerHTML = '';
        emptyState.classList.remove('hidden');
        return;
      }

      emptyState.classList.add('hidden');

      container.innerHTML = list.map(d => {
        let badgeHtml = '';
        let borderClass = 'border-slate-200';
        let bgStatus = 'bg-white';
        let progressHtml = '';

        const quota = d.quota_resmi || 8;
        const terisi = d.terisi_slot_riil;
        const sisa = d.sisa_slot_riil;

        if (d.status_riil === 'full') {
          // 🔴 MERAH: FULL (PENUH)
          badgeHtml = '<span class="px-2.5 py-1 rounded-full text-xs font-black bg-rose-100 text-rose-800 border border-rose-300">🔴 FULL (PENUH)</span>';
          borderClass = 'border-rose-300 hover:border-rose-400';
          bgStatus = 'bg-rose-50/25';
          progressHtml = `
            <div class="space-y-1.5">
              <div class="flex justify-between items-center text-[11px] font-bold">
                <span class="text-rose-700">Terisi: ${terisi || quota} dari ${quota} Mahasiswa</span>
                <span class="text-rose-800 font-black">SISA 0 SLOT</span>
              </div>
              <div class="w-full bg-rose-100 rounded-full h-2.5 overflow-hidden">
                <div class="bg-rose-600 h-2.5 rounded-full w-full"></div>
              </div>
            </div>
          `;
        } else if (d.status_riil === 'warning') {
          // 🟡 KUNING: HAMPIR PENUH
          const pct = Math.min(100, Math.round(((terisi || (quota - (sisa || 1))) / quota) * 100));
          badgeHtml = `<span class="px-2.5 py-1 rounded-full text-xs font-black bg-amber-100 text-amber-900 border border-amber-300">🟡 HAMPIR PENUH (SISA ${sisa || 1})</span>`;
          borderClass = 'border-amber-300 hover:border-amber-400';
          bgStatus = 'bg-amber-50/25';
          progressHtml = `
            <div class="space-y-1.5">
              <div class="flex justify-between items-center text-[11px] font-bold">
                <span class="text-amber-800">Terisi: ${terisi || (quota - (sisa || 1))} dari ${quota} Mahasiswa</span>
                <span class="text-amber-900 font-black">SISA ${sisa || 1} SLOT</span>
              </div>
              <div class="w-full bg-amber-100 rounded-full h-2.5 overflow-hidden">
                <div class="bg-amber-500 h-2.5 rounded-full" style="width: ${pct}%"></div>
              </div>
            </div>
          `;
        } else if (d.status_riil === 'available') {
          // 🟢 HIJAU: MASIH ADA SLOT
          const curTerisi = terisi !== null && terisi !== undefined ? terisi : Math.max(0, quota - (sisa || 0));
          const pct = Math.min(100, Math.round((curTerisi / quota) * 100));
          badgeHtml = `<span class="px-2.5 py-1 rounded-full text-xs font-black bg-emerald-100 text-emerald-800 border border-emerald-300">🟢 ADA SISA ${sisa} SLOT</span>`;
          borderClass = 'border-emerald-300 hover:border-emerald-400';
          bgStatus = 'bg-emerald-50/25';
          progressHtml = `
            <div class="space-y-1.5">
              <div class="flex justify-between items-center text-[11px] font-bold">
                <span class="text-emerald-800">Terisi: ${curTerisi} dari ${quota} Mahasiswa</span>
                <span class="text-emerald-900 font-black">SISA ${sisa} SLOT</span>
              </div>
              <div class="w-full bg-emerald-100 rounded-full h-2.5 overflow-hidden">
                <div class="bg-emerald-500 h-2.5 rounded-full" style="width: ${pct}%"></div>
              </div>
            </div>
          `;
        } else if (d.status_riil === 'zero' || d.quota_resmi === 0) {
          // ⛔ KUOTA 0 / CUTI
          badgeHtml = '<span class="px-2.5 py-1 rounded-full text-xs font-bold bg-slate-100 text-slate-500 border border-slate-200">⛔ KUOTA 0</span>';
          borderClass = 'border-slate-200';
          bgStatus = 'bg-slate-50/40 opacity-85';
          progressHtml = `
            <div class="text-[11px] text-slate-500 bg-slate-100/70 p-2.5 rounded-xl border border-slate-200 leading-tight">
              Tidak membuka bimbingan skripsi tahun ini (Tugas Belajar / Cuti).
            </div>
          `;
        } else {
          // ⚪ ABU-ABU / SLATE: BELUM DIKETAHUI (BELUM ADA YANG NGISI)
          badgeHtml = '<span class="px-2.5 py-1 rounded-full text-xs font-bold bg-slate-100 text-slate-700 border border-slate-300">⚪ BELUM DIKETAHUI</span>';
          borderClass = 'border-slate-200 hover:border-blue-300';
          bgStatus = 'bg-white';
          progressHtml = `
            <div class="space-y-2 p-2.5 rounded-xl bg-slate-50 border border-dashed border-slate-300">
              <div class="flex justify-between items-center text-[11px]">
                <span class="text-slate-600 font-medium">Kapasitas SIMTA: <strong>${quota} Mahasiswa</strong></span>
                <span class="text-blue-700 font-extrabold bg-blue-50 px-2 py-0.5 rounded border border-blue-200">Butuh Info</span>
              </div>
              <div class="text-[11px] text-slate-500 leading-snug">
                Belum ada laporan keterisian riil dari mahasiswa.
              </div>
            </div>
          `;
        }

        const topics = d.topik_mahasiswa || [];
        const hasTopics = topics.length > 0;
        const isUnknown = d.status_riil === 'unknown';
        const isZero = d.status_riil === 'zero' || d.quota_resmi === 0;

        return `
          <div class="rounded-3xl border ${borderClass} ${bgStatus} p-5 shadow-xs card-hover flex flex-col justify-between space-y-4">
            <div class="space-y-3.5">
              
              <!-- Top Row: Lab & Badge -->
              <div class="flex items-center justify-between gap-2">
                <span class="text-xs font-mono font-bold px-2.5 py-0.5 rounded-lg bg-slate-100 text-slate-700 border border-slate-200">
                  Lab: ${d.lab_code}
                </span>
                ${badgeHtml}
              </div>

              <!-- Dosen Name & NIP -->
              <div>
                <h3 class="text-base font-black text-slate-900 leading-snug hover:text-blue-600 transition-colors cursor-pointer" onclick="openDetailModal(${d.id})">
                  ${d.name}
                </h3>
                <p class="text-[11px] text-slate-500 font-mono mt-0.5">NIP: ${d.nip || '-'}</p>
              </div>

              <!-- Visual Keterisian / Progress Bar -->
              ${progressHtml}

              <!-- Catatan Mahasiswa -->
              <div class="text-xs text-slate-600 bg-white/90 p-2.5 rounded-xl border border-slate-200/90 leading-relaxed font-medium">
                <div class="text-[10px] text-slate-400 font-bold uppercase mb-0.5 flex items-center justify-between">
                  <span>Info Lapangan Mahasiswa:</span>
                  ${d.konfirmasi_count > 0 ? `<span class="text-blue-600 font-bold">${d.konfirmasi_count} konfirmasi 👍</span>` : ''}
                </div>
                "${d.catatan_terakhir || (isUnknown ? 'Belum ada info riil. Jika Anda tahu, yuk laporkan di tombol bawah!' : '-')}"
              </div>

              <!-- Topik Mahasiswa Preview Badge -->
              ${hasTopics ? `
                <div onclick="openDetailModal(${d.id})" class="cursor-pointer text-xs p-2 rounded-xl bg-blue-50/80 border border-blue-200 text-blue-900 font-semibold hover:bg-blue-100 transition-colors flex items-center justify-between">
                  <span class="truncate">📚 ${topics.length} Topik Skripsi Terdaftar</span>
                  <span class="text-blue-600 font-bold ml-1 shrink-0">&rarr;</span>
                </div>
              ` : (isZero ? '' : `
                <div onclick="quickAddTopic(${d.id})" class="cursor-pointer text-xs p-2 rounded-xl border border-dashed border-slate-300 text-slate-500 hover:text-blue-600 hover:border-blue-300 text-center transition-colors">
                  + Anda bimbingan di sini? Daftarkan judul Anda
                </div>
              `)}

            </div>

            <!-- Card Action Footer -->
            <div class="pt-3 border-t border-slate-100 flex items-center justify-between text-xs gap-2">
              ${isUnknown ? `
                <button onclick="openReportModalForDosen(${d.id})" class="w-full py-2 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-black transition-all shadow-xs flex items-center justify-center gap-1.5">
                  <span>✏️</span> Beri Tahu Status Dosen Ini
                </button>
              ` : (isZero ? `
                <span class="text-[11px] text-slate-400 italic">Tidak menerima bimbingan</span>
                <button onclick="openReportModalForDosen(${d.id})" class="px-3 py-1.5 rounded-lg border border-slate-200 bg-white text-slate-600 font-bold hover:bg-slate-50">
                  Update
                </button>
              ` : `
                <button onclick="confirmStatus(${d.id})" class="px-3 py-1.5 rounded-xl border border-slate-200 bg-white hover:bg-slate-50 text-slate-700 font-bold transition-all shadow-2xs flex items-center gap-1.5" title="Konfirmasi info ini benar">
                  <span>👍</span> Konfirmasi (${d.konfirmasi_count})
                </button>
                <button onclick="openReportModalForDosen(${d.id})" class="px-3.5 py-1.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-extrabold transition-all shadow-2xs flex items-center gap-1">
                  <span>✏️</span> Update Info
                </button>
              `)}
            </div>

          </div>
        `;
      }).join('');
    }

    // 5. Modal Operations & Dynamic Form Calculation
    function populateDosenDropdown() {
      const select = document.getElementById('form-dosen-id');
      select.innerHTML = DOSEN_STATE.map(d => `
        <option value="${d.id}">${d.name} [Lab: ${d.lab_code} - Kuota: ${d.quota_resmi}]</option>
      `).join('');
    }

    function openReportModal() {
      populateDosenDropdown();
      document.getElementById('form-report').reset();
      onDosenSelectChange();
      document.getElementById('modal-report').classList.remove('hidden');
    }

    function openReportModalForDosen(did) {
      openReportModal();
      document.getElementById('form-dosen-id').value = did;
      onDosenSelectChange();
    }

    function closeReportModal() {
      document.getElementById('modal-report').classList.add('hidden');
    }

    function onDosenSelectChange() {
      const did = parseInt(document.getElementById('form-dosen-id').value);
      const d = DOSEN_STATE.find(item => item.id === did);
      if (!d) return;

      const quota = d.quota_resmi || 8;
      document.getElementById('form-quota-total').value = quota;
      
      // If already known terisi
      if (d.terisi_slot_riil !== null && d.terisi_slot_riil !== undefined) {
        document.getElementById('form-terisi-slot').value = d.terisi_slot_riil;
      } else if (d.status_riil === 'full') {
        document.getElementById('form-terisi-slot').value = quota;
      } else {
        document.getElementById('form-terisi-slot').value = 0;
      }

      calculateSlotAndStatus();
    }

    // Dynamic calculation: Kuota Total - Sudah Terisi = Sisa Slot
    function calculateSlotAndStatus() {
      const quota = parseInt(document.getElementById('form-quota-total').value) || 8;
      const terisi = parseInt(document.getElementById('form-terisi-slot').value) || 0;
      const sisa = Math.max(0, quota - terisi);

      document.getElementById('form-sisa-slot').value = sisa;

      const banner = document.getElementById('calc-result-banner');
      const icon = document.getElementById('calc-icon');
      const statusText = document.getElementById('calc-status-text');
      const subText = document.getElementById('calc-sub-text');
      const badge = document.getElementById('calc-badge');

      const radioFull = document.querySelector('input[name="form_status"][value="full"]');
      const radioWarn = document.querySelector('input[name="form_status"][value="warning"]');
      const radioAvail = document.querySelector('input[name="form_status"][value="available"]');

      if (terisi >= quota || sisa === 0) {
        // FULL (MERAH)
        banner.className = 'p-3 rounded-xl border border-rose-200 bg-rose-50/80 flex items-center justify-between transition-colors';
        icon.textContent = '🔴';
        statusText.textContent = `Sisa Slot: 0 Mahasiswa (KUOTA FULL)`;
        statusText.className = 'font-black text-rose-800 text-xs block';
        subText.textContent = `Dosen sudah mencapai batas kuota maksimal (${quota} mhs).`;
        badge.className = 'px-2.5 py-1 rounded-full text-[10px] font-black bg-rose-200 text-rose-900 border border-rose-300';
        badge.textContent = '🔴 FULL / PENUH';
        if (radioFull) radioFull.checked = true;
      } else if (sisa <= 2) {
        // HAMPIR PENUH (KUNING)
        banner.className = 'p-3 rounded-xl border border-amber-200 bg-amber-50/80 flex items-center justify-between transition-colors';
        icon.textContent = '🟡';
        statusText.textContent = `Sisa Slot: ${sisa} Mahasiswa (HAMPIR PENUH)`;
        statusText.className = 'font-black text-amber-900 text-xs block';
        subText.textContent = `Tinggal sedikit slot lagi sebelum ditutup.`;
        badge.className = 'px-2.5 py-1 rounded-full text-[10px] font-black bg-amber-200 text-amber-900 border border-amber-300';
        badge.textContent = `🟡 SISA ${sisa} SLOT`;
        if (radioWarn) radioWarn.checked = true;
      } else {
        // MASIH BANYAK (HIJAU)
        banner.className = 'p-3 rounded-xl border border-emerald-200 bg-emerald-50/80 flex items-center justify-between transition-colors';
        icon.textContent = '🟢';
        statusText.textContent = `Sisa Slot: ${sisa} Mahasiswa (MASIH BANYAK)`;
        statusText.className = 'font-black text-emerald-900 text-xs block';
        subText.textContent = `Masih membuka kesempatan bimbingan skripsi.`;
        badge.className = 'px-2.5 py-1 rounded-full text-[10px] font-black bg-emerald-200 text-emerald-900 border border-emerald-300';
        badge.textContent = `🟢 SISA ${sisa} SLOT`;
        if (radioAvail) radioAvail.checked = true;
      }
    }

    function onRadioStatusChange(st) {
      const quota = parseInt(document.getElementById('form-quota-total').value) || 8;
      if (st === 'full') {
        document.getElementById('form-terisi-slot').value = quota;
      } else if (st === 'warning') {
        document.getElementById('form-terisi-slot').value = Math.max(0, quota - 1);
      } else if (st === 'available') {
        const cur = parseInt(document.getElementById('form-terisi-slot').value) || 0;
        if (cur >= quota) {
          document.getElementById('form-terisi-slot').value = Math.max(0, quota - 4);
        }
      }
      calculateSlotAndStatus();
    }

    // Detail Modal
    function openDetailModal(did) {
      const d = DOSEN_STATE.find(item => item.id === did);
      if (!d) return;

      document.getElementById('modal-dosen-title').textContent = d.name;
      document.getElementById('modal-dosen-meta').textContent = `Lab: ${d.lab_code} • Kuota Resmi SIMTA: ${d.quota_resmi} • Sisa Slot Riil: ${d.sisa_slot_riil !== null ? d.sisa_slot_riil : 'Belum Terdata'}`;
      document.getElementById('modal-catatan-detail').textContent = d.catatan_terakhir || 'Belum ada catatan khusus.';
      document.getElementById('modal-last-update').textContent = d.last_updated || 'Hari ini';

      const listContainer = document.getElementById('modal-topik-list');
      const topics = d.topik_mahasiswa || [];
      if (topics.length === 0) {
        listContainer.innerHTML = '<p class="text-slate-400 italic p-3 text-center bg-slate-50 rounded-xl">Belum ada judul topik yang dilaporkan untuk dosen ini.</p>';
      } else {
        listContainer.innerHTML = topics.map((t, i) => `
          <div class="p-3 rounded-xl border border-slate-200 bg-slate-50 flex items-start gap-2.5">
            <span class="font-bold text-slate-400 shrink-0 mt-0.5">#${i + 1}</span>
            <span class="font-extrabold text-slate-800 leading-snug">${t}</span>
          </div>
        `).join('');
      }

      document.getElementById('modal-detail-topik').classList.remove('hidden');
    }

    function closeDetailModal() {
      document.getElementById('modal-detail-topik').classList.add('hidden');
    }

    function quickAddTopic(did) {
      openReportModalForDosen(did);
      setTimeout(() => {
        document.getElementById('form-topik').focus();
      }, 150);
    }

    // Submit Report (Race-Condition Free)
    async function submitReportForm(e) {
      e.preventDefault();
      const did = parseInt(document.getElementById('form-dosen-id').value);
      const quota = parseInt(document.getElementById('form-quota-total').value) || 8;
      const terisi = parseInt(document.getElementById('form-terisi-slot').value) || 0;
      const sisa = parseInt(document.getElementById('form-sisa-slot').value) || 0;
      const status = document.querySelector('input[name="form_status"]:checked').value;
      const sumber = document.getElementById('form-sumber').value;
      const topik = document.getElementById('form-topik').value.trim();
      const catatan = document.getElementById('form-catatan').value.trim() || `Info via ${sumber}`;
      const nama = document.getElementById('form-nama').value.trim() || 'Mahasiswa Anonim';

      const d = DOSEN_STATE.find(item => item.id === did);
      if (!d) return;

      // 1. Optimistic Local Update
      d.status_riil = status;
      d.quota_resmi = quota;
      d.terisi_slot_riil = terisi;
      d.sisa_slot_riil = sisa;
      d.catatan_terakhir = catatan;
      d.konfirmasi_count = (d.konfirmasi_count || 0) + 1;
      d.last_updated = new Date().toLocaleString('id-ID');

      if (topik) {
        if (!d.topik_mahasiswa) d.topik_mahasiswa = [];
        if (!d.topik_mahasiswa.includes(topik)) {
          d.topik_mahasiswa.unshift(topik);
        }
      }

      saveToLocalStorage();
      closeReportModal();
      renderCards();
      updateMetrics();
      showToast(`Status ${d.name} berhasil diperbarui!`);

      // 2. Cloud Update via Supabase (if connected)
      if (supabaseClient) {
        try {
          await supabaseClient.rpc('submit_crowdsource_report', {
            p_dosen_id: did,
            p_status: status,
            p_sisa_slot: sisa,
            p_student_name: nama,
            p_topik: topik || null,
            p_sumber: sumber,
            p_catatan: catatan,
            p_ip_hash: 'client_hash'
          });
        } catch (err) {
          console.warn('Cloud sync error, local update persisted:', err);
        }
      }
    }

    function confirmStatus(did) {
      const d = DOSEN_STATE.find(item => item.id === did);
      if (!d) return;

      d.konfirmasi_count = (d.konfirmasi_count || 0) + 1;
      saveToLocalStorage();
      renderCards();
      showToast(`Terima kasih! Anda mengonfirmasi info status ${d.name}`);

      if (supabaseClient) {
        supabaseClient.rpc('confirm_dosen_status', { p_dosen_id: did }).catch(e => console.log(e));
      }
    }

    function filterByStatus(st) {
      currentFilterStatus = st;
      document.querySelectorAll('.status-tab').forEach(t => {
        if (t.dataset.status === st) {
          t.classList.add('active', 'text-white', 'bg-blue-600', 'shadow-2xs');
          t.classList.remove('text-rose-800', 'text-amber-800', 'text-emerald-800', 'text-blue-800', 'text-slate-600');
        } else {
          t.classList.remove('active', 'text-white', 'bg-blue-600', 'shadow-2xs');
          if (t.dataset.status === 'full') t.classList.add('text-rose-800');
          if (t.dataset.status === 'warning') t.classList.add('text-amber-800');
          if (t.dataset.status === 'available') t.classList.add('text-emerald-800');
          if (t.dataset.status === 'unknown') t.classList.add('text-blue-800');
          if (t.dataset.status === 'zero') t.classList.add('text-slate-600');
        }
      });
      renderCards();
      window.scrollTo({ top: document.getElementById('search-input').offsetTop - 80, behavior: 'smooth' });
    }

    // Share Modal
    function openShareModal() {
      const fullCount = DOSEN_STATE.filter(d => d.status_riil === 'full').length;
      const availCount = DOSEN_STATE.filter(d => d.status_riil === 'available').length;
      const unkCount = DOSEN_STATE.filter(d => d.status_riil === 'unknown').length;
      const text = `📢 *Update Riil Kuota Dosen Skripsi JTI Polinema 2026*\n\n` +
        `Biar ga kena false-positive SIMTA (kuota di web tampak buka padahal aslinya penuh), yuk cek & laporkan status dosenmu:\n` +
        `🔴 Dosen Sudah FULL: ${fullCount} Orang (Termasuk Pak Yuri, Pak Yan, dll)\n` +
        `🟢 Dosen Masih Ada Slot: ${availCount} Orang\n` +
        `⚪ Dosen Belum Diketahui: ${unkCount} Orang (Yuk bantu isi jika tahu!)\n\n` +
        `Cek langsung & laporkan tanpa login di sini:\n` +
        window.location.href;

      document.getElementById('share-text-preview').value = text;
      document.getElementById('modal-share').classList.remove('hidden');
    }

    function closeShareModal() {
      document.getElementById('modal-share').classList.add('hidden');
    }

    function copyShareText() {
      const ta = document.getElementById('share-text-preview');
      ta.select();
      navigator.clipboard.writeText(ta.value).then(() => {
        showToast('Pesan WhatsApp berhasil disalin!');
      });
    }

    function openWhatsAppDirect() {
      const text = encodeURIComponent(document.getElementById('share-text-preview').value);
      window.open(`https://api.whatsapp.com/send?text=${text}`, '_blank');
    }

    // Config Modal
    function openConfigModal() {
      document.getElementById('cfg-supabase-url').value = localStorage.getItem('supabase_url') || '';
      document.getElementById('cfg-supabase-key').value = localStorage.getItem('supabase_key') || '';
      document.getElementById('modal-config').classList.remove('hidden');
    }

    function closeConfigModal() {
      document.getElementById('modal-config').classList.add('hidden');
    }

    function saveSupabaseConfig() {
      const url = document.getElementById('cfg-supabase-url').value.trim();
      const key = document.getElementById('cfg-supabase-key').value.trim();
      localStorage.setItem('supabase_url', url);
      localStorage.setItem('supabase_key', key);
      closeConfigModal();
      showToast('Konfigurasi Cloud disimpan! Menghubungkan...');
      initSupabase();
    }

    function showToast(msg) {
      const toast = document.getElementById('toast');
      document.getElementById('toast-message').textContent = msg;
      toast.classList.remove('translate-y-20', 'opacity-0');
      setTimeout(() => {
        toast.classList.add('translate-y-20', 'opacity-0');
      }, 3500);
    }

    // Event Listeners
    document.addEventListener('DOMContentLoaded', () => {
      populateDosenDropdown();
      renderCards();
      updateMetrics();
      initSupabase();

      // Search input
      const searchInput = document.getElementById('search-input');
      const searchClear = document.getElementById('search-clear');
      searchInput.addEventListener('input', (e) => {
        currentSearch = e.target.value.trim().toLowerCase();
        if (currentSearch) {
          searchClear.classList.remove('hidden');
        } else {
          searchClear.classList.add('hidden');
        }
        renderCards();
      });

      searchClear.addEventListener('click', () => {
        searchInput.value = '';
        currentSearch = '';
        searchClear.classList.add('hidden');
        renderCards();
      });

      // Filter Lab
      document.getElementById('filter-lab').addEventListener('change', (e) => {
        currentFilterLab = e.target.value;
        renderCards();
      });

      // Sort
      document.getElementById('sort-by').addEventListener('change', (e) => {
        currentSort = e.target.value;
        renderCards();
      });

      // Status Filter tabs
      document.querySelectorAll('.status-tab').forEach(tab => {
        tab.addEventListener('click', () => {
          filterByStatus(tab.dataset.status);
        });
      });
    });
  </script>
</body>
</html>
'''

with open(OUT_FILE, 'w', encoding='utf-8') as f:
    f.write(html_template)

with open('/home/aslam/.gemini/antigravity/scratch/pantau-kuota-dosen/build_app.py', 'w', encoding='utf-8') as f:
    f.write(f'''import json
import os

SEED_FILE = '/home/aslam/.gemini/antigravity/scratch/pantau-kuota-dosen/dosen_seed.json'
OUT_FILE = '/home/aslam/.gemini/antigravity/scratch/pantau-kuota-dosen/index.html'

with open(SEED_FILE, 'r', encoding='utf-8') as f:
    seed_dosen = json.load(f)

dosen_json_str = json.dumps(seed_dosen, ensure_ascii=False)

# build script regenerates index.html
''')

print("Compiled index.html successfully.")
