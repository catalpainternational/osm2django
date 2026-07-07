.PHONY: db-up db-down install migrate pbf import psql clean help

PBF ?= ./pbf/east-timor-latest.osm.pbf
PBF_URL ?= https://download.geofabrik.de/asia/east-timor-latest.osm.pbf

help:
	@echo "Targets:"
	@echo "  db-up      start PostGIS container on :49155"
	@echo "  db-down    stop and remove PostGIS container"
	@echo "  install    uv sync (creates .venv, installs osmflex)"
	@echo "  migrate    apply migrations"
	@echo "  pbf        download $(PBF) (override PBF=... PBF_URL=...)"
	@echo "  import     run_osm2pgsql then import_from_pgosmflex --truncate"
	@echo "  psql       open psql session against the running container"

db-up:
	docker compose up -d
	@printf "waiting for postgres "; \
	for i in 1 2 3 4 5 6 7 8 9 10; do \
	  if docker compose exec -T postgis pg_isready -U postgres >/dev/null 2>&1; then echo " ready"; exit 0; fi; \
	  printf "."; sleep 1; \
	done; \
	echo " timeout"; exit 1

db-down:
	docker compose down -v

install:
	uv sync

migrate: install
	uv run python manage.py migrate

pbf:
	mkdir -p pbf
	@if [ ! -f "$(PBF)" ]; then \
	  echo "Fetching $(PBF_URL) -> $(PBF)"; \
	  curl -L -o "$(PBF)" "$(PBF_URL)"; \
	else \
	  echo "$(PBF) already present"; \
	fi

import: migrate pbf
	uv run python manage.py run_osm2pgsql "$(PBF)"
	uv run python manage.py import_from_pgosmflex --truncate

psql:
	PGPASSWORD=post1234 psql -h localhost -p 49155 -U postgres -d postgres

clean:
	rm -rf .venv pbf
