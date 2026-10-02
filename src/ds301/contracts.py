"""Validated domain contracts used by DS301's reusable utilities."""

from __future__ import annotations

import re

from pydantic import BaseModel, ConfigDict, Field, field_validator


class DatasetSpec(BaseModel):
    """A documented dataset that may be acquired for a teaching case study."""

    model_config = ConfigDict(frozen=True, str_strip_whitespace=True)

    key: str = Field(pattern=r"^[a-z][a-z0-9_]*$")
    title: str = Field(min_length=3)
    provider: str = Field(min_length=3)
    source_url: str
    licence: str = Field(min_length=3)
    teaching_use: str = Field(min_length=3)
    uci_id: int | None = Field(default=None, ge=1)
    caution: str = ""

    @field_validator("source_url")
    @classmethod
    def require_https_source(cls, value: str) -> str:
        if not value.startswith("https://"):
            raise ValueError("source_url must use HTTPS")
        return value

    @field_validator("key")
    @classmethod
    def reject_reserved_path_names(cls, value: str) -> str:
        if value in {"open", "synthetic", "metadata"} or not re.fullmatch(
            r"[a-z][a-z0-9_]*", value
        ):
            raise ValueError("key must be a safe, non-reserved dataset directory name")
        return value


class DatasetMetadata(BaseModel):
    """Validated provenance metadata written beside a locally acquired dataset."""

    model_config = ConfigDict(str_strip_whitespace=True)

    key: str
    title: str
    provider: str
    source_url: str
    licence: str
    teaching_use: str
    caution: str = ""
    rows: int = Field(ge=0)
    columns: int = Field(ge=1)
