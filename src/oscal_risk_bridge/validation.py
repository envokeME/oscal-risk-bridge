from __future__ import annotations

import json
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any


OBJECTIVE_STATUS_STATES = {"satisfied", "not-satisfied"}
IMPLEMENTATION_STATUS_STATES = {
    "implemented",
    "partial",
    "planned",
    "alternative",
    "not-applicable",
}
CUSTOM_PROP_NAMES = {"control-id", "risk-severity", "severity", "status"}


@dataclass(frozen=True)
class ValidationMessage:
    level: str
    path: str
    message: str


def validate_oscal_file(path: Path) -> list[ValidationMessage]:
    with path.open("r", encoding="utf-8") as file:
        document = json.load(file)

    return validate_assessment_results(document)


def validate_assessment_results(document: dict[str, Any]) -> list[ValidationMessage]:
    messages: list[ValidationMessage] = []
    assessment_results = document.get("assessment-results")

    if not isinstance(assessment_results, dict):
        return [
            ValidationMessage(
                level="error",
                path="assessment-results",
                message="OSCAL assessment-results root object is required.",
            )
        ]

    _require_uuid(messages, assessment_results, "assessment-results.uuid")
    _require_object(messages, assessment_results, "metadata", "assessment-results.metadata")
    _validate_metadata(messages, assessment_results.get("metadata", {}))
    _validate_import_ap(messages, assessment_results.get("import-ap"))

    results = assessment_results.get("results")
    if not isinstance(results, list) or not results:
        messages.append(
            ValidationMessage(
                level="error",
                path="assessment-results.results",
                message="At least one assessment result is required.",
            )
        )
        return messages

    for index, result in enumerate(results):
        _validate_result(messages, result, index)

    return messages


def has_errors(messages: list[ValidationMessage]) -> bool:
    return any(message.level == "error" for message in messages)


def format_validation_messages(messages: list[ValidationMessage]) -> str:
    if not messages:
        return "OSCAL validation passed."

    return "\n".join(
        f"{message.level.upper()}: {message.path}: {message.message}"
        for message in messages
    )


def _validate_metadata(messages: list[ValidationMessage], metadata: Any) -> None:
    if not isinstance(metadata, dict):
        return

    for key in ("title", "last-modified", "version", "oscal-version"):
        if not metadata.get(key):
            messages.append(
                ValidationMessage(
                    level="error",
                    path=f"assessment-results.metadata.{key}",
                    message="Required OSCAL metadata field is missing.",
                )
            )

    _validate_props(
        messages,
        metadata.get("props", []) or [],
        "assessment-results.metadata.props",
    )


def _validate_import_ap(messages: list[ValidationMessage], import_ap: Any) -> None:
    if not isinstance(import_ap, dict):
        messages.append(
            ValidationMessage(
                level="error",
                path="assessment-results.import-ap",
                message="Required import-ap object is missing.",
            )
        )
        return

    if not import_ap.get("href"):
        messages.append(
            ValidationMessage(
                level="error",
                path="assessment-results.import-ap.href",
                message="import-ap.href is required.",
            )
        )


def _validate_result(
    messages: list[ValidationMessage],
    result: Any,
    index: int,
) -> None:
    path = f"assessment-results.results[{index}]"
    if not isinstance(result, dict):
        messages.append(
            ValidationMessage(
                level="error",
                path=path,
                message="Assessment result must be an object.",
            )
        )
        return

    _require_uuid(messages, result, f"{path}.uuid")

    for key in ("title", "description", "start"):
        if not result.get(key):
            messages.append(
                ValidationMessage(
                    level="error",
                    path=f"{path}.{key}",
                    message="Required assessment result field is missing.",
                )
            )

    reviewed_controls = result.get("reviewed-controls")
    if not isinstance(reviewed_controls, dict):
        messages.append(
            ValidationMessage(
                level="error",
                path=f"{path}.reviewed-controls",
                message="reviewed-controls is required for an assessment result.",
            )
        )
    else:
        control_selections = reviewed_controls.get("control-selections")
        if not isinstance(control_selections, list) or not control_selections:
            messages.append(
                ValidationMessage(
                    level="error",
                    path=f"{path}.reviewed-controls.control-selections",
                    message="At least one reviewed control selection is required.",
                )
            )

    _validate_props(messages, result.get("props", []) or [], f"{path}.props")

    findings = result.get("findings", []) or []
    if not isinstance(findings, list):
        messages.append(
            ValidationMessage(
                level="error",
                path=f"{path}.findings",
                message="findings must be an array when provided.",
            )
        )
        return

    for finding_index, finding in enumerate(findings):
        _validate_finding(messages, finding, f"{path}.findings[{finding_index}]")


def _validate_finding(messages: list[ValidationMessage], finding: Any, path: str) -> None:
    if not isinstance(finding, dict):
        messages.append(
            ValidationMessage(level="error", path=path, message="Finding must be an object.")
        )
        return

    _require_uuid(messages, finding, f"{path}.uuid")

    for key in ("title", "description"):
        if not finding.get(key):
            messages.append(
                ValidationMessage(
                    level="error",
                    path=f"{path}.{key}",
                    message="Required finding field is missing.",
                )
            )

    target = finding.get("target")
    if not isinstance(target, dict):
        messages.append(
            ValidationMessage(
                level="error",
                path=f"{path}.target",
                message="Finding target object is required.",
            )
        )
    else:
        for key in ("type", "target-id"):
            if not target.get(key):
                messages.append(
                    ValidationMessage(
                        level="error",
                        path=f"{path}.target.{key}",
                        message="Finding target field is required.",
                    )
                )

    status = finding.get("status")
    if not isinstance(status, dict):
        messages.append(
            ValidationMessage(
                level="error",
                path=f"{path}.status",
                message="Finding status object is required.",
            )
        )
    else:
        state = str(status.get("state", "")).strip()
        if state not in OBJECTIVE_STATUS_STATES:
            messages.append(
                ValidationMessage(
                    level="error",
                    path=f"{path}.status.state",
                    message="Finding objective status must be satisfied or not-satisfied.",
                )
            )

    implementation_status = finding.get("implementation-status")
    if isinstance(implementation_status, dict):
        state = str(implementation_status.get("state", "")).strip()
        if state and state not in IMPLEMENTATION_STATUS_STATES:
            messages.append(
                ValidationMessage(
                    level="error",
                    path=f"{path}.implementation-status.state",
                    message="Implementation status is not an OSCAL-defined state.",
                )
            )

    _validate_props(messages, finding.get("props", []) or [], f"{path}.props")


def _validate_props(
    messages: list[ValidationMessage],
    props: list[dict[str, Any]],
    path: str,
) -> None:
    for index, prop in enumerate(props):
        if not isinstance(prop, dict):
            messages.append(
                ValidationMessage(
                    level="error",
                    path=f"{path}[{index}]",
                    message="Property must be an object.",
                )
            )
            continue

        name = str(prop.get("name", "")).strip()
        value = prop.get("value")
        namespace = str(prop.get("ns", "")).strip()

        if not name:
            messages.append(
                ValidationMessage(
                    level="error",
                    path=f"{path}[{index}].name",
                    message="Property name is required.",
                )
            )
        if value is None:
            messages.append(
                ValidationMessage(
                    level="error",
                    path=f"{path}[{index}].value",
                    message="Property value is required.",
                )
            )
        if name in CUSTOM_PROP_NAMES and not namespace:
            messages.append(
                ValidationMessage(
                    level="warning",
                    path=f"{path}[{index}].ns",
                    message="Custom GRC property should use a custom namespace.",
                )
            )


def _require_object(
    messages: list[ValidationMessage],
    item: dict[str, Any],
    key: str,
    path: str,
) -> None:
    if not isinstance(item.get(key), dict):
        messages.append(
            ValidationMessage(
                level="error",
                path=path,
                message="Required OSCAL object is missing.",
            )
        )


def _require_uuid(
    messages: list[ValidationMessage],
    item: dict[str, Any],
    path: str,
) -> None:
    value = item.get("uuid")
    if not value:
        messages.append(
            ValidationMessage(level="error", path=path, message="UUID is required.")
        )
        return

    try:
        uuid.UUID(str(value))
    except ValueError:
        messages.append(
            ValidationMessage(
                level="error",
                path=path,
                message="Value must be a valid UUID.",
            )
        )
