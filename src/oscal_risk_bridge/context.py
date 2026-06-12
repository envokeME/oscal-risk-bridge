from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .models import (
    RiskContext,
    RiskContextAdjustment,
    RiskContextAnswer,
    RiskContextQuestion,
)


def load_risk_context(
    questions_path: Path | None,
    answers_path: Path | None,
) -> RiskContext:
    if questions_path is None and answers_path is None:
        return RiskContext()

    questions = _load_questions(questions_path) if questions_path else ()
    answers = _load_answers(answers_path) if answers_path else ()
    return RiskContext(questions=questions, answers=answers)


def get_context_adjustments(
    context: RiskContext,
    scenario_id: str,
) -> list[RiskContextAdjustment]:
    questions = {question.question_id: question for question in context.questions}
    adjustments: list[RiskContextAdjustment] = []

    for answer in context.answers:
        question = questions.get(answer.question_id)
        if question is None or not _applies_to(question, scenario_id):
            continue

        centered_value = answer.value - 3
        if centered_value == 0:
            continue

        delta = (centered_value / 2) * question.weight
        if question.direction == "decrease":
            delta *= -1

        adjustments.append(
            RiskContextAdjustment(
                question_id=answer.question_id,
                prompt=question.prompt,
                dimension=question.dimension,
                delta=round(delta, 2),
                value=answer.value,
                rationale=question.rationale,
                notes=answer.notes,
            )
        )

    return adjustments


def _load_questions(path: Path) -> tuple[RiskContextQuestion, ...]:
    with path.open("r", encoding="utf-8") as file:
        document = json.load(file)

    questions = document.get("questions", document if isinstance(document, list) else [])
    return tuple(_to_question(item) for item in questions)


def _load_answers(path: Path) -> tuple[RiskContextAnswer, ...]:
    with path.open("r", encoding="utf-8") as file:
        document = json.load(file)

    answers = document.get("answers", document if isinstance(document, list) else [])

    if isinstance(answers, dict):
        return tuple(
            RiskContextAnswer(question_id=str(question_id), value=_answer_value(value))
            for question_id, value in answers.items()
        )

    return tuple(_to_answer(item) for item in answers)


def _to_question(item: dict[str, Any]) -> RiskContextQuestion:
    applies_to = item.get("applies_to", ["*"])
    if isinstance(applies_to, str):
        applies_to = [applies_to]

    return RiskContextQuestion(
        question_id=str(item.get("id") or item["question_id"]),
        prompt=str(item["prompt"]),
        dimension=str(item.get("dimension", "likelihood")).strip().lower(),
        direction=str(item.get("direction", "increase")).strip().lower(),
        weight=float(item.get("weight", 1.0)),
        applies_to=tuple(str(value) for value in applies_to),
        rationale=str(item.get("rationale", "")),
    )


def _to_answer(item: dict[str, Any]) -> RiskContextAnswer:
    return RiskContextAnswer(
        question_id=str(item.get("id") or item["question_id"]),
        value=_answer_value(item.get("value")),
        notes=str(item.get("notes", "")),
    )


def _answer_value(value: Any) -> int:
    try:
        score = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Risk context answer values must be integers from 1 to 5: {value}") from exc

    if score < 1 or score > 5:
        raise ValueError(f"Risk context answer value must be between 1 and 5: {score}")
    return score


def _applies_to(question: RiskContextQuestion, scenario_id: str) -> bool:
    scenario_ids = {value.strip().upper() for value in question.applies_to}
    return "*" in scenario_ids or scenario_id.strip().upper() in scenario_ids
