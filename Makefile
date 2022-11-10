python=python3
venv_path=venv
pytest=pytest

pip=pip3

test:
	@echo "[!] Activating virtual environment ..."
	@test -d $(venv_path) || $(python) -m venv $(venv_path)
	
	@echo "[!] Starting test ..."
	@. $(venv_path)/bin/activate && (\
		$(pytest) --verbose -s; \
	)