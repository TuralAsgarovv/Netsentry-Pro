import argparse
import sys
import yaml
import os
from colorama import init, Fore, Style

# Local Imports
from utils.logger import ScannerLogger
from utils.validators import validate_target, parse_ports
from scanner.host_discovery import HostDiscoverer
from scanner.port_scanner import PortScanner

# Initialize colorama for cross-platform colored output
init(autoreset=True)

def load_config(config_path: str):
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def main():
    parser = argparse.ArgumentParser(description="NetSentry-Pro: Network Recon Tool")
    parser.add_argument("--target", "-t", required=True, help="Target IP or CIDR (e.g., 192.168.1.0/24)")
    parser.add_argument("--ports", "-p", default="22,80,443", help="Ports to scan (e.g. 20-100, 443)")
    parser.add_argument("--config", "-c", default="config/settings.yaml", help="Path to config file")
    
    args = parser.parse_args()
    
    # Setup Config & Logging
    try:
        config = load_config(args.config)
        logger = ScannerLogger.setup_logger(
            log_file=config['logging']['file_path'],
            level=config['logging']['level']
        )
    except Exception as e:
        print(f"{Fore.RED}[CRITICAL] Failed to load config: {e}")
        sys.exit(1)

    # Validation
    if not validate_target(args.target):
        logger.error(f"Invalid target format: {args.target}")
        sys.exit(1)
        
    port_list = parse_ports(args.ports)
    if not port_list:
        logger.error("No valid ports provided.")
        sys.exit(1)

    print(f"{Style.BRIGHT}{Fore.CYAN}=== NetSentry-Pro Started ==={Style.RESET_ALL}")

    # Phase 1: Host Discovery
    discoverer = HostDiscoverer(logger)
    active_hosts = discoverer.scan_arp(args.target, timeout=config['scanner']['arp_timeout'])
    
    if not active_hosts:
        logger.warning("No active hosts found via ARP. Aborting port scan.")
        sys.exit(0)

    logger.info(f"Found {len(active_hosts)} active hosts.")
    target_ips = [h['ip'] for h in active_hosts]

    # Phase 2: Port Scanning
    scanner = PortScanner(
        max_threads=config['scanner']['max_threads'],
        timeout=config['scanner']['timeout'],
        logger=logger
    )
    
    results = scanner.scan(target_ips, port_list)

    # Reporting
    print(f"\n{Style.BRIGHT}--- Scan Results ---{Style.RESET_ALL}")
    for ip, ports in results.items():
        if ports:
            print(f"{Fore.GREEN}[+] {ip} is active.")
            for port in sorted(ports):
                print(f"    {Fore.YELLOW}OPEN{Fore.RESET} : {port}/tcp")
        else:
            print(f"{Fore.RED}[-] {ip} has no open ports in specified range.")
            
    logger.info("Scan completed successfully.")

if __name__ == "__main__":
    # Scapy often warns about ipv6 if not configured, suppressing for clean output
    logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
    main()
