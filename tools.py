def ask_tool(question: str) -> dict:
    """Mock the RAG /ask tool for now."""
    return {
        "answer": f"Retrieved information relevant to: {question}",
        "source": "mock_knowledge_base"
    }


def predict_tool(customer_id: str) -> dict:
    """Mock the churn /predict tool for now."""
    return {
        "customer_id": customer_id,
        "prediction": 0,
        "churn_probability": 0.25
    }


def lookup_tool(record_id: str) -> dict:
    """Mock a lookup tool."""
    if record_id == "ERROR_TEST":
        raise RuntimeError("Simulated lookup failure")

    records = {
        "C001": {"name": "Jane", "status": "active"},
        "C002": {"name": "John", "status": "inactive"}
    }

    record = records.get(record_id)

    if record is None:
        return {"error": "Record not found"}

    return record
