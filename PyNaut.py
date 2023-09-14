#!/usr/bin/env python3

import nmap
import re
import argparse

def validate_ip(ip):
    ip_pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
    return ip_pattern.match(ip)

def validate_port_range(port_range):
    port_range_pattern = re.compile(r"([0-9]+)-([0-9]+)")
    match = port_range_pattern.match(port_range.replace(" ", ""))
    if match:
        port_min = int(match.group(1))
        port_max = int(match.group(2))
        if 0 <= port_min <= port_max <= 65535:
            return port_min, port_max
    return None, None

def scan_ports(target_ip, port_min, port_max):
    open_ports = []
    nm = nmap.PortScanner()

    for port in range(port_min, port_max + 1):
        try:
            result = nm.scan(target_ip, str(port))
            port_status = result['scan'][target_ip]['tcp'][port]['state']
            print(f"Port {port} is {port_status}")
            if port_status == 'open':
                open_ports.append(port)
        except nmap.PortScannerError as e:
            print(f"Error scanning port {port}: {e}")

    return open_ports

def main():
    parser = argparse.ArgumentParser(description="Simple port scanner using python-nmap")
    parser.add_argument("target_ip", nargs="?", help="Target IP address to scan")
    parser.add_argument("port_range", nargs="?", help="Port range to scan in format <int>-<int>")

    args = parser.parse_args()

    while args.target_ip is None or not validate_ip(args.target_ip):
        args.target_ip = input("Please enter a valid IP address that you want to scan: ")

    while args.port_range is None:
        port_range_input = input("Please enter the port range to scan in format <int>-<int> (e.g. 80-100): ")
        port_min, port_max = validate_port_range(port_range_input)
        if port_min is not None and port_max is not None:
            args.port_range = f"{port_min}-{port_max}"
        else:
            print("Invalid port range format. Please provide a valid range (e.g. 80-100).")

    port_min, port_max = validate_port_range(args.port_range)

    print(f"Scanning ports {port_min}-{port_max} on {args.target_ip}...")
    open_ports = scan_ports(args.target_ip, port_min, port_max)

    if open_ports:
        print(f"Open ports on {args.target_ip}: {', '.join(map(str, open_ports))}")
    else:
        print(f"No open ports found on {args.target_ip}.")

if __name__ == "__main__":
    main()
