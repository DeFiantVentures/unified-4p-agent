Title: feat: v0.1 minimal Unified-4P agent

Summary

Adds runnable reference: Transformer interface + Seq2Seq planner + MCTS + Info monitor.

Exposes FastAPI endpoints /plan, /execute, /telemetry.

Includes tests, CI, Docker, Dev Container, and Makefile.

Checklist

 Repo bootstrapped

 API runs locally (uvicorn server.app:app)

 pytest -q passes

 python examples/run_example.py executes

 CI workflow green

 MIT license

 (Optional) Branch protection enabled on main

Next Steps

 Swap seq2seq_plan with a real LLM

 Add domain tools (retrieval, spreadsheets, CRM, web)

 Add operator console (Streamlit) for plan DAG & telemetry

Acceptance Criteria (agent should verify)

 CI is passing on the PR.

 Example and tests run successfully.

 PR is ready for review; link returned.
