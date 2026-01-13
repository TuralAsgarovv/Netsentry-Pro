import socket
import threading
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict
import logging

class PortScanner:
    """
    Multi-threaded TCP Connect Scanner.
    """
    
    def __init__(self, max_threads: int, timeout: float, logger: logging.Logger):
        self.max_threads = max_threads
        self.timeout = timeout
        self.logger = logger
        self.lock = threading.Lock()
        self.results = {}

    def _scan_port(self, ip: str, port: int) -> None:
        """
        Internal method to check a single port.
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(self.timeout)
                result = s.connect_ex((ip, port))
                if result == 0:
                    with self.lock:
                        if ip not in self.results:
                            self.results[ip] = []
                        self.results[ip].append(port)
                        # TODO: Attempt banner grabbing here in v1.2
        except Exception:
            pass

    def scan(self, targets: List[str], ports: List[int]) -> Dict[str, List[int]]:
        """
        Orchestrates the threaded scan.
        """
        self.logger.info(f"Starting Port Scan on {len(targets)} hosts scanning {len(ports)} ports each.")
        self.results = {}
        
        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            for ip in targets:
                for port in ports:
                    executor.submit(self._scan_port, ip, port)
        
        return self.results
