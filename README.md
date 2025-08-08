# Enterprise AppData Deep Clean Suite

A production-ready, enterprise-grade Python tool for comprehensive AppData cleanup across multiple systems with advanced security, compliance, and monitoring capabilities.

## 🚀 Features

### Core Functionality
- **Intelligent File Detection**: Advanced algorithms to identify orphaned files while preserving enterprise software data
- **Secure Deletion**: DOD 5220.22-M compliant multi-pass secure deletion
- **Compliance Framework**: Built-in support for NIST, ISO 27001, SOX, and PCI DSS compliance
- **Enterprise Software Awareness**: Automatic detection and protection of enterprise applications
- **Batch Deployment**: Multi-host deployment with parallel processing
- **Comprehensive Reporting**: JSON, YAML, and CSV report formats

### Security & Compliance
- **Audit Trail**: Complete logging of all operations for compliance
- **SIEM Integration**: Real-time security event reporting
- **Backup & Restore**: Automatic backup creation and system restore points
- **Access Control**: Administrative privilege validation
- **Data Classification**: Automatic detection of sensitive data

### Enterprise Integration
- **Configuration Management**: Integration with Ansible, Puppet, Chef, and SaltStack
- **Performance Monitoring**: Real-time performance metrics and alerts
- **Disk Space Analysis**: Pre-cleanup disk space assessment
- **Impact Analysis**: Risk assessment and recommendations
- **Email Notifications**: Automated reporting and alerting

## 📋 Requirements

### System Requirements
- Windows 10/11 or Windows Server 2016+
- Python 3.8+
- Administrative privileges (for full functionality)
- 4GB RAM minimum (8GB recommended)
- 1GB free disk space

### Python Dependencies
```bash
pip install -r requirements.txt
```

**Core Dependencies:**
- `pyyaml` - YAML configuration support
- `psutil` - System and process utilities
- `wmi` - Windows Management Instrumentation
- `requests` - HTTP client for API integration

**Optional Dependencies:**
- `pywinrm` - Windows Remote Management
- `paramiko` - SSH client for remote deployment
- `cryptography` - Encryption support

## 🛠 Installation

### Quick Start
```bash
# Clone the repository
git clone https://github.com/your-org/enterprise-appdata-cleaner.git
cd enterprise-appdata-cleaner

# Install dependencies
pip install -r requirements.txt

# Run with default settings (dry-run mode)
python cleaner.py --dry-run
```

### Enterprise Deployment
1. **Configuration Setup**
   ```bash
   # Copy example configuration
   cp cleaner_config_example.yaml config.yaml
   
   # Edit configuration for your environment
   nano config.yaml
   ```

2. **Validate Configuration**
   ```bash
   python cleaner.py --config config.yaml --validate
   ```

3. **Test Run**
   ```bash
   python cleaner.py --config config.yaml --dry-run
   ```

## 📖 Usage

### Basic Usage

```bash
# Dry run (scan only, no deletion)
python cleaner.py --dry-run

# Clean specific directories
python cleaner.py --directories "C:\Users\Admin\AppData\Local\Temp" "C:\Users\Admin\AppData\Roaming\Temp"

# Use custom configuration
python cleaner.py --config config.yaml

# Generate YAML report
python cleaner.py --report-format yaml
```

### Enterprise Usage

```bash
# Batch deployment to multiple hosts
python cleaner.py --batch --hosts hosts.txt

# Clean old logs (older than 30 days)
python cleaner.py --clean-logs 30

# Validate configuration only
python cleaner.py --validate
```

### Command Line Options

| Option | Description | Example |
|--------|-------------|---------|
| `--config, -c` | Configuration file path | `--config config.yaml` |
| `--dry-run, -n` | Dry run mode (no deletion) | `--dry-run` |
| `--batch, -b` | Batch deployment mode | `--batch` |
| `--hosts` | File containing target hosts | `--hosts hosts.txt` |
| `--directories, -d` | Specific directories to clean | `--directories "C:\Temp"` |
| `--report-format` | Report format (json/yaml/csv) | `--report-format yaml` |
| `--clean-logs` | Clean logs older than N days | `--clean-logs 30` |
| `--validate` | Validate configuration only | `--validate` |

## 🔧 Configuration

### Configuration Structure

The configuration file supports the following sections:

#### Enterprise Settings
```yaml
enterprise:
  organization: "Your Company"
  environment: "production"
  compliance_level: "strict"
  security_framework: "nist"
  audit_required: true
```

#### Security Settings
```yaml
security:
  require_elevation: true
  audit_all_operations: true
  create_backup: true
  create_restore_point: true
  secure_deletion_passes: 3
```

#### Software Patterns
```yaml
software_patterns:
  protected_enterprise:
    - "microsoft"
    - "office"
    - "adobe"
  development_tools:
    - "vscode"
    - "intellij"
  safe_to_clean:
    - "temp"
    - "cache"
    - "logs"
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `CLEANER_CONFIG` | Configuration file path | `config.yaml` |
| `CLEANER_LOG_LEVEL` | Logging level | `INFO` |
| `CLEANER_DRY_RUN` | Enable dry-run mode | `false` |

## 📊 Reporting

### Report Formats

The tool generates comprehensive reports in multiple formats:

#### JSON Report
```json
{
  "cleanup_summary": {
    "directory": "C:\\Users\\Admin\\AppData",
    "total_files_scanned": 15420,
    "orphaned_files_found": 1234,
    "files_deleted": 1234,
    "size_freed": 2147483648
  },
  "compliance_report": {
    "framework": "nist",
    "overall_score": 95.2,
    "issues": []
  },
  "security_events": [],
  "timestamp": "2024-01-15T10:30:00"
}
```

#### CSV Report
```csv
File Path,Size (bytes),Deleted At,Compliance Score,Error
C:\Users\Admin\AppData\Local\Temp\file1.tmp,1024,2024-01-15T10:30:00,100,
C:\Users\Admin\AppData\Local\Temp\file2.tmp,2048,2024-01-15T10:30:01,100,
```

### Report Locations

- **Detailed Logs**: `logs/appdata_clean_detailed_YYYYMMDD_HHMMSS.log`
- **Audit Logs**: `logs/audit_YYYYMMDD.log`
- **Reports**: `cleanup_report_YYYYMMDD_HHMMSS.json`
- **Backups**: `backups/appdata_backup_YYYYMMDD_HHMMSS/`

## 🔒 Security Features

### Secure Deletion
- **Multi-pass deletion**: 3-pass secure deletion (zeros, ones, random data)
- **DOD 5220.22-M compliance**: Meets Department of Defense standards
- **Audit trail**: Complete logging of deletion operations

### Access Control
- **Administrative privileges**: Validates elevated permissions
- **Domain membership**: Checks for domain-joined systems
- **Security software detection**: Identifies installed security products

### Compliance Frameworks

#### NIST Cybersecurity Framework
- Data retention policies
- Secure deletion requirements
- Audit trail maintenance

#### ISO 27001
- Information classification
- Data protection requirements
- Risk assessment

#### SOX Compliance
- 7-year retention for financial data
- Audit log requirements
- Data integrity validation

#### PCI DSS
- Cardholder data protection
- Secure deletion requirements
- Audit frequency compliance

## 🚀 Enterprise Deployment

### Batch Deployment

1. **Prepare Host List**
   ```bash
   # Create hosts.txt file
   echo "host1.company.com" > hosts.txt
   echo "host2.company.com" >> hosts.txt
   echo "host3.company.com" >> hosts.txt
   ```

2. **Run Batch Deployment**
   ```bash
   python cleaner.py --batch --hosts hosts.txt --config config.yaml
   ```

### Configuration Management Integration

#### Ansible Integration
```yaml
config_management:
  type: "ansible"
  server: "ansible.company.com"
  playbook_path: "/opt/ansible/playbooks/appdata_cleanup.yml"
  inventory_path: "/opt/ansible/inventory/hosts"
```

#### Puppet Integration
```yaml
config_management:
  type: "puppet"
  server: "puppet.company.com"
  cert_path: "/etc/puppetlabs/puppet/ssl/certs"
```

### Monitoring and Alerting

#### SIEM Integration
```yaml
security:
  send_to_siem: true
  siem_endpoint: "https://siem.company.com/api/events"
```

#### Performance Monitoring
```yaml
monitoring:
  enabled: true
  metrics_endpoint: "https://metrics.company.com/api/v1/write"
  alert_thresholds:
    files_deleted_percent: 50
    disk_space_freed_gb: 10
```

## 🐛 Troubleshooting

### Common Issues

#### Permission Denied
```bash
# Run as administrator
# Right-click PowerShell/Command Prompt and select "Run as administrator"
python cleaner.py --dry-run
```

#### Configuration Errors
```bash
# Validate configuration
python cleaner.py --validate

# Check configuration syntax
python -c "import yaml; yaml.safe_load(open('config.yaml'))"
```

#### Network Issues
```bash
# Test connectivity
ping siem.company.com
curl -k https://siem.company.com/api/health
```

### Log Analysis

#### Check Detailed Logs
```bash
# View latest detailed log
Get-Content logs/appdata_clean_detailed_*.log | Select-Object -Last 50
```

#### Check Audit Logs
```bash
# View audit events
Get-Content logs/audit_*.log | Where-Object { $_ -match "SECURE_DELETE" }
```

## 📈 Performance

### Optimization Tips

1. **Parallel Processing**: Adjust `parallel_threads` in configuration
2. **Batch Size**: Optimize `batch_size` for your environment
3. **Timeout Settings**: Increase `timeout_minutes` for large directories
4. **Memory Usage**: Monitor memory usage during large operations

### Performance Metrics

| Metric | Typical Value | Notes |
|--------|---------------|-------|
| Files per second | 100-500 | Depends on file size and disk speed |
| Memory usage | 100-500MB | Varies with directory size |
| CPU usage | 20-80% | Multi-threaded operations |
| Disk I/O | 50-200MB/s | Secure deletion operations |

## 🤝 Contributing

### Development Setup

1. **Fork the repository**
2. **Create feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make changes and test**
   ```bash
   python cleaner.py --dry-run --config test_config.yaml
   ```
4. **Submit pull request**

### Code Standards

- Follow PEP 8 style guidelines
- Add type hints for all functions
- Include docstrings for all methods
- Write unit tests for new features

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

### Documentation
- [User Guide](docs/user-guide.md)
- [API Reference](docs/api-reference.md)
- [Configuration Guide](docs/configuration.md)

### Community
- [Issues](https://github.com/your-org/enterprise-appdata-cleaner/issues)
- [Discussions](https://github.com/your-org/enterprise-appdata-cleaner/discussions)
- [Wiki](https://github.com/your-org/enterprise-appdata-cleaner/wiki)

### Enterprise Support
For enterprise support and custom development:
- Email: enterprise-support@company.com
- Phone: +1-555-123-4567
- SLA: 24/7 support available

## 🔄 Version History

### v1.0.0 (2024-01-15)
- Initial release
- Core cleanup functionality
- Enterprise software detection
- Compliance framework support
- Secure deletion implementation

### v1.1.0 (2024-02-01)
- Added batch deployment
- Enhanced reporting
- Performance monitoring
- SIEM integration

### v1.2.0 (2024-03-01)
- Configuration management integration
- Advanced compliance features
- Backup and restore functionality
- Enhanced security features 