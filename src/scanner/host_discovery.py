from scapy.all import ARP, Ether, srp
from typing import List
import logging

class HostDiscoverer:
    """
    Handles Layer 2 discovery using ARP.
    Note: This requires root privileges to craft raw packets.
    """

    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def scan_arp(self, target_ip: str, timeout: int = 2) -> List[dict]:
        """
        Sends ARP requests to the target subnet.
        Returns a list of dicts with 'ip' and 'mac'.
        """
        self.logger.info(f"Starting ARP discovery on {target_ip}...")
        
        active_hosts = []
        
        try:
            # Construct the ARP packet
            # ether dst="ff..." is broadcast
            packet = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=target_ip)
            
            # srp = send and receive packets at layer 2
            result = srp(packet, timeout=timeout, verbose=0)[0]
            
            for sent, received in result:
                host_info = {'ip': received.psrc, 'mac': received.hwsrc}
                active_hosts.append(host_info)
                self.logger.debug(f"Host found: {host_info['ip']} ({host_info['mac']})")
                
        except PermissionError:
            self.logger.error("Permission denied: Scapy requires root/sudo privileges.")
        except Exception as e:
            self.logger.error(f"Unexpected error during ARP scan: {e}")
            
        return active_hosts
