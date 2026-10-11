PY ?= python

.PHONY: install run test sim snapshot check
install:  ; $(PY) -m pip install -r requirements-dev.txt
run:      ; $(PY) main.py
test:     ; $(PY) -m pytest -q
sim:      ; $(PY) -m tools.simulate --fights 5000
snapshot: ; $(PY) -m tools.snapshot
check: test   ## gate completo: testes + balanceamento + assets/snapshots
	$(PY) -m tools.simulate --fights 2000 --check
	$(PY) -m tools.snapshot
