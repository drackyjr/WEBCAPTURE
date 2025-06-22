# @ibrahimsql 
# Advanced port scanner modules
import socket
import threading
import time
import random
import struct
import select
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

class PortScanner:
    def __init__(self, target, timeout=1, max_threads=100, stealth_mode=False):
        self.target = target
        self.timeout = timeout
        self.max_threads = max_threads
        self.stealth_mode = stealth_mode
        self.open_ports = []
        self.filtered_ports = []
        self.closed_ports = []
        self.lock = threading.Lock()
        self.scan_start_time = None
        
        # Common ports to scan (expanded list)
        self.common_ports = [
            21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 993, 995,
            1723, 3306, 3389, 5432, 5900, 8080, 8443, 8888, 9090, 3000, 5000,
            6379, 27017, 1433, 1521, 5984, 6667, 6697, 1194, 1701, 4500,
            500, 1194, 8000, 8001, 8008, 8081, 8082, 8083, 8084,
            9000, 9001, 9002, 9200, 9300, 11211, 50070, 50030, 1080, 3128,
            8888, 9999, 10000, 20000, 30000, 40000, 50000, 60000
        ]
        
        # Top 1000 ports for comprehensive scanning
        self.top_1000_ports = self._generate_top_1000_ports()
    
    def _generate_top_1000_ports(self):
        """Generate top 1000 most common ports"""
        return list(range(1, 1001))
    
    def scan_port_tcp(self, port, grab_banner=False):
        """
        Scan a single TCP port with optional banner grabbing
        
        Args:
            port (int): Port number to scan
            grab_banner (bool): Whether to grab service banner
        
        Returns:
            dict: Port scan result
        """
        try:
            if self.stealth_mode:
                time.sleep(random.uniform(0.1, 0.5))  # Random delay for stealth
            
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            
            start_time = time.time()
            result = sock.connect_ex((self.target, port))
            response_time = round((time.time() - start_time) * 1000, 2)
            
            if result == 0:
                service = self.get_service_name(port)
                banner = None
                version = None
                
                if grab_banner:
                    banner, version = self._grab_banner(sock, port)
                
                sock.close()
                
                port_info = {
                    'port': port,
                    'protocol': 'tcp',
                    'service': service,
                    'status': 'open',
                    'response_time': response_time
                }
                
                if banner:
                    port_info['banner'] = banner
                if version:
                    port_info['version'] = version
                
                with self.lock:
                    self.open_ports.append(port_info)
                
                return port_info
            else:
                sock.close()
                port_info = {
                    'port': port,
                    'protocol': 'tcp',
                    'status': 'closed',
                    'response_time': response_time
                }
                
                with self.lock:
                    self.closed_ports.append(port_info)
                
                return port_info
                
        except socket.timeout:
            return {
                'port': port,
                'protocol': 'tcp',
                'status': 'filtered',
                'error': 'Connection timeout'
            }
        except socket.gaierror:
            return {
                'port': port,
                'protocol': 'tcp',
                'status': 'error',
                'error': 'Hostname resolution failed'
            }
        except Exception as e:
            return {
                'port': port,
                'protocol': 'tcp',
                'status': 'error',
                'error': str(e)
            }
    
    def scan_port_udp(self, port):
        """
        Scan a single UDP port
        
        Args:
            port (int): Port number to scan
        
        Returns:
            dict: Port scan result
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(self.timeout)
            
            # Send UDP packet
            sock.sendto(b'\x00', (self.target, port))
            
            try:
                # Try to receive response
                data, addr = sock.recvfrom(1024)
                sock.close()
                
                service = self.get_service_name(port)
                port_info = {
                    'port': port,
                    'protocol': 'udp',
                    'service': service,
                    'status': 'open',
                    'response': data[:100].decode('utf-8', errors='ignore') if data else None
                }
                
                with self.lock:
                    self.open_ports.append(port_info)
                
                return port_info
                
            except socket.timeout:
                sock.close()
                return {
                    'port': port,
                    'protocol': 'udp',
                    'status': 'open|filtered'
                }
                
        except Exception as e:
            return {
                'port': port,
                'protocol': 'udp',
                'status': 'error',
                'error': str(e)
            }
    
    def _grab_banner(self, sock, port):
        """
        Grab service banner from an open port
        
        Args:
            sock: Socket object
            port (int): Port number
        
        Returns:
            tuple: (banner, version)
        """
        try:
            # Send appropriate probe based on port
            probe = self._get_service_probe(port)
            if probe:
                sock.send(probe)
            
            # Receive banner
            banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
            version = self._extract_version(banner, port)
            
            return banner, version
            
        except:
            return None, None
    
    def _get_service_probe(self, port):
        """
        Get appropriate probe for service detection
        
        Args:
            port (int): Port number
        
        Returns:
            bytes: Probe data
        """
        probes = {
            21: b'USER anonymous\r\n',
            22: b'SSH-2.0-Scanner\r\n',
            25: b'EHLO scanner\r\n',
            80: b'GET / HTTP/1.1\r\nHost: ' + self.target.encode() + b'\r\n\r\n',
            110: b'USER test\r\n',
            143: b'A001 CAPABILITY\r\n',
            443: b'GET / HTTP/1.1\r\nHost: ' + self.target.encode() + b'\r\n\r\n',
            993: b'A001 CAPABILITY\r\n',
            995: b'USER test\r\n'
        }
        return probes.get(port, b'')
    
    def _extract_version(self, banner, port):
        """
        Extract version information from banner
        
        Args:
            banner (str): Service banner
            port (int): Port number
        
        Returns:
            str: Version information
        """
        if not banner:
            return None
        
        # Common version patterns
        import re
        
        patterns = {
            'SSH': r'SSH-([\d\.]+)',
            'HTTP': r'Server: ([^\r\n]+)',
            'FTP': r'([\d\.]+)',
            'SMTP': r'([\d\.]+)',
        }
        
        for service, pattern in patterns.items():
            match = re.search(pattern, banner)
            if match:
                return match.group(1)
        
        return banner[:50] if len(banner) > 50 else banner
    
    def get_service_name(self, port):
        """
        Get common service name for a port (expanded database)
        
        Args:
            port (int): Port number
        
        Returns:
            str: Service name
        """
        services = {
            21: 'FTP', 22: 'SSH', 23: 'Telnet', 25: 'SMTP', 53: 'DNS',
            80: 'HTTP', 110: 'POP3', 111: 'RPC', 135: 'RPC', 139: 'NetBIOS',
            143: 'IMAP', 443: 'HTTPS', 993: 'IMAPS', 995: 'POP3S',
            1433: 'MSSQL', 1521: 'Oracle', 1723: 'PPTP', 3306: 'MySQL',
            3389: 'RDP', 5432: 'PostgreSQL', 5900: 'VNC', 6379: 'Redis',
            8080: 'HTTP-Alt', 8443: 'HTTPS-Alt', 27017: 'MongoDB',
            # Additional services
            20: 'FTP-Data', 69: 'TFTP', 123: 'NTP', 161: 'SNMP', 162: 'SNMP-Trap',
            389: 'LDAP', 636: 'LDAPS', 1080: 'SOCKS', 3128: 'Squid-Proxy',
            5060: 'SIP', 5061: 'SIP-TLS', 8888: 'HTTP-Alt2', 9090: 'Zeus-Admin',
            10000: 'Webmin', 11211: 'Memcached', 50070: 'Hadoop-NameNode',
            # Database ports
            1434: 'MSSQL-Monitor', 3050: 'Firebird', 5984: 'CouchDB',
            # Web services
            8000: 'HTTP-Alt3', 8001: 'HTTP-Alt4', 8008: 'HTTP-Alt5',
            8081: 'HTTP-Alt6', 8082: 'HTTP-Alt7', 8083: 'HTTP-Alt8',
            8084: 'HTTP-Alt9', 9000: 'HTTP-Alt10', 9001: 'HTTP-Alt11',
            9002: 'HTTP-Alt12', 9200: 'Elasticsearch', 9300: 'Elasticsearch-Node',
            # Gaming and media
            25565: 'Minecraft', 27015: 'Steam', 6667: 'IRC', 6697: 'IRC-SSL',
            # VPN and tunneling
            1194: 'OpenVPN', 1701: 'L2TP', 4500: 'IPSec-NAT', 500: 'IPSec'
        }
        return services.get(port, 'Unknown')
    
    def scan_common_ports(self, protocol='tcp', grab_banner=False):
        """
        Scan common ports using threading
        
        Args:
            protocol (str): 'tcp', 'udp', or 'both'
            grab_banner (bool): Whether to grab service banners
        
        Returns:
            dict: Scan results
        """
        self.scan_start_time = datetime.now()
        print(f"[{self.scan_start_time.strftime('%H:%M:%S')}] Starting {protocol.upper()} scan of {len(self.common_ports)} common ports on {self.target}...")
        
        if self.stealth_mode:
            print("[INFO] Stealth mode enabled - scan will be slower but less detectable")
        
        start_time = time.time()
        self._reset_port_lists()
        
        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            futures = []
            
            for port in self.common_ports:
                if protocol in ['tcp', 'both']:
                    future = executor.submit(self.scan_port_tcp, port, grab_banner)
                    futures.append(future)
                
                if protocol in ['udp', 'both']:
                    future = executor.submit(self.scan_port_udp, port)
                    futures.append(future)
            
            # Process results
            completed = 0
            for future in as_completed(futures):
                completed += 1
                try:
                    result = future.result()
                    if completed % 50 == 0:  # Progress indicator
                        print(f"[INFO] Scanned {completed}/{len(futures)} ports...")
                except Exception as exc:
                    print(f'[ERROR] Port scan generated an exception: {exc}')
        
        end_time = time.time()
        scan_duration = round(end_time - start_time, 2)
        
        return self._generate_scan_report('common', scan_duration, len(self.common_ports))
    
    def scan_top_1000_ports(self, protocol='tcp', grab_banner=False):
        """
        Scan top 1000 ports
        
        Args:
            protocol (str): 'tcp', 'udp', or 'both'
            grab_banner (bool): Whether to grab service banners
        
        Returns:
            dict: Scan results
        """
        self.scan_start_time = datetime.now()
        print(f"[{self.scan_start_time.strftime('%H:%M:%S')}] Starting comprehensive {protocol.upper()} scan of top 1000 ports on {self.target}...")
        
        start_time = time.time()
        self._reset_port_lists()
        
        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            futures = []
            
            for port in self.top_1000_ports:
                if protocol in ['tcp', 'both']:
                    future = executor.submit(self.scan_port_tcp, port, grab_banner)
                    futures.append(future)
                
                if protocol in ['udp', 'both']:
                    future = executor.submit(self.scan_port_udp, port)
                    futures.append(future)
            
            # Process results with progress
            completed = 0
            for future in as_completed(futures):
                completed += 1
                try:
                    result = future.result()
                    if completed % 100 == 0:
                        progress = (completed / len(futures)) * 100
                        print(f"[INFO] Progress: {progress:.1f}% ({completed}/{len(futures)} ports)")
                except Exception as exc:
                    print(f'[ERROR] Port scan generated an exception: {exc}')
        
        end_time = time.time()
        scan_duration = round(end_time - start_time, 2)
        
        return self._generate_scan_report('top1000', scan_duration, len(self.top_1000_ports))
    
    def _reset_port_lists(self):
        """Reset port lists for new scan"""
        with self.lock:
            self.open_ports = []
            self.filtered_ports = []
            self.closed_ports = []
    
    def scan_port_range(self, start_port, end_port, protocol='tcp', grab_banner=False):
        """
        Scan a range of ports with enhanced features
        
        Args:
            start_port (int): Starting port number
            end_port (int): Ending port number
            protocol (str): 'tcp', 'udp', or 'both'
            grab_banner (bool): Whether to grab service banners
        
        Returns:
            dict: Scan results
        """
        ports_to_scan = list(range(start_port, end_port + 1))
        self.scan_start_time = datetime.now()
        
        print(f"[{self.scan_start_time.strftime('%H:%M:%S')}] Starting {protocol.upper()} scan of ports {start_port}-{end_port} on {self.target}...")
        print(f"[INFO] Total ports to scan: {len(ports_to_scan)}")
        
        start_time = time.time()
        self._reset_port_lists()
        
        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            futures = []
            
            for port in ports_to_scan:
                if protocol in ['tcp', 'both']:
                    future = executor.submit(self.scan_port_tcp, port, grab_banner)
                    futures.append(future)
                
                if protocol in ['udp', 'both']:
                    future = executor.submit(self.scan_port_udp, port)
                    futures.append(future)
            
            # Process results with detailed progress
            completed = 0
            for future in as_completed(futures):
                completed += 1
                try:
                    result = future.result()
                    if completed % 100 == 0 or completed == len(futures):
                        progress = (completed / len(futures)) * 100
                        elapsed = time.time() - start_time
                        rate = completed / elapsed if elapsed > 0 else 0
                        eta = (len(futures) - completed) / rate if rate > 0 else 0
                        print(f"[INFO] Progress: {progress:.1f}% | Rate: {rate:.1f} ports/sec | ETA: {eta:.0f}s")
                except Exception as exc:
                    print(f'[ERROR] Port {futures.index(future)} generated an exception: {exc}')
        
        end_time = time.time()
        scan_duration = round(end_time - start_time, 2)
        
        result = self._generate_scan_report('range', scan_duration, len(ports_to_scan))
        result['port_range'] = f'{start_port}-{end_port}'
        
        return result
    
    def _generate_scan_report(self, scan_type, duration, total_ports):
        """
        Generate comprehensive scan report
        
        Args:
            scan_type (str): Type of scan performed
            duration (float): Scan duration in seconds
            total_ports (int): Total ports scanned
        
        Returns:
            dict: Comprehensive scan report
        """
        end_time = datetime.now()
        
        # Calculate statistics
        open_count = len(self.open_ports)
        filtered_count = len(self.filtered_ports)
        closed_count = len(self.closed_ports)
        
        # Sort ports by port number
        open_ports_sorted = sorted(self.open_ports, key=lambda x: x['port'])
        
        # Generate service summary
        services_found = {}
        for port_info in self.open_ports:
            service = port_info.get('service', 'Unknown')
            if service not in services_found:
                services_found[service] = []
            services_found[service].append(port_info['port'])
        
        report = {
            'scan_info': {
                'target': self.target,
                'scan_type': scan_type,
                'start_time': self.scan_start_time.strftime('%Y-%m-%d %H:%M:%S'),
                'end_time': end_time.strftime('%Y-%m-%d %H:%M:%S'),
                'duration': duration,
                'stealth_mode': self.stealth_mode
            },
            'statistics': {
                'total_ports_scanned': total_ports,
                'open_ports_count': open_count,
                'filtered_ports_count': filtered_count,
                'closed_ports_count': closed_count,
                'scan_rate': round(total_ports / duration, 2) if duration > 0 else 0
            },
            'open_ports': open_ports_sorted,
            'services_summary': services_found,
            'recommendations': self._generate_security_recommendations()
        }
        
        return report
    
    def _generate_security_recommendations(self):
        """
        Generate security recommendations based on open ports
        
        Returns:
            list: Security recommendations
        """
        recommendations = []
        
        # Check for common vulnerable services
        vulnerable_services = {
            21: "FTP service detected. Consider using SFTP instead.",
            23: "Telnet service detected. This is highly insecure - use SSH instead.",
            135: "RPC service detected. Ensure it's properly configured and firewalled.",
            139: "NetBIOS service detected. Consider disabling if not needed.",
            445: "SMB service detected. Ensure it's updated and properly secured.",
            1433: "MSSQL service detected. Ensure strong authentication and encryption.",
            3389: "RDP service detected. Use strong passwords and consider VPN access.",
            5900: "VNC service detected. Ensure strong authentication is enabled."
        }
        
        for port_info in self.open_ports:
            port = port_info['port']
            if port in vulnerable_services:
                recommendations.append(vulnerable_services[port])
        
        # General recommendations
        if len(self.open_ports) > 10:
            recommendations.append("Many open ports detected. Review and close unnecessary services.")
        
        if not recommendations:
            recommendations.append("No obvious security issues detected, but regular security audits are recommended.")
        
        return recommendations

def scan_target_ports(target, scan_type='common', start_port=1, end_port=1000, 
                     protocol='tcp', grab_banner=False, stealth_mode=False, 
                     max_threads=100, timeout=1):
    """
    Advanced main function to scan ports on a target with multiple options
    
    Args:
        target (str): Target hostname or IP
        scan_type (str): 'common', 'top1000', or 'range'
        start_port (int): Start port for range scan
        end_port (int): End port for range scan
        protocol (str): 'tcp', 'udp', or 'both'
        grab_banner (bool): Whether to grab service banners
        stealth_mode (bool): Enable stealth scanning
        max_threads (int): Maximum number of threads
        timeout (int): Connection timeout in seconds
    
    Returns:
        dict: Comprehensive scan results
    """
    try:
        print(f"[INFO] Resolving hostname: {target}")
        target_ip = socket.gethostbyname(target)
        print(f"[INFO] Target IP: {target_ip}")
        
        # Initialize advanced scanner
        scanner = AdvancedPortScanner(
            target=target_ip,
            timeout=timeout,
            max_threads=max_threads,
            stealth_mode=stealth_mode
        )
        
        print(f"[INFO] Scan configuration:")
        print(f"  - Protocol: {protocol.upper()}")
        print(f"  - Banner grabbing: {'Enabled' if grab_banner else 'Disabled'}")
        print(f"  - Stealth mode: {'Enabled' if stealth_mode else 'Disabled'}")
        print(f"  - Threads: {max_threads}")
        print(f"  - Timeout: {timeout}s")
        print()
        
        # Execute scan based on type
        if scan_type == 'common':
            return scanner.scan_common_ports(protocol=protocol, grab_banner=grab_banner)
        elif scan_type == 'top1000':
            return scanner.scan_top_1000_ports(protocol=protocol, grab_banner=grab_banner)
        elif scan_type == 'range':
            return scanner.scan_port_range(
                start_port=start_port, 
                end_port=end_port, 
                protocol=protocol, 
                grab_banner=grab_banner
            )
        else:
            return {
                'error': 'Invalid scan type. Use "common", "top1000", or "range"',
                'available_types': ['common', 'top1000', 'range']
            }
            
    except socket.gaierror:
        return {
            'error': f'Could not resolve hostname: {target}',
            'suggestion': 'Check if the hostname is correct and you have internet connectivity'
        }
    except KeyboardInterrupt:
        return {
            'error': 'Scan interrupted by user',
            'status': 'cancelled'
        }
    except Exception as e:
        return {
            'error': f'Unexpected error: {str(e)}',
            'type': type(e).__name__
        }

def quick_scan(target, grab_banner=False):
    """
    Quick scan of most common ports
    
    Args:
        target (str): Target hostname or IP
        grab_banner (bool): Whether to grab service banners
    
    Returns:
        dict: Scan results
    """
    return scan_target_ports(
        target=target,
        scan_type='common',
        protocol='tcp',
        grab_banner=grab_banner,
        max_threads=50,
        timeout=1
    )

def stealth_scan(target, scan_type='common', grab_banner=True):
    """
    Stealth scan with banner grabbing
    
    Args:
        target (str): Target hostname or IP
        scan_type (str): Type of scan to perform
        grab_banner (bool): Whether to grab service banners
    
    Returns:
        dict: Scan results
    """
    return scan_target_ports(
        target=target,
        scan_type=scan_type,
        protocol='tcp',
        grab_banner=grab_banner,
        stealth_mode=True,
        max_threads=20,
        timeout=2
    )

def comprehensive_scan(target, grab_banner=True):
    """
    Comprehensive scan of top 1000 ports with banner grabbing
    
    Args:
        target (str): Target hostname or IP
        grab_banner (bool): Whether to grab service banners
    
    Returns:
        dict: Scan results
    """
    return scan_target_ports(
        target=target,
        scan_type='top1000',
        protocol='both',
        grab_banner=grab_banner,
        max_threads=100,
        timeout=2
    )

def format_scan_results(results):
    """
    Format scan results for display
    
    Args:
        results (dict): Scan results
    
    Returns:
        str: Formatted results
    """
    if 'error' in results:
        return f"❌ Error: {results['error']}"
    
    output = []
    
    # Scan info
    scan_info = results.get('scan_info', {})
    output.append(f"🎯 Target: {scan_info.get('target', 'Unknown')}")
    output.append(f"⏱️  Duration: {scan_info.get('duration', 0)}s")
    output.append(f"🔍 Scan Type: {scan_info.get('scan_type', 'Unknown').upper()}")
    output.append("")
    
    # Statistics
    stats = results.get('statistics', {})
    output.append("📊 Statistics:")
    output.append(f"  • Total ports scanned: {stats.get('total_ports_scanned', 0)}")
    output.append(f"  • Open ports: {stats.get('open_ports_count', 0)}")
    output.append(f"  • Scan rate: {stats.get('scan_rate', 0)} ports/sec")
    output.append("")
    
    # Open ports
    open_ports = results.get('open_ports', [])
    if open_ports:
        output.append("🔓 Open Ports:")
        for port_info in open_ports:
            port = port_info['port']
            service = port_info.get('service', 'Unknown')
            protocol = port_info.get('protocol', 'tcp')
            response_time = port_info.get('response_time', 'N/A')
            
            line = f"  • {port}/{protocol} - {service}"
            if response_time != 'N/A':
                line += f" ({response_time}ms)"
            
            if 'banner' in port_info:
                line += f"\n    Banner: {port_info['banner'][:100]}..."
            
            output.append(line)
        output.append("")
    
    # Services summary
    services = results.get('services_summary', {})
    if services:
        output.append("🛠️  Services Found:")
        for service, ports in services.items():
            output.append(f"  • {service}: {', '.join(map(str, ports))}")
        output.append("")
    
    # Security recommendations
    recommendations = results.get('recommendations', [])
    if recommendations:
        output.append("⚠️  Security Recommendations:")
        for rec in recommendations:
            output.append(f"  • {rec}")
    
    return "\n".join(output)

# Backward compatibility
PortScanner = AdvancedPortScanner