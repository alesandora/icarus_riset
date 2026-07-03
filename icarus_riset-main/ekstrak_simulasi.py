import pandas as pd
import pickle

print("Sedang mengekstrak 216 data dari simulasi_1.pickle...\n")

baris_data = []

# Membaca file backup pilihan Anda
with open('simulasi_1.pickle', 'rb') as f:
    data_mentah = pickle.load(f)
    
    for d in data_mentah:
        p = d[0]  
        r = d[1]  
        
        chr_raw = r.get('CACHE_HIT_RATIO', 0)
        chr_mean = chr_raw['mean'] if isinstance(chr_raw, dict) else chr_raw
        
        lat_raw = r.get('LATENCY', 0)
        lat_mean = lat_raw['mean'] if isinstance(lat_raw, dict) else lat_raw
        
        baris_data.append({
            'Topologi': p['topology']['name'],
            'Strategi': p['strategy']['name'],
            'Alpha': p['workload']['alpha'],
            'Cache Size': p['cache_placement']['network_cache'],
            'Cache Hit Ratio': chr_mean,
            'Latency': lat_mean
        })

df = pd.DataFrame(baris_data)
df = df.sort_values(by=['Topologi', 'Cache Size', 'Alpha', 'Strategi'])

nama_file_csv = 'Hasil_Simulasi_1.csv'
df.to_csv(nama_file_csv, index=False)

print(df.head(15).to_string(index=False))
print(f"\n[SUKSES] Seluruh data telah diekspor dengan aman ke file: {nama_file_csv}")
