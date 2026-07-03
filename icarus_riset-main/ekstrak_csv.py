import pickle
import csv

# 1. Buka file hasil eksperimen
with open('hasil_hybrid_mcdm.pickle', 'rb') as f:
    hasil = pickle.load(f)

# Dapatkan struktur antrean (deque) Icarus
data_mentah = hasil.results if hasattr(hasil, 'results') else hasil

# 2. Siapkan file CSV yang rapi
nama_file_rapi = 'tabel_tesis_rapi.csv'

with open(nama_file_rapi, 'w', newline='') as f:
    writer = csv.writer(f)
    
    # Tulis Header (Judul Kolom Tesis Anda)
    writer.writerow([
        'Topologi', 'Strategi', 'Alpha', 'Network Cache', 
        'Cache Hit Ratio (MEAN)', 'Latency (MEAN)', 'Path Stretch (MEAN)',
        'Link Load Internal (MEAN)', 'Link Load External (MEAN)'
    ])
    
    # 3. Ekstrak data satu per satu dari dalam Tree
    for eksperimen in data_mentah:
        skenario = eksperimen[0]
        metrik = eksperimen[1]
        
        # Ambil Parameter Skenario
        topologi = skenario['topology']['name']
        strategi = skenario['strategy']['name']
        alpha = skenario['workload']['alpha']
        cache = skenario['cache_placement']['network_cache']
        
        # Ambil Hasil Metrik (Hanya ambil nilai MEAN / Rata-rata)
        chr_mean = metrik['CACHE_HIT_RATIO']['MEAN']
        latency_mean = metrik['LATENCY']['MEAN']
        stretch_mean = metrik['PATH_STRETCH']['MEAN']
        
        # Menghindari error jika Link Load tidak terekam
        try:
            load_int = metrik['LINK_LOAD']['MEAN_INTERNAL']
            load_ext = metrik['LINK_LOAD']['MEAN_EXTERNAL']
        except:
            load_int = "N/A"
            load_ext = "N/A"
            
        # Tulis ke dalam baris Excel secara berurutan
        writer.writerow([
            topologi, strategi, alpha, cache,
            chr_mean, latency_mean, stretch_mean, load_int, load_ext
        ])

print(f"✅ BINGO! Data tesis Anda berhasil dirapikan ke dalam {nama_file_rapi}")
