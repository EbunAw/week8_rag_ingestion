# Week 11 Evaluation: Secrets, Privacy, and Observability

## Overview

This week, I updated my Week 10 tool-using agent to improve privacy-aware logging and add local observability. The aim was to avoid exposing sensitive request and tool data in logs while making application activity easier to inspect.

## Implementation

### 1. Privacy-aware logging
- Updated application logs to record the selected tool and whether human review is required.
- Avoided logging user prompts, tool arguments, and tool results.
- Kept error logs focused on tool execution failures without deliberately including request content.

### 2. Observability with OpenTelemetry
- Configured an OpenTelemetry tracer provider with service name `week11-hardened-agent` and version `1.0.0`.
- Instrumented the FastAPI application to trace incoming requests.
- Used a local console exporter to display trace information in the terminal.
- Switched to `SimpleSpanProcessor` during local testing to address the batch-exporter closed-output-stream exception.

### 3. Guardrails and tool execution
- Retained the existing rule-based tool routing and human-review checkpoint.
- Kept execution limited to one tool call per request.
- Returned a generic error message when tool execution fails.

## Evaluation Results

### Automated tests

Ran:

```bash
pytest -v evals.py
```

**Result: 8 passed, 1 warning.**

The passing tests cover:
- Routing requests to the ask and predict tools.
- Refusing unsupported tasks.
- Handling lookup failures and unknown records safely.
- Automatic routing and ambiguous-request review.

The remaining warning concerns deprecated usage in the Starlette test client; it did not cause a test failure.

### Manual verification

- Tested the FastAPI agent locally on port `8005`.
- Confirmed the agent responded to a sample question.
- Inspected terminal logs and confirmed that application decision and tool-completion messages did not contain the prompt or tool result.
- Observed OpenTelemetry request traces in the terminal.

## Limitations

- The application and tracing were tested locally.
- The console exporter is a local development setup, not a production monitoring service.
- Azure Key Vault, managed identity, and Azure Application Insights were not configured or verified.
- The existing evaluation tests primarily verify agent routing and guardrails; they do not constitute a comprehensive privacy audit or validate production observability.


## PII Handling and Retention Decisions

### Data minimization
The application logs operational metadata, such as the selected tool and whether a request requires human review. Routine application logs exclude user prompts, tool arguments, and tool results because these may contain personal or sensitive information.

### Access control
The current prototype runs locally. Access to the application and its logs is limited by the local development environment. Production access controls using Microsoft Entra ID and managed identity have not yet been configured.

### Retention
The prototype uses local terminal output for logs and traces. A formal retention period, automated deletion policy, and centralized production log storage have not been configured. In a production deployment, retention should be defined according to business needs, applicable privacy requirements, and the organization's data-retention policy.

### Privacy limitations
The current logging changes reduce unnecessary exposure of request content, but they do not constitute a complete PII audit. Tool responses are still returned to the requesting client, and exception messages should be reviewed to ensure they do not inadvertently disclose sensitive data.


## Conclusion

The Week 11 changes preserved the existing agent behavior, with all eight evaluation tests passing. Privacy-aware logs and local OpenTelemetry tracing were demonstrated. Cloud-based secret management and monitoring remain outside the verified scope of this implementation.