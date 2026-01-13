import ipaddress
import re
from typing import Tuple, List, Optional

def validate_target(target: str) -> bool:
    """
    Validates if the target is a valid IPv4 address or CIDR block.
    TODO: Add support for hostname resolution validation.
    """
    try:
        ipaddress.ip_network(target, strict=False)
        return True
    except ValueError:
        return False

def parse_ports(port_str: str) -> List[int]:
    """
    Parses port string (e.g. "80,443,1000-2000") into a list of integers.
    """
    ports = set()
    parts = port_str.split(',')
    
    for part in parts:
        part = part.strip()
        if '-' in part:
            try:
                start, end = map(int, part.split('-'))
                if 1 <= start <= 65535 and 1 <= end <= 65535:
                    ports.update(range(start, end + 1))
            except ValueError:
                continue
        else:
            try:
                p = int(part)
                if 1 <= p <= 65535:
                    ports.add(p)
            except ValueError:
                continue
                
    return sorted(list(ports))
