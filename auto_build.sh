#!/bin/bash
# Automated build for LG MEN3 Activator for Linux/Mac
# Usage: ./auto_build.sh [--update|--verify|--no-backup|--quiet]

python3 auto_build.py "$@"

if [ $? -eq 0 ]; then
    echo ""
    echo "========================================"
    echo "BUILD COMPLETED SUCCESSFULLY"
    echo "========================================"
else
    echo ""
    echo "========================================"
    echo "BUILD COMPLETED WITH ERRORS"
    echo "========================================"
    exit $?
fi

