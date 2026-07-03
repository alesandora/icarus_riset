"""
Skenario 1 — Perbandingan Semua Strategi (Eksperimen Utama)
============================================================
Reproduksi Section 4.1 paper C3CPS + tambahan LTP-CPS

Strategi: LCE, LCD, CL4M, PROB_CACHE, MCDM, LTP_CPS
Topologi: TISCALI + GEANT
Zipf α  : {0.8, 1.0}
Cache   : {5%, 10%, 15%, 20%, 25%}
Replikasi: 15

Hasil skenario ini = grafik utama jurnal:
  - CHR vs Cache Capacity
  - Latency vs Cache Capacity
  - Path Stretch vs Cache Capacity
  - Link Load vs Cache Capacity

Alpha/beta LTP-CPS (0.5/0.5) dikelola di ltpcps.py.
Dipilih berdasarkan hasil Skenario 2 (selisih <0.7% antar variasi).

Jalankan: python -m icarus run config_skenario1.py

Total: 6 strategi x 2 Zipf x 2 topologi x 5 cache
     = 120 eksperimen x 15 replikasi = 1800 runs
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
    "LINK_LOAD",        # metrik tambahan untuk jurnal
]

# =============================================================================
# PARAMETER — sesuai Table 5 paper C3CPS
# =============================================================================
N_CONTENTS          = 1 * 10 ** 5
N_WARMUP_REQUESTS   = 5 * 10 ** 4
N_MEASURED_REQUESTS = 2.5 * 10 ** 5
REQ_RATE            = 12.0
CACHE_POLICY        = "IN_CACHE_LFU"
ALPHA               = [0.8, 1.0]
NETWORK_CACHE       = [0.05, 0.10, 0.15, 0.20, 0.25]

# Dua topologi untuk generalisasi hasil
# TISCALI : topologi utama sesuai paper C3CPS
# GEANT   : topologi tambahan untuk jurnal
TOPOLOGIES = ["TISCALI", "GEANT"]

# =============================================================================
# STRATEGI
# =============================================================================
STRATEGIES = [
    "LCE",        # baseline — Leave Copy Everywhere
    "LCD",        # baseline — Leave Copy Down
    "CL4M",       # baseline — Cache Less for More (hanya BC)
    "PROB_CACHE", # baseline — ProbCache
    "MCDM",       # C3CPS, O(n²m) — upper bound pembanding
    "LTP_CPS",    # usulan — O(m), alpha=0.5 beta=0.5
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
                    "S1 | Zipf={} | {} | topo={} | cache={}".format(
                        alpha, strategy, topology, network_cache
                    )
                )
                EXPERIMENT_QUEUE.append(experiment)

# =============================================================================
# RINGKASAN
# 6 strategi x 2 Zipf x 2 topologi x 5 cache = 120 eksperimen
# 120 x 15 replikasi = 1800 runs
# =============================================================================
