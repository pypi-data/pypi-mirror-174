from typing import Optional

from lnschema_core.dev.sqlmodel import schema_sqlmodel

# import lnschema_core  # noqa
from sqlmodel import Field, ForeignKeyConstraint

from . import _name as schema_name
from .dev import id as idg

SQLModel, prefix, schema_arg = schema_sqlmodel(schema_name)


class BfxPipeline(SQLModel, table=True):  # type: ignore
    """Bioinformatics pipeline metadata."""

    __tablename__ = f"{prefix}bfx_pipeline"

    __table_args__ = (
        ForeignKeyConstraint(
            ["id", "v"],
            ["core.pipeline.id", "core.pipeline.v"],
            name="bfx_pipeline_pipeline",
        ),
    )
    id: str = Field(primary_key=True, index=True)
    v: str = Field(primary_key=True, index=True)


class BfxRun(SQLModel, table=True):  # type: ignore
    """Bioinformatics pipeline run metadata."""

    __tablename__ = f"{prefix}run"
    __table_args__ = (
        ForeignKeyConstraint(
            ["bfx_pipeline_id", "bfx_pipeline_v"],
            ["bfx.pipeline.id", "bfx.pipeline.v"],
            name="bfx_run_pipeline",
        ),
    )
    id: str = Field(primary_key=True, foreign_key="core.pipeline_run.id", index=True)
    dir: Optional[str] = None
    bfx_pipeline_id: str = Field(index=True)
    bfx_pipeline_v: str = Field(index=True)


class Bfxmeta(SQLModel, table=True):  # type: ignore
    """Metadata for files associated with bioinformatics pipelines."""

    id: Optional[str] = Field(default_factory=idg.bfxmeta, primary_key=True)
    file_type: Optional[str] = None
    dir: Optional[str] = None


class DObjectBfxmeta(SQLModel, table=True):  # type: ignore
    """Link table between dobject and bfxmeta tables."""

    __tablename__ = f"{prefix}dobject_bfxmeta"
    dobject_id: str = Field(primary_key=True, foreign_key="core.dobject.id")
    bfxmeta_id: str = Field(primary_key=True, foreign_key="bfx.bfxmeta.id")
