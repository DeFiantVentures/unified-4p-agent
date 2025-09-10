# Unified-4P Agent (Transformer + Seq2Seq + MCTS + Info Theory)

A minimal, runnable reference implementation of the unified agent blueprint:
- **Representation** core (Transformer interface – stubbed, easy to swap)
- **Seq2Seq** planner (generates structured plans)
- **AlphaGo-style** **MCTS** planner
- **Shannon-style** **Info Monitor** (entropy & expected information gain)
- **FastAPI** service: `/plan`, `/execute`, `/telemetry`
- **CI**, **tests**, **Docker**, **Dev Container**

## Quickstart
```bash
python -m venv .venv && source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn server.app:app --reload --port 8000
```

Try the example
python examples/run_example.py

API

POST /plan — Drafts a plan from a spec (goal, constraints, context)

POST /execute — Runs MCTS over plan/tools and returns outputs + evidence graph

GET /telemetry — Last-run telemetry (mocked tokens/costs, last plan, etc.)

Replaceable components

agent_core/llm.py::seq2seq_plan → plug real LLM (OpenAI/HF/vLLM)

planner/mcts.py → tune UCB and rollout

monitor/info.py → extend entropy/MI estimators

tools/ → add domain tools (retrieval, spreadsheets, CRM, web)

Dev
make install        # pip install -r requirements.txt
make test          # run pytest
make run           # start FastAPI on :8000
make example       # run example script

Docker
docker build -t unified-4p-agent .
docker run -p 8000:8000 unified-4p-agent

License

MIT
