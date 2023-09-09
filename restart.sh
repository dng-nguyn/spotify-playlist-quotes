#!/bin/bash

while true; do
    python3 main.py
    echo "Restarting main.py..."
    sleep 60  # Optional delay between restarts (in seconds)
done
