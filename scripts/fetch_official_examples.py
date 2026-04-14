#!/usr/bin/env python3
"""Download and filter HL7 FHIR R4 official JSON examples."""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import ssl
import shutil
import sys
import urllib.request
import zipfile
from pathlib import Path


SOURCE_URL = "https://www.hl7.org/fhir/R4/examples-json.zip"
TARGET_RESOURCE_TYPES = ("Patient", "Observation", "Condition")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    root = repo_root()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-url", default=SOURCE_URL)
    parser.add_argument(
        "--zip-path",
        type=Path,
        default=root / "data" / "raw" / "downloads" / "examples-json.zip",
    )
    parser.add_argument(
        "--raw-root",
        type=Path,
        default=root / "data" / "raw",
    )
    parser.add_argument(
        "--manifest-path",
        type=Path,
        default=root / "data" / "raw" / "official_examples_manifest.csv",
    )
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument(
        "--force-download",
        action="store_true",
        help="Redownload the source archive even if it already exists.",
    )
    return parser.parse_args()


def download_file(url: str, destination: Path, timeout: int, force: bool) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists() and not force:
        print(f"Using existing archive: {destination}")
        return

    request = urllib.request.Request(
        url,
        headers={"User-Agent": "FHIR-official-seeds/1.0"},
    )
    with urllib.request.urlopen(request, timeout=timeout, context=build_ssl_context()) as response:
        destination.write_bytes(response.read())
    print(f"Downloaded archive to {destination}")


def build_ssl_context() -> ssl.SSLContext:
    context = ssl.create_default_context()
    candidate_paths = [
        os.environ.get("SSL_CERT_FILE"),
        "/etc/ssl/cert.pem",
        "/private/etc/ssl/cert.pem",
    ]
    for candidate in candidate_paths:
        if candidate and Path(candidate).exists():
            return ssl.create_default_context(cafile=candidate)
    return context


def clean_target_directories(raw_root: Path, manifest_path: Path) -> None:
    for resource_type in TARGET_RESOURCE_TYPES:
        resource_dir = raw_root / resource_type
        if resource_dir.exists():
            shutil.rmtree(resource_dir)
    if manifest_path.exists():
        manifest_path.unlink()


def safe_filename(source_name: str) -> str:
    compact = source_name.strip("/\\").replace("/", "__").replace("\\", "__")
    return re.sub(r"[^A-Za-z0-9._-]+", "-", compact)


def extract_target_examples(zip_path: Path, raw_root: Path, manifest_path: Path) -> dict[str, int]:
    raw_root.mkdir(parents=True, exist_ok=True)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    counts = {resource_type: 0 for resource_type in TARGET_RESOURCE_TYPES}

    with zipfile.ZipFile(zip_path) as archive, manifest_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["resource_type", "resource_id", "source_zip_path", "extracted_path"],
        )
        writer.writeheader()

        for info in archive.infolist():
            if info.is_dir() or not info.filename.endswith(".json"):
                continue

            raw_bytes = archive.read(info.filename)
            try:
                payload = json.loads(raw_bytes.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError):
                continue

            resource_type = payload.get("resourceType")
            if resource_type not in TARGET_RESOURCE_TYPES:
                continue

            resource_dir = raw_root / resource_type
            resource_dir.mkdir(parents=True, exist_ok=True)
            output_name = safe_filename(info.filename)
            output_path = resource_dir / output_name

            with output_path.open("w", encoding="utf-8") as output_handle:
                json.dump(payload, output_handle, indent=2, ensure_ascii=True, sort_keys=True)
                output_handle.write("\n")

            counts[resource_type] += 1
            writer.writerow(
                {
                    "resource_type": resource_type,
                    "resource_id": payload.get("id", ""),
                    "source_zip_path": info.filename,
                    "extracted_path": str(output_path.relative_to(repo_root())),
                }
            )

    return counts


def main() -> int:
    args = parse_args()
    clean_target_directories(args.raw_root, args.manifest_path)
    download_file(args.source_url, args.zip_path, args.timeout, args.force_download)
    counts = extract_target_examples(args.zip_path, args.raw_root, args.manifest_path)

    print("Retained official examples:")
    for resource_type in TARGET_RESOURCE_TYPES:
        print(f"  {resource_type}: {counts[resource_type]}")
    print(f"Manifest: {args.manifest_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
