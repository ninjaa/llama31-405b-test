#!/bin/bash

# Check if arguments are provided
if [ $# -gt 0 ]; then
    # Join all arguments with commas
    PROMPT_LIST=$(IFS=,; echo "$*")
    export SELECTED_PROMPTS="$PROMPT_LIST"
else
    unset SELECTED_PROMPTS
fi

locust -H http://localhost:8000 -f locustfile.py

