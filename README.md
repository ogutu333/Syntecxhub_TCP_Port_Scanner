# TCP Port Scanner

**Week 1 at Syntecxhub | Cybersecurity Internship**  

For my first week at Syntecxhub, I worked on building a TCP port scanner using Python.  

The goal was to understand how port scanning works, how Python sockets establish connections, and how multithreading can make the process faster.  

The scanner checks a target for open, closed, and unresponsive ports, then displays the results and saves them to a log file.  

## Objectives

* Build a TCP port scanner that checks open ports on a host.  
* Learn socket programming basics and concurrency (threads).  
* Add options for scanning a single host or a range of ports.  
* Print and log results (open/closed/timeouts) and handle exceptions.  

## How It Works

The scanner attempts to connect to each specified port using Python's `socket` module and `connect_ex()`.

Depending on the response, it identifies whether a port is open, closed, or timed out.

To avoid checking every port one at a time, I used Python's `ThreadPoolExecutor` to run multiple connection attempts concurrently.

The scanner identifies the following states:

| Result     | Meaning                                              |
| ---------- | ---------------------------------------------------- |
| 🟢 Open    | A TCP connection was successfully established.       |
| 🔴 Closed  | The connection was refused.                          |
| 🟡 Timeout | No response was received within the configured time. |
| ⚠️ Error   | A connection or other execution error occurred.      |

## Technologies & Tools

* **Language:** Python 3.8+
* **Networking:** Socket Programming
* **Concurrency:** `ThreadPoolExecutor`, `as_completed()`
* **Logging:** Python Logging Module
* **CLI:** `argparse`
* **Libraries:** Python Standard Library

No third-party packages are required.

## Project Structure

```text
tcp-port-scanner/
│
├── scanner.py       # Main port scanning script
├── scan.log         # Scan results and activity logs
└── README.md        # Project documentation
```

## 💻 Usage

The scanner accepts a target hostname or IP address, along with optional scanning parameters.

### Scan the default port range (1–1024)

```bash
python3 scanner.py 127.0.0.1
```

### Scan a single port

```bash
python3 scanner.py 127.0.0.1 -p 22
```

### Scan a custom port range

```bash
python3 scanner.py 127.0.0.1 -p 1-1000
```

### Scan specific ports

```bash
python3 scanner.py 127.0.0.1 -p 22,80,443,8080
```

### Adjust the connection timeout

```bash
python3 scanner.py 127.0.0.1 -p 1-1024 -t 2
```

### Change the number of concurrent workers

```bash
python3 scanner.py 127.0.0.1 -p 1-1024 -w 50
```

### Specify a log file

```bash
python3 scanner.py 127.0.0.1 -p 1-1024 -l results.log
```

## Sample Output

The following is an example of what the scan summary looks like:

```text
Scanning 127.0.0.1 (127.0.0.1) — 1024 port(s)...

=== Scan Summary ===
Target:   127.0.0.1 (127.0.0.1)
Time:     2026-11-17 10:30:00
Open:     2 -> [22, 80]
Closed:   1024
Timeouts: 0
Errors:   0
```

## What I Learned

This lab gave me a chance to get more comfortable working with Python sockets and understand what actually happens during a TCP connection attempt.

Some of the things I worked with along the way:

* **TCP Socket Programming:** Creating sockets and attempting network connections.
* **Port Scanning:** Identifying open and closed ports on a target.
* **Multithreading:** Using `ThreadPoolExecutor` to scan multiple ports concurrently.
* **Exception Handling:** Handling connection failures, timeouts, and hostname resolution errors.
* **Input Validation:** Checking hostnames and port specifications before scanning.
* **Resource Management:** Making sure sockets are properly closed using `finally`.
* **Logging:** Saving scan results for later review.
* **CLI Design:** Using `argparse` to make the scanner configurable from the terminal.

## What's Next?

I'd like to build on this scanner by experimenting with a few additional features:

* **Banner Grabbing:** Identifying services running on open ports.
* **Service Name Lookup:** Mapping commonly used port numbers to service names.
* **CSV/JSON Export:** Saving scan results in structured formats.
* **Rate Limiting:** Controlling scanning speed to avoid overwhelming a target.
* **Asynchronous Scanning:** Exploring Python's `asyncio` as an alternative to multithreading.

## ⚠️ Responsible Use

This tool was developed for educational purposes and network reconnaissance practice.

Only scan systems you own or have explicit permission to assess. Always follow applicable laws and network usage policies.

---

**Part of my Week 1 cybersecurity tasks at Syntecxhub.** 🔐
