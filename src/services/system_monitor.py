"""
System monitoring service for collecting system information
"""

import socket
import platform
import psutil
from pydantic import BaseModel


class SystemInfo(BaseModel):
    """System information model"""
    ip_address: str
    mac_address: str
    hostname: str
    os_info: str
    cpu_usage: float
    memory_usage: float
    disk_usage: float


class SystemMonitorService:
    """Service for collecting system information and metrics"""
    
    @staticmethod
    def get_system_info() -> SystemInfo:
        """Collect system information including IP, MAC, and resource usage"""
        # Get IP address
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip_address = s.getsockname()[0]
            s.close()
        except Exception:
            ip_address = "127.0.0.1"
        
        # Get MAC address
        import uuid
        mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) 
                               for elements in range(0, 2*6, 2)][::-1])
        
        # Get system metrics
        cpu_usage = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return SystemInfo(
            ip_address=ip_address,
            mac_address=mac_address,
            hostname=socket.gethostname(),
            os_info=f"{platform.system()} {platform.release()}",
            cpu_usage=cpu_usage,
            memory_usage=memory.percent,
            disk_usage=disk.percent
        ) 