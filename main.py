from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import logging

from tools import ask_tool, predict_tool, lookup_tool


app = FastAPI(title="Week 10 Tool-Using Agent")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger("week10_agent")

templates = Jinja2Templates(directory="templates")


class AgentRequest(BaseModel):
    # task is optional: the agent can infer it from the user's input
    task: str | None = None
    input: str


@app.get("/", response_class=HTMLResponse)
def show_ui(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


@app.get("/health")
def health():
    return {"message": "Week 10 agent is running"}


def choose_tool(user_input: str, requested_task: str | None = None):
    """
    Select a tool using simple keyword rules.
    This is a basic rule-based router, not an LLM planner.
    """
    text = user_input.lower()

    # If the user explicitly selected a supported task, respect it.
    if requested_task:
        task = requested_task.lower().strip()
        if task in ["ask", "predict", "lookup"]:
            return task, False

        return None, False

    # Human-review checkpoint for ambiguous or sensitive requests.
    review_terms = [
        "delete", "cancel", "transfer money", "change my account",
        "medical", "legal", "urgent", "approve"
    ]

    if any(term in text for term in review_terms):
        return None, True

    # Infer tool from request language.
    if any(word in text for word in [
        "predict churn", "churn probability", "will this customer churn",
        "predict", "prediction"
    ]):
        return "predict", False

    if any(word in text for word in [
        "customer id", "record", "lookup", "look up",
        "find customer", "customer status"
    ]):
        return "lookup", False

    if any(word in text for word in [
        "how", "what", "why", "explain", "policy",
        "process", "procedure", "tell me"
    ]):
        return "ask", False

    # No confident match: ask for clarification/review.
    return None, True


@app.post("/agent")
def run_agent(request: AgentRequest):
    task, needs_review = choose_tool(request.input, request.task)

    logger.info(
        "Agent decision | requested_task=%s | selected_tool=%s | review=%s | input=%s",
        request.task,
        task,
        needs_review,
        request.input
    )

    # Guardrail: flag unclear or sensitive requests for human review.
    if needs_review:
        return {
            "status": "needs_review",
            "message": (
                "This request needs clarification or human review "
                "before a tool can be called."
            ),
            "tool_calls": 0
        }

    # Guardrail: refuse unsupported task names.
    if task not in ["ask", "predict", "lookup"]:
        return {
            "status": "refused",
            "message": "Unsupported task. Choose ask, predict, or lookup.",
            "tool_calls": 0
        }

    # Guardrail: allow at most one tool call per request.
    max_tool_calls = 1
    tool_calls = 1

    if tool_calls > max_tool_calls:
        logger.warning("Tool-call limit reached | limit=%s", max_tool_calls)
        return {
            "status": "stopped",
            "message": "Maximum tool-call limit reached.",
            "tool_calls": tool_calls
        }

    try:
        if task == "ask":
            result = ask_tool(request.input)
        elif task == "predict":
            result = predict_tool(request.input)
        else:
            result = lookup_tool(request.input)

        logger.info(
            "Tool completed | tool=%s | args=%s | result=%s",
            task,
            request.input,
            result
        )

        return {
            "status": "success",
            "tool": task,
            "result": result,
            "tool_calls": tool_calls
        }

    except Exception:
        logger.exception(
            "Tool failed | tool=%s | args=%s",
            task,
            request.input
        )

        return {
            "status": "error",
            "message": "The tool failed. Please try again.",
            "tool": task,
            "tool_calls": tool_calls
        }