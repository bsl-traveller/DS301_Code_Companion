"""Open-data catalogue and reproducible loaders for the book companion.

UCI datasets are retrieved through UCI's official ``ucimlrepo`` client. The
World Bank loader uses the official version-2 Indicators API, which requires no
API key. Each loader writes a flat teaching extract plus metadata so that a
notebook can be rerun without hiding source provenance.
"""

from __future__ import annotations

import gzip
import io
import zipfile
from collections.abc import Callable
from pathlib import Path

import pandas as pd
import requests
from ucimlrepo import fetch_ucirepo

from .contracts import DatasetMetadata, DatasetSpec
from .paths import data_path

DATASETS: dict[str, DatasetSpec] = {
    "bank_marketing": DatasetSpec(
        key="bank_marketing",
        title="Bank Marketing",
        provider="UCI Machine Learning Repository",
        source_url="https://archive.ics.uci.edu/dataset/222/bank+marketing",
        licence="CC BY 4.0",
        teaching_use="classification, imbalance, campaign decisions and leakage",
        uci_id=222,
    ),
    "bike_sharing": DatasetSpec(
        key="bike_sharing",
        title="Bike Sharing",
        provider="UCI Machine Learning Repository",
        source_url="https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset",
        licence="CC BY 4.0",
        teaching_use="time series, regression, seasonality and operations planning",
        uci_id=275,
    ),
    "wholesale_customers": DatasetSpec(
        key="wholesale_customers",
        title="Wholesale Customers",
        provider="UCI Machine Learning Repository",
        source_url="https://archive.ics.uci.edu/dataset/292/wholesale+customers",
        licence="CC BY 4.0",
        teaching_use="scaling, clustering and segment interpretation",
        uci_id=292,
    ),
    "credit_default": DatasetSpec(
        key="credit_default",
        title="Default of Credit Card Clients",
        provider="UCI Machine Learning Repository",
        source_url="https://archive.ics.uci.edu/dataset/350/default+of+credit+card+clients",
        licence="CC BY 4.0",
        teaching_use="classification, asymmetric errors, calibration and responsible use",
        uci_id=350,
        caution="A historical observational dataset; not a template for automated credit denial.",
    ),
    "online_retail": DatasetSpec(
        key="online_retail",
        title="Online Retail",
        provider="UCI Machine Learning Repository",
        source_url="https://archive.ics.uci.edu/dataset/352/online+retail",
        licence="CC BY 4.0",
        teaching_use="transactions, returns, RFM summaries, cohorts and customer analytics",
        uci_id=352,
    ),
    "adult": DatasetSpec(
        key="adult",
        title="Adult (Census Income)",
        provider="UCI Machine Learning Repository",
        source_url="https://archive.ics.uci.edu/dataset/2/adult",
        licence="CC BY 4.0",
        teaching_use="measurement limitations, subgroup error analysis and fairness concepts",
        uci_id=2,
        caution=(
            "Extracted from 1994 US census records with historical category choices. "
            "Use for critical audit, not to essentialise groups or justify consequential decisions."
        ),
    ),
    "sms_spam": DatasetSpec(
        key="sms_spam",
        title="SMS Spam Collection",
        provider="UCI Machine Learning Repository",
        source_url="https://archive.ics.uci.edu/dataset/228/sms+spam+collection",
        licence="CC BY 4.0",
        teaching_use="text representation, sparse classification and review-queue evaluation",
        uci_id=228,
        caution=(
            "Messages combine several collection sources and historical spam patterns. "
            "Do not interpret benchmark accuracy as current production readiness."
        ),
    ),
    "email_eu_core": DatasetSpec(
        key="email_eu_core",
        title="email-Eu-core network",
        provider="Stanford Network Analysis Project",
        source_url="https://snap.stanford.edu/data/email-Eu-core.html",
        licence="Public research dataset; cite the documented source publications",
        teaching_use="directed networks, degree, density, components and boundary reasoning",
        caution=(
            "An edge records at least one internal email under the source boundary; "
            "it does not establish friendship, influence, performance or misconduct."
        ),
    ),
    "world_bank_india": DatasetSpec(
        key="world_bank_india",
        title="World Development Indicators: India teaching extract",
        provider="World Bank Indicators API v2",
        source_url="https://datahelpdesk.worldbank.org/knowledgebase/articles/889392",
        licence="World Bank Dataset Terms; verify attribution for redistribution",
        teaching_use="public indicators, metadata, time series and BI",
    ),
}


def _write_metadata(folder: Path, spec: DatasetSpec, rows: int, columns: int) -> None:
    metadata = DatasetMetadata(
        key=spec.key,
        title=spec.title,
        provider=spec.provider,
        source_url=spec.source_url,
        licence=spec.licence,
        teaching_use=spec.teaching_use,
        caution=spec.caution,
        rows=rows,
        columns=columns,
    )
    (folder / "metadata.json").write_text(metadata.model_dump_json(indent=2), encoding="utf-8")


def _load_uci(spec: DatasetSpec, output_root: Path) -> pd.DataFrame:
    if spec.uci_id is None:
        raise ValueError(f"{spec.key} has no UCI identifier")
    repository = fetch_ucirepo(id=spec.uci_id)
    frames = []
    identifiers = getattr(repository.data, "ids", None)
    if identifiers is not None:
        frames.append(identifiers)
    frames.append(repository.data.features)
    if repository.data.targets is not None:
        frames.append(repository.data.targets)
    data = pd.concat(frames, axis=1)
    folder = output_root / spec.key
    folder.mkdir(parents=True, exist_ok=True)
    data.to_csv(folder / "data.csv", index=False)
    variables = getattr(repository, "variables", None)
    if isinstance(variables, pd.DataFrame):
        variables.to_csv(folder / "variables.csv", index=False)
    _write_metadata(folder, spec, len(data), data.shape[1])
    return data


def _load_world_bank(spec: DatasetSpec, output_root: Path) -> pd.DataFrame:
    indicators = {
        "NY.GDP.MKTP.KD.ZG": "GDP growth (annual %)",
        "SP.URB.TOTL.IN.ZS": "Urban population (% of total)",
        "IT.NET.USER.ZS": "Individuals using the Internet (% of population)",
        "SL.UEM.TOTL.ZS": "Unemployment, total (% of labour force)",
    }
    records: list[dict[str, object]] = []
    for code, label in indicators.items():
        url = f"https://api.worldbank.org/v2/country/IND/indicator/{code}"
        response = requests.get(
            url,
            params={"format": "json", "date": "2000:2025", "per_page": 100},
            timeout=45,
        )
        response.raise_for_status()
        payload = response.json()
        for item in payload[1] or []:
            records.append(
                {
                    "country": item["country"]["value"],
                    "country_code": item["countryiso3code"],
                    "year": int(item["date"]),
                    "indicator_code": code,
                    "indicator": label,
                    "value": item["value"],
                    "unit": item.get("unit", ""),
                    "observation_status": item.get("obs_status", ""),
                }
            )
    data = pd.DataFrame(records).sort_values(["indicator_code", "year"])
    folder = output_root / spec.key
    folder.mkdir(parents=True, exist_ok=True)
    data.to_csv(folder / "data.csv", index=False)
    _write_metadata(folder, spec, len(data), data.shape[1])
    return data


def _load_email_eu_core(spec: DatasetSpec, output_root: Path) -> pd.DataFrame:
    """Download and unpack the official SNAP edge list."""
    response = requests.get(
        "https://snap.stanford.edu/data/email-Eu-core.txt.gz",
        timeout=60,
    )
    response.raise_for_status()
    with gzip.GzipFile(fileobj=io.BytesIO(response.content)) as archive:
        data = pd.read_csv(
            archive,
            sep=r"\s+",
            comment="#",
            names=["source", "target"],
            dtype={"source": "int64", "target": "int64"},
        )
    folder = output_root / spec.key
    folder.mkdir(parents=True, exist_ok=True)
    data.to_csv(folder / "data.csv", index=False)
    _write_metadata(folder, spec, len(data), data.shape[1])
    return data


def _load_sms_spam(spec: DatasetSpec, output_root: Path) -> pd.DataFrame:
    """Download the official UCI archive, which is not exposed by ucimlrepo."""
    response = requests.get(
        "https://archive.ics.uci.edu/static/public/228/sms+spam+collection.zip",
        timeout=60,
    )
    response.raise_for_status()
    with (
        zipfile.ZipFile(io.BytesIO(response.content)) as archive,
        archive.open("SMSSpamCollection") as source,
    ):
        data = pd.read_csv(source, sep="\t", names=["Category", "Message"])
    folder = output_root / spec.key
    folder.mkdir(parents=True, exist_ok=True)
    data.to_csv(folder / "data.csv", index=False)
    _write_metadata(folder, spec, len(data), data.shape[1])
    return data


LOADERS: dict[str, Callable[[DatasetSpec, Path], pd.DataFrame]] = {
    "email_eu_core": _load_email_eu_core,
    "sms_spam": _load_sms_spam,
    "world_bank_india": _load_world_bank,
}


def load_dataset(key: str, output_root: str | Path | None = None) -> pd.DataFrame:
    """Download one catalog dataset to the repository data area and return its table."""
    if key not in DATASETS:
        raise KeyError(f"Unknown dataset {key!r}; choose from {sorted(DATASETS)}")
    spec = DATASETS[key]
    root = data_path("open") if output_root is None else Path(output_root)
    loader = LOADERS.get(key, _load_uci)
    return loader(spec, root)
