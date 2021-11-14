#!/bin/sh

exec /sbin/tini -- venv/bin/gunicorn -b=0.0.0.0:8000 "--workers=$WORKERS" "$@"  "--timeout=120" elg_stance:app
