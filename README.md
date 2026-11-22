# TCP Port Scanner

**A Python-based TCP Port Scanner | Cybersecurity Project**  

## Project Overview

For this project, I built a simple TCP port scanner using Python to understand how port scanning works and how devices communicate over a network.  

The assignment was to create a tool that checks a target machine for open, closed, and timed-out TCP ports. I also wanted to get more comfortable with Python socket programming, multithreading and handling network errors.  

I built and tested the scanner in Kali Linux.

## What the Project Does

The scanner can:

- Scan a single target IP address.
- Scan a specified range of TCP ports.
- Identify open and closed ports.
- Detect connection timeouts.
- Use multithreading to scan multiple ports concurrently.
- Handle connection errors and exceptions.
- Record scan results in a log file.

## Technologies Used

- **Python 3** – Main programming language.
- **Kali Linux** – Environment used to execute and test the scanner.
- **Socket Programming** – Establishing TCP connections.
- **ThreadPoolExecutor** – Managing concurrent port scans.
- **Logging** – Recording scan results.

## How It Works

The scanner uses Python's `socket` library to attempt TCP connections to individual ports on a target machine.

Depending on the response, each port is classified as:

- **OPEN:** A TCP connection was successfully established.
- **CLOSED:** The target refused the connection.
- **TIMEOUT:** No response was received within the configured timeout.
- **ERROR:** Another connection or network error occurred.

To make scanning more efficient, I used `ThreadPoolExecutor` to check multiple ports concurrently instead of scanning them one at a time.

## Testing and Results

For testing, I used the **Kioptrix Level 1 vulnerable machine** from my local lab environment.

I used its assigned IP address as the target to see how the scanner performed against a deliberately vulnerable machine with network services running.

The testing helped me understand how exposed ports can reveal services running on a target machine and why port enumeration is an important part of network reconnaissance.

I also tested the scanner against localhost (`127.0.0.1`) to verify its basic functionality.

## Running the Project

Run the scanner:

```bash
python3 port_scanner.py --host 127.0.0.1 --start-port 1 --end-port 100
```

To scan the Kioptrix machine:

```bash
python3 port_scanner.py --host 192.168.100.7 --start-port 1 --end-port 1024
```

You can also adjust the number of threads and connection timeout:

```bash
python3 port_scanner.py --host 192.168.100.7 --start-port 1 --end-port 1024 --threads 50 --timeout 1
```

## What I Learned

This project gave me an opportunity to put some Python and networking concepts into practice.

Some of my key takeaways were:

- Understanding how TCP connections work through socket programming.
- Learning how open and closed ports respond to connection attempts.
- Using multithreading to improve scanning efficiency.
- Handling network timeouts and connection exceptions.
- Understanding how port scanning contributes to reconnaissance during a security assessment.

It was also a good exercise in troubleshooting, especially when working with virtual machines and making sure the target and scanning machine could communicate over the same network.

## Future Improvements

There are a few things I'd like to explore as I continue working on this project:

- Add basic service detection for open ports.
- Export scan results to CSV.
- Improve the scan summary and reporting.
- Add command-line options for saving results to custom log files.

---

**Note:** This tool was developed for educational purposes and testing within my own lab environment. Only scan systems you own or have explicit permission to assess.
