"""Fast, offline checks for the reusable companion utilities."""

from pathlib import Path

import pandas as pd
import pytest

from ds301 import DATASETS, DatasetSpec, data_path, load_dataset, project_root
from ds301.reporting import audit_table, ensure_output


def test_catalogue_contains_documented_project_datasets() -> None:
    expected = {
        "adult",
        "bank_marketing",
        "bike_sharing",
        "credit_default",
        "email_eu_core",
        "online_retail",
        "sms_spam",
        "wholesale_customers",
        "world_bank_india",
    }
    assert expected == set(DATASETS)
    assert all(spec.source_url.startswith("https://") for spec in DATASETS.values())
    assert all(spec.licence for spec in DATASETS.values())


def test_unknown_dataset_is_rejected_before_network_access(tmp_path: Path) -> None:
    with pytest.raises(KeyError, match="Unknown dataset"):
        load_dataset("not_in_catalogue", output_root=tmp_path)


def test_dataset_contract_rejects_unsafe_keys_and_non_https_sources() -> None:
    common = {
        "title": "Teaching data",
        "provider": "Example provider",
        "licence": "Example licence",
        "teaching_use": "testing validation",
    }
    with pytest.raises(ValueError, match="safe"):
        DatasetSpec(key="../unsafe", source_url="https://example.test/data", **common)
    with pytest.raises(ValueError, match="HTTPS"):
        DatasetSpec(key="safe_key", source_url="http://example.test/data", **common)


def test_audit_table_reports_missingness_and_cardinality() -> None:
    data = pd.DataFrame({"region": ["East", "East", None], "sales": [10.0, 12.0, 9.0]})
    audit = audit_table(data)

    assert audit.loc["region", "missing_n"] == 1
    assert audit.loc["region", "missing_pct"] == pytest.approx(33.33)
    assert audit.loc["region", "unique_n"] == 1
    assert audit.loc["sales", "unique_n"] == 3


def test_ensure_output_creates_named_folder(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(project_root() / "notebooks" / "solutions")
    output = ensure_output("quality-audit")

    assert output == project_root() / "outputs" / "quality-audit"
    assert output.is_dir()


def test_data_path_resolves_from_a_nested_notebook_directory(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    notebook_folder = project_root() / "notebooks" / "case_studies"
    monkeypatch.chdir(notebook_folder)

    assert data_path("synthetic_customer_operations/customer_operations.csv") == (
        project_root() / "data" / "synthetic_customer_operations" / "customer_operations.csv"
    )


def test_project_root_uses_the_installed_package_when_started_elsewhere(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.delenv("DS301_PROJECT_ROOT", raising=False)
    monkeypatch.chdir(tmp_path)

    assert project_root().name == "DS301_Code_Companion"
