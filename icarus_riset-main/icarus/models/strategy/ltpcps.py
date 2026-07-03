"""LTP-CPS: Lightweight Topology-Popularity Cache Placement Strategy"""

import networkx as nx
from icarus.registry import register_strategy
from icarus.util import inheritdoc, path_links
from .base import Strategy

__all__ = ["LTPCPS"]


@register_strategy('LTP_CPS')
class LTPCPS(Strategy):
    """LTP-CPS: Lightweight Topology-Popularity Cache Placement Strategy.

    Strategi caching kooperatif berbasis dua kriteria:
      1. Betweenness Centrality (BC) — representasi topologi jaringan
      2. Popularitas konten — frekuensi request dinormalisasi [0,1]

    Formula:
      score(node) = alpha * BC_norm(node) + beta * pop_norm(content)
      best_node   = argmax(score) untuk semua node di vcand

    Nilai alpha=0.5 dan beta=0.5 ditetapkan berdasarkan hasil
    eksperimen sensitivitas (Skenario 2). Tiga variasi bobot diuji
    dan selisih performa antar variasi < 0.7%, menunjukkan LTP-CPS
    robust terhadap pilihan bobot. Variasi seimbang (0.5/0.5) dipilih
    karena performa kompetitif dan justifikasi paling netral.

    Semua pengaturan alpha/beta dikelola di file ini, bukan di config.py.

    Kompleksitas: O(m) per keputusan caching.
    Bandingkan dengan C3CPS: O(n²m) + overhead pandas per event.

    Referensi:
      - Freeman (1977): definisi Betweenness Centrality
      - Brandes (2001): algoritma BC efisien O(nm)
      - Breslau et al. (1999): model popularitas Zipf untuk NDN
      - Yazdani et al. (2019): Weighted Sum Model (WSM)
      - Negara et al. (2023): C3CPS — paper yang disederhanakan
    """

    @inheritdoc(Strategy)
    def __init__(self, view, controller, **kwargs):
        super().__init__(view, controller)

        # Bobot tetap — ditetapkan dari hasil Skenario 2
        self.alpha = 0.5   # bobot topologi (BC)
        self.beta  = 0.5   # bobot popularitas

        # Pre-compute Betweenness Centrality — SEKALI saat init
        # Algoritma Brandes (2001): O(nm) untuk graf tak berbobot
        # Disimpan sebagai dictionary → lookup O(1) saat runtime
        topology = view.topology()
        self.betw = nx.betweenness_centrality(topology)
        max_betw  = max(self.betw.values()) if self.betw else 1.0
        if max_betw == 0:
            max_betw = 1.0
        self.betw_norm = {
            node: val / max_betw
            for node, val in self.betw.items()
        }

        # Tabel popularitas konten — update O(1) per request
        self.tabel_popularitas = {}

    @inheritdoc(Strategy)
    def process_event(self, time, receiver, content, log):
        source = self.view.content_source(content)
        path   = self.view.shortest_path(receiver, source)
        self.controller.start_session(time, receiver, content, log)

        # ── Phase 1: Update popularitas — O(1) ──
        self.tabel_popularitas[content] = \
            self.tabel_popularitas.get(content, 0) + 1

        # ── Phase 2: Forward request, cek cache ──
        serving_node = source
        for u, v in path_links(path):
            self.controller.forward_request_hop(u, v)
            if self.view.has_cache(v):
                if self.controller.get_content(v):
                    serving_node = v
                    break
            if v == source:
                self.controller.get_content(v)

        # ── Phase 3: Scoring LTP-CPS — O(m) ──
        return_path = list(reversed(
            self.view.shortest_path(receiver, serving_node)
        ))
        vcand = [
            n for n in return_path[1:-1]
            if self.view.has_cache(n)
        ]

        best_node = None
        if vcand:
            max_pop = max(self.tabel_popularitas.values())
            if max_pop == 0:
                max_pop = 1.0
            pop_norm  = self.tabel_popularitas[content] / max_pop
            max_score = -1.0
            for node in vcand:
                bc_norm = self.betw_norm.get(node, 0.0)
                score   = (self.alpha * bc_norm) + (self.beta * pop_norm)
                if score > max_score:
                    max_score = score
                    best_node = node

        # ── Phase 4: Forward content + cache di best_node ──
        for u, v in path_links(return_path):
            self.controller.forward_content_hop(u, v)
            if v == best_node:
                self.controller.put_content(v)

        self.controller.end_session()
