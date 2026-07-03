"""
Config Skenario 2 — FIXED: Sensitivitas Bobot Alpha/Beta LTP-CPS
=================================================================
Perbaikan: setiap variasi alpha/beta diberi nama strategi berbeda
sehingga hasil bisa dibandingkan langsung antar variasi.

Nama strategi:
  LTP_CPS_7_3 → alpha=0.7, beta=0.3 (topologi dominan)
  LTP_CPS_5_5 → alpha=0.5, beta=0.5 (seimbang)
  LTP_CPS_3_7 → alpha=0.3, beta=0.7 (popularitas dominan)

PENTING: Daftarkan ketiga nama di __init__.py strategy:
  Karena ketiganya menggunakan class LTPCPS yang sama,
  tambahkan registrasi di ltpcps.py atau buat wrapper.
  Lihat bagian bawah file ini untuk instruksi.

Parameter simulasi sesuai Table 5 paper C3CPS:
  Topologi : TISCALI
  Konten   : 100,000
  Warmup   : 50,000 requests
  Measured : 250,000 requests
  Rate     : 12 req/s
  Policy   : IN_CACHE_LFU
  Zipf     : [0.8, 1.0]
  Cache    : [5%, 10%, 15%, 20%, 25%]
  Replikasi: 15
"""

from multiprocessing import cpu_count
from collections import deque
import copy
from icarus.util import Tree

# =============================================================================
# GENERAL SETTINGS
# =============================================================================
LOG_LEVEL           = "INFO"
PARALLEL_EXECUTION  = True
N_PROCESSES         = cpu_count()
RESULTS_FORMAT      = "PICKLE"
N_REPLICATIONS      = 15

DATA_COLLECTORS = [
    "CACHE_HIT_RATIO",
    "LATENCY",
    "PATH_STRETCH",
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
TOPOLOGIES          = ["TISCALI"]

# =============================================================================
# STRATEGI PEMBANDING (baseline + C3CPS)
# =============================================================================
BASELINE_STRATEGIES = [
    "LCE",
    "LCD",
    "CL4M",       # penting: BC saja tanpa popularitas
    "PROB_CACHE",
    "MCDM",       # C3CPS — pembanding utama
]

# =============================================================================
# TIGA VARIASI LTP-CPS — masing-masing nama berbeda
# =============================================================================
LTP_VARIANTS = [
    {
        "name"  : "LTP_CPS_7_3",   # nama unik di hasil simulasi
        "alpha" : 0.7,
        "beta"  : 0.3,
        "label" : "Topologi dominan"
    },
    {
        "name"  : "LTP_CPS_5_5",
        "alpha" : 0.5,
        "beta"  : 0.5,
        "label" : "Seimbang"
    },
    {
        "name"  : "LTP_CPS_3_7",
        "alpha" : 0.3,
        "beta"  : 0.7,
        "label" : "Popularitas dominan"
    },
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

# -----------------------------------------------------------------------------
# BAGIAN 1: Strategi Baseline + C3CPS
# -----------------------------------------------------------------------------
for zipf_alpha in ALPHA:
    for strategy in BASELINE_STRATEGIES:
        for topology in TOPOLOGIES:
            for network_cache in NETWORK_CACHE:
                experiment = copy.deepcopy(default)
                experiment["workload"]["alpha"]                = zipf_alpha
                experiment["strategy"]["name"]                 = strategy
                experiment["topology"]["name"]                 = topology
                experiment["cache_placement"]["network_cache"] = network_cache
                experiment["desc"] = (
                    "S2 | Zipf={} | {} | topo={} | cache={}".format(
                        zipf_alpha, strategy, topology, network_cache
                    )
                )
                EXPERIMENT_QUEUE.append(experiment)

# -----------------------------------------------------------------------------
# BAGIAN 2: Tiga Variasi LTP-CPS dengan nama berbeda
# -----------------------------------------------------------------------------
for zipf_alpha in ALPHA:
    for variant in LTP_VARIANTS:
        for topology in TOPOLOGIES:
            for network_cache in NETWORK_CACHE:
                experiment = copy.deepcopy(default)
                experiment["workload"]["alpha"]                = zipf_alpha
                experiment["strategy"]["name"]                 = variant["name"]
                experiment["strategy"]["alpha"]                = variant["alpha"]
                experiment["strategy"]["beta"]                 = variant["beta"]
                experiment["topology"]["name"]                 = topology
                experiment["cache_placement"]["network_cache"] = network_cache
                experiment["desc"] = (
                    "S2 | Zipf={} | {} (a={},b={}) | topo={} | cache={}".format(
                        zipf_alpha,
                        variant["name"],
                        variant["alpha"],
                        variant["beta"],
                        topology,
                        network_cache
                    )
                )
                EXPERIMENT_QUEUE.append(experiment)

# =============================================================================
# Total eksperimen:
#   Baseline : 5 strategi x 2 Zipf x 1 topo x 5 cache = 50
#   LTP-CPS  : 3 variasi  x 2 Zipf x 1 topo x 5 cache = 30
#   Total    : 80 eksperimen x 15 replikasi = 1200 runs
# =============================================================================
