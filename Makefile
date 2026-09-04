PYTHON      := python
UV          := uv
RUFF        := $(UV) run ruff
PYTEST      := $(UV) run pytest
COVERAGE    := $(UV) run coverage
SPHINX      := $(UV) run --group docs sphinx-build
TWINE       := $(UV) run --group publish twine

SRC_DIRS    := src tests
DOCS_SRC    := docs
DOCS_BUILD  := docs/_build/html
COV_HTML    := htmlcov
DIST_DIR    := dist

# Colour helpers (gracefully degrade if the terminal does not support them)
BOLD  := $(shell tput bold   2>/dev/null || true)
GREEN := $(shell tput setaf 2 2>/dev/null || true)
CYAN  := $(shell tput setaf 6 2>/dev/null || true)
RESET := $(shell tput sgr0   2>/dev/null || true)

tf-check:
	@echo "$(BOLD)$(CYAN)► terraform validate$(RESET)"
	cd infrastructure
	terraform validate

tf-plan:
	@echo "$(BOLD)$(CYAN)► terraform plan$(RESET)"
	cd infrastructure
	terraform plan

tf-deploy:
	@echo "$(BOLD)$(CYAN)► terraform apply$(RESET)"
	cd infrastructure
	terraform apply

tf-format:
	@echo "$(BOLD)$(CYAN)► terraform format$(RESET)"
	cd infrastructure
	terraform fmt

prune:
	podman system prune -a --volumes


.PHONY: help install install-docs sync upgrade \
        check lint format fmt fix \
        test cov cov-report \
        build publish \
        docs docs-clean \
        clean distclean all ci

.DEFAULT_GOAL := help

help:
	@echo ""
	@echo "$(BOLD)$(CYAN)Aksjonærregisteret – available make targets$(RESET)"
	@echo ""
	@echo "$(BOLD)Environment$(RESET)"
	@echo "  install        Create the virtual environment and install runtime + dev deps"
	@echo "  install-docs   Install the documentation extra deps on top of dev"
	@echo "  sync           Re-sync the venv to exactly the lockfile (uv.lock)"
	@echo "  upgrade        Upgrade all deps and regenerate uv.lock"
	@echo ""
	@echo "$(BOLD)Code quality$(RESET)"
	@echo "  check          Run ruff lint check (read-only, exits non-zero on violations)"
	@echo "  lint           Alias for check"
	@echo "  format         Run ruff format check (read-only, exits non-zero if unformatted)"
	@echo "  fmt            Auto-format all source files with ruff format"
	@echo "  fix            Auto-fix all safe lint violations, then format"
	@echo ""
	@echo "$(BOLD)Tests$(RESET)"
	@echo "  test           Run the full test suite + terminal coverage summary"
	@echo "  cov            Run tests with coverage + HTML report in htmlcov/"
	@echo "  cov-report     Open the HTML coverage report in the browser"
	@echo ""
	@echo "$(BOLD)Build & publish$(RESET)"
	@echo "  build          Build sdist + wheel into dist/ using uv build"
	@echo "  publish        Upload dist/ to PyPI with twine (set TWINE_PASSWORD)"
	@echo ""
	@echo "$(BOLD)Documentation$(RESET)"
	@echo "  docs           Build the Sphinx HTML documentation"
	@echo "  docs-clean     Remove the Sphinx build artefacts"
	@echo ""
	@echo "$(BOLD)Housekeeping$(RESET)"
	@echo "  clean          Remove cache and build artefacts (keep venv)"
	@echo "  distclean      Remove everything including the venv"
	@echo ""
	@echo "$(BOLD)CI$(RESET)"
	@echo "  all / ci       check + test (no auto-fix, suitable for CI pipelines)"
	@echo ""
	@echo "$(BOLD)Terraform$(RESET)"
	@echo "  tf-validate - validate ALL configuration files."
	@echo "  tf-format   - format ALL configuration files. "
	@echo "  tf-deploy   - deploy containers."
	@echo "  "
	@echo ""
	@echo "$(BOLD)Podman$(RESET)"
	@echo "  prune   - remove all unused volumes."
	# ---------------------------------------------------------------------------
# Environment
# ---------------------------------------------------------------------------

## Create the venv and install runtime + dev dependencies.
install:
	@echo "$(BOLD)$(GREEN)► Installing dependencies with uv$(RESET)"
	$(UV) sync --group dev

## Install the docs extras (Sphinx, nbsphinx, …) on top of dev.
install-docs:
	@echo "$(BOLD)$(GREEN)► Installing docs dependencies with uv$(RESET)"
	$(UV) sync --group dev --group docs

## Re-sync the venv to exactly what is recorded in uv.lock.
sync:
	$(UV) sync --group dev

## Upgrade all dependencies and regenerate uv.lock.
upgrade:
	@echo "$(BOLD)$(GREEN)► Upgrading all dependencies$(RESET)"
	$(UV) lock --upgrade
	$(UV) sync --group dev

# ---------------------------------------------------------------------------
# Code quality
# ---------------------------------------------------------------------------

## Lint – run ruff check without modifying files (exits 1 on violations).
check:
	@echo "$(BOLD)$(CYAN)► ruff check$(RESET)"
	$(RUFF) check $(SRC_DIRS)

## Alias for check.
lint: check

## Format check – verify formatting without modifying files.
format:
	@echo "$(BOLD)$(CYAN)► ruff format --check$(RESET)"
	$(RUFF) format --check $(SRC_DIRS)

## Auto-format – rewrite files to comply with ruff formatting rules.
fmt:
	@echo "$(BOLD)$(CYAN)► ruff format$(RESET)"
	$(RUFF) format $(SRC_DIRS)

## Fix – auto-fix all safe lint violations, then auto-format.
fix:
	@echo "$(BOLD)$(CYAN)► ruff check --fix$(RESET)"




# ---------------------------------------------------------------------------
# Documentation
# ---------------------------------------------------------------------------


## Open the HTML coverage report (macOS / Linux).
cov-report:
	@echo "$(BOLD)$(CYAN)► opening coverage report$(RESET)"
	@open $(COV_HTML)/index.html 2>/dev/null || xdg-open $(COV_HTML)/index.html

# ---------------------------------------------------------------------------
# Build & publish
# ---------------------------------------------------------------------------

build:
	@echo "$(BOLD)$(CYAN)► building image --fix$(RESET)"
	podman build -t backend-registry .

## Upload the contents of dist/ to PyPI.
## Set TWINE_USERNAME / TWINE_PASSWORD (or use a .pypirc / keyring) before running.
deploy: build
	@echo "$(BOLD)$(CYAN)► deploy to pod $(RESET)"
# ---------------------------------------------------------------------------
# Documentation
# ---------------------------------------------------------------------------

## Build the Sphinx HTML documentation.
docs:
	@echo "$(BOLD)$(CYAN)► sphinx-build$(RESET)"
	$(SPHINX) -b html $(DOCS_SRC) $(DOCS_BUILD)
	@echo "Docs written to $(DOCS_BUILD)/index.html"

## Remove Sphinx build artefacts.
docs-clean:
	@rm -rf $(DOCS_BUILD)
	@echo "Removed $(DOCS_BUILD)"

# ---------------------------------------------------------------------------
# Housekeeping
# ---------------------------------------------------------------------------

## Remove Python and tool caches (keep the venv).
clean:
	@echo "$(BOLD)Cleaning caches$(RESET)"
	find . -type d -name "__pycache__"   ! -path "./.venv/*" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache"   ! -path "./.venv/*" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" ! -path "./.venv/*" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info"    ! -path "./.venv/*" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "$(COV_HTML)"   ! -path "./.venv/*" -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -o -name "*.pyo" -o -name ".coverage" | xargs rm -f 2>/dev/null || true
	@rm -rf $(DIST_DIR)
	@echo "Done."

## Remove everything including the virtual environment.
distclean: clean docs-clean
	@rm -rf .venv
	@echo "Removed .venv"

# ---------------------------------------------------------------------------
# CI / composite targets
# ---------------------------------------------------------------------------

## Run check + test – no auto-fix.  Use this in CI pipelines.
all: check test

ci: all