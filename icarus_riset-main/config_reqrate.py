"""
Gap 6a — Variasi Request Rate
==============================
Tujuan  : Melihat stabilitas performa LTP-CPS di berbagai traffic load
REQ_RATE: [6, 12, 18, 24] req/s
Cache   : 10% dan 20% (fixed — dua titik representatif)
Topologi: TISCALI + GEANT
Zipf α  : 0.8 dan 1.0
Replikasi: 15

Pertanyaan yang dijawab:
  - Apakah LTP-CPS stabil di berbagai load?
  - Di load tinggi (24 req/s), apakah gap LTP vs MCDM membesar/mengecil?
  - Bagaimana link load setiap strategi berubah seiring traffic naik?

Analoginya dengan paper referensi COMNET-D-26-00393
yang memvariasikan load 200–1000 interest/sec (Figure 3 & 4).

Jalankan: python -m icarus run config_reqrate.py

Total: 4 rate x 6 strategi x 2 Zipf x 2 topologi x 2 cache
     = 192 eksperimen x 15 replikasi = 2880 runs
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
CACHE_POLICY        = "IN_CACHE_LFU"
ALPHA               = [0.8, 1.0]
TOPOLOGIES          = ["TISCALI", "GEANT"]

# Variasi request rate — Gap 6a
# 12 req/s = nilai paper C3CPS (baseline)
# 6  req/s = traffic ringan
# 18 req/s = traffic sedang-tinggi
# 24 req/s = traffic tinggi
REQ_RATES = [6, 12, 18, 24]

# Cache capacity fixed di dua titik representatif
# 10% = cache kecil, 20% = cache sedang
NETWORK_CACHE = [0.10, 0.20]

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
}
default["cache_placement"]["name"]   = "UNIFORM"
default["content_placement"]["name"] = "UNIFORM"
default["cache_policy"]["name"]      = CACHE_POLICY

for req_rate in REQ_RATES:
    for alpha in ALPHA:
        for strategy in STRATEGIES:
            for topology in TOPOLOGIES:
                for network_cache in NETWORK_CACHE:
                    experiment = copy.deepcopy(default)
                    experiment["workload"]["alpha"]                = alpha
                    experiment["workload"]["rate"]                 = req_rate
                    experiment["strategy"]["name"]                 = strategy
                    experiment["topology"]["name"]                 = topology
                    experiment["cache_placement"]["network_cache"] = network_cache
                    experiment["desc"] = (
                        "S6a | rate={} | Zipf={} | {} | topo={} | cache={}".format(
                            req_rate, alpha, strategy, topology, network_cache
                        )
                    )
                    EXPERIMENT_QUEUE.append(experiment)

# =============================================================================
# RINGKASAN
# 4 rate x 6 strategi x 2 Zipf x 2 topologi x 2 cache = 192 eksperimen
# 192 x 15 replikasi = 2880 runs
#
# PANDUAN ANALISIS:
#   Plot: CHR vs Request Rate (per strategi, per topologi)
#   Plot: Latency vs Request Rate
#   Plot: Link Load vs Request Rate
#
#   Pertanyaan kunci:
#   1. Di rate=6 (ringan): semua strategi CHR mirip?
#   2. Di rate=24 (berat): LTP-CPS tetap stabil atau turun drastis?
#   3. Gap LTP-CPS vs MCDM: membesar atau mengecil saat rate naik?
#   4. Konsisten di TISCALI dan GEANT?
# =============================================================================
