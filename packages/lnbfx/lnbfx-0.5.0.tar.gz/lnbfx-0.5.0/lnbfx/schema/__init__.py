"""Schema.

Tables.

.. autosummary::
   :toctree: .

   BfxPipeline
   BfxRun
   Bfxmeta
   DObjectBfxmeta

Dev tools.

.. autosummary::
   :toctree: .

   dev

"""
from .. import __version__ as _version

_schema_id = "tsds"
_name = "bfx"
_migration = "cfda12fc80a8"
__version__ = _version

from . import dev
from ._core import Bfxmeta, BfxPipeline, BfxRun, DObjectBfxmeta  # noqa
