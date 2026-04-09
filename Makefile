.PHONY: verify verify-static verify-contract verify-local-runtime verify-deployed

PYTHON := $(if $(wildcard ./.venv/bin/python),./.venv/bin/python,python3)

verify: verify-static verify-contract

verify-static:
	./scripts/verify_static.sh

verify-contract:
	$(PYTHON) ./scripts/verify_runtime_contract.py

verify-local-runtime:
	$(PYTHON) ./scripts/verify_runtime_api.py

verify-deployed:
	./scripts/verify_deployed_console.sh
