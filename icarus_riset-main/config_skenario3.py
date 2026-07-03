"""
Skenario 3 — Pengaruh Cache Replacement Policy (LFU vs LRU)
=============================================================
Reproduksi Section 4.2 paper C3CPS + tambahan LTP-CPS

Strategi: LCE, LCD, MCDM, LTP_CPS
Policy  : IN_CACHE_LFU, LRU
Topologi: TISCALI + GEANT
Zipf α  : 0.8 (sesuai Figure 10 paper C3CPS)
Cache   : {5%, 10%, 15%, 20%, 25%}
Replikasi: 15

Hipotesis:
  LTP-CPS performanya konsisten di LFU maupun LRU
  karena popularitas sudah masuk ke scoring criterion
  — berbeda dengan CL4M yang tidak memperhitungkan popularitas.

Jalankan: python -m icarus run config_skenario3.py

Total: 2 policy x 4 strategi x 2 topologi x 5 cache
     = 80 eksperimen x 15 replikasi = 1200 runs
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
REQ_RATE            = 12.0
ZIPF_ALPHA          = 0.8       # fixed, sesuai Figure 10 paper C3CPS
NETWORK_CACHE       = [0.05, 0.10, 0.15, 0.20, 0.25]

# Dua topologi untuk generalisasi hasil
TOPOLOGIES    = ["TISCALI", "GEANT"]

# Dua cache replacement policy yang dibandingkan
CACHE_POLICIES = ["IN_CACHE_LFU", "LRU"]

# Strategi yang dibandingkan — subset dari Skenario 1
# Fokus pada strategi yang relevan untuk pengaruh cache policy
STRATEGIES = [
    "LCE",      # baseline — tidak peduli replacement policy
    "LCD",      # baseline — cache dekat source
    "MCDM",     # C3CPS — dirancang dengan mempertimbangkan RC (storage)
    "LTP_CPS",  # usulan — popularitas sudah di scoring, bukan di policy
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

for cache_policy in CACHE_POLICIES:
    for strategy in STRATEGIES:
        for topology in TOPOLOGIES:
            for network_cache in NETWORK_CACHE:
                experiment = copy.deepcopy(default)
                experiment["workload"]["alpha"]                = ZIPF_ALPHA
                experiment["strategy"]["name"]                 = strategy
                experiment["topology"]["name"]                 = topology
                experiment["cache_placement"]["network_cache"] = network_cache
                experiment["cache_policy"]["name"]             = cache_policy
                experiment["desc"] = (
                    "S3 | Policy={} | {} | topo={} | cache={}".format(
                        cache_policy, strategy, topology, network_cache
                    )
                )
                EXPERIMENT_QUEUE.append(experiment)

# =============================================================================
# RINGKASAN
# 2 policy x 4 strategi x 2 topologi x 5 cache = 80 eksperimen
# 80 x 15 replikasi = 1200 runs
# =============================================================================
