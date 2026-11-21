#!/usr/bin/env python3

"""
TCP Port Scanner
Built and executed on Kali Linux.
"""

import argparse
import logging
import socket
import errno
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime


# Configure logging
logging.basicConfig(
    filename="scan.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


# Scan an individual TCP port
def scan_port(host, port, timeout):

    try:
        with socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        ) as sock:

            sock.settimeout(timeout)

            result = sock.connect_ex((host, port))

            if result == 0:
                status = "OPEN"

            elif result == errno.ECONNREFUSED:
                status = "CLOSED"

            elif result == errno.ETIMEDOUT:
                status = "TIMEOUT"

            else:
                status = f"ERROR ({result})"

    except socket.timeout:
        status = "TIMEOUT"

    except OSError as error:
        status = f"ERROR: {error}"

    logger.info("%s:%s - %s", host, port, status)

    return port, status


# Main function
def main():

    parser = argparse.ArgumentParser(
        description="Kali Linux TCP Port Scanner"
    )

    parser.add_argument(
        "--host",
        required=True,
        help="Target IP address or hostname"
    )

    parser.add_argument(
        "--start-port",
        type=int,
        default=1
    )

    parser.add_argument(
        "--end-port",
        type=int,
        default=1024
    )

    parser.add_argument(
        "--timeout",
        type=float,
        default=1.0
    )

    parser.add_argument(
        "--threads",
        type=int,
        default=50
    )

    args = parser.parse_args()

    # Validate input
    if not (1 <= args.start_port <= args.end_port <= 65535):
        parser.error("Invalid port range.")

    if args.timeout <= 0 or args.threads < 1:
        parser.error("Timeout and threads must be positive.")

    # Resolve target IP
    try:
        target_ip = socket.gethostbyname(args.host)

    except socket.gaierror:
        parser.error("Could not resolve hostname.")

    # Display scan details
    print("\n===================================")
    print("       KALI TCP PORT SCANNER")
    print("===================================")

    print(f"Target: {args.host} ({target_ip})")
    print(f"Port range: {args.start_port}-{args.end_port}")
    print(f"Threads: {args.threads}")
    print(f"Scan started: {datetime.now()}")

    print("-----------------------------------")

    results = []

    # Execute concurrent port scanning
    try:
        with ThreadPoolExecutor(
            max_workers=args.threads
        ) as executor:

            futures = [
                executor.submit(
                    scan_port,
                    target_ip,
                    port,
                    args.timeout
                )
                for port in range(
                    args.start_port,
                    args.end_port + 1
                )
            ]

            for future in as_completed(futures):

                port, status = future.result()

                results.append((port, status))

                print(f"Port {port}: {status}")

    except KeyboardInterrupt:
        print("\nScan interrupted by user.")
        return

    # Display results
    print("\n===================================")
    print("            SCAN SUMMARY")
    print("===================================")

    for status in ["OPEN", "CLOSED", "TIMEOUT", "ERROR"]:

        count = sum(
            1 for _, result in results
            if result == status or
            (status == "ERROR" and result.startswith("ERROR"))
        )

        print(f"{status}: {count}")

    print("-----------------------------------")
    print(f"Scan completed: {datetime.now()}")
    print("Results saved to scan.log")


if __name__ == "__main__":
    main()
