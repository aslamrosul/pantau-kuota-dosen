-- ====================================================================
-- SISTEM PANTAU KUOTA DOSEN & TOPIK SKRIPSI JTI POLINEMA
-- Database Schema for Supabase (PostgreSQL with Realtime & Concurrency Safe)
-- ====================================================================

-- 1. Enable UUID Extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 2. Master Table: Dosen JTI (81 Dosen)
CREATE TABLE IF NOT EXISTS public.dosen (
    id INT PRIMARY KEY,
    name TEXT NOT NULL,
    nip TEXT,
    lab_code TEXT DEFAULT 'General',
    quota_resmi INT DEFAULT 8,
    terpakai_resmi INT DEFAULT 0,
    status_riil TEXT DEFAULT 'available' CHECK (status_riil IN ('available', 'warning', 'full', 'zero')),
    sisa_slot_riil INT DEFAULT 8,
    catatan_terakhir TEXT,
    konfirmasi_count INT DEFAULT 1,
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. Event Sourcing Table: Crowdsource Reports (Append-Only = ZERO Race Conditions)
CREATE TABLE IF NOT EXISTS public.crowdsource_reports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    dosen_id INT NOT NULL REFERENCES public.dosen(id) ON DELETE CASCADE,
    status_reported TEXT NOT NULL CHECK (status_reported IN ('available', 'warning', 'full', 'zero')),
    sisa_slot_reported INT DEFAULT 0,
    student_name TEXT DEFAULT 'Mahasiswa Anonim',
    topik_skripsi TEXT,
    sumber_info TEXT DEFAULT 'Tatap Muka / Chat Langsung',
    catatan TEXT,
    ip_hash TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 4. Realtime Registry Table: Topik Skripsi Mahasiswa Berjalan
CREATE TABLE IF NOT EXISTS public.topik_bimbingan_riil (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    dosen_id INT NOT NULL REFERENCES public.dosen(id) ON DELETE CASCADE,
    judul_topik TEXT NOT NULL,
    mahasiswa_name TEXT DEFAULT 'Anonim',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 5. Atomic Stored Procedure: Submit Report (Anti Race-Condition ACID Transaction)
CREATE OR REPLACE FUNCTION public.submit_crowdsource_report(
    p_dosen_id INT,
    p_status TEXT,
    p_sisa_slot INT,
    p_student_name TEXT,
    p_topik TEXT,
    p_sumber TEXT,
    p_catatan TEXT,
    p_ip_hash TEXT
)
RETURNS JSONB
LANGUAGE plpgsql
SECURITY DEFINER
AS 12417
DECLARE
    v_result JSONB;
BEGIN
    -- 1. Insert immutable log record
    INSERT INTO public.crowdsource_reports (
        dosen_id, status_reported, sisa_slot_reported, student_name, topik_skripsi, sumber_info, catatan, ip_hash
    ) VALUES (
        p_dosen_id, p_status, p_sisa_slot, p_student_name, p_topik, p_sumber, p_catatan, p_ip_hash
    );

    -- 2. Optional: Record student thesis topic if provided
    IF p_topik IS NOT NULL AND length(trim(p_topik)) > 3 THEN
        INSERT INTO public.topik_bimbingan_riil (dosen_id, judul_topik, mahasiswa_name)
        VALUES (p_dosen_id, trim(p_topik), COALESCE(NULLIF(trim(p_student_name), ''), 'Mahasiswa JTI'));
    END IF;

    -- 3. Atomic update on master dosen with row-locking
    UPDATE public.dosen
    SET status_riil = p_status,
        sisa_slot_riil = p_sisa_slot,
        catatan_terakhir = p_catatan,
        konfirmasi_count = konfirmasi_count + 1,
        updated_at = NOW()
    WHERE id = p_dosen_id;

    -- 4. Return updated record
    SELECT to_jsonb(d) INTO v_result FROM public.dosen d WHERE id = p_dosen_id;
    RETURN v_result;
END;
12417;

-- 6. Atomic Stored Procedure: Confirm / Upvote Report
CREATE OR REPLACE FUNCTION public.confirm_dosen_status(p_dosen_id INT)
RETURNS INT
LANGUAGE plpgsql
SECURITY DEFINER
AS 12417
DECLARE
    v_new_count INT;
BEGIN
    UPDATE public.dosen
    SET konfirmasi_count = konfirmasi_count + 1,
        updated_at = NOW()
    WHERE id = p_dosen_id
    RETURNING konfirmasi_count INTO v_new_count;
    
    RETURN v_new_count;
END;
12417;

-- 7. Row Level Security (RLS) Configuration for Anonymous Public Access
ALTER TABLE public.dosen ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.crowdsource_reports ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.topik_bimbingan_riil ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Public Read Dosen" ON public.dosen FOR SELECT TO anon, authenticated USING (true);
CREATE POLICY "Public Read Reports" ON public.crowdsource_reports FOR SELECT TO anon, authenticated USING (true);
CREATE POLICY "Public Insert Reports" ON public.crowdsource_reports FOR INSERT TO anon, authenticated WITH CHECK (true);
CREATE POLICY "Public Read Topik" ON public.topik_bimbingan_riil FOR SELECT TO anon, authenticated USING (true);
CREATE POLICY "Public Insert Topik" ON public.topik_bimbingan_riil FOR INSERT TO anon, authenticated WITH CHECK (true);

-- 8. Enable Realtime Replication
ALTER PUBLICATION supabase_realtime ADD TABLE public.dosen;
ALTER PUBLICATION supabase_realtime ADD TABLE public.crowdsource_reports;
ALTER PUBLICATION supabase_realtime ADD TABLE public.topik_bimbingan_riil;

-- 9. Seed 81 Dosen JTI
INSERT INTO public.dosen (id, name, nip, lab_code, quota_resmi, terpakai_resmi, status_riil, sisa_slot_riil, catatan_terakhir, konfirmasi_count)
VALUES
(6, 'Ade Ismail S.Kom., M.TI', '199107042019031021', 'NCS', 11, 4, 'available', 7, 'Masih tersedia sisa 7 slot bimbingan.', 1),
(7, 'Adevian Fairuz Pratama, S.S.T, M.Eng', '199408192025212049', 'MMT', 7, 6, 'warning', 1, 'Hampir penuh! Sisa 1 slot.', 1),
(8, 'Agung Nugroho Pramudhita, S.T., M.T.', '198902102019031020', 'InLET', 8, 6, 'warning', 2, 'Hampir penuh! Sisa 2 slot.', 1),
(9, 'Ahmadi Yuli Ananta, ST., M.M.', '198107052005011002', 'BA', 8, 7, 'warning', 1, 'Hampir penuh! Sisa 1 slot.', 1),
(10, 'Annisa Puspa Kirana, S. Kom, M.Kom', '198901232019032016', 'SE', 0, 1, 'zero', 0, 'Tidak membuka kuota bimbingan periode ini (studi lanjut / struktural).', 1),
(11, 'Annisa Taufika Firdausi, ST., MT.', '198712142019032012', 'SE', 0, 0, 'zero', 0, 'Tidak membuka kuota bimbingan periode ini (studi lanjut / struktural).', 1),
(12, 'Anugrah Nur Rahmanto, S.Sn., M.Ds.', '199112302019031016', 'MMT', 10, 10, 'full', 0, 'Status SIMTA & konfirmasi mahasiswa: Kuota penuh.', 3),
(13, 'Ariadi Retno Tri Hayati Ririd, S.Kom., M.Kom.', '198108102005012002', 'SE', 8, 1, 'available', 7, 'Masih tersedia sisa 7 slot bimbingan.', 1),
(14, 'Arie Rachmad Syulistyo, S.Kom., M.Kom., Ph.D.', '198708242019031010', 'DT', 8, 0, 'available', 8, 'Masih tersedia sisa 8 slot bimbingan.', 1),
(15, 'Arief Prasetyo, S.Kom., M.Kom.', '197903132008121002', 'SE', 0, 0, 'zero', 0, 'Tidak membuka kuota bimbingan periode ini (studi lanjut / struktural).', 1),
(16, 'Astrifidha Rahma Amalia,S.Pd., M.Pd.', '', 'SE', 0, 0, 'zero', 0, 'Tidak membuka kuota bimbingan periode ini (studi lanjut / struktural).', 1),
(17, 'Atiqah Nurul Asri, S.Pd., M.Pd.', '197606252005012001', 'SE', 0, 0, 'zero', 0, 'Tidak membuka kuota bimbingan periode ini (studi lanjut / struktural).', 1),
(18, 'Bagas Satya Dian Nugraha, ST., MT.', '199006192019031017', 'MMT', 8, 0, 'available', 8, 'Masih tersedia sisa 8 slot bimbingan.', 1),
(20, 'Budi Harijanto, ST., M.MKom.', '196201051990031002', 'InLET', 8, 1, 'available', 7, 'Masih tersedia sisa 7 slot bimbingan.', 1),
(22, 'Candra Bella Vista, S.Kom., MT.', '199412172019032020', 'BA', 8, 8, 'full', 0, 'Status SIMTA & konfirmasi mahasiswa: Kuota penuh.', 3),
(23, 'Candrasena Setiadi, ST., M.MT', '', 'SE', 0, 0, 'zero', 0, 'Tidak membuka kuota bimbingan periode ini (studi lanjut / struktural).', 1),
(24, 'Deddy Kusbianto PA, Ir., M.Mkom.', '196211281988111001', 'AI', 8, 1, 'available', 7, 'Masih tersedia sisa 7 slot bimbingan.', 1),
(25, 'Dhebys Suryani, S.Kom., MT', '198311092014042001', 'BA', 8, 1, 'full', 0, 'Terkonfirmasi: kuota bimbingan penuh (8/8).', 4),
(26, 'Dian Hanifudin Subhi, S.Kom., M.Kom.', '198806102019031018', 'SE', 8, 1, 'available', 7, 'Masih tersedia sisa 7 slot bimbingan.', 1),
(27, 'Dika Rizky Yunianto, S.Kom, M.Kom', '199206062019031017', 'DT', 8, 0, 'available', 8, 'Masih tersedia sisa 8 slot bimbingan.', 1),
(28, 'Dimas Wahyu Wibowo, ST., MT.', '198410092015041001', 'MMT', 8, 0, 'available', 8, 'Masih tersedia sisa 8 slot bimbingan.', 1),
(81, 'Dodit Suprianto', '', 'SE', 0, 0, 'zero', 0, 'Tidak membuka kuota bimbingan periode ini (studi lanjut / struktural).', 1),
(29, 'Dr. Ely Setyo Astuti, S.T., M.T.', '197605152009122001', 'IVSS', 8, 6, 'warning', 2, 'Hampir penuh! Sisa 2 slot.', 1),
(45, 'Dr. Indra Dharma Wijaya, ST., M.MT.', '197305102008011010', 'InLET', 8, 0, 'available', 8, 'Masih tersedia sisa 8 slot bimbingan.', 1),
(30, 'Dr. Rakhmat Arianto, S.ST., M.Kom.', '198701082019031004', 'BA', 9, 1, 'available', 8, 'Masih tersedia sisa 8 slot bimbingan.', 1),
(31, 'Dr. Ulla Delfana Rosiani, ST., MT.', '197803272003122002', 'IVSS', 8, 8, 'full', 0, 'Status SIMTA & konfirmasi mahasiswa: Kuota penuh.', 3),
(80, 'Dr. Yuri Ariyanto, S.Kom., M.Kom.', '198007162010121002', 'AI', 10, 10, 'full', 0, 'Terkonfirmasi langsung via chat/tatap muka: kuota 10 mahasiswa sudah penuh.', 5),
(19, 'Dr.Eng. Banni Satria Andoko, S. Kom., M.MSI.', '198108092010121002', 'InLET', 8, 0, 'available', 8, 'Masih tersedia sisa 8 slot bimbingan.', 1),
(32, 'Dwi Puspitasari, S.Kom., M.Kom.', '197911152005012002', 'SE', 0, 0, 'zero', 0, 'Tidak membuka kuota bimbingan periode ini (studi lanjut / struktural).', 1),
(33, 'Eka Larasati Amalia, S.ST., MT.', '198807112015042005', 'MMT', 8, 0, 'available', 8, 'Masih tersedia sisa 8 slot bimbingan.', 1),
(34, 'Ekojono, ST., M.Kom.', '195912081985031004', 'SE', 0, 0, 'zero', 0, 'Tidak membuka kuota bimbingan periode ini (studi lanjut / struktural).', 1),
(35, 'Elok Nur Hamdana, S.T., M.T', '198610022019032011', 'SE', 8, 8, 'full', 0, 'Status SIMTA & konfirmasi mahasiswa: Kuota penuh.', 3),
(36, 'Endah Septa Sintiya. SPd., MKom.', '199401312022032007', 'BA', 8, 7, 'warning', 1, 'Hampir penuh! Sisa 1 slot.', 1),
(37, 'Erfan Rohadi, ST., M.Eng., Ph.D.', '197201232008011006', 'NCS', 9, 9, 'full', 0, 'Status SIMTA & konfirmasi mahasiswa: Kuota penuh.', 3),
(38, 'Faiz Ushbah Mubarok, S.Pd., M.Pd.', '199305052019031018', 'SE', 0, 0, 'zero', 0, 'Tidak membuka kuota bimbingan periode ini (studi lanjut / struktural).', 1),
(39, 'Farid Angga Pribadi, S.Kom.,M.Kom', '198910072020121003', 'BA', 8, 0, 'available', 8, 'Masih tersedia sisa 8 slot bimbingan.', 1),
(40, 'Farida Ulfa, S.Pd., M.Pd.', '', 'SE', 0, 0, 'zero', 0, 'Tidak membuka kuota bimbingan periode ini (studi lanjut / struktural).', 1),
(41, 'Gunawan Budi Prasetyo, ST., MMT., Ph.D.', '197704242008121001', 'DT', 8, 0, 'available', 8, 'Masih tersedia sisa 8 slot bimbingan.', 1),
(3, 'Habibie Ed Dien, S.Kom., M.T.', '199204122019031013', 'DT', 9, 9, 'full', 0, 'Status SIMTA & konfirmasi mahasiswa: Kuota penuh.', 3),
(42, 'Hendra Pradibta, SE., M.Sc.', '198305212006041003', 'BA', 8, 4, 'available', 4, 'Masih tersedia sisa 4 slot bimbingan.', 1),
(43, 'Ika Kusumaning Putri, MT.', '199110142019032020', 'SE', 0, 0, 'zero', 0, 'Tidak membuka kuota bimbingan periode ini (studi lanjut / struktural).', 1),
(44, 'Imam Fahrur Rozi, ST., MT.', '198406102008121004', 'SE', 8, 1, 'available', 7, 'Masih tersedia sisa 7 slot bimbingan.', 1),
(66, 'Ir. Rudy Ariyanto, ST., M.Cs.', '197111101999031002', 'BA', 8, 1, 'full', 0, 'Terkonfirmasi: kuota bimbingan penuh (8/8).', 4),
(46, 'Irsyad Arif Mashudi, M.Kom', '198902012019031009', 'InLET', 0, 0, 'zero', 0, 'Tidak membuka kuota bimbingan periode ini (studi lanjut / struktural).', 1),
(47, 'Kadek Suarjuna Batubulan, S.Kom, MT', '199003202019031016', 'SE', 0, 0, 'zero', 0, 'Tidak membuka kuota bimbingan periode ini (studi lanjut / struktural).', 1),
(48, 'Luqman Affandi, S.Kom., MMSI', '198211302014041001', 'DT', 8, 6, 'warning', 2, 'Hampir penuh! Sisa 2 slot.', 1),
(5, 'M. Hasyim ratsanjani, S.Kom., M.Kom.', '199003052019031013', 'DT', 8, 2, 'available', 6, 'Masih tersedia sisa 6 slot bimbingan.', 1),
(49, 'Mamluatul Hani&#039;ah, S.Kom., M.Kom.', '199002062019032013', 'IVSS', 8, 1, 'available', 7, 'Masih tersedia sisa 7 slot bimbingan.', 1),
(50, 'Marsma TNI Dr. Ir. Arwin Datumaya Wahyudi Sumari, S.T., M.T., IPU, ASEAN Eng., ACPE', '515561', 'SE', 0, 0, 'zero', 0, 'Tidak membuka kuota bimbingan periode ini (studi lanjut / struktural).', 1),
(51, 'Meyti Eka Apriyani ST., MT.', '198704242019032017', 'NCS', 8, 2, 'full', 0, 'Terkonfirmasi: kuota bimbingan penuh (8/8).', 4),
(52, 'Milyun Nima Shoumi, S.Kom., M.Kom., Ph.D.', '198805072019032012', 'SE', 8, 1, 'available', 7, 'Masih tersedia sisa 7 slot bimbingan.', 1),
(1, 'Moch Zawaruddin Abdullah, S.ST., M.Kom.', '198902102019031019', 'SE', 8, 8, 'full', 0, 'Status SIMTA & konfirmasi mahasiswa: Kuota penuh.', 3),
(53, 'Muhammad Afif Hendrawan., S.Kom., M.T.', '199111282019031013', 'AI', 8, 2, 'available', 6, 'Masih tersedia sisa 6 slot bimbingan.', 1),
(54, 'Muhammad Shulhan Khairy, S.Kom, M.Kom', '199205172019031020', 'SE', 0, 0, 'zero', 0, 'Tidak membuka kuota bimbingan periode ini (studi lanjut / struktural).', 1),
(55, 'Muhammad Unggul Pamenang, S.ST., M.T.', '199108232025211038', 'MMT', 7, 0, 'available', 7, 'Masih tersedia sisa 7 slot bimbingan.', 1),
(56, 'Mungki Astiningrum, ST., M.Kom.', '197710302005012001', 'IVSS', 8, 2, 'available', 6, 'Masih tersedia sisa 6 slot bimbingan.', 1),
(57, 'Mustika Mentari, S.Kom., M.Kom., Ph.D.', '198806072019032016', 'AI', 8, 4, 'available', 4, 'Masih tersedia sisa 4 slot bimbingan.', 1),
(58, 'Muthrofin', '', 'SE', 0, 0, 'zero', 0, 'Tidak membuka kuota bimbingan periode ini (studi lanjut / struktural).', 1),
(4, 'Noprianto, S.Kom., M.Eng', '198911082019031020', 'SE', 0, 0, 'zero', 0, 'Tidak membuka kuota bimbingan periode ini (studi lanjut / struktural).', 1),
(59, 'Pramana Yoga Saputra, S.Kom., MMT.', '198805042015041001', 'AI', 9, 9, 'full', 0, 'Status SIMTA & konfirmasi mahasiswa: Kuota penuh.', 3),
(21, 'Prof. Dr. Eng. Cahya Rahmad, ST., M.Kom.', '197202022005011002', 'MMT', 8, 1, 'available', 7, 'Masih tersedia sisa 7 slot bimbingan.', 1),
(65, 'Prof. Dr. Eng. Rosa Andrie Asmara, ST., MT.', '198010102005011001', 'IVSS', 8, 0, 'available', 8, 'Masih tersedia sisa 8 slot bimbingan.', 1),
(79, 'Prof. Ir. Yan Watequlis Syaifudin, ST., M.MT., Ph.D.', '198101052005011005', 'AI', 8, 9, 'full', 0, 'Terkonfirmasi: kuota bimbingan penuh (8/8).', 4),
(60, 'Putra Prima A., ST., M.Kom.', '198611032014041001', 'SE', 0, 0, 'zero', 0, 'Tidak membuka kuota bimbingan periode ini (studi lanjut / struktural).', 1),
(61, 'Retno Damayanti, S.Pd., M.T.', '198910042019032023', 'MMT', 8, 4, 'full', 0, 'Terkonfirmasi: kuota bimbingan penuh (8/8).', 4),
(62, 'Ridwan Rismanto, S.ST., M.Kom., Ph.D.', '198603182012121001', 'SE', 8, 5, 'available', 3, 'Masih tersedia sisa 3 slot bimbingan.', 1),
(63, 'Robby Anggriawan SE., ME.', '', 'SE', 0, 0, 'zero', 0, 'Tidak membuka kuota bimbingan periode ini (studi lanjut / struktural).', 1),
(64, 'Rokhimatul Wakhidah, S.Pd., M.T.', '198903192019032013', 'BA', 8, 3, 'available', 5, 'Masih tersedia sisa 5 slot bimbingan.', 1),
(67, 'Satrio Binusa S, SS, M.Pd', '', 'SE', 0, 0, 'zero', 0, 'Tidak membuka kuota bimbingan periode ini (studi lanjut / struktural).', 1),
(68, 'Septian Enggar Sukmana, S.Pd., M.T', '198909012019031010', 'SE', 0, 0, 'zero', 0, 'Tidak membuka kuota bimbingan periode ini (studi lanjut / struktural).', 1),
(69, 'Sofyan Noor Arief, S.ST., M.Kom.', '198908132019031017', 'NCS', 9, 2, 'full', 0, 'Terkonfirmasi: kuota bimbingan penuh (8/8).', 4),
(70, 'Triana Fatmawati, S.T., M.T.', '198005142005022001', 'AI', 8, 1, 'available', 7, 'Masih tersedia sisa 7 slot bimbingan.', 1),
(71, 'Usman Nurhasan, S.Kom., MT.', '198609232015041001', 'InLET', 8, 0, 'available', 8, 'Masih tersedia sisa 8 slot bimbingan.', 1),
(72, 'Very Sugiarto, S.Pd', '', 'SE', 0, 0, 'zero', 0, 'Tidak membuka kuota bimbingan periode ini (studi lanjut / struktural).', 1),
(73, 'Vipkas Al Hadid Firdaus, ST,. MT', '199105052019031029', 'NCS', 0, 1, 'zero', 0, 'Tidak membuka kuota bimbingan periode ini (studi lanjut / struktural).', 1),
(74, 'Vit Zuraida, S.Kom., M.Kom.', '198901092020122005', 'DT', 8, 0, 'available', 8, 'Masih tersedia sisa 8 slot bimbingan.', 1),
(75, 'Vivi Nur Wijayaningrum, S.Kom, M.Kom', '199308112019032025', 'IVSS', 8, 1, 'full', 0, 'Terkonfirmasi: kuota bimbingan penuh (8/8).', 4),
(76, 'Vivin Ayu Lestari, S.Pd., M.Kom', '199106212019032020', 'InLET', 8, 7, 'warning', 1, 'Hampir penuh! Sisa 1 slot.', 1),
(77, 'Widaningsih Condrowardhani, SH, MH.', '', 'SE', 0, 0, 'zero', 0, 'Tidak membuka kuota bimbingan periode ini (studi lanjut / struktural).', 1),
(78, 'Wilda Imama Sabilla, S.Kom., M.Kom.', '199208292019032023', 'IVSS', 8, 1, 'available', 7, 'Masih tersedia sisa 7 slot bimbingan.', 1),
(2, 'Yoppy Yunhasnawa, S.ST., M.Sc.', '198906212019031013', 'DT', 8, 2, 'available', 6, 'Masih tersedia sisa 6 slot bimbingan.', 1)
ON CONFLICT (id) DO UPDATE SET
    status_riil = EXCLUDED.status_riil,
    sisa_slot_riil = EXCLUDED.sisa_slot_riil,
    catatan_terakhir = EXCLUDED.catatan_terakhir;
