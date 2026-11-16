import subprocess
import platform
import re
import socket
from collections import OrderedDict

def get_arp_table():
    system = platform.system().lower()

    if "windows" in system:
        output = subprocess.check_output("arp -a", shell=True, text=True, encoding="utf-8", errors="ignore")
        return parse_windows_arp(output)
    else:
        output = subprocess.check_output(["arp", "-a"], text=True, encoding="utf-8", errors="ignore")
        return parse_unix_arp(output)

def parse_windows_arp(output):
    devices = OrderedDict()
    pattern = re.compile(r"(\d+\.\d+\.\d+\.\d+)\s+([a-fA-F0-9-]{17})\s+\w+")
    for line in output.splitlines():
        match = pattern.search(line)
        if match:
            ip, mac = match.groups()
            devices[ip] = mac
    return devices

def parse_unix_arp(output):
    devices = OrderedDict()
    pattern = re.compile(r"\((\d+\.\d+\.\d+\.\d+)\) at ([a-fA-F0-9:]{17})")
    for line in output.splitlines():
        match = pattern.search(line)
        if match:
            ip, mac = match.groups()
            devices[ip] = mac
    return devices

def resolve_hostname(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except Exception:
        return "Unknown"

def main():
    print("\n" + "=" * 60)
    print("           WIFI DEVICE FINDER")
    print("=" * 60)
    print(f"{'#':<4}{'IP Address':<18}{'MAC Address':<20}{'Hostname'}")
    print("-" * 60)

    devices = get_arp_table()

    if not devices:
        print("No devices found in ARP table.")
        return

    for i, (ip, mac) in enumerate(devices.items(), 1):
        hostname = resolve_hostname(ip)
        print(f"{i:<4}{ip:<18}{mac:<20}{hostname}")

    print("=" * 60)

if __name__ == "__main__":
    main()


