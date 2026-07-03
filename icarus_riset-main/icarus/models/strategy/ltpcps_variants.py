"""ltpcps_variants.py — Registrasi Variasi Bobot LTP-CPS

File ini mendaftarkan tiga variasi bobot LTP-CPS
untuk kebutuhan Skenario 2 (sensitivitas bobot).

Cara pakai:
  Letakkan di folder yang sama dengan ltpcps.py:
    icarus/models/strategy/ltpcps_variants.py

  Tambahkan ke __init__.py folder strategy:
    from .ltpcps_variants import *

Tidak ada perubahan pada ltpcps.py yang utama.
Tidak ada perubahan pada on-path logic.

Strategi yang didaftarkan:
  LTP_CPS_7_3 → w_t=0.7, w_p=0.3 (topologi dominan)
  LTP_CPS_5_5 → w_t=0.5, w_p=0.5 (seimbang)
  LTP_CPS_3_7 → w_t=0.3, w_p=0.7 (popularitas dominan)
"""

from icarus.registry import register_strategy
from icarus.util import inheritdoc
from .base import Strategy
from .ltpcps import LTPCPS   # ← import base class dari ltpcps.py


@register_strategy('LTP_CPS_7_3')
class LTPCPS_7_3(LTPCPS):
    """LTP-CPS w_t=0.7, w_p=0.3 — topologi dominan."""
    @inheritdoc(Strategy)
    def __init__(self, view, controller, **kwargs):
        super().__init__(view, controller, w_t=0.7, w_p=0.3, **kwargs)


@register_strategy('LTP_CPS_5_5')
class LTPCPS_5_5(LTPCPS):
    """LTP-CPS w_t=0.5, w_p=0.5 — seimbang."""
    @inheritdoc(Strategy)
    def __init__(self, view, controller, **kwargs):
        super().__init__(view, controller, w_t=0.5, w_p=0.5, **kwargs)


@register_strategy('LTP_CPS_3_7')
class LTPCPS_3_7(LTPCPS):
    """LTP-CPS w_t=0.3, w_p=0.7 — popularitas dominan."""
    @inheritdoc(Strategy)
    def __init__(self, view, controller, **kwargs):
        super().__init__(view, controller, w_t=0.3, w_p=0.7, **kwargs)
