#!/usr/bin/env python3
"""Simple TCP port scanner for learning purposes."""
import argparse
import logging
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime


def scan_port(host, port, timeout=1.0):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        return "open" if sock.connect_ex((host, port)) == 0 else "closed"
    except socket.timeout:
        return "timeout"
    except OSError as e:
        return f"error: {e}"
    finally:
        sock.close()


def scan_range(host, ports, timeout=1.0, workers=100):
    results = {}
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futures = {ex.submit(scan_port, host, p, timeout): p for p in ports}
        for fut in as_completed(futures):
            port = futures[fut]
            try:
                results[port] = fut.result()
            except Exception as e:
                results[port] = f"error: {e}"
    return results


def resolve_host(host):
    try:
        return socket.gethostbyname(host)
    except socket.gaierror:
        raise ValueError(f"Could not resolve host: {host}")


def parse_port_spec(spec):
    ports = set()
    for chunk in spec.split(","):
        chunk = chunk.strip()
        if "-" in chunk:
            a, b = chunk.split("-", 1)
            ports.update(range(int(a), int(b) + 1))
        else:
            ports.add(int(chunk))
    if not ports or min(ports) < 0 or max(ports) > 65535:
        raise ValueError("Ports must be between 0 and 65535")
    return sorted(ports)


def report(results, target, ip, log):
    open_ports = sorted(p for p, s in results.items() if s == "open")
    closed = sum(1 for s in results.values() if s == "closed")
    timeouts = sum(1 for s in results.values() if s == "timeout")
    errors = sum(1 for s in results.values() if s.startswith("error"))

    print("\n=== Scan Summary ===")
    print(f"Target:   {target} ({ip})")
    print(f"Time:     {datetime.now():%Y-%m-%d %H:%M:%S}")
    print(f"Open:     {len(open_ports)} -> {open_ports}")
    print(f"Closed:   {closed}")
    print(f"Timeouts: {timeouts}")
    print(f"Errors:   {errors}")

    log.info("scan target=%s ip=%s open=%s closed=%d timeouts=%d errors=%d",
             target, ip, open_ports, closed, timeouts, errors)


def main():
    parser = argparse.ArgumentParser(description="TCP port scanner")
    parser.add_argument("host")
    parser.add_argument("-p", "--ports", default="1-1024")
    parser.add_argument("-t", "--timeout", type=float, default=1.0)
    parser.add_argument("-w", "--workers", type=int, default=100)
    parser.add_argument("-l", "--log", default="scan.log")
    args = parser.parse_args()

    logging.basicConfig(filename=args.log, level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(message)s")
    log = logging.getLogger("scanner")

    try:
        ip = resolve_host(args.host)
        ports = parse_port_spec(args.ports)
        print(f"Scanning {args.host} ({ip}) — {len(ports)} port(s)...")
        results = scan_range(ip, ports, args.timeout, args.workers)
        report(results, args.host, ip, log)
    except (ValueError, OSError) as e:
        print(f"[!] Error: {e}")
        log.error("fatal: %s", e)


if __name__ == "__main__":
    main()
