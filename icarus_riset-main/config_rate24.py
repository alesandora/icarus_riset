"""
Variasi Request Rate — Rate 24 req/s
=====================================
Bagian dari Gap 6a: Stabilitas LTP-CPS di berbagai traffic load
REQ_RATE : 24 req/s (traffic tinggi)
Cache    : 10% dan 20% (fixed)
Topologi : TISCALI + GEANT
Zipf α   : 0.8 dan 1.0
Replikasi: 15

Jalankan: python -m icarus run config_rate24.py
Total   : 6 × 2 × 2 × 2 × 15 = 720 runs
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
REQ_RATE            = 24.0         # ← traffic tinggi
CACHE_POLICY        = "IN_CACHE_LFU"
ALPHA               = [0.8, 1.0]
NETWORK_CACHE       = [0.10, 0.20]
TOPOLOGIES          = ["TISCALI", "GEANT"]
STRATEGIES          = ["LCE", "LCD", "CL4M", "PROB_CACHE", "MCDM", "LTP_CPS"]

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
                experiment["desc"] = "rate=24 | Zipf={} | {} | topo={} | cache={}".format(
                    alpha, strategy, topology, network_cache)
                EXPERIMENT_QUEUE.append(experiment)
