VENV=.venv

bootstrap:
	python -m venv $(VENV)
	$(VENV)/bin/pip install --upgrade pip
	$(VENV)/bin/pip install -r requirements.txt

serve:
	$(VENV)/bin/uvicorn main:app --reload

docker-build:
	docker build -t ai-agent-workshop .

docker-run:
	docker run -p 8000:8000 --env-file .env ai-agent-workshop
