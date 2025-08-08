# Windows Executable - Technical Specification

## 🎯 Project Overview

Create a native Windows executable application that provides a modern, user-friendly interface for the enterprise AppData cleaner script, packaged as a standalone .exe file using PyInstaller.

---

## 🏗️ Technical Architecture

### **Tech Stack**
- **Language**: Python 3.8+
- **GUI Framework**: PyQt6 (Professional, feature-rich)
- **Packaging**: PyInstaller
- **Configuration**: YAML + JSON
- **Logging**: Structured logging with file rotation
- **Database**: SQLite (local storage)
- **Testing**: pytest + pytest-qt
- **CI/CD**: GitHub Actions

### **Project Structure**
```
enterprise-appdata-cleaner-exe/
├── src/
│   ├── main.py                 # Application entry point
│   ├── gui/
│   │   ├── main_window.py      # Main application window
│   │   ├── dialogs/
│   │   │   ├── config_dialog.py
│   │   │   ├── scan_dialog.py
│   │   │   ├── report_dialog.py
│   │   │   └── about_dialog.py
│   │   ├── widgets/
│   │   │   ├── directory_tree.py
│   │   │   ├── progress_bar.py
│   │   │   ├── status_panel.py
│   │   │   ├── log_viewer.py
│   │   │   └── metrics_display.py
│   │   ├── resources/
│   │   │   ├── icons/
│   │   │   │   ├── app.ico
│   │   │   │   ├── folder.ico
│   │   │   │   ├── file.ico
│   │   │   │   └── settings.ico
│   │   │   ├── styles/
│   │   │   │   ├── main.qss
│   │   │   │   └── dark.qss
│   │   │   └── templates/
│   │   │       ├── config_template.yaml
│   │   │       └── report_template.html
│   │   └── utils/
│   │       ├── qt_helpers.py
│   │       ├── validators.py
│   │       └── formatters.py
│   ├── core/
│   │   ├── cleaner_wrapper.py  # Python script wrapper
│   │   ├── config_manager.py   # Configuration management
│   │   ├── report_generator.py # Report generation
│   │   ├── system_monitor.py   # System monitoring
│   │   └── database.py         # Local database
│   ├── utils/
│   │   ├── file_utils.py
│   │   ├── validation.py
│   │   ├── logging.py
│   │   └── security.py
│   └── resources/
│       ├── configs/
│       ├── templates/
│       └── assets/
├── build/
│   ├── spec/
│   │   └── app.spec
│   ├── dist/
│   └── build/
├── tests/
│   ├── test_gui/
│   ├── test_core/
│   └── test_utils/
├── docs/
│   ├── user_guide.md
│   ├── developer_guide.md
│   └── api_reference.md
├── requirements/
│   ├── requirements.txt
│   └── requirements-dev.txt
└── scripts/
    ├── build.bat
    ├── test.bat
    └── package.bat
```

---

## 🎨 GUI Design & Implementation

### **Main Window Design**
```python
# src/gui/main_window.py
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QStatusBar, QMenuBar, QToolBar
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QIcon, QAction

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Enterprise AppData Cleaner")
        self.setWindowIcon(QIcon(":/icons/app.ico"))
        self.setMinimumSize(1200, 800)
        
        # Initialize components
        self.init_ui()
        self.init_menu()
        self.init_toolbar()
        self.init_statusbar()
        
        # Setup timers
        self.setup_timers()
        
        # Load initial state
        self.load_initial_state()
    
    def init_ui(self):
        """Initialize the main UI components"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        layout = QVBoxLayout(central_widget)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabPosition(QTabWidget.TabPosition.North)
        
        # Add tabs
        self.dashboard_tab = DashboardTab()
        self.cleanup_tab = CleanupTab()
        self.reports_tab = ReportsTab()
        self.settings_tab = SettingsTab()
        
        self.tab_widget.addTab(self.dashboard_tab, "Dashboard")
        self.tab_widget.addTab(self.cleanup_tab, "Cleanup")
        self.tab_widget.addTab(self.reports_tab, "Reports")
        self.tab_widget.addTab(self.settings_tab, "Settings")
        
        layout.addWidget(self.tab_widget)
    
    def init_menu(self):
        """Initialize the menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("&File")
        
        new_action = QAction("&New Configuration", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.new_configuration)
        file_menu.addAction(new_action)
        
        open_action = QAction("&Open Configuration", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_configuration)
        file_menu.addAction(open_action)
        
        save_action = QAction("&Save Configuration", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_configuration)
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Tools menu
        tools_menu = menubar.addMenu("&Tools")
        
        scan_action = QAction("&Scan Directories", self)
        scan_action.setShortcut("F5")
        scan_action.triggered.connect(self.scan_directories)
        tools_menu.addAction(scan_action)
        
        cleanup_action = QAction("&Execute Cleanup", self)
        cleanup_action.setShortcut("F6")
        cleanup_action.triggered.connect(self.execute_cleanup)
        tools_menu.addAction(cleanup_action)
        
        # Help menu
        help_menu = menubar.addMenu("&Help")
        
        about_action = QAction("&About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def init_toolbar(self):
        """Initialize the toolbar"""
        toolbar = self.addToolBar("Main Toolbar")
        toolbar.setMovable(False)
        
        # Add toolbar actions
        toolbar.addAction(QIcon(":/icons/scan.ico"), "Scan", self.scan_directories)
        toolbar.addAction(QIcon(":/icons/cleanup.ico"), "Cleanup", self.execute_cleanup)
        toolbar.addSeparator()
        toolbar.addAction(QIcon(":/icons/settings.ico"), "Settings", self.show_settings)
        toolbar.addAction(QIcon(":/icons/help.ico"), "Help", self.show_help)
    
    def init_statusbar(self):
        """Initialize the status bar"""
        self.statusbar = self.statusBar()
        
        # Add status indicators
        self.status_label = QLabel("Ready")
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        
        self.statusbar.addWidget(self.status_label)
        self.statusbar.addPermanentWidget(self.progress_bar)
    
    def setup_timers(self):
        """Setup application timers"""
        # System monitoring timer
        self.system_timer = QTimer()
        self.system_timer.timeout.connect(self.update_system_info)
        self.system_timer.start(5000)  # Update every 5 seconds
        
        # Status update timer
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.update_status)
        self.status_timer.start(1000)  # Update every second
```

### **Dashboard Tab**
```python
# src/gui/widgets/dashboard_tab.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QProgressBar, QFrame, QPushButton
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QPalette

class DashboardTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_data()
    
    def init_ui(self):
        """Initialize the dashboard UI"""
        layout = QVBoxLayout(self)
        
        # Header
        header = QLabel("System Overview")
        header.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        layout.addWidget(header)
        
        # Metrics grid
        metrics_layout = QGridLayout()
        
        # System health
        self.health_card = MetricCard("System Health", "95%", "Good")
        metrics_layout.addWidget(self.health_card, 0, 0)
        
        # Disk usage
        self.disk_card = MetricCard("Disk Usage", "67%", "Moderate")
        metrics_layout.addWidget(self.disk_card, 0, 1)
        
        # Files cleaned
        self.files_card = MetricCard("Files Cleaned", "1,234", "Today")
        metrics_layout.addWidget(self.files_card, 0, 2)
        
        # Space freed
        self.space_card = MetricCard("Space Freed", "2.5 GB", "Total")
        metrics_layout.addWidget(self.space_card, 0, 3)
        
        layout.addLayout(metrics_layout)
        
        # Quick actions
        actions_layout = QHBoxLayout()
        
        scan_btn = QPushButton("Quick Scan")
        scan_btn.clicked.connect(self.quick_scan)
        actions_layout.addWidget(scan_btn)
        
        cleanup_btn = QPushButton("Quick Cleanup")
        cleanup_btn.clicked.connect(self.quick_cleanup)
        actions_layout.addWidget(cleanup_btn)
        
        report_btn = QPushButton("Generate Report")
        report_btn.clicked.connect(self.generate_report)
        actions_layout.addWidget(report_btn)
        
        layout.addLayout(actions_layout)
        
        # Recent activity
        self.activity_widget = RecentActivityWidget()
        layout.addWidget(self.activity_widget)
    
    def load_data(self):
        """Load dashboard data"""
        # Load system information
        system_info = self.get_system_info()
        self.update_metrics(system_info)
        
        # Load recent activity
        self.activity_widget.load_activity()
    
    def update_metrics(self, system_info):
        """Update dashboard metrics"""
        self.health_card.update_value(f"{system_info['health']}%")
        self.disk_card.update_value(f"{system_info['disk_usage']}%")
        self.files_card.update_value(f"{system_info['files_cleaned']:,}")
        self.space_card.update_value(f"{system_info['space_freed']:.1f} GB")

class MetricCard(QFrame):
    def __init__(self, title, value, subtitle):
        super().__init__()
        self.setFrameStyle(QFrame.Shape.StyledPanel)
        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 16px;
            }
        """)
        
        layout = QVBoxLayout(self)
        
        # Title
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 10))
        title_label.setStyleSheet("color: #666;")
        layout.addWidget(title_label)
        
        # Value
        self.value_label = QLabel(value)
        self.value_label.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        self.value_label.setStyleSheet("color: #2563eb;")
        layout.addWidget(self.value_label)
        
        # Subtitle
        subtitle_label = QLabel(subtitle)
        subtitle_label.setFont(QFont("Arial", 9))
        subtitle_label.setStyleSheet("color: #999;")
        layout.addWidget(subtitle_label)
    
    def update_value(self, value):
        """Update the metric value"""
        self.value_label.setText(value)
```

### **Cleanup Tab**
```python
# src/gui/widgets/cleanup_tab.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QTreeWidget, QTreeWidgetItem, QTextEdit, QPushButton,
    QProgressBar, QLabel, QGroupBox, QCheckBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal

class CleanupTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setup_connections()
    
    def init_ui(self):
        """Initialize the cleanup UI"""
        layout = QVBoxLayout(self)
        
        # Top controls
        controls_layout = QHBoxLayout()
        
        self.scan_btn = QPushButton("Scan Directories")
        self.scan_btn.clicked.connect(self.scan_directories)
        controls_layout.addWidget(self.scan_btn)
        
        self.cleanup_btn = QPushButton("Execute Cleanup")
        self.cleanup_btn.clicked.connect(self.execute_cleanup)
        self.cleanup_btn.setEnabled(False)
        controls_layout.addWidget(self.cleanup_btn)
        
        self.stop_btn = QPushButton("Stop")
        self.stop_btn.clicked.connect(self.stop_operation)
        self.stop_btn.setEnabled(False)
        controls_layout.addWidget(self.stop_btn)
        
        controls_layout.addStretch()
        
        layout.addLayout(controls_layout)
        
        # Main content area
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left panel - Directory tree
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        left_layout.addWidget(QLabel("Directories"))
        
        self.directory_tree = DirectoryTreeWidget()
        self.directory_tree.itemChanged.connect(self.on_directory_selection_changed)
        left_layout.addWidget(self.directory_tree)
        
        splitter.addWidget(left_panel)
        
        # Right panel - Details and progress
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # Configuration group
        config_group = QGroupBox("Configuration")
        config_layout = QVBoxLayout(config_group)
        
        self.dry_run_cb = QCheckBox("Dry Run (No deletion)")
        self.dry_run_cb.setChecked(True)
        config_layout.addWidget(self.dry_run_cb)
        
        self.backup_cb = QCheckBox("Create backup before cleanup")
        self.backup_cb.setChecked(True)
        config_layout.addWidget(self.backup_cb)
        
        self.secure_delete_cb = QCheckBox("Secure deletion")
        config_layout.addWidget(self.secure_delete_cb)
        
        right_layout.addWidget(config_group)
        
        # Progress group
        progress_group = QGroupBox("Progress")
        progress_layout = QVBoxLayout(progress_group)
        
        self.progress_bar = QProgressBar()
        progress_layout.addWidget(self.progress_bar)
        
        self.status_label = QLabel("Ready")
        progress_layout.addWidget(self.status_label)
        
        right_layout.addWidget(progress_group)
        
        # Log viewer
        log_group = QGroupBox("Log")
        log_layout = QVBoxLayout(log_group)
        
        self.log_viewer = QTextEdit()
        self.log_viewer.setMaximumHeight(200)
        log_layout.addWidget(self.log_viewer)
        
        right_layout.addWidget(log_group)
        
        splitter.addWidget(right_panel)
        
        # Set splitter proportions
        splitter.setSizes([400, 600])
        
        layout.addWidget(splitter)
    
    def setup_connections(self):
        """Setup signal connections"""
        # Connect to cleaner wrapper
        self.cleaner_wrapper = CleanerWrapper()
        self.cleaner_wrapper.progress_updated.connect(self.update_progress)
        self.cleaner_wrapper.status_updated.connect(self.update_status)
        self.cleaner_wrapper.log_updated.connect(self.update_log)
        self.cleaner_wrapper.finished.connect(self.on_operation_finished)
    
    def scan_directories(self):
        """Scan selected directories"""
        selected_directories = self.directory_tree.get_selected_directories()
        
        if not selected_directories:
            self.show_message("Please select directories to scan")
            return
        
        self.scan_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.status_label.setText("Scanning directories...")
        
        # Start scan in background thread
        self.cleaner_wrapper.scan_directories(selected_directories)
    
    def execute_cleanup(self):
        """Execute cleanup operation"""
        if not hasattr(self, 'scan_results'):
            self.show_message("Please scan directories first")
            return
        
        # Get configuration
        config = {
            'dry_run': self.dry_run_cb.isChecked(),
            'create_backup': self.backup_cb.isChecked(),
            'secure_deletion': self.secure_delete_cb.isChecked(),
        }
        
        self.cleanup_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.status_label.setText("Executing cleanup...")
        
        # Start cleanup in background thread
        self.cleaner_wrapper.execute_cleanup(self.scan_results, config)
    
    def update_progress(self, value, maximum):
        """Update progress bar"""
        self.progress_bar.setMaximum(maximum)
        self.progress_bar.setValue(value)
    
    def update_status(self, status):
        """Update status label"""
        self.status_label.setText(status)
    
    def update_log(self, message):
        """Update log viewer"""
        self.log_viewer.append(message)
        # Auto-scroll to bottom
        self.log_viewer.verticalScrollBar().setValue(
            self.log_viewer.verticalScrollBar().maximum()
        )
    
    def on_operation_finished(self, results):
        """Handle operation completion"""
        self.scan_btn.setEnabled(True)
        self.cleanup_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        
        if results.get('success'):
            self.status_label.setText("Operation completed successfully")
            self.show_message("Operation completed successfully", "Success")
        else:
            self.status_label.setText("Operation failed")
            self.show_message(f"Operation failed: {results.get('error')}", "Error")

class DirectoryTreeWidget(QTreeWidget):
    def __init__(self):
        super().__init__()
        self.setHeaderLabel("Directories")
        self.setColumnCount(2)
        self.setHeaderLabels(["Directory", "Size"])
        
        # Load directories
        self.load_directories()
    
    def load_directories(self):
        """Load system directories"""
        # Common AppData directories
        directories = [
            ("AppData\\Local", "C:\\Users\\%USERNAME%\\AppData\\Local"),
            ("AppData\\Roaming", "C:\\Users\\%USERNAME%\\AppData\\Roaming"),
            ("AppData\\LocalLow", "C:\\Users\\%USERNAME%\\AppData\\LocalLow"),
            ("Temp", "C:\\Users\\%USERNAME%\\AppData\\Local\\Temp"),
            ("Windows Temp", "C:\\Windows\\Temp"),
        ]
        
        for name, path in directories:
            item = QTreeWidgetItem(self)
            item.setText(0, name)
            item.setText(1, "Calculating...")
            item.setCheckState(0, Qt.CheckState.Unchecked)
            
            # Load directory size in background
            self.load_directory_size(item, path)
    
    def load_directory_size(self, item, path):
        """Load directory size in background"""
        # This would be implemented with a background thread
        pass
    
    def get_selected_directories(self):
        """Get selected directories"""
        selected = []
        for i in range(self.topLevelItemCount()):
            item = self.topLevelItem(i)
            if item.checkState(0) == Qt.CheckState.Checked:
                selected.append(item.text(1))
        return selected
```

---

## 🔧 Core Integration

### **Cleaner Wrapper**
```python
# src/core/cleaner_wrapper.py
import subprocess
import json
import threading
from pathlib import Path
from PyQt6.QtCore import QObject, pyqtSignal

class CleanerWrapper(QObject):
    progress_updated = pyqtSignal(int, int)  # value, maximum
    status_updated = pyqtSignal(str)
    log_updated = pyqtSignal(str)
    finished = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.cleaner_script = Path(__file__).parent.parent.parent / "cleaner.py"
        self.current_process = None
        self.is_running = False
    
    def scan_directories(self, directories):
        """Scan directories using the cleaner script"""
        if self.is_running:
            return
        
        self.is_running = True
        
        # Start scan in background thread
        thread = threading.Thread(
            target=self._run_scan,
            args=(directories,)
        )
        thread.daemon = True
        thread.start()
    
    def _run_scan(self, directories):
        """Run scan operation"""
        try:
            cmd = [
                "python",
                str(self.cleaner_script),
                "--scan",
                "--directories"
            ] + directories + ["--dry-run"]
            
            self.current_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # Monitor output
            while True:
                output = self.current_process.stdout.readline()
                if output == '' and self.current_process.poll() is not None:
                    break
                if output:
                    self.log_updated.emit(output.strip())
                    
                    # Parse progress from output
                    if "Progress:" in output:
                        try:
                            progress = self._parse_progress(output)
                            self.progress_updated.emit(progress['current'], progress['total'])
                        except:
                            pass
            
            # Get results
            return_code = self.current_process.poll()
            
            if return_code == 0:
                # Parse scan results
                results = self._parse_scan_results()
                self.finished.emit({"success": True, "results": results})
            else:
                error_output = self.current_process.stderr.read()
                self.finished.emit({"success": False, "error": error_output})
                
        except Exception as e:
            self.finished.emit({"success": False, "error": str(e)})
        finally:
            self.is_running = False
            self.current_process = None
    
    def execute_cleanup(self, scan_results, config):
        """Execute cleanup operation"""
        if self.is_running:
            return
        
        self.is_running = True
        
        # Start cleanup in background thread
        thread = threading.Thread(
            target=self._run_cleanup,
            args=(scan_results, config)
        )
        thread.daemon = True
        thread.start()
    
    def _run_cleanup(self, scan_results, config):
        """Run cleanup operation"""
        try:
            cmd = [
                "python",
                str(self.cleaner_script),
                "--execute",
                "--config", json.dumps(config)
            ]
            
            self.current_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # Monitor output (similar to scan)
            while True:
                output = self.current_process.stdout.readline()
                if output == '' and self.current_process.poll() is not None:
                    break
                if output:
                    self.log_updated.emit(output.strip())
                    
                    # Parse progress
                    if "Progress:" in output:
                        try:
                            progress = self._parse_progress(output)
                            self.progress_updated.emit(progress['current'], progress['total'])
                        except:
                            pass
            
            return_code = self.current_process.poll()
            
            if return_code == 0:
                results = self._parse_cleanup_results()
                self.finished.emit({"success": True, "results": results})
            else:
                error_output = self.current_process.stderr.read()
                self.finished.emit({"success": False, "error": error_output})
                
        except Exception as e:
            self.finished.emit({"success": False, "error": str(e)})
        finally:
            self.is_running = False
            self.current_process = None
    
    def stop_operation(self):
        """Stop current operation"""
        if self.current_process and self.is_running:
            self.current_process.terminate()
            self.is_running = False
    
    def _parse_progress(self, output):
        """Parse progress from output"""
        # Implementation to parse progress information
        pass
    
    def _parse_scan_results(self):
        """Parse scan results"""
        # Implementation to parse scan results
        pass
    
    def _parse_cleanup_results(self):
        """Parse cleanup results"""
        # Implementation to parse cleanup results
        pass
```

---

## 📦 Packaging Configuration

### **PyInstaller Specification**
```python
# build/spec/app.spec
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['src/main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('src/gui/resources', 'gui/resources'),
        ('cleaner.py', '.'),
        ('cleaner_config_example.yaml', '.'),
        ('requirements.txt', '.'),
    ],
    hiddenimports=[
        'yaml',
        'psutil',
        'wmi',
        'requests',
        'json',
        'pathlib',
        'datetime',
        'threading',
        'subprocess',
        'sqlite3',
        'PyQt6',
        'PyQt6.QtCore',
        'PyQt6.QtWidgets',
        'PyQt6.QtGui',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='EnterpriseAppDataCleaner',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='src/gui/resources/icons/app.ico',
    version='version_info.txt',
)
```

### **Version Information**
```text
# version_info.txt
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 2, 0, 0),
    prodvers=(1, 2, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo([
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'Enterprise AppData Cleaner Team'),
         StringStruct(u'FileDescription', u'Enterprise AppData Deep Clean Suite'),
         StringStruct(u'FileVersion', u'1.2.0'),
         StringStruct(u'InternalName', u'EnterpriseAppDataCleaner'),
         StringStruct(u'LegalCopyright', u'Copyright (c) 2024'),
         StringStruct(u'OriginalFilename', u'EnterpriseAppDataCleaner.exe'),
         StringStruct(u'ProductName', u'Enterprise AppData Cleaner'),
         StringStruct(u'ProductVersion', u'1.2.0')])
    ]),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
```

---

## 🧪 Testing Strategy

### **Unit Tests**
```python
# tests/test_gui/test_main_window.py
import pytest
from PyQt6.QtWidgets import QApplication
from PyQt6.QtTest import QTest
from PyQt6.QtCore import Qt

from src.gui.main_window import MainWindow

@pytest.fixture
def app():
    """Create QApplication instance"""
    return QApplication([])

@pytest.fixture
def window(app):
    """Create MainWindow instance"""
    return MainWindow()

def test_main_window_creation(window):
    """Test main window creation"""
    assert window is not None
    assert window.windowTitle() == "Enterprise AppData Cleaner"

def test_tab_widget_creation(window):
    """Test tab widget creation"""
    assert window.tab_widget is not None
    assert window.tab_widget.count() == 4
    
    # Check tab names
    tab_names = ["Dashboard", "Cleanup", "Reports", "Settings"]
    for i, name in enumerate(tab_names):
        assert window.tab_widget.tabText(i) == name

def test_menu_creation(window):
    """Test menu creation"""
    menubar = window.menuBar()
    assert menubar is not None
    
    # Check menu items
    file_menu = menubar.findChild(QMenu, "File")
    assert file_menu is not None
    
    # Check menu actions
    actions = file_menu.actions()
    action_names = [action.text() for action in actions]
    assert "New Configuration" in action_names
    assert "Open Configuration" in action_names
    assert "Save Configuration" in action_names
    assert "Exit" in action_names

def test_toolbar_creation(window):
    """Test toolbar creation"""
    toolbars = window.findChildren(QToolBar)
    assert len(toolbars) > 0
    
    main_toolbar = toolbars[0]
    assert main_toolbar is not None
    
    # Check toolbar actions
    actions = main_toolbar.actions()
    assert len(actions) > 0

def test_statusbar_creation(window):
    """Test status bar creation"""
    statusbar = window.statusBar()
    assert statusbar is not None
    
    # Check status label
    status_label = statusbar.findChild(QLabel)
    assert status_label is not None
    assert status_label.text() == "Ready"
```

### **Integration Tests**
```python
# tests/test_integration/test_cleanup_flow.py
import pytest
import tempfile
import os
from pathlib import Path

from src.core.cleaner_wrapper import CleanerWrapper

class TestCleanupFlow:
    def test_scan_directories(self):
        """Test directory scanning"""
        wrapper = CleanerWrapper()
        
        # Create test directories
        with tempfile.TemporaryDirectory() as temp_dir:
            test_dirs = [
                os.path.join(temp_dir, "test1"),
                os.path.join(temp_dir, "test2")
            ]
            
            for dir_path in test_dirs:
                os.makedirs(dir_path)
                # Create some test files
                with open(os.path.join(dir_path, "test.txt"), "w") as f:
                    f.write("test content")
            
            # Test scan
            results = wrapper.scan_directories(test_dirs)
            assert results is not None
            assert "files_found" in results
    
    def test_cleanup_execution(self):
        """Test cleanup execution"""
        wrapper = CleanerWrapper()
        
        # Mock scan results
        scan_results = {
            "files_found": 10,
            "total_size": 1024,
            "directories": ["test_dir"]
        }
        
        config = {
            "dry_run": True,
            "create_backup": False,
            "secure_deletion": False
        }
        
        # Test cleanup
        results = wrapper.execute_cleanup(scan_results, config)
        assert results is not None
        assert "success" in results
```

---

## 🚀 Deployment Strategy

### **Build Script**
```batch
@echo off
REM build.bat - Build executable

echo Building Enterprise AppData Cleaner...

REM Set environment variables
set PYTHONPATH=%CD%
set BUILD_DIR=build
set DIST_DIR=%BUILD_DIR%\dist

REM Create build directories
if not exist %BUILD_DIR% mkdir %BUILD_DIR%
if not exist %DIST_DIR% mkdir %DIST_DIR%

REM Install dependencies
echo Installing dependencies...
pip install -r requirements/requirements.txt

REM Run tests
echo Running tests...
python -m pytest tests/ -v

REM Build executable
echo Building executable...
pyinstaller build/spec/app.spec --distpath %DIST_DIR% --workpath %BUILD_DIR%\build

REM Copy additional files
echo Copying additional files...
copy README.md %DIST_DIR%\
copy LICENSE %DIST_DIR%\
copy CHANGELOG.md %DIST_DIR%\

REM Create installer
echo Creating installer...
iscc installer.iss

echo Build completed successfully!
echo Executable location: %DIST_DIR%\EnterpriseAppDataCleaner.exe
```

### **Inno Setup Script**
```inno
; installer.iss - Inno Setup script

[Setup]
AppName=Enterprise AppData Cleaner
AppVersion=1.2.0
AppPublisher=Enterprise AppData Cleaner Team
AppPublisherURL=https://github.com/tonycondone/enterprise-appdata-cleaner
AppSupportURL=https://github.com/tonycondone/enterprise-appdata-cleaner/issues
AppUpdatesURL=https://github.com/tonycondone/enterprise-appdata-cleaner/releases
DefaultDirName={autopf}\EnterpriseAppDataCleaner
DefaultGroupName=Enterprise AppData Cleaner
AllowNoIcons=yes
LicenseFile=LICENSE
OutputDir=build\installer
OutputBaseFilename=EnterpriseAppDataCleaner-Setup-1.2.0
SetupIconFile=src\gui\resources\icons\app.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "build\dist\EnterpriseAppDataCleaner.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "build\dist\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\Enterprise AppData Cleaner"; Filename: "{app}\EnterpriseAppDataCleaner.exe"
Name: "{group}\{cm:UninstallProgram,Enterprise AppData Cleaner}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\Enterprise AppData Cleaner"; Filename: "{app}\EnterpriseAppDataCleaner.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\EnterpriseAppDataCleaner.exe"; Description: "{cm:LaunchProgram,Enterprise AppData Cleaner}"; Flags: nowait postinstall skipifsilent
```

This comprehensive specification provides a detailed roadmap for building a professional Windows executable application around your enterprise AppData cleaner. 