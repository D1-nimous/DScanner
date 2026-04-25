#!/bin/bash
# Full network scan with report generation

echo "[*] Running full network scan on 192.168.1.0/24"
python3 dscanner.py -t 192.168.1.0/24 --full --report vulnerability_report.html -v

echo "[+] Scan complete. Report saved to vulnerability_report.html"
