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
    questions_key = os.environ.get("QUESTIONS_KEY")
    context_key = os.environ.get("CONTEXT_KEY")
    output_prefix = os.environ.get("OUTPUT_PREFIX", "risk-registers/")
    validate_oscal = os.environ.get("VALIDATE_OSCAL", "true").lower() == "true"

    s3 = boto3.client("s3")

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        findings_path = temp_path / "findings.json"
        mapping_path = temp_path / "mapping.json"
        questions_path = temp_path / "questions.json"
        context_path = temp_path / "context.json"
        csv_path = temp_path / "risk-register.csv"
        json_path = temp_path / "risk-register.json"

        s3.download_file(bucket, key, str(findings_path))
        s3.download_file(bucket, mapping_key, str(mapping_path))
        if questions_key:
            s3.download_file(bucket, questions_key, str(questions_path))
        if context_key:
            s3.download_file(bucket, context_key, str(context_path))

        cli_args = [
            "--findings",
            str(findings_path),
            "--mapping",
            str(mapping_path),
            "--out",
            str(csv_path),
            "--json-out",
            str(json_path),
        ]
        if validate_oscal:
            cli_args.insert(0, "--validate-oscal")
        if questions_key:
            cli_args.extend(["--questions", str(questions_path)])
        if context_key:
            cli_args.extend(["--context", str(context_path)])

        exit_code = main(cli_args)
        if exit_code:
            raise RuntimeError(f"oscal-risk-bridge failed with exit code {exit_code}")

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
