
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import logging

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    SimpleSpanProcessor,
    ConsoleSpanExporter,
)
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from tools import ask_tool, predict_tool, lookup_tool


# ---------------------------------------------------------
# Application and observability configuration
# ---------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger("week11_agent")

resource = Resource.create(
    {
        "service.name": "week11-hardened-agent",
        "service.version": "1.0.0",
    }
)

provider = TracerProvider(resource=resource)

# Local development exporter: prints trace information
# to the terminal. No Azure account is required.
provider.add_span_processor(
    SimpleSpanProcessor(ConsoleSpanExporter())
)

trace.set_tracer_provider(provider)

app = FastAPI(title="Week 11 Hardened Agent")

# Automatically trace incoming FastAPI requests.
FastAPIInstrumentor.instrument_app(app)

templates = Jinja2Templates(directory="templates")


# ---------------------------------------------------------
# Request schema
# ---------------------------------------------------------

class AgentRequest(BaseModel):
    # Task is optional; the agent can infer it from the input.
    task: str | None = None
    input: str


# ---------------------------------------------------------
# Routes
# ---------------------------------------------------------

@app.get("/", response_class=HTMLResponse)
def show_ui(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
    )


@app.get("/health")
def health():
    return {"message": "Week 11 agent is running"}


# ---------------------------------------------------------
# Tool routing and guardrails
# ---------------------------------------------------------

def choose_tool(
    user_input: str,
    requested_task: str | None = None,
):
    """
    Select a tool using simple keyword rules.

    This is a basic rule-based router, not an LLM planner.
    """

    text = user_input.lower()

    # Respect explicitly requested supported tasks.
    if requested_task:
        task = requested_task.lower().strip()

        if task in ["ask", "predict", "lookup"]:
            return task, False

        return None, False

    # Requests requiring clarification or human review.
    review_terms = [
        "delete",
        "cancel",
        "transfer money",
        "change my account",
        "medical",
        "legal",
        "urgent",
        "approve",
    ]

    if any(term in text for term in review_terms):
        return None, True

    # Infer the appropriate tool.
    if any(
        word in text
        for word in [
            "predict churn",
            "churn probability",
            "will this customer churn",
            "predict",
            "prediction",
        ]
    ):
        return "predict", False

    if any(
        word in text
        for word in [
            "customer id",
            "record",
            "lookup",
            "look up",
            "find customer",
            "customer status",
        ]
    ):
        return "lookup", False

    if any(
        word in text
        for word in [
            "how",
            "what",
            "why",
            "explain",
            "policy",
            "process",
            "procedure",
            "tell me",
        ]
    ):
        return "ask", False

    # Unclear requests go to human review.
    return None, True


# ---------------------------------------------------------
# Agent endpoint
# ---------------------------------------------------------

@app.post("/agent")
def run_agent(request: AgentRequest):

    task, needs_review = choose_tool(
        request.input,
        request.task,
    )

    # PII control:
    # Do not log request.input, customer identifiers,
    # or the contents of the user's request.
    logger.info(
        "Agent decision | selected_tool=%s | review=%s",
        task,
        needs_review,
    )

    # Human-review checkpoint.
    if needs_review:
        logger.info("Agent request requires review")

        return {
            "status": "needs_review",
            "message": (
                "This request needs clarification or human review "
                "before a tool can be called."
            ),
            "tool_calls": 0,
        }

    # Refuse unsupported tasks.
    if task not in ["ask", "predict", "lookup"]:
        logger.warning("Agent refused unsupported task")

        return {
            "status": "refused",
            "message": "Unsupported task. Choose ask, predict, or lookup.",
            "tool_calls": 0,
        }

    # Limit execution to one tool call per request.
    max_tool_calls = 1
    tool_calls = 1

    if tool_calls > max_tool_calls:
        logger.warning("Agent tool-call limit reached")

        return {
            "status": "stopped",
            "message": "Maximum tool-call limit reached.",
            "tool_calls": tool_calls,
        }

    try:
        if task == "ask":
            result = ask_tool(request.input)

        elif task == "predict":
            result = predict_tool(request.input)

        else:
            result = lookup_tool(request.input)

        # Do not log tool arguments or results.
        # Tool results may contain personal information.
        logger.info(
            "Tool completed | tool=%s",
            task,
        )

        return {
            "status": "success",
            "tool": task,
            "result": result,
            "tool_calls": tool_calls,
        }

    except Exception:
        # Log exception details for debugging, but do not
        # include the user input or tool arguments.
        logger.exception(
            "Tool execution failed | tool=%s",
            task,
        )

        return {
            "status": "error",
            "message": "The tool failed. Please try again.",
            "tool": task,
            "tool_calls": tool_calls,
        }
