# NetSentry-Pro

![License](https://img.shields.io/badge/license-MIT-blue.svg) ![Python](https://img.shields.io/badge/python-3.9%2B-blue) ![Status](https://img.shields.io/badge/status-maintenance-yellow)

NetSentry-Pro is a lightweight, multi-threaded network scanner designed for defensive security auditing. It performs active host discovery via ARP/ICMP and identifies open service ports using TCP connect scanning.

## ⚠️ Disclaimer

**This tool is for educational purposes and authorized security audits only.** The authors are not responsible for misuse. scan only networks you own or have explicit permission to audit.

## Features

- 🔍 **Host Discovery**: ARP scanning for local networks.
- 🚪 **Port Scanning**: Multi-threaded TCP connect scan.
- ⚙️ **Configurable**: YAML-based configuration for timeouts and threads.
- 📊 **Logging**: detailed logs for audit trails.

## Installation

### Prerequisites
- Python 3.9+
- Root/Administrator privileges (required for Scapy raw sockets)
- `libpcap` (Linux) or `Npcap` (Windows)

### Local Setup

```bash
./setup.sh
```

## Usage

```bash
# Activate virtual environment
source venv/bin/activate

# Run scanner (requires sudo for ARP)
sudo python3 src/main.py --target 192.168.1.0/24 --ports 20-1024
```

## Configuration

Edit `config/settings.yaml` to tune concurrency and timeouts.

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting PRs.
