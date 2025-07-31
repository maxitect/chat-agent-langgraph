VENV=.venv

bootstrap:
	python3 -m venv $(VENV)
	$(VENV)/bin/pip install --upgrade pip
	$(VENV)/bin/pip install -r requirements.txt

serve:
	$(VENV)/bin/uvicorn main:app --reload

frontend:
	$(VENV)/bin/streamlit run streamlit_app.py --server.port 8501

dev:
	@echo "Starting both API and Frontend..."
	@echo "API will run on http://localhost:8000"
	@echo "Frontend will run on http://localhost:8501"
	@echo ""
	@echo "Run 'make serve' in one terminal and 'make frontend' in another"

docker-build:
	docker build -t ai-agent-workshop .

docker-run:
	docker run -p 8000:8000 --env-file .env ai-agent-workshop
