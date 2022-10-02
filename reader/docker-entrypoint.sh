#!/bin/sh

set -e

# Commands available using `docker-compose run backend [COMMAND]`
case "$1" in
    python)
        python
    ;;
    test)
        PYTHONUNBUFFERED=1 python -m pytest --durations=3
    ;;
    *)
        PYTHONUNBUFFERED=1 python reader.py
    ;;
esac
