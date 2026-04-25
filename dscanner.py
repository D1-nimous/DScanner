#!/usr/bin/env python3
"""
DScanner - Network Security Vulnerability Scanner
A comprehensive tool to scan networks for vulnerabilities and security misconfigurations.
"""

import argparse
import sys
import socket
import subprocess
import re
from datetime import datetime
from pathlib import Path
try:
    import nmap
except ImportError:
    nmap = None
import requests
from urllib.parse import urlparse
import ssl
from ipaddress import ip_network, ip_address
import json
from typing import List, Dict, Tuple
from enum import Enum

class SeverityLevel(Enum):
    """Vulnerability severity levels"""
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    INFO = "Info"

class VulnerabilityDatabase:
    """Database of known vulnerabilities"""
    
    COMMON_VULNERABILITIES = {
        21: {"service": "FTP", "severity": SeverityLevel.HIGH, "issue": "Unencrypted FTP service detected"},
        23: {"service": "Telnet", "severity": SeverityLevel.CRITICAL, "issue": "Insecure Telnet service detected"},
        80: {"service": "HTTP", "severity": SeverityLevel.MEDIUM, "issue": "Unencrypted HTTP detected"},
        135: {"service": "RPC", "severity": SeverityLevel.HIGH, "issue": "RPC service exposed"},
        139: {"service": "NetBIOS", "severity": SeverityLevel.HIGH, "issue": "NetBIOS service exposed"},
        445: {"service": "SMB", "severity": SeverityLevel.HIGH, "issue": "SMB service exposed"},
        3306: {"service": "MySQL", "severity": SeverityLevel.CRITICAL, "issue": "MySQL exposed to network"},
        5432: {"service": "PostgreSQL", "severity": SeverityLevel.CRITICAL, "issue": "PostgreSQL exposed to network"},
        5984: {"service": "CouchDB", "severity": SeverityLevel.CRITICAL, "issue": "CouchDB exposed without authentication"},
        6379: {"service": "Redis", "severity": SeverityLevel.CRITICAL, "issue": "Redis exposed without authentication"},
        27017: {"service": "MongoDB", "severity": SeverityLevel.CRITICAL, "issue": "MongoDB exposed without authentication"},
    }
    
    WEAK_PASSWORDS = ["admin", "password", "123456", "admin123", "root", "test"]

class NetworkScanner:
    """Main network scanning class"""
    
    def __init__(self, target: str, timeout: int = 5, verbose: bool = False):
        self.target = target
        self.timeout = timeout
        self.verbose = verbose
        self.results = {
            "target": target,
            "scan_time": datetime.now().isoformat(),
            "open_ports": [],
            "services": [],
            "vulnerabilities": [],
            "hosts": []
        }
    
    def scan_port(self, host: str, port: int) -> bool:
        """Scan a single port"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            result = sock.connect_ex((host, port))
            sock.close()
            return result == 0
        except socket.gaierror:
            if self.verbose:
                print(f"[!] Hostname {host} could not be resolved")
            return False
        except socket.error:
            if self.verbose:
                print(f"[!] Could not connect to {host}:{port}")
            return False
    
    def get_service_name(self, port: int) -> str:
        """Get service name for a port"""
        try:
            return socket.getservbyport(port)
        except:
            return "Unknown"
    
    def scan_ports(self, host: str, ports: List[int] = None) -> List[int]:
        """Scan multiple ports"""
        if ports is None:
            # Common ports
            ports = [20, 21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 3306, 3389, 5432, 5984, 6379, 8080, 27017]
        
        open_ports = []
        for port in ports:
            if self.scan_port(host, port):
                open_ports.append(port)
                service = self.get_service_name(port)
                self.results["open_ports"].append({
                    "port": port,
                    "service": service,
                    "host": host
                })
                if self.verbose:
                    print(f"[+] Port {port} ({service}) is OPEN on {host}")
        
        return open_ports
    
    def check_vulnerabilities(self, host: str, open_ports: List[int]):
        """Check for known vulnerabilities"""
        for port in open_ports:
            if port in VulnerabilityDatabase.COMMON_VULNERABILITIES:
                vuln = VulnerabilityDatabase.COMMON_VULNERABILITIES[port]
                self.results["vulnerabilities"].append({
                    "host": host,
                    "port": port,
                    "service": vuln["service"],
                    "issue": vuln["issue"],
                    "severity": vuln["severity"].value,
                    "recommendation": self._get_recommendation(port)
                })
                if self.verbose:
                    print(f"[!] VULNERABILITY: {vuln['service']} on port {port} - {vuln['issue']}")
    
    def _get_recommendation(self, port: int) -> str:
        """Get remediation recommendation for a port"""
        recommendations = {
            21: "Use SFTP or SCP instead of FTP for secure file transfer",
            23: "Replace Telnet with SSH for secure remote access",
            80: "Use HTTPS (port 443) instead of HTTP",
            135: "Restrict RPC access to trusted networks",
            139: "Disable NetBIOS if not needed; use SMB signing",
            445: "Implement SMB signing and disable SMBv1",
            3306: "Use firewall rules; enable authentication and encryption",
            5432: "Restrict database access; use strong passwords and SSL",
            5984: "Enable authentication and restrict network access",
            6379: "Enable Redis AUTH and restrict to localhost/VPN",
            27017: "Enable authentication and restrict network access",
        }
        return recommendations.get(port, "Restrict access to this port")
    
    def check_ssl_certificate(self, host: str, port: int = 443) -> Dict:
        """Check SSL/TLS certificate"""
        try:
            context = ssl.create_default_context()
            with socket.create_connection((host, port), timeout=self.timeout) as sock:
                with context.wrap_socket(sock, server_hostname=host) as ssock:
                    cert = ssock.getpeercert()
                    if cert:
                        return {
                            "host": host,
                            "valid": True,
                            "subject": dict(x[0] for x in cert.get('subject', [])),
                            "issuer": dict(x[0] for x in cert.get('issuer', [])),
                            "version": cert.get('version'),
                            "notBefore": cert.get('notBefore'),
                            "notAfter": cert.get('notAfter')
                        }
        except Exception as e:
            if self.verbose:
                print(f"[!] SSL check failed for {host}:{port} - {str(e)}")
        return None
    
    def check_http_headers(self, host: str, port: int = 80) -> Dict:
        """Check for missing security headers"""
        try:
            url = f"http://{host}:{port}"
            response = requests.get(url, timeout=self.timeout, verify=False)
            
            required_headers = [
                'X-Content-Type-Options',
                'X-Frame-Options',
                'X-XSS-Protection',
                'Strict-Transport-Security',
                'Content-Security-Policy'
            ]
            
            missing_headers = [h for h in required_headers if h not in response.headers]
            
            return {
                "host": host,
                "port": port,
                "missing_headers": missing_headers,
                "headers_found": len(response.headers)
            }
        except Exception as e:
            if self.verbose:
                print(f"[!] Header check failed for {host}:{port}")
            return None
    
    def scan_host(self, host: str, full_scan: bool = False) -> Dict:
        """Scan a single host"""
        print(f"\n[*] Scanning host: {host}")
        
        # Port scan
        open_ports = self.scan_ports(host)
        
        # Vulnerability check
        self.check_vulnerabilities(host, open_ports)
        
        if full_scan:
            # SSL check
            if 443 in open_ports:
                ssl_info = self.check_ssl_certificate(host, 443)
                if ssl_info:
                    self.results["services"].append(ssl_info)
            
            # HTTP headers check
            if 80 in open_ports or 443 in open_ports:
                headers_info = self.check_http_headers(host)
                if headers_info:
                    if len(headers_info.get("missing_headers", [])) > 0:
                        self.results["vulnerabilities"].append({
                            "host": host,
                            "port": 80,
                            "service": "HTTP",
                            "issue": f"Missing security headers: {', '.join(headers_info['missing_headers'])}",
                            "severity": SeverityLevel.MEDIUM.value,
                            "recommendation": "Add security headers to HTTP responses"
                        })
        
        return self.results
    
    def scan_network(self, full_scan: bool = False):
        """Scan a network range"""
        try:
            network = ip_network(self.target, strict=False)
            hosts = list(network.hosts())
            if not hosts:
                hosts = [network.network_address]
            
            print(f"[*] Scanning network: {self.target} ({len(hosts)} hosts)")
            
            for host in hosts:
                try:
                    if self.scan_port(str(host), 22) or self.scan_port(str(host), 80):
                        self.scan_host(str(host), full_scan)
                except Exception as e:
                    if self.verbose:
                        print(f"[!] Error scanning {host}: {str(e)}")
        except Exception as e:
            print(f"[!] Invalid network: {self.target}")
            raise
    
    def generate_report(self, output_file: str):
        """Generate HTML report"""
        html_template = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>DScanner Vulnerability Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1 {{ color: #333; border-bottom: 3px solid #007bff; padding-bottom: 10px; }}
                h2 {{ color: #007bff; margin-top: 30px; }}
                table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
                th {{ background-color: #007bff; color: white; }}
                tr:nth-child(even) {{ background-color: #f9f9f9; }}
                .critical {{ color: #dc3545; font-weight: bold; }}
                .high {{ color: #fd7e14; font-weight: bold; }}
                .medium {{ color: #ffc107; }}
                .low {{ color: #28a745; }}
                .info {{ color: #17a2b8; }}
                .summary {{ background-color: #f8f9fa; padding: 15px; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <h1>DScanner - Network Security Vulnerability Report</h1>
            <div class="summary">
                <p><strong>Scan Date:</strong> {self.results['scan_time']}</p>
                <p><strong>Target:</strong> {self.results['target']}</p>
                <p><strong>Total Vulnerabilities Found:</strong> {len(self.results['vulnerabilities'])}</p>
                <p><strong>Open Ports Found:</strong> {len(self.results['open_ports'])}</p>
            </div>
            
            <h2>Open Ports</h2>
            <table>
                <tr><th>Host</th><th>Port</th><th>Service</th></tr>
        """
        
        for port_info in self.results['open_ports']:
            html_template += f"<tr><td>{port_info['host']}</td><td>{port_info['port']}</td><td>{port_info['service']}</td></tr>"
        
        html_template += "</table><h2>Vulnerabilities</h2><table><tr><th>Host</th><th>Port</th><th>Service</th><th>Issue</th><th>Severity</th><th>Recommendation</th></tr>"
        
        for vuln in self.results['vulnerabilities']:
            severity_class = vuln['severity'].lower()
            html_template += f"""<tr>
                <td>{vuln['host']}</td>
                <td>{vuln.get('port', 'N/A')}</td>
                <td>{vuln.get('service', 'N/A')}</td>
                <td>{vuln['issue']}</td>
                <td><span class="{severity_class}">{vuln['severity']}</span></td>
                <td>{vuln.get('recommendation', 'N/A')}</td>
            </tr>"""
        
        html_template += """</table>
            <footer style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; color: #666;">
                <p>Report generated by DScanner - Network Security Vulnerability Scanner</p>
            </footer>
        </body>
        </html>
        """
        
        with open(output_file, 'w') as f:
            f.write(html_template)
        
        print(f"[+] Report generated: {output_file}")

def main():
    parser = argparse.ArgumentParser(
        description="DScanner - Network Security Vulnerability Scanner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -t 192.168.1.1
  %(prog)s -t 192.168.1.0/24 --full
  %(prog)s -t 192.168.1.1 -p 80,443,22
  %(prog)s -t 192.168.1.1 --report output.html
        """
    )
    
    parser.add_argument('-t', '--target', required=True, help='Target IP address or CIDR range')
    parser.add_argument('-p', '--ports', help='Specific ports to scan (comma-separated)')
    parser.add_argument('--timeout', type=int, default=5, help='Scan timeout in seconds (default: 5)')
    parser.add_argument('--full', action='store_true', help='Perform full comprehensive scan')
    parser.add_argument('--report', help='Generate HTML report')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    try:
        # Create scanner
        scanner = NetworkScanner(args.target, timeout=args.timeout, verbose=args.verbose)
        
        # Parse ports if specified
        ports = None
        if args.ports:
            ports = [int(p.strip()) for p in args.ports.split(',')]
        
        # Determine if target is a single host or network
        if '/' in args.target:
            # Network scan
            scanner.scan_network(full_scan=args.full)
        else:
            # Single host scan
            scanner.scan_host(args.target, full_scan=args.full)
        
        # Print results
        print("\n" + "="*60)
        print("SCAN RESULTS")
        print("="*60)
        
        if scanner.results['open_ports']:
            print(f"\n[+] Open Ports Found: {len(scanner.results['open_ports'])}")
            for port_info in scanner.results['open_ports']:
                print(f"    - {port_info['host']}:{port_info['port']} ({port_info['service']})")
        else:
            print("\n[-] No open ports found")
        
        if scanner.results['vulnerabilities']:
            print(f"\n[!] Vulnerabilities Found: {len(scanner.results['vulnerabilities'])}")
            for vuln in scanner.results['vulnerabilities']:
                print(f"    - [{vuln['severity']}] {vuln['issue']}")
                print(f"      Recommendation: {vuln.get('recommendation', 'N/A')}")
        else:
            print("\n[+] No vulnerabilities detected")
        
        # Generate report if requested
        if args.report:
            scanner.generate_report(args.report)
        
        print("\n[+] Scan completed successfully")
        
    except KeyboardInterrupt:
        print("\n[!] Scan interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"[!] Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
