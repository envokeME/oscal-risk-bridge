from __future__ import annotations

import os
import tempfile
from pathlib import Path

from .cli import main


def handler(event: dict, context: object) -> dict:
    """Example Lambda entrypoint for S3-triggered OSCAL processing.

    The local CLI is the source of truth. This handler only adapts S3 events to
    temporary local files and can be completed once a real AWS account is chosen.
    """
    try:
        import boto3
    except ImportError as exc:
        raise RuntimeError("boto3 is required only for AWS Lambda execution") from exc

    record = event["Records"][0]
    bucket = record["s3"]["bucket"]["name"]
    key = record["s3"]["object"]["key"]
    output_bucket = os.environ.get("OUTPUT_BUCKET", bucket)
    mapping_key = os.environ["MAPPING_KEY"]
    output_prefix = os.environ.get("OUTPUT_PREFIX", "risk-registers/")

    s3 = boto3.client("s3")

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        findings_path = temp_path / "findings.json"
        mapping_path = temp_path / "mapping.json"
        csv_path = temp_path / "risk-register.csv"
        json_path = temp_path / "risk-register.json"

        s3.download_file(bucket, key, str(findings_path))
        s3.download_file(bucket, mapping_key, str(mapping_path))

        main(
            [
                "--findings",
                str(findings_path),
                "--mapping",
                str(mapping_path),
                "--out",
                str(csv_path),
                "--json-out",
                str(json_path),
            ]
        )

        base_name = Path(key).stem
        csv_key = f"{output_prefix}{base_name}.csv"
        json_key = f"{output_prefix}{base_name}.json"
        s3.upload_file(str(csv_path), output_bucket, csv_key)
        s3.upload_file(str(json_path), output_bucket, json_key)

    return {
        "status": "ok",
        "input": f"s3://{bucket}/{key}",
        "csv_output": f"s3://{output_bucket}/{csv_key}",
        "json_output": f"s3://{output_bucket}/{json_key}",
    }

