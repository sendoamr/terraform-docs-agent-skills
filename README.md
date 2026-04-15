# terraform-docs-agent-skills

Auto generator for docs and basic test of terraform modules, using agent skills framework and ollama

## Setup
Create virtual env
```
python3 -m venv .venv
source .venv/bin/activate
```

### Install
```
pip install -r requirements.txt
```

## Run 
### Up ollama
```
ollama serve
```

### Execute agents
```
python agent/runner.py
```
or
```
make run
```