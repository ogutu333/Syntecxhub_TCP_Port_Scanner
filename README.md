# TCP Port Scanner

**A Python-based TCP Port Scanner | Cybersecurity Project**  

## Project Overview

For this project, I built a simple TCP port scanner using Python to understand how port scanning works and how devices communicate over a network.  

The assignment was to create a tool that checks a target machine for open, closed, and timed-out TCP ports. I also wanted to get more comfortable with Python socket programming, multithreading and handling network errors.  

I built and tested the scanner in Kali Linux.

> **Ethical Use & Disclaimer**
>
> This tool was developed for educational purposes and tested within my own lab environment. Only scan systems you own or have explicit permission to assess. Unauthorized scanning may violate organizational policies or applicable laws.

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

I tested the scanner against Kioptrix Level 1, a deliberately vulnerable machine running in my local lab environment.

**Target:** `192.168.100.7`  
**Scan Type:** TCP Connect Scan  
**Port Range:** `1–1024`  
**Environment:** Kali Linux and Kioptrix Level 1

### Scan Findings

The scan identified the following open ports:

| Port | Detected Service | Observation |
|---|---|---|
| 22 | SSH | Remote administration service accepting TCP connections |
| 80 | HTTP | Web service accepting TCP connections |

The remaining ports recorded in the scan output were classified as closed.

### Security Observations

The results revealed two accessible services on the target machine: SSH and HTTP. From a defender's perspective, these services represent potential entry points that should be monitored and assessed for unnecessary exposure, weak configurations and known vulnerabilities.

SSH provides remote administration access, while HTTP exposes a web service that may require further security assessment. Identifying these services is an important first step in understanding a host's network attack surface.

The scan results demonstrate how basic TCP port scanning can support reconnaissance, asset visibility and defensive security assessments.

The scan also demonstrated why identifying open ports is important during network reconnaissance. On Kioptrix Level 1, ports 22 (SSH) and 80 (HTTP) were accessible, revealing remote administration and web services exposed by the target. In a SOC environment, comparing these findings against expected network configurations can help identify unauthorised services, unexpected exposure and potential attack surfaces.

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

## Security Observations

Port scanning provides visibility into the network attack surface by identifying which TCP ports accept incoming connections.

Some important security observations from this project:

- **Attack Surface Visibility:** Open ports reveal services that may be accessible to an attacker during reconnaissance. Unnecessary exposed services increase the potential attack surface.
- **Service Exposure:** Services running on unexpected ports or services that should not be publicly accessible may indicate misconfiguration or unauthorised changes.
- **Network Behaviour:** Connection responses provide useful information about how a target handles incoming connections. Timeouts and refused connections can help distinguish different network conditions, although they do not independently confirm a security incident.
- **Defensive Monitoring:** Repeated or unusual connection attempts across multiple ports can be useful indicators when investigating reconnaissance activity in network logs.

From a SOC perspective, understanding normal network exposure makes it easier to identify unexpected services, investigate suspicious scanning activity and recognise potential attack paths.

## Future Improvements

There are a few areas I'd like to explore as I continue developing this project:

- **Service Detection:** Identify common services running on open ports to help detect unexpected or potentially unauthorised services on monitored hosts.
- **CSV Export:** Export scan results into structured CSV reports for easier analysis, comparison and security documentation.
- **Improved Scan Reporting:** Generate more detailed reports highlighting exposed ports and potential attack-surface risks.
- **Custom Logging:** Add configurable log file paths to make scan results easier to organise and integrate into security analysis workflows.
- **Scan Comparison:** Introduce functionality to compare scan results over time and identify newly exposed or closed ports that could indicate changes in the host's network configuration.
