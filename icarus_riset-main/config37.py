"""
Skenario 2 — Variasi Bobot LTP-CPS: w_t=0.3, w_p=0.7
========================================================
Popularitas dominan — bobot popularitas lebih besar dari BC

Jalankan: python -m icarus run --results hasil_bobot37.pickle config_bobot37.py
Total   : 6 strategi × 2 Zipf × 1 topo × 5 cache × 15 rep = 900 runs
"""

from multiprocessing import cpu_count
from collections import deque
import copy
from icarus.util import Tree

LOG_LEVEL          = "INFO"
PARALLEL_EXECUTION = True
N_PROCESSES        = cpu_count()
RESULTS_FORMAT     = "PICKLE"
N_REPLICATIONS     = 15

DATA_COLLECTORS = ["CACHE_HIT_RATIO", "LATENCY", "PATH_STRETCH", "LINK_LOAD"]

N_CONTENTS          = 1 * 10 ** 5
N_WARMUP_REQUESTS   = 5 * 10 ** 4
N_MEASURED_REQUESTS = 2.5 * 10 ** 5
REQ_RATE            = 12.0
CACHE_POLICY        = "IN_CACHE_LFU"
ALPHA               = [0.8, 1.0]
NETWORK_CACHE       = [0.05, 0.10, 0.15, 0.20, 0.25]
TOPOLOGIES          = ["TISCALI"]

# Strategi: LTP-CPS variasi ini + semua baseline
STRATEGIES = ["LCE", "LCD", "CL4M", "PROB_CACHE", "MCDM", "LTP_CPS_3_7"]

EXPERIMENT_QUEUE = deque()
default = Tree()
default["workload"] = {
    "name": "STATIONARY", "n_contents": N_CONTENTS,
    "n_warmup": N_WARMUP_REQUESTS, "n_measured": N_MEASURED_REQUESTS,
    "rate": REQ_RATE,
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
                experiment["desc"] = "S2 | w_t=0.3 w_p=0.7 | Zipf={} | {} | cache={}".format(
                    alpha, strategy, network_cache)
                EXPERIMENT_QUEUE.append(experiment)
