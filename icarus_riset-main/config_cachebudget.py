"""
Gap 6b — Variasi Cache Budget
===============================
Tujuan  : Analisis performa di rentang cache capacity yang lebih luas
Cache   : [1%, 5%, 25%, 50%] — dari sangat kecil hingga sangat besar
REQ_RATE: 12 req/s (fixed — sesuai paper C3CPS)
Topologi: TISCALI + GEANT
Zipf α  : 0.8 dan 1.0
Replikasi: 15

Pertanyaan yang dijawab:
  - Di cache sangat kecil (1%): strategi mana paling efisien?
  - Di cache sangat besar (50%): apakah perbedaan antar strategi hilang?
  - LTP-CPS vs MCDM: di cache berapa persen gap-nya paling kecil?
  - Apakah BC masih dominan di kondisi cache ekstrem?

Analoginya dengan paper referensi COMNET-D-26-00393
yang memvariasikan K=3,5,7 middlebox (Figure 9 & 10).

Jalankan: python -m icarus run config_cachebudget.py

Total: 4 cache x 6 strategi x 2 Zipf x 2 topologi
     = 96 eksperimen x 15 replikasi = 1440 runs
"""

from multiprocessing import cpu_count
from collections import deque
import copy
from icarus.util import Tree

# =============================================================================
# GENERAL SETTINGS
# =============================================================================
LOG_LEVEL          = "INFO"
PARALLEL_EXECUTION = True
N_PROCESSES        = cpu_count()
RESULTS_FORMAT     = "PICKLE"
N_REPLICATIONS     = 15

DATA_COLLECTORS = [
    "CACHE_HIT_RATIO",
    "LATENCY",
    "PATH_STRETCH",
    "LINK_LOAD",
]

# =============================================================================
# PARAMETER
# =============================================================================
N_CONTENTS          = 1 * 10 ** 5
N_WARMUP_REQUESTS   = 5 * 10 ** 4
N_MEASURED_REQUESTS = 2.5 * 10 ** 5
REQ_RATE            = 12.0        # fixed sesuai paper C3CPS
CACHE_POLICY        = "IN_CACHE_LFU"
ALPHA               = [0.8, 1.0]
TOPOLOGIES          = ["TISCALI", "GEANT"]

# Variasi cache budget — Gap 6b
# 0.01 = 1%  → cache sangat kecil, kondisi resource-constrained
# 0.05 = 5%  → titik terkecil Skenario 1 (overlap untuk validasi)
# 0.25 = 25% → titik terbesar Skenario 1 (overlap untuk validasi)
# 0.50 = 50% → cache sangat besar, hampir semua konten bisa disimpan
NETWORK_CACHE = [0.01, 0.05, 0.25, 0.50]

# =============================================================================
# STRATEGI
# =============================================================================
STRATEGIES = [
    "LCE",
    "LCD",
    "CL4M",
    "PROB_CACHE",
    "MCDM",
    "LTP_CPS",
]

# =============================================================================
# BUILD EXPERIMENT QUEUE
# =============================================================================
EXPERIMENT_QUEUE = deque()

default = Tree()
default["workload"] = {
    "name"      : "STATIONARY",
    "n_contents": N_CONTENTS,
    "n_warmup"  : N_WARMUP_REQUESTS,
    "n_measured": N_MEASURED_REQUESTS,
    "rate"      : REQ_RATE,
}
default["cache_placement"]["name"]   = "UNIFORM"
default["content_placement"]["name"] = "UNIFORM"
default["cache_policy"]["name"]      = CACHE_POLICY

for alpha in ALPHA:
    for strategy in STRATEGIES:
        for topology in TOPOLOGIES:
            for network_cache in NETWORK_CACHE:
                experiment = copy.deepcopy(default)
                experiment["workload"]["alpha"]                = alpha
                experiment["strategy"]["name"]                 = strategy
                experiment["topology"]["name"]                 = topology
                experiment["cache_placement"]["network_cache"] = network_cache
                experiment["desc"] = (
                    "S6b | Zipf={} | {} | topo={} | cache={}".format(
                        alpha, strategy, topology, network_cache
                    )
                )
                EXPERIMENT_QUEUE.append(experiment)

# =============================================================================
# RINGKASAN
# 6 strategi x 2 Zipf x 2 topologi x 4 cache = 96 eksperimen
# 96 x 15 replikasi = 1440 runs
#
# CATATAN: cache 5% dan 25% overlap dengan Skenario 1
#   → bisa digunakan untuk cross-validasi antar skenario
#   → jika hasil konsisten = data reliable
#
# PANDUAN ANALISIS:
#   Plot: CHR vs Cache Capacity (rentang diperluas 1%–50%)
#   Plot: Path Stretch vs Cache Capacity
#
#   Pertanyaan kunci:
#   1. Cache 1%: LTP-CPS vs CL4M — masih mirip atau berbeda?
#      → Jika berbeda di 1%: popularitas lebih berperan saat cache sangat terbatas
#   2. Cache 50%: apakah semua strategi konvergen (CHR hampir sama)?
#      → Jika ya: menunjukkan cache cukup besar membuat algoritma tidak terlalu penting
#   3. Di titik mana (cache berapa %) gap LTP vs MCDM paling kecil?
# =============================================================================
