from icarus.registry import register_strategy
from icarus.models.strategy.base import Strategy
from icarus.util import path_links
import networkx as nx

@register_strategy('HYBRID_MCDM')
class HybridMCDM(Strategy):

    def __init__(self, view, controller, alpha=0.5, beta=0.5, **kwargs):
        super(HybridMCDM, self).__init__(view, controller, **kwargs)
        # Pre-compute BC sekali saja di awal → O(1) saat runtime
        self.betw = nx.betweenness_centrality(view.topology())
        # Normalisasi BC ke [0,1]
        max_betw = max(self.betw.values()) if self.betw else 1.0
        self.betw_norm = {
            node: val / max_betw 
            for node, val in self.betw.items()
        }
        self.tabel_popularitas = {}
        self.alpha = alpha  # bobot topologi
        self.beta = beta    # bobot popularitas

    def process_event(self, time, receiver, content, log):
        self.controller.start_session(time, receiver, content, log)

        # Update popularitas
        self.tabel_popularitas[content] = \
            self.tabel_popularitas.get(content, 0) + 1

        source = self.view.content_source(content)
        if source is None:
            self.controller.end_session()
            return

        path = self.view.shortest_path(receiver, source)

        # === PHASE 1: Forward Request ===
        serving_node = source
        for u, v in path_links(path):
            self.controller.forward_request_hop(u, v)
            if self.view.has_cache(v):
                if self.controller.get_content(v):
                    serving_node = v
                    break
            # Jika v adalah source
            if v == source:
                self.controller.get_content(v)
                serving_node = v

        # === PHASE 2: Return Content ===
        return_path = list(reversed(
            self.view.shortest_path(receiver, serving_node)
        ))

        # Kandidat node cache (kecuali receiver dan serving_node)
        vcand = [
            node for node in return_path[1:-1]
            if self.view.has_cache(node)
        ]

        # === PHASE 3: Scoring HYBRID MCDM ===
        best_node = None
        max_score = -1.0

        if vcand:
            # Normalisasi popularitas terhadap max yang diketahui
            max_pop = max(self.tabel_popularitas.values())

            for node in vcand:
                # Topologi: BC yang sudah dinormalisasi [0,1]
                skor_topologi = self.betw_norm.get(node, 0.0)

                # Popularitas: dinormalisasi [0,1]
                skor_popularitas = \
                    self.tabel_popularitas[content] / max_pop

                # Agregasi MCDM: weighted sum (bukan perkalian)
                skor_akhir = (self.alpha * skor_topologi +
                              self.beta  * skor_popularitas)

                if skor_akhir > max_score:
                    max_score = skor_akhir
                    best_node = node

        # === PHASE 4: Forward Content + Cache ===
        for u, v in path_links(return_path):
            self.controller.forward_content_hop(u, v)  # ← WAJIB ada
            if v == best_node:
                self.controller.put_content(v)

        self.controller.end_session()
