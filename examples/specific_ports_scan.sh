#!/bin/bash
# Scan specific ports

echo "[*] Scanning specific ports (22, 80, 443, 3306)"
python3 dscanner.py -t 192.168.1.1 -p 22,80,443,3306 -v
