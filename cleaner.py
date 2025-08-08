#!/usr/bin/env python3
"""
Enterprise AppData Deep Clean Suite
Production-ready tool for DevOps teams to manage AppData cleanup across multiple systems.

Features:
- Enterprise software awareness
- Configuration management integration
- Security framework compliance
- Batch deployment capabilities
- Comprehensive auditing and reporting
"""

import os
import sys
import json
import yaml
import time
import shutil
import hashlib
import winreg
import logging
import argparse
import threading
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Set, Tuple, Optional
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
import configparser

# Enterprise integrations
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

try:
    import wmi
    HAS_WMI = True
except ImportError:
    HAS_WMI = False

class EnterpriseAppDataCleaner:
    def __init__(self, config_file: str = None, dry_run: bool = True):
        self.dry_run = dry_run
        self.config = self.load_configuration(config_file)
        self.results = {
            'start_time': datetime.now().isoformat(),
            'hostname': os.environ.get('COMPUTERNAME', 'unknown'),
            'user': os.environ.get('USERNAME', 'unknown'),
            'deleted_files': [],
            'deleted_size': 0,
            'errors': [],
            'compliance_report': {},
            'security_events': []
        }
        
        # Setup enterprise logging
        self.setup_enterprise_logging()
        
        # Initialize security framework
        self.security_context = self.initialize_security_context()
        
        # Load enterprise software definitions
        self.enterprise_software = self.load_enterprise_software_db()
        
        # Initialize configuration management client
        self.config_mgmt_client = self.initialize_config_management()

    def load_configuration(self, config_file: str = None) -> Dict:
        """Load enterprise configuration from multiple sources"""
        default_config = {
            'enterprise': {
                'organization': 'DefaultOrg',
                'environment': 'production',
                'compliance_level': 'standard',
                'security_framework': 'nist',
                'audit_required': True
            },
            'software_patterns': {
                'protected_enterprise': [
                    'microsoft', 'office', 'teams', 'outlook', 'onedrive',
                    'adobe', 'acrobat', 'creative', 'photoshop',
                    'zoom', 'webex', 'slack', 'skype',
                    'vmware', 'citrix', 'rdp',
                    'antivirus', 'endpoint', 'defender', 'symantec', 'mcafee',
                    'tableau', 'powerbi', 'splunk', 'datadog',
                    'jenkins', 'git', 'docker', 'kubernetes',
                    'chrome', 'firefox', 'edge', 'java', 'python'
                ],
                'development_tools': [
                    'vscode', 'visualstudio', 'intellij', 'eclipse',
                    'nodejs', 'npm', 'gradle', 'maven',
                    'postman', 'insomnia', 'wireshark'
                ],
                'safe_to_clean': [
                    'temp', 'cache', 'logs', 'backup',
                    'old', 'deprecated', 'unused'
                ]
            },
            'security': {
                'require_elevation': True,
                'audit_all_operations': True,
                'encrypt_reports': False,
                'send_to_siem': False,
                'siem_endpoint': None,
                'max_file_age_days': 90,
                'min_file_size_mb': 1
            },
            'deployment': {
                'batch_size': 50,
                'parallel_threads': 4,
                'timeout_minutes': 30,
                'retry_attempts': 3,
                'target_hosts': [],
                'ssh_key_path': None,
                'winrm_config': {}
            },
            'config_management': {
                'type': None,  # 'ansible', 'puppet', 'chef', 'saltstack'
                'server': None,
                'api_key': None,
                'playbook_path': None
            },
            'reporting': {
                'formats': ['json', 'yaml', 'csv'],
                'destinations': ['local', 'network', 'api'],
                'webhook_url': None,
                'email_notifications': False
            }
        }
        
        if config_file and Path(config_file).exists():
            with open(config_file, 'r') as f:
                if config_file.endswith('.yaml') or config_file.endswith('.yml'):
                    user_config = yaml.safe_load(f)
                else:
                    user_config = json.load(f)
            
            # Deep merge configurations
            default_config = self.deep_merge_config(default_config, user_config)
        
        return default_config

    def deep_merge_config(self, base: Dict, update: Dict) -> Dict:
        """Deep merge configuration dictionaries"""
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                base[key] = self.deep_merge_config(base[key], value)
            else:
                base[key] = value
        return base

    def setup_enterprise_logging(self):
        """Setup enterprise-grade logging with multiple outputs"""
        log_level = logging.INFO
        if self.config['enterprise']['environment'] == 'development':
            log_level = logging.DEBUG
        
        # Create logs directory
        log_dir = Path('logs')
        log_dir.mkdir(exist_ok=True)
        
        # Setup formatters
        detailed_formatter = logging.Formatter(
            '%(asctime)s - %(hostname)s - %(user)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
        )
        
        # File handler for detailed logs
        detailed_log = log_dir / f"appdata_clean_detailed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        file_handler = logging.FileHandler(detailed_log)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(detailed_formatter)
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        
        # Setup logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
        # Add hostname and user to log records
        class EnterpriseFilter(logging.Filter):
            def filter(self, record):
                record.hostname = os.environ.get('COMPUTERNAME', 'unknown')
                record.user = os.environ.get('USERNAME', 'unknown')
                return True
        
        self.logger.addFilter(EnterpriseFilter())
        
        # Audit log for security events
        audit_log = log_dir / f"audit_{datetime.now().strftime('%Y%m%d')}.log"
        self.audit_handler = logging.FileHandler(audit_log)
        self.audit_handler.setLevel(logging.INFO)
        self.audit_handler.setFormatter(logging.Formatter(
            '%(asctime)s - AUDIT - %(hostname)s - %(user)s - %(message)s'
        ))
        
        self.audit_logger = logging.getLogger('audit')
        self.audit_logger.addHandler(self.audit_handler)
        self.audit_logger.addFilter(EnterpriseFilter())

    def initialize_security_context(self) -> Dict:
        """Initialize security framework context"""
        context = {
            'framework': self.config['security'].get('security_framework', 'nist'),
            'compliance_level': self.config['enterprise'].get('compliance_level', 'standard'),
            'elevated': self.check_elevation(),
            'domain_joined': self.check_domain_membership(),
            'security_software': self.detect_security_software()
        }
        
        self.audit_logger.info(f"Security context initialized: {context}")
        return context

    def check_elevation(self) -> bool:
        """Check if running with administrative privileges"""
        try:
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def check_domain_membership(self) -> bool:
        """Check if machine is domain joined"""
        try:
            import socket
            return '.' in socket.getfqdn()
        except:
            return False

    def detect_security_software(self) -> List[str]:
        """Detect installed security software"""
        security_products = []
        
        if not HAS_WMI:
            return security_products
        
        try:
            c = wmi.WMI()
            # Check for antivirus products
            for product in c.Win32_Product():
                if any(av in product.Name.lower() for av in ['antivirus', 'defender', 'security', 'endpoint']):
                    security_products.append(product.Name)
        except Exception as e:
            self.logger.warning(f"Could not detect security software: {e}")
        
        return security_products

    def load_enterprise_software_db(self) -> Dict:
        """Load enterprise software database from multiple sources"""
        software_db = {
            'installed_programs': set(),
            'running_services': set(),
            'enterprise_apps': set(),
            'development_tools': set()
        }
        
        # Load from Windows registry
        software_db['installed_programs'] = self.get_installed_programs()
        
        # Load from running services
        if HAS_PSUTIL:
            software_db['running_services'] = self.get_running_services()
        
        # Load enterprise-specific applications
        software_db['enterprise_apps'] = set(self.config['software_patterns']['protected_enterprise'])
        software_db['development_tools'] = set(self.config['software_patterns']['development_tools'])
        
        # Load from configuration management system
        if self.config_mgmt_client:
            cm_software = self.get_software_from_config_mgmt()
            if cm_software:
                software_db['enterprise_apps'].update(cm_software)
        
        return software_db

    def get_installed_programs(self) -> Set[str]:
        """Get installed programs from registry with enterprise focus"""
        programs = set()
        
        registry_paths = [
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
            (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
        ]
        
        for hkey, subkey in registry_paths:
            try:
                with winreg.OpenKey(hkey, subkey) as key:
                    i = 0
                    while True:
                        try:
                            program_key = winreg.EnumKey(key, i)
                            programs.add(program_key.lower())
                            
                            try:
                                with winreg.OpenKey(key, program_key) as prog_key:
                                    display_name, _ = winreg.QueryValueEx(prog_key, "DisplayName")
                                    programs.add(display_name.lower())
                                    
                                    # Also get publisher for enterprise software
                                    try:
                                        publisher, _ = winreg.QueryValueEx(prog_key, "Publisher")
                                        programs.add(publisher.lower())
                                    except (FileNotFoundError, OSError):
                                        pass
                            except (FileNotFoundError, OSError):
                                pass
                            
                            i += 1
                        except OSError:
                            break
            except Exception as e:
                self.logger.warning(f"Registry access error {hkey}\\{subkey}: {e}")
        
        return programs

    def get_running_services(self) -> Set[str]:
        """Get running Windows services"""
        services = set()
        
        try:
            for service in psutil.win_service_iter():
                try:
                    info = service.as_dict()
                    if info['status'] == 'running':
                        services.add(info['name'].lower())
                        services.add(info['display_name'].lower())
                except Exception:
                    continue
        except Exception as e:
            self.logger.warning(f"Could not enumerate services: {e}")
        
        return services

    def initialize_config_management(self):
        """Initialize configuration management client"""
        cm_type = self.config['config_management'].get('type')
        
        if not cm_type:
            return None
        
        if cm_type.lower() == 'ansible':
            return self.initialize_ansible_client()
        elif cm_type.lower() == 'puppet':
            return self.initialize_puppet_client()
        elif cm_type.lower() == 'chef':
            return self.initialize_chef_client()
        elif cm_type.lower() == 'saltstack':
            return self.initialize_saltstack_client()
        
        return None

    def initialize_ansible_client(self):
        """Initialize Ansible integration"""
        try:
            ansible_config = self.config['config_management']
            return {
                'type': 'ansible',
                'inventory': ansible_config.get('inventory_path'),
                'playbook': ansible_config.get('playbook_path'),
                'vault_password': ansible_config.get('vault_password_file')
            }
        except Exception as e:
            self.logger.warning(f"Ansible initialization failed: {e}")
            return None

    def initialize_puppet_client(self):
        """Initialize Puppet integration"""
        try:
            return {
                'type': 'puppet',
                'server': self.config['config_management'].get('server'),
                'cert_path': self.config['config_management'].get('cert_path')
            }
        except Exception as e:
            self.logger.warning(f"Puppet initialization failed: {e}")
            return None

    def initialize_chef_client(self):
        """Initialize Chef integration"""
        try:
            return {
                'type': 'chef',
                'server_url': self.config['config_management'].get('server'),
                'client_key': self.config['config_management'].get('client_key'),
                'node_name': os.environ.get('COMPUTERNAME', 'unknown')
            }
        except Exception as e:
            self.logger.warning(f"Chef initialization failed: {e}")
            return None

    def initialize_saltstack_client(self):
        """Initialize SaltStack integration"""
        try:
            return {
                'type': 'saltstack',
                'master': self.config['config_management'].get('server'),
                'minion_id': os.environ.get('COMPUTERNAME', 'unknown')
            }
        except Exception as e:
            self.logger.warning(f"SaltStack initialization failed: {e}")
            return None

    def get_software_from_config_mgmt(self) -> Set[str]:
        """Get software inventory from configuration management system"""
        if not self.config_mgmt_client:
            return set()
        
        cm_type = self.config_mgmt_client['type']
        
        try:
            if cm_type == 'ansible':
                return self.get_ansible_software_inventory()
            elif cm_type == 'puppet':
                return self.get_puppet_software_inventory()
            elif cm_type == 'chef':
                return self.get_chef_software_inventory()
            elif cm_type == 'saltstack':
                return self.get_saltstack_software_inventory()
        except Exception as e:
            self.logger.warning(f"Config management software inventory failed: {e}")
        
        return set()

    def get_ansible_software_inventory(self) -> Set[str]:
        """Get software from Ansible facts"""
        software = set()
        try:
            # Run ansible facts gathering
            result = subprocess.run([
                'ansible', 'localhost', '-m', 'setup', '--connection=local'
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                # Parse Ansible facts for installed packages
                import re
                packages = re.findall(r'"(.+?)": {[^}]*"version":', result.stdout)
                software.update(pkg.lower() for pkg in packages)
        except Exception as e:
            self.logger.debug(f"Ansible facts gathering failed: {e}")
        
        return software

    def get_puppet_software_inventory(self) -> Set[str]:
        """Get software from Puppet facts"""
        software = set()
        try:
            result = subprocess.run([
                'facter', '--json'
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                facts = json.loads(result.stdout)
                if 'packages' in facts:
                    software.update(facts['packages'].keys())
        except Exception as e:
            self.logger.debug(f"Puppet facts gathering failed: {e}")
        
        return software

    def get_chef_software_inventory(self) -> Set[str]:
        """Get software from Chef node attributes"""
        software = set()
        try:
            result = subprocess.run([
                'knife', 'node', 'show', self.config_mgmt_client['node_name'], '-F', 'json'
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                node_data = json.loads(result.stdout)
                if 'packages' in node_data.get('automatic', {}):
                    software.update(node_data['automatic']['packages'].keys())
        except Exception as e:
            self.logger.debug(f"Chef node data gathering failed: {e}")
        
        return software

    def get_saltstack_software_inventory(self) -> Set[str]:
        """Get software from SaltStack grains"""
        software = set()
        try:
            result = subprocess.run([
                'salt-call', '--local', 'pkg.list_pkgs', '--out=json'
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                packages = json.loads(result.stdout)
                if 'local' in packages:
                    software.update(packages['local'].keys())
        except Exception as e:
            self.logger.debug(f"SaltStack grains gathering failed: {e}")
        
        return software

    def is_enterprise_software_linked(self, file_path: Path) -> Tuple[bool, str]:
        """Enhanced enterprise software link detection"""
        file_name = file_path.name.lower()
        parent_name = file_path.parent.name.lower()
        full_path = str(file_path).lower()
        
        # Check enterprise software patterns
        for category, software_list in self.enterprise_software.items():
            for software in software_list:
                if software in full_path or software in parent_name or software in file_name:
                    return True, f"Enterprise software ({category}): {software}"
        
        # Check file age against policy
        try:
            file_age_days = (time.time() - file_path.stat().st_mtime) / (24 * 60 * 60)
            max_age = self.config['security']['max_file_age_days']
            
            if file_age_days < max_age:
                return True, f"File too recent (age: {file_age_days:.1f} days, policy: {max_age} days)"
        except OSError:
            pass
        
        # Check file size against policy
        try:
            file_size_mb = file_path.stat().st_size / (1024 * 1024)
            min_size = self.config['security']['min_file_size_mb']
            
            if file_size_mb < min_size:
                return True, f"File too small (size: {file_size_mb:.2f}MB, policy min: {min_size}MB)"
        except OSError:
            pass
        
        # Enterprise-specific extensions to preserve
        enterprise_extensions = {
            '.pfx', '.p12', '.crt', '.cer', '.key',  # Certificates
            '.msi', '.msp',  # Installation packages
            '.reg', '.pol',  # Registry and policy files
            '.admx', '.adml',  # Group policy templates
            '.rdp', '.vnc',  # Remote desktop configs
        }
        
        if file_path.suffix.lower() in enterprise_extensions:
            return True, f"Enterprise file type: {file_path.suffix}"
        
        return False, "No enterprise links found"

    def scan_with_compliance(self, directory: Path) -> Dict:
        """Scan directory with compliance and security considerations"""
        results = {
            'directory': str(directory),
            'total_files': 0,
            'total_size': 0,
            'orphaned_files': [],
            'protected_files': [],
            'compliance_issues': [],
            'security_events': [],
            'errors': []
        }
        
        self.logger.info(f"Compliance scan starting: {directory}")
        self.audit_logger.info(f"SCAN_START: {directory}")
        
        try:
            for root, dirs, files in os.walk(directory):
                root_path = Path(root)
                
                # Security check: Skip encrypted or protected directories
                if self.is_protected_directory(root_path):
                    self.audit_logger.info(f"PROTECTED_DIR_SKIPPED: {root_path}")
                    continue
                
                for file_name in files:
                    file_path = root_path / file_name
                    
                    try:
                        if not file_path.exists():
                            continue
                        
                        file_size = file_path.stat().st_size
                        results['total_files'] += 1
                        results['total_size'] += file_size
                        
                        # Enterprise software link check
                        is_linked, reason = self.is_enterprise_software_linked(file_path)
                        
                        if is_linked:
                            results['protected_files'].append({
                                'path': str(file_path),
                                'size': file_size,
                                'reason': reason,
                                'protected_at': datetime.now().isoformat()
                            })
                        else:
                            # Compliance check before marking as orphaned
                            compliance_result = self.check_compliance(file_path)
                            
                            if compliance_result['compliant']:
                                results['orphaned_files'].append({
                                    'path': str(file_path),
                                    'size': file_size,
                                    'modified': datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
                                    'compliance_score': compliance_result['score']
                                })
                            else:
                                results['compliance_issues'].append({
                                    'path': str(file_path),
                                    'issues': compliance_result['issues']
                                })
                    
                    except (OSError, PermissionError) as e:
                        results['errors'].append({
                            'path': str(file_path),
                            'error': str(e)
                        })
                        self.audit_logger.warning(f"FILE_ACCESS_ERROR: {file_path}: {e}")
        
        except Exception as e:
            self.logger.error(f"Compliance scan error {directory}: {e}")
            results['errors'].append({'directory': str(directory), 'error': str(e)})
        
        self.audit_logger.info(f"SCAN_COMPLETE: {directory} - Found {len(results['orphaned_files'])} orphaned files")
        return results

    def is_protected_directory(self, directory: Path) -> bool:
        """Check if directory is protected by security policies"""
        protected_patterns = [
            'system32', 'syswow64', 'windows', 'program files',
            'certificates', 'keys', 'crypto', 'security',
            '.ssh', '.gnupg', 'credentials'
        ]
        
        dir_str = str(directory).lower()
        return any(pattern in dir_str for pattern in protected_patterns)

    def check_compliance(self, file_path: Path) -> Dict:
        """Check file against compliance requirements"""
        compliance_result = {
            'compliant': True,
            'score': 100,
            'issues': []
        }
        
        framework = self.security_context['framework']
        
        if framework == 'nist':
            compliance_result = self.check_nist_compliance(file_path)
        elif framework == 'iso27001':
            compliance_result = self.check_iso27001_compliance(file_path)
        elif framework == 'sox':
            compliance_result = self.check_sox_compliance(file_path)
        elif framework == 'pci':
            compliance_result = self.check_pci_compliance(file_path)
        
        return compliance_result

    def check_nist_compliance(self, file_path: Path) -> Dict:
        """Check NIST Cybersecurity Framework compliance"""
        result = {'compliant': True, 'score': 100, 'issues': []}
        
        # NIST guidelines for data retention and deletion
        try:
            file_age_days = (time.time() - file_path.stat().st_mtime) / (24 * 60 * 60)
            
            # Check if file contains sensitive data patterns
            if self.contains_sensitive_data(file_path):
                if file_age_days < 365:  # NIST recommends 1 year retention for sensitive data
                    result['compliant'] = False
                    result['issues'].append('Sensitive data with insufficient retention period')
                    result['score'] -= 50
        
        except Exception as e:
            result['issues'].append(f'Compliance check error: {e}')
            result['score'] -= 10
        
        return result

    def check_iso27001_compliance(self, file_path: Path) -> Dict:
        """Check ISO 27001 compliance"""
        result = {'compliant': True, 'score': 100, 'issues': []}
        
        # ISO 27001 information classification requirements
        if self.is_classified_information(file_path):
            result['compliant'] = False
            result['issues'].append('Classified information requires special handling')
            result['score'] -= 75
        
        return result

    def check_sox_compliance(self, file_path: Path) -> Dict:
        """Check SOX compliance for financial data"""
        result = {'compliant': True, 'score': 100, 'issues': []}
        
        # SOX requires 7-year retention for financial records
        if self.contains_financial_data(file_path):
            try:
                file_age_days = (time.time() - file_path.stat().st_mtime) / (24 * 60 * 60)
                if file_age_days < (7 * 365):  # 7 years
                    result['compliant'] = False
                    result['issues'].append('Financial data requires 7-year retention')
                    result['score'] -= 90
            except Exception:
                pass
        
        return result

    def check_pci_compliance(self, file_path: Path) -> Dict:
        """Check PCI DSS compliance"""
        result = {'compliant': True, 'score': 100, 'issues': []}
        
        # PCI DSS cardholder data protection
        if self.contains_cardholder_data(file_path):
            result['compliant'] = False
            result['issues'].append('Potential cardholder data found - requires secure deletion')
            result['score'] -= 100
        
        return result

    def contains_sensitive_data(self, file_path: Path) -> bool:
        """Check if file contains sensitive data patterns"""
        sensitive_patterns = [
            'password', 'secret', 'key', 'token', 'credential',
            'ssn', 'social security', 'passport', 'license',
            'confidential', 'restricted', 'classified'
        ]
        
        try:
            file_name = file_path.name.lower()
            parent_dir = file_path.parent.name.lower()
            
            return any(pattern in file_name or pattern in parent_dir for pattern in sensitive_patterns)
        except Exception:
            return False

    def is_classified_information(self, file_path: Path) -> bool:
        """Check if file contains classified information"""
        classification_markers = [
            'confidential', 'restricted', 'secret', 'top secret',
            'internal', 'proprietary', 'classified'
        ]
        
        try:
            file_content = str(file_path).lower()
            return any(marker in file_content for marker in classification_markers)
        except Exception:
            return False

    def contains_financial_data(self, file_path: Path) -> bool:
        """Check if file contains financial data"""
        financial_patterns = [
            'financial', 'accounting', 'revenue', 'expense',
            'invoice', 'payment', 'transaction', 'audit',
            'budget', 'cost', 'profit', 'loss'
        ]
        
        try:
            file_content = str(file_path).lower()
            return any(pattern in file_content for pattern in financial_patterns)
        except Exception:
            return False

    def contains_cardholder_data(self, file_path: Path) -> bool:
        """Check if file might contain cardholder data"""
        pci_patterns = [
            'card', 'credit', 'debit', 'payment', 'pan',
            'cardholder', 'cvv', 'expiry', 'visa', 'mastercard'
        ]
        
        try:
            file_content = str(file_path).lower()
            return any(pattern in file_content for pattern in pci_patterns)
        except Exception:
            return False

    def secure_delete_file(self, file_path: Path) -> bool:
        """Securely delete file with DOD 5220.22-M compliance"""
        try:
            if self.dry_run:
                self.logger.info(f"[DRY RUN] Would securely delete: {file_path}")
                return True
            
            file_size = file_path.stat().st_size
            
            # Multi-pass secure deletion
            with open(file_path, "r+b") as file:
                # Pass 1: Write zeros
                file.write(b'\x00' * file_size)
                file.flush()
                os.fsync(file.fileno())
                
                # Pass 2: Write ones
                file.seek(0)
                file.write(b'\xFF' * file_size)
                file.flush()
                os.fsync(file.fileno())
                
                # Pass 3: Write random data
                file.seek(0)
                import random
                random_data = bytes(random.getrandbits(8) for _ in range(file_size))
                file.write(random_data)
                file.flush()
                os.fsync(file.fileno())
            
            # Finally delete the file
            file_path.unlink()
            
            self.audit_logger.info(f"SECURE_DELETE: {file_path} - {file_size} bytes")
            return True
            
        except Exception as e:
            self.logger.error(f"Secure delete failed for {file_path}: {e}")
            self.audit_logger.error(f"SECURE_DELETE_FAILED: {file_path}: {e}")
            return False

    def backup_before_cleanup(self, directory: Path) -> Optional[Path]:
        """Create backup before cleanup operations"""
        try:
            if not self.config['security'].get('create_backup', False):
                return None
            
            backup_dir = Path('backups') / f"appdata_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            backup_dir.mkdir(parents=True, exist_ok=True)
            
            self.logger.info(f"Creating backup: {backup_dir}")
            
            # Use robocopy for efficient backup on Windows
            try:
                result = subprocess.run([
                    'robocopy', str(directory), str(backup_dir),
                    '/MIR', '/R:3', '/W:1', '/MT:8', '/LOG+:' + str(backup_dir / 'backup.log')
                ], capture_output=True, text=True, timeout=3600)
                
                if result.returncode < 8:  # Robocopy success codes
                    self.logger.info(f"Backup completed successfully: {backup_dir}")
                    return backup_dir
                else:
                    self.logger.error(f"Backup failed: {result.stderr}")
                    return None
                    
            except subprocess.TimeoutExpired:
                self.logger.error("Backup operation timed out")
                return None
            except FileNotFoundError:
                # Fallback to shutil if robocopy not available
                shutil.copytree(directory, backup_dir, dirs_exist_ok=True)
                self.logger.info(f"Backup completed using fallback method: {backup_dir}")
                return backup_dir
                
        except Exception as e:
            self.logger.error(f"Backup creation failed: {e}")
            return None

    def monitor_performance(self, operation: str, start_time: float):
        """Monitor and log performance metrics"""
        end_time = time.time()
        duration = end_time - start_time
        
        performance_metrics = {
            'operation': operation,
            'duration_seconds': duration,
            'timestamp': datetime.now().isoformat(),
            'hostname': self.results['hostname'],
            'user': self.results['user']
        }
        
        # Log performance metrics
        self.logger.info(f"Performance: {operation} completed in {duration:.2f} seconds")
        
        # Store in results for reporting
        if 'performance_metrics' not in self.results:
            self.results['performance_metrics'] = []
        self.results['performance_metrics'].append(performance_metrics)
        
        # Alert if operation takes too long
        if duration > self.config['deployment'].get('timeout_minutes', 30) * 60:
            self.logger.warning(f"Performance alert: {operation} took {duration:.2f} seconds")

    def check_disk_space(self, directory: Path) -> Dict:
        """Check available disk space before cleanup"""
        try:
            total, used, free = shutil.disk_usage(directory)
            
            space_info = {
                'total_gb': total / (1024**3),
                'used_gb': used / (1024**3),
                'free_gb': free / (1024**3),
                'usage_percent': (used / total) * 100
            }
            
            # Warn if disk usage is high
            if space_info['usage_percent'] > 90:
                self.logger.warning(f"High disk usage detected: {space_info['usage_percent']:.1f}%")
            
            return space_info
            
        except Exception as e:
            self.logger.error(f"Could not check disk space: {e}")
            return {}

    def analyze_cleanup_impact(self, scan_results: Dict) -> Dict:
        """Analyze the potential impact of cleanup operations"""
        impact_analysis = {
            'total_files_affected': len(scan_results['orphaned_files']),
            'total_size_affected': sum(f['size'] for f in scan_results['orphaned_files']),
            'risk_level': 'low',
            'recommendations': [],
            'warnings': []
        }
        
        # Calculate risk level based on various factors
        risk_score = 0
        
        # Check for sensitive data
        sensitive_files = [f for f in scan_results['orphaned_files'] 
                          if self.contains_sensitive_data(Path(f['path']))]
        if sensitive_files:
            risk_score += 50
            impact_analysis['warnings'].append(f"Found {len(sensitive_files)} files with potential sensitive data")
        
        # Check for recent files
        recent_files = [f for f in scan_results['orphaned_files']
                       if (time.time() - Path(f['path']).stat().st_mtime) < (7 * 24 * 60 * 60)]  # 7 days
        if recent_files:
            risk_score += 30
            impact_analysis['warnings'].append(f"Found {len(recent_files)} files modified in the last 7 days")
        
        # Check for large files
        large_files = [f for f in scan_results['orphaned_files'] if f['size'] > (100 * 1024 * 1024)]  # 100MB
        if large_files:
            risk_score += 20
            impact_analysis['warnings'].append(f"Found {len(large_files)} files larger than 100MB")
        
        # Determine risk level
        if risk_score >= 80:
            impact_analysis['risk_level'] = 'high'
        elif risk_score >= 50:
            impact_analysis['risk_level'] = 'medium'
        else:
            impact_analysis['risk_level'] = 'low'
        
        # Generate recommendations
        if impact_analysis['risk_level'] == 'high':
            impact_analysis['recommendations'].append("Review all files before deletion")
            impact_analysis['recommendations'].append("Consider running in dry-run mode first")
        
        if sensitive_files:
            impact_analysis['recommendations'].append("Implement secure deletion for sensitive files")
        
        return impact_analysis

    def create_restore_point(self) -> bool:
        """Create system restore point before cleanup"""
        try:
            if not self.config['security'].get('create_restore_point', False):
                return True
            
            self.logger.info("Creating system restore point...")
            
            # Use PowerShell to create restore point
            powershell_cmd = [
                'powershell', '-Command',
                'Checkpoint-Computer -Description "AppData Cleanup - ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '" -RestorePointType "MODIFY_SETTINGS"'
            ]
            
            result = subprocess.run(powershell_cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                self.logger.info("System restore point created successfully")
                return True
            else:
                self.logger.warning(f"Failed to create restore point: {result.stderr}")
                return False
                
        except Exception as e:
            self.logger.error(f"Restore point creation failed: {e}")
            return False

    def cleanup_appdata_directory(self, directory: Path = None) -> Dict:
        """Main method to clean AppData directory with enterprise considerations"""
        start_time = time.time()
        
        if directory is None:
            directory = Path(os.environ.get('APPDATA', ''))
        
        if not directory.exists():
            self.logger.error(f"AppData directory not found: {directory}")
            return {'error': f'Directory not found: {directory}'}
        
        self.logger.info(f"Starting enterprise AppData cleanup: {directory}")
        self.audit_logger.info(f"CLEANUP_START: {directory}")
        
        # Check disk space
        disk_space = self.check_disk_space(directory)
        
        # Create backup if configured
        backup_path = self.backup_before_cleanup(directory)
        
        # Create restore point if configured
        restore_point_created = self.create_restore_point()
        
        # Scan with compliance
        scan_results = self.scan_with_compliance(directory)
        
        # Analyze cleanup impact
        impact_analysis = self.analyze_cleanup_impact(scan_results)
        
        # Process orphaned files
        deleted_count = 0
        deleted_size = 0
        
        for orphaned_file in scan_results['orphaned_files']:
            file_path = Path(orphaned_file['path'])
            
            try:
                if self.secure_delete_file(file_path):
                    deleted_count += 1
                    deleted_size += orphaned_file['size']
                    
                    # Update results
                    self.results['deleted_files'].append({
                        'path': str(file_path),
                        'size': orphaned_file['size'],
                        'deleted_at': datetime.now().isoformat(),
                        'compliance_score': orphaned_file.get('compliance_score', 100)
                    })
                    self.results['deleted_size'] += orphaned_file['size']
                
            except Exception as e:
                error_msg = f"Failed to delete {file_path}: {e}"
                self.logger.error(error_msg)
                self.results['errors'].append({
                    'path': str(file_path),
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                })
        
        # Generate compliance report
        compliance_report = self.generate_compliance_report(scan_results)
        self.results['compliance_report'] = compliance_report
        
        # Send to SIEM if configured
        if self.config['security']['send_to_siem']:
            self.send_to_siem(scan_results)
        
        # Monitor performance
        self.monitor_performance('appdata_cleanup', start_time)
        
        # Generate final report
        final_report = {
            'cleanup_summary': {
                'directory': str(directory),
                'total_files_scanned': scan_results['total_files'],
                'total_size_scanned': scan_results['total_size'],
                'orphaned_files_found': len(scan_results['orphaned_files']),
                'protected_files_found': len(scan_results['protected_files']),
                'files_deleted': deleted_count,
                'size_freed': deleted_size,
                'compliance_issues': len(scan_results['compliance_issues']),
                'errors': len(scan_results['errors'])
            },
            'compliance_report': compliance_report,
            'security_events': scan_results['security_events'],
            'impact_analysis': impact_analysis,
            'disk_space': disk_space,
            'backup_path': str(backup_path) if backup_path else None,
            'restore_point_created': restore_point_created,
            'timestamp': datetime.now().isoformat()
        }
        
        self.logger.info(f"Cleanup completed: {deleted_count} files deleted, {deleted_size / (1024*1024):.2f}MB freed")
        self.audit_logger.info(f"CLEANUP_COMPLETE: {directory} - {deleted_count} files deleted")
        
        return final_report

    def generate_compliance_report(self, scan_results: Dict) -> Dict:
        """Generate comprehensive compliance report"""
        report = {
            'framework': self.security_context['framework'],
            'compliance_level': self.security_context['compliance_level'],
            'scan_timestamp': datetime.now().isoformat(),
            'overall_score': 100,
            'issues': [],
            'recommendations': []
        }
        
        # Calculate overall compliance score
        total_files = scan_results['total_files']
        if total_files > 0:
            compliant_files = total_files - len(scan_results['compliance_issues'])
            report['overall_score'] = (compliant_files / total_files) * 100
        
        # Add compliance issues
        for issue in scan_results['compliance_issues']:
            report['issues'].append({
                'path': issue['path'],
                'issues': issue['issues'],
                'severity': 'high' if 'sensitive' in str(issue['issues']).lower() else 'medium'
            })
        
        # Generate recommendations
        if report['overall_score'] < 90:
            report['recommendations'].append("Consider implementing stricter data retention policies")
        
        if len(scan_results['compliance_issues']) > 0:
            report['recommendations'].append("Review files with compliance issues before deletion")
        
        return report

    def send_to_siem(self, scan_results: Dict):
        """Send security events to SIEM system"""
        if not self.config['security']['siem_endpoint']:
            return
        
        try:
            siem_data = {
                'timestamp': datetime.now().isoformat(),
                'hostname': self.results['hostname'],
                'user': self.results['user'],
                'event_type': 'appdata_cleanup',
                'security_events': scan_results['security_events'],
                'compliance_issues': len(scan_results['compliance_issues']),
                'files_processed': scan_results['total_files']
            }
            
            if HAS_REQUESTS:
                response = requests.post(
                    self.config['security']['siem_endpoint'],
                    json=siem_data,
                    headers={'Content-Type': 'application/json'},
                    timeout=30
                )
                
                if response.status_code == 200:
                    self.logger.info("Security events sent to SIEM successfully")
                else:
                    self.logger.warning(f"SIEM submission failed: {response.status_code}")
            else:
                self.logger.warning("Requests library not available - cannot send to SIEM")
                
        except Exception as e:
            self.logger.error(f"SIEM submission error: {e}")

    def batch_deploy(self, target_hosts: List[str] = None) -> Dict:
        """Deploy cleanup to multiple hosts"""
        if not target_hosts:
            target_hosts = self.config['deployment']['target_hosts']
        
        if not target_hosts:
            self.logger.error("No target hosts specified for batch deployment")
            return {'error': 'No target hosts specified'}
        
        deployment_results = {
            'total_hosts': len(target_hosts),
            'successful': 0,
            'failed': 0,
            'results': []
        }
        
        self.logger.info(f"Starting batch deployment to {len(target_hosts)} hosts")
        
        # Use ThreadPoolExecutor for parallel deployment
        with ThreadPoolExecutor(max_workers=self.config['deployment']['parallel_threads']) as executor:
            future_to_host = {
                executor.submit(self.deploy_to_host, host): host 
                for host in target_hosts
            }
            
            for future in as_completed(future_to_host):
                host = future_to_host[future]
                try:
                    result = future.result(timeout=self.config['deployment']['timeout_minutes'] * 60)
                    deployment_results['results'].append({
                        'host': host,
                        'status': 'success',
                        'result': result
                    })
                    deployment_results['successful'] += 1
                except Exception as e:
                    deployment_results['results'].append({
                        'host': host,
                        'status': 'failed',
                        'error': str(e)
                    })
                    deployment_results['failed'] += 1
        
        self.logger.info(f"Batch deployment completed: {deployment_results['successful']} successful, {deployment_results['failed']} failed")
        return deployment_results

    def deploy_to_host(self, host: str) -> Dict:
        """Deploy cleanup to a single host"""
        try:
            # Check if it's a local deployment
            if host in ['localhost', '127.0.0.1', os.environ.get('COMPUTERNAME', '')]:
                return self.clean_appdata_directory()
            
            # Remote deployment using WinRM or SSH
            if self.config['deployment']['winrm_config']:
                return self.deploy_via_winrm(host)
            else:
                return self.deploy_via_ssh(host)
                
        except Exception as e:
            self.logger.error(f"Deployment to {host} failed: {e}")
            return {'error': str(e)}

    def deploy_via_winrm(self, host: str) -> Dict:
        """Deploy via Windows Remote Management"""
        try:
            # This would use pywinrm or similar library
            # For now, return a placeholder
            return {
                'host': host,
                'method': 'winrm',
                'status': 'not_implemented',
                'message': 'WinRM deployment not yet implemented'
            }
        except Exception as e:
            return {'error': f'WinRM deployment failed: {e}'}

    def deploy_via_ssh(self, host: str) -> Dict:
        """Deploy via SSH"""
        try:
            # This would use paramiko or similar library
            # For now, return a placeholder
            return {
                'host': host,
                'method': 'ssh',
                'status': 'not_implemented',
                'message': 'SSH deployment not yet implemented'
            }
        except Exception as e:
            return {'error': f'SSH deployment failed: {e}'}

    def generate_report(self, format: str = 'json') -> str:
        """Generate comprehensive report in specified format"""
        report_data = {
            'cleanup_summary': self.results,
            'security_context': self.security_context,
            'configuration': self.config,
            'timestamp': datetime.now().isoformat()
        }
        
        if format.lower() == 'json':
            return json.dumps(report_data, indent=2)
        elif format.lower() == 'yaml':
            return yaml.dump(report_data, default_flow_style=False)
        elif format.lower() == 'csv':
            return self.generate_csv_report(report_data)
        else:
            raise ValueError(f"Unsupported report format: {format}")

    def generate_csv_report(self, report_data: Dict) -> str:
        """Generate CSV report"""
        import csv
        from io import StringIO
        
        output = StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow(['File Path', 'Size (bytes)', 'Deleted At', 'Compliance Score', 'Error'])
        
        # Write data
        for deleted_file in report_data['cleanup_summary']['deleted_files']:
            writer.writerow([
                deleted_file['path'],
                deleted_file['size'],
                deleted_file['deleted_at'],
                deleted_file.get('compliance_score', 'N/A'),
                ''
            ])
        
        # Write errors
        for error in report_data['cleanup_summary']['errors']:
            writer.writerow([
                error['path'],
                '',
                error['timestamp'],
                '',
                error['error']
            ])
        
        return output.getvalue()

    def cleanup_old_logs(self, days: int = 30):
        """Clean up old log files"""
        log_dir = Path('logs')
        if not log_dir.exists():
            return
        
        cutoff_date = datetime.now() - timedelta(days=days)
        deleted_count = 0
        
        for log_file in log_dir.glob('*.log'):
            try:
                if datetime.fromtimestamp(log_file.stat().st_mtime) < cutoff_date:
                    log_file.unlink()
                    deleted_count += 1
            except Exception as e:
                self.logger.warning(f"Could not delete old log {log_file}: {e}")
        
        self.logger.info(f"Cleaned up {deleted_count} old log files")

    def validate_configuration(self) -> bool:
        """Validate current configuration"""
        errors = []
        
        # Check required fields
        required_fields = [
            'enterprise.organization',
            'security.require_elevation',
            'deployment.batch_size'
        ]
        
        for field in required_fields:
            keys = field.split('.')
            value = self.config
            for key in keys:
                if key not in value:
                    errors.append(f"Missing required configuration: {field}")
                    break
                value = value[key]
        
        # Check security settings
        if self.config['security']['require_elevation'] and not self.security_context['elevated']:
            errors.append("Administrative privileges required but not available")
        
        # Check deployment settings
        if self.config['deployment']['target_hosts'] and not self.config['deployment']['ssh_key_path']:
            errors.append("SSH key path required for remote deployment")
        
        if errors:
            for error in errors:
                self.logger.error(f"Configuration validation error: {error}")
            return False
        
        return True

    def run(self, directories: List[str] = None, batch_mode: bool = False) -> Dict:
        """Main execution method"""
        if not self.validate_configuration():
            return {'error': 'Configuration validation failed'}
        
        if batch_mode:
            return self.batch_deploy()
        
        if not directories:
            # Default to common AppData locations
            directories = [
                os.environ.get('APPDATA', ''),
                os.environ.get('LOCALAPPDATA', ''),
                os.path.join(os.environ.get('USERPROFILE', ''), 'AppData', 'Local', 'Temp')
            ]
        
        all_results = {
            'start_time': datetime.now().isoformat(),
            'directories_processed': [],
            'total_files_deleted': 0,
            'total_size_freed': 0,
            'errors': []
        }
        
        for directory in directories:
            if directory and Path(directory).exists():
                try:
                    result = self.clean_appdata_directory(Path(directory))
                    all_results['directories_processed'].append(result)
                    
                    if 'cleanup_summary' in result:
                        all_results['total_files_deleted'] += result['cleanup_summary']['files_deleted']
                        all_results['total_size_freed'] += result['cleanup_summary']['size_freed']
                    
                except Exception as e:
                    error_msg = f"Failed to process directory {directory}: {e}"
                    self.logger.error(error_msg)
                    all_results['errors'].append(error_msg)
        
        all_results['end_time'] = datetime.now().isoformat()
        
        # Generate final report
        report = self.generate_report('json')
        
        # Save report
        report_file = Path(f"cleanup_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(report_file, 'w') as f:
            f.write(report)
        
        self.logger.info(f"Cleanup completed. Report saved to: {report_file}")
        self.logger.info(f"Total files deleted: {all_results['total_files_deleted']}")
        self.logger.info(f"Total size freed: {all_results['total_size_freed'] / (1024*1024):.2f}MB")
        
        return all_results


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Enterprise AppData Deep Clean Suite",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --dry-run                    # Scan only, don't delete
  %(prog)s --config config.yaml         # Use custom configuration
  %(prog)s --batch --hosts hosts.txt    # Batch deployment
  %(prog)s --report-format yaml         # Generate YAML report
        """
    )
    
    parser.add_argument('--config', '-c', help='Configuration file path')
    parser.add_argument('--dry-run', '-n', action='store_true', help='Dry run mode (no deletion)')
    parser.add_argument('--batch', '-b', action='store_true', help='Batch deployment mode')
    parser.add_argument('--hosts', help='File containing target hosts for batch deployment')
    parser.add_argument('--directories', '-d', nargs='+', help='Specific directories to clean')
    parser.add_argument('--report-format', choices=['json', 'yaml', 'csv'], default='json', help='Report format')
    parser.add_argument('--clean-logs', type=int, metavar='DAYS', help='Clean logs older than DAYS')
    parser.add_argument('--validate', action='store_true', help='Validate configuration only')
    
    args = parser.parse_args()
    
    try:
        # Initialize cleaner
        cleaner = EnterpriseAppDataCleaner(
            config_file=args.config,
            dry_run=args.dry_run
        )
        
        if args.validate:
            if cleaner.validate_configuration():
                print("Configuration validation passed")
                return 0
            else:
                print("Configuration validation failed")
                return 1
        
        # Clean old logs if requested
        if args.clean_logs:
            cleaner.cleanup_old_logs(args.clean_logs)
            return 0
        
        # Load hosts for batch deployment
        target_hosts = []
        if args.batch and args.hosts:
            try:
                with open(args.hosts, 'r') as f:
                    target_hosts = [line.strip() for line in f if line.strip()]
            except Exception as e:
                print(f"Error loading hosts file: {e}")
                return 1
        
        # Run cleanup
        results = cleaner.run(
            directories=args.directories,
            batch_mode=args.batch
        )
        
        # Generate and display report
        report = cleaner.generate_report(args.report_format)
        print(report)
        
        return 0 if 'error' not in results else 1
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        return 1
    except Exception as e:
        print(f"Fatal error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())