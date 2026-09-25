#!/bin/sh
set -eu

for interpreter in python3 python; do
    if command -v "$interpreter" >/dev/null 2>&1 &&
       "$interpreter" -c 'import sys; sys.exit(sys.version_info < (3, 11))' >/dev/null 2>&1; then
        PYTHONIOENCODING=utf-8
        export PYTHONIOENCODING
        exec "$interpreter" -B "$@"
    fi
done

if command -v py >/dev/null 2>&1 &&
   py -3 -c 'import sys; sys.exit(sys.version_info < (3, 11))' >/dev/null 2>&1; then
    PYTHONIOENCODING=utf-8
    export PYTHONIOENCODING
    exec py -3 -B "$@"
fi

printf '%s\n' 'Codex Advisor requires Python 3.11 or later on PATH (python3, python, or py -3).' >&2
exit 127
