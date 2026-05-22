ifeq (run,$(firstword $(MAKECMDGOALS)))
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  $(eval $(RUN_ARGS):;@:)
endif

.PHONY: all install run debug clean lint

all: install run

install:
	python3 -m pip install --upgrade pip
	python3 -m pip install rich flake8 mypy matplotlib

run:
	@python3 main.py $(if $(RUN_ARGS),$(RUN_ARGS),maps/01_maze_nightmare.txt)

debug:
	@python3 -m pdb main.py $(if $(RUN_ARGS),$(RUN_ARGS),maps/01_maze_nightmare.txt)

clean:
	@find . -type d -name "__pycache__" -exec rm -r {} + 2>/dev/null || true
	@find . -type d -name ".mypy_cache" -exec rm -r {} + 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -r {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type f -name "*.pyo" -delete 2>/dev/null || true
	rm -rf .mypy_cache __pycache__

lint: clean
	flake8 . --exclude=.venv,venv,env,__pycache__,.mypy_cache,.pytest_cache,build,dist
	mypy . --exclude "(\.venv|venv|env|\.mypy_cache|__pycache__|build|dist)" --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs