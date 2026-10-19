# Week 10 Agent Evaluation

## Test results

The agent was evaluated using eight automated tests with pytest.

| Test | Expected behavior | Result |
|---|---|---|
| Ask routing | Routes an explicit ask request to the ask tool | Passed |
| Predict routing | Routes an explicit predict request to the predict tool | Passed |
| Unsupported task | Refuses an unsupported task without calling a tool | Passed |
| Lookup tool failure | Handles a simulated tool failure safely | Passed |
| Unknown lookup record | Returns a not-found result for an unknown record | Passed |
| Automatic ask routing | Infers the ask tool for a question without an explicit task | Passed |
| Automatic predict routing | Infers the predict tool for a churn prediction request | Passed |
| Ambiguous request | Flags an unclear request for human review without calling a tool | Passed |

**Overall: 8 passed, 0 failed.**

The test run displayed one Starlette/httpx deprecation warning related to the test client. It did not affect the test results.

## Guardrails and failure recovery

The agent supports a limited set of tools: ask, predict, and lookup. It refuses unsupported task names, limits each request to one tool call, and flags ambiguous or potentially sensitive requests for human review.

When a tool raises an exception, the agent logs the failure and returns a safe error response rather than exposing the exception details to the user.

## Limitations

The tools currently return mock data. The evaluation verifies routing, guardrails, and basic failure handling; it does not measure real retrieval quality, prediction accuracy, or performance against a live data source.

The automatic tool selection uses simple keyword rules. It is not an LLM-based planner and does not support multi-step tool execution or persistent agent memory.

## Observability

The agent logs incoming requests and routing decisions. Successful tool execution logs the selected tool, arguments, and result. Tool failures are recorded with exception details for debugging.

## Evaluation status

The latest automated evaluation completed successfully: **all eight tests passed**. The results demonstrate that the current prototype can route supported requests, handle unclear requests with a review checkpoint, refuse unsupported tasks, and recover safely from a simulated tool failure.