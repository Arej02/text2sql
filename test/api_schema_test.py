import pytest
from pydantic import ValidationError

from src.api.schemas import OutputSchema


def convert_response(confidence_score: float) -> dict:
    return {
        "Question": "How many students are there?",
        "SQL_Query": "SELECT COUNT(*) FROM students LIMIT 10",
        "Confidence_Score": confidence_score,
        "Feedback": "Query generated successfully.",
        "Rows_Count": 1,
        "Rows": [{"count": 10}],
        "Execution_Time_Ms": 1.5,
        "Messages": [],
    }


def test_convert_response_includes_bounded_confidence_score():
    response = OutputSchema(**convert_response(0.85))

    assert response.Confidence_Score == 0.85


@pytest.mark.parametrize("confidence_score", [-0.01, 1.01])
def test_convert_response_rejects_confidence_outside_zero_to_one(confidence_score):
    with pytest.raises(ValidationError):
        OutputSchema(**convert_response(confidence_score))
