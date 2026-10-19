from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_ask_routes_to_ask_tool():
    response = client.post(
        "/agent",
        json={
            "task": "ask",
            "input": "How do I request annual leave?"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["tool"] == "ask"
    assert data["tool_calls"] == 1


def test_predict_routes_to_predict_tool():
    response = client.post(
        "/agent",
        json={"task": "predict", "input": "C001"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["tool"] == "predict"


def test_unsupported_task_is_refused():
    response = client.post(
        "/agent",
        json={"task": "book_flight", "input": "Book a flight"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "refused"
    assert data["tool_calls"] == 0


def test_lookup_tool_failure_is_handled_safely():
    response = client.post(
        "/agent",
        json={"task": "lookup", "input": "ERROR_TEST"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "error"
    assert data["message"] == "The tool failed. Please try again."
    assert data["tool_calls"] == 1

def test_lookup_unknown_record_returns_not_found():
    response = client.post(
        "/agent",
        json={"task": "lookup", "input": "UNKNOWN_ID"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["result"] == {"error": "Record not found"}
    assert data["tool_calls"] == 1
def test_auto_router_selects_ask():
    response = client.post(
        "/agent",
        json={
            "task": None,
            "input": "How do I request annual leave?"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["tool"] == "ask"
    assert data["tool_calls"] == 1


def test_auto_router_selects_predict():
    response = client.post(
        "/agent",
        json={
            "task": None,
            "input": "What is the churn probability for customer C001?"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["tool"] == "predict"
    assert data["tool_calls"] == 1


def test_ambiguous_request_is_flagged_for_review():
    response = client.post(
        "/agent",
        json={
            "task": None,
            "input": "Please do something for me"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "needs_review"
    assert data["tool_calls"] == 0