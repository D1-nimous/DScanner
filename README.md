# DScanner - Network Security Vulnerability Scanner

A comprehensive Python-based network security tool designed to scan networks for vulnerabilities, open ports, weak services, and security misconfigurations.

## Features

✅ **Port Scanning** - Identify open ports and services
✅ **Service Detection** - Detect running services and their versions
✅ **SSL/TLS Analysis** - Check SSL certificate validity and vulnerabilities
✅ **Common Vulnerability Check** - Detect known vulnerabilities
✅ **Network Mapping** - Discover active hosts on the network
✅ **Security Headers Analysis** - Check for missing HTTP security headers
✅ **DNS Security** - Verify DNS configuration and security
✅ **Detailed Reporting** - Generate comprehensive vulnerability reports

## Requirements

- Python 3.8+
- Administrative/Root privileges (for some features)
- Linux, macOS, or Windows

## Installation

```bash
git clone https://github.com/D1-nimous/DScanner.git
cd DScanner
pip install -r requirements.txt
```

## Quick Start

### Basic Port Scan
```bash
python dscanner.py -t 192.168.1.1
```

### Scan Specific Ports
```bash
python dscanner.py -t 192.168.1.1 -p 80,443,22
```

### Full Network Scan
```bash
python dscanner.py -t 192.168.1.0/24 --full
```

### Generate Report
```bash
python dscanner.py -t 192.168.1.1 --report output.html
```

## Usage

```
usage: dscanner.py [-h] -t TARGET [-p PORTS] [--timeout TIMEOUT] 
                    [--full] [--report REPORT] [-v]

Network Security Vulnerability Scanner

optional arguments:
  -h, --help            show this help message and exit
  -t TARGET, --target TARGET
                        Target IP address or CIDR range
  -p PORTS, --ports PORTS
                        Specific ports to scan (comma-separated)
  --timeout TIMEOUT     Scan timeout in seconds (default: 5)
  --full                Perform full comprehensive scan
  --report REPORT       Generate HTML report
  -v, --verbose         Verbose output
```

## Examples

### Scan Single Host
```bash
python dscanner.py -t 192.168.1.100 -v
```

### Scan Network Range
```bash
python dscanner.py -t 192.168.1.0/24 --timeout 10
```

### Full Scan with Report
```bash
python dscanner.py -t 192.168.1.1 --full --report vulnerability_report.html
```

## Vulnerability Database

DScanner includes a database of common vulnerabilities including:
- Default credentials
- Known service vulnerabilities
- Outdated software versions
- Weak SSL/TLS configurations
- Missing security headers

## Output

The scanner generates detailed reports including:
- Open ports and services
- Vulnerability severity levels (Critical, High, Medium, Low)
- Remediation recommendations
- HTML reports for easy sharing

## Security Considerations

⚠️ **IMPORTANT**: Use this tool only on networks and systems you own or have explicit permission to test. Unauthorized network scanning may be illegal.

## Contributing

Contributions are welcome! Please feel free to submit pull requests.

## License

MIT License

## Disclaimer

This tool is provided as-is for educational and authorized security testing purposes only. The authors assume no liability for misuse or damage caused by this tool.
