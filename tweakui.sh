#!/usr/bin/env bash

# fail on error
set -e
set -o pipefail

# run the system one
unset PYTHON_PATH
unset PYTHONPATH
unset PYTHON_ROOT
export PATH='/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin'

#export GIO_EXTRA_MODULES='/usr/lib/x86_64-linux-gnu/gio/modules/'

python3 tweakui.py
