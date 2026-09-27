from types import SimpleNamespace

import pytest

from frontend.ingest import validate_uploaded_files


def uploaded_file(name: str, size: int):
    return SimpleNamespace(name=name, size=size)


def test_rejects_empty_upload(monkeypatch):
    monkeypatch.setenv("MAX_CSV_FILE_SIZE_MB", "1")

    errors = validate_uploaded_files([uploaded_file("empty.csv", 0)])

    assert errors == ["empty.csv: file is empty."]


def test_rejects_upload_larger_than_configured_limit(monkeypatch):
    monkeypatch.setenv("MAX_CSV_FILE_SIZE_MB", "1")

    errors = validate_uploaded_files([uploaded_file("large.csv", 1_048_577)])

    assert errors == ["large.csv: exceeds the 1 MB upload limit."]


def test_rejects_duplicate_filenames_case_insensitively(monkeypatch):
    monkeypatch.setenv("MAX_CSV_FILE_SIZE_MB", "1")

    errors = validate_uploaded_files([
        uploaded_file("Sales.csv", 10),
        uploaded_file("sales.CSV", 10),
    ])

    assert errors == [
        "Sales.csv: duplicate filename in this upload.",
        "sales.CSV: duplicate filename in this upload.",
    ]


def test_accepts_valid_unique_uploads(monkeypatch):
    monkeypatch.setenv("MAX_CSV_FILE_SIZE_MB", "1")

    assert validate_uploaded_files([
        uploaded_file("sales.csv", 10),
        uploaded_file("customers.csv", 20),
    ]) == []


def test_rejects_invalid_file_size_setting(monkeypatch):
    monkeypatch.setenv("MAX_CSV_FILE_SIZE_MB", "0")

    with pytest.raises(ValueError, match="positive number"):
        validate_uploaded_files([uploaded_file("sales.csv", 10)])
