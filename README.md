# AI Agent Workshop Starter

This repository is the hands‑on starting point for the **AI Agents for Fun & Profit** workshop.

## Quick start

```bash
# Clone or download the starter kit, then:
make bootstrap        # create virtual‑env and install dependencies
cp .env.example .env  # add your OpenRouter API key
python agent.py       # run the console agent
make serve            # start FastAPI server at http://localhost:8000
```

## Docker

```bash
make docker-build
make docker-run   # available at http://localhost:8000
```

## Next steps

* **Lab 2** – implement `tools/search.py`
* **Lab 3** – production‑grade deployment with Docker & FastAPI
* **Lab 4** – add guard‑rails (rate‑limit & sanitiser)
