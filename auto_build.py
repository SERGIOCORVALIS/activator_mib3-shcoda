#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fully automated script for LG MEN3 Activator
Updates checksums, bypasses signature verification and verifies result
"""

import os
import sys
import json
import hashlib
import shutil
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional

# Colors for output (Windows and Linux support)
try:
    import colorama
    colorama.init()
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
except ImportError:
    GREEN = YELLOW = RED = CYAN = BLUE = RESET = BOLD = ''

# Constants
BASE_DIR = Path(__file__).parent
SCRIPT_PATH = BASE_DIR / "Data" / "activator_device.script.module_20251204-1914" / "0" / "activation.sh"
INSTALLER_PATH = BASE_DIR / "Data" / "activator_device.script.module_20251204-1914" / "0" / "installer.txt"
MNF_PATH = BASE_DIR / "Meta" / "Normal_release_2" / "activator_device" / "script.module" / "1.0.0.mnf"
BACKUP_DIR = BASE_DIR / ".backups"
CHECKSUM_SIZE = 524288

class ActivatorBuilder:
    """Class for automating activator build"""
    
    def __init__(self, create_backup: bool = True, verbose: bool = True):
        self.create_backup = create_backup
        self.verbose = verbose
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.info: List[str] = []
        self.backup_files: List[Path] = []
        
    def log(self, message: str, level: str = "info"):
        """Logging with colors"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        prefix = f"[{timestamp}]"
        
        if level == "error":
            print(f"{RED}{prefix} ❌ {message}{RESET}")
            self.errors.append(message)
        elif level == "warning":
            print(f"{YELLOW}{prefix} ⚠️  {message}{RESET}")
            self.warnings.append(message)
        elif level == "success":
            print(f"{GREEN}{prefix} ✅ {message}{RESET}")
        elif level == "info":
            print(f"{CYAN}{prefix} ℹ️  {message}{RESET}")
            self.info.append(message)
        elif level == "step":
            print(f"{BOLD}{BLUE}{prefix} 📋 {message}{RESET}")
        else:
            print(f"{prefix} {message}")
    
    def calculate_sha256(self, file_path: Path) -> str:
        """Calculate SHA256 hash of file"""
        sha256 = hashlib.sha256()
        try:
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    sha256.update(chunk)
            return sha256.hexdigest()
        except Exception as e:
            self.log(f"Error calculating hash {file_path}: {e}", "error")
            return ""
    
    def create_backup_file(self, file_path: Path) -> bool:
        """Create backup of file"""
        if not self.create_backup:
            return True
            
        try:
            BACKUP_DIR.mkdir(exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"{file_path.name}.{timestamp}.bak"
            backup_path = BACKUP_DIR / backup_name
            
            shutil.copy2(file_path, backup_path)
            self.backup_files.append(backup_path)
            if self.verbose:
                self.log(f"Backup created: {backup_path.name}", "info")
            return True
        except Exception as e:
            self.log(f"Failed to create backup {file_path}: {e}", "warning")
            return False
    
    def check_files_exist(self) -> bool:
        """Check if all required files exist"""
        self.log("Checking for files...", "step")
        
        files_to_check = [
            (SCRIPT_PATH, "activation.sh"),
            (INSTALLER_PATH, "installer.txt"),
            (MNF_PATH, "1.0.0.mnf")
        ]
        
        all_exist = True
        for file_path, name in files_to_check:
            if file_path.exists():
                self.log(f"File found: {name}", "success")
            else:
                self.log(f"File not found: {name} ({file_path})", "error")
                all_exist = False
        
        return all_exist
    
    def update_checksums(self) -> bool:
        """Update all checksums"""
        self.log("Updating checksums...", "step")
        
        # 1. Create backups
        if self.create_backup:
            self.log("Creating backups...", "info")
            self.create_backup_file(INSTALLER_PATH)
            self.create_backup_file(MNF_PATH)
        
        # 2. Calculate hash for activation.sh
        self.log("Calculating SHA256 for activation.sh...", "info")
        if not SCRIPT_PATH.exists():
            self.log("File activation.sh not found!", "error")
            return False
        
        file_size = SCRIPT_PATH.stat().st_size
        script_hash = self.calculate_sha256(SCRIPT_PATH)
        
        if not script_hash:
            return False
        
        self.log(f"Size: {file_size} bytes", "info")
        self.log(f"SHA256: {script_hash}", "info")
        
        # 3. Update installer.txt
        self.log("Updating installer.txt...", "info")
        try:
            with open(INSTALLER_PATH, 'r', encoding='utf-8') as f:
                installer_data = json.load(f)
            
            # Update data
            installer_data['Scripts'][0]['Length'] = file_size
            installer_data['Scripts'][0]['CheckSum'] = [script_hash]
            installer_data['Scripts'][0]['CheckSumSize'] = CHECKSUM_SIZE
            
            # Remove ExtraFiles to bypass signature verification
            if 'ExtraFiles' in installer_data['Scripts'][0]:
                del installer_data['Scripts'][0]['ExtraFiles']
                self.log("ExtraFiles section removed (signature bypass)", "success")
            else:
                self.log("ExtraFiles section absent (bypass active)", "success")
            
            # Save
            with open(INSTALLER_PATH, 'w', encoding='utf-8') as f:
                json.dump(installer_data, f, indent=4, ensure_ascii=False)
            
            self.log("installer.txt updated", "success")
            
        except Exception as e:
            self.log(f"Error updating installer.txt: {e}", "error")
            return False
        
        # 4. Calculate hash for installer.txt
        self.log("Calculating SHA256 for installer.txt...", "info")
        installer_hash = self.calculate_sha256(INSTALLER_PATH)
        
        if not installer_hash:
            return False
        
        self.log(f"SHA256 installer.txt: {installer_hash}", "info")
        
        # 5. Update .mnf file
        self.log("Updating 1.0.0.mnf...", "info")
        try:
            with open(MNF_PATH, 'r', encoding='utf-8') as f:
                mnf_data = json.load(f)
            
            # Update data
            mnf_data['HWIndex'][0]['InstallerFile'] = "activator_device.script.module_20251204-1914/0/installer.txt"
            mnf_data['HWIndex'][0]['CheckSum'] = [installer_hash]
            mnf_data['HWIndex'][0]['CheckSumSize'] = CHECKSUM_SIZE
            
            # Save
            with open(MNF_PATH, 'w', encoding='utf-8') as f:
                json.dump(mnf_data, f, indent=4, ensure_ascii=False)
            
            self.log("1.0.0.mnf updated", "success")
            
        except Exception as e:
            self.log(f"Error updating 1.0.0.mnf: {e}", "error")
            return False
        
        return True
    
    def verify_checksums(self) -> Tuple[bool, Dict[str, str]]:
        """Verify all checksums"""
        self.log("Verifying checksums...", "step")
        
        results = {
            'activation.sh': '',
            'installer.txt': '',
            'status': 'unknown'
        }
        
        all_ok = True
        
        # 1. Verify activation.sh in installer.txt
        self.log("Verifying activation.sh in installer.txt...", "info")
        if not SCRIPT_PATH.exists() or not INSTALLER_PATH.exists():
            self.log("Required files not found", "error")
            return False, results
        
        actual_script_hash = self.calculate_sha256(SCRIPT_PATH)
        actual_script_size = SCRIPT_PATH.stat().st_size
        
        try:
            with open(INSTALLER_PATH, 'r', encoding='utf-8') as f:
                installer_data = json.load(f)
            
            expected_script_hash = installer_data['Scripts'][0]['CheckSum'][0]
            expected_script_size = installer_data['Scripts'][0]['Length']
            
            if actual_script_hash == expected_script_hash:
                self.log("✅ activation.sh checksum matches", "success")
                results['activation.sh'] = 'ok'
            else:
                self.log("❌ activation.sh checksum mismatch", "error")
                self.log(f"   Expected: {expected_script_hash}", "error")
                self.log(f"   Got:      {actual_script_hash}", "error")
                results['activation.sh'] = 'mismatch'
                all_ok = False
            
            if actual_script_size != expected_script_size:
                self.log(f"⚠️  File size mismatch: {actual_script_size} != {expected_script_size}", "warning")
            
            # Check ExtraFiles
            if 'ExtraFiles' in installer_data['Scripts'][0]:
                self.log("⚠️  ExtraFiles section present (signature check may fail)", "warning")
            else:
                self.log("✅ ExtraFiles section removed (signature bypass active)", "success")
                
        except Exception as e:
            self.log(f"Error verifying installer.txt: {e}", "error")
            all_ok = False
        
        # 2. Verify installer.txt in .mnf
        self.log("Verifying installer.txt in .mnf...", "info")
        if not MNF_PATH.exists():
            self.log(".mnf file not found", "error")
            return False, results
        
        actual_installer_hash = self.calculate_sha256(INSTALLER_PATH)
        
        try:
            with open(MNF_PATH, 'r', encoding='utf-8') as f:
                mnf_data = json.load(f)
            
            expected_installer_hash = mnf_data['HWIndex'][0]['CheckSum'][0]
            
            if actual_installer_hash == expected_installer_hash:
                self.log("✅ installer.txt checksum matches", "success")
                results['installer.txt'] = 'ok'
            else:
                self.log("❌ installer.txt checksum mismatch", "error")
                self.log(f"   Expected: {expected_installer_hash}", "error")
                self.log(f"   Got:      {actual_installer_hash}", "error")
                results['installer.txt'] = 'mismatch'
                all_ok = False
                
        except Exception as e:
            self.log(f"Error verifying .mnf: {e}", "error")
            all_ok = False
        
        results['status'] = 'ok' if all_ok else 'failed'
        return all_ok, results
    
    def generate_report(self) -> str:
        """Generate report"""
        report = []
        report.append("=" * 60)
        report.append("LG MEN3 ACTIVATOR BUILD REPORT")
        report.append("=" * 60)
        report.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        if self.errors:
            report.append(f"❌ ERRORS ({len(self.errors)}):")
            for error in self.errors:
                report.append(f"  - {error}")
            report.append("")
        
        if self.warnings:
            report.append(f"⚠️  WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                report.append(f"  - {warning}")
            report.append("")
        
        if self.backup_files:
            report.append(f"📦 BACKUPS ({len(self.backup_files)}):")
            for backup in self.backup_files:
                report.append(f"  - {backup.name}")
            report.append("")
        
        report.append("=" * 60)
        
        return "\n".join(report)
    
    def run_full_build(self) -> bool:
        """Full automated build"""
        print(f"{BOLD}{BLUE}{'='*60}{RESET}")
        print(f"{BOLD}{BLUE}LG MEN3 ACTIVATOR - FULL AUTOMATION{RESET}")
        print(f"{BOLD}{BLUE}{'='*60}{RESET}\n")
        
        # Step 1: Check files
        if not self.check_files_exist():
            self.log("File check failed. Aborting.", "error")
            return False
        
        # Step 2: Update checksums
        if not self.update_checksums():
            self.log("Checksum update failed. Aborting.", "error")
            return False
        
        # Step 3: Verify result
        verify_ok, results = self.verify_checksums()
        
        # Final report
        print(f"\n{BOLD}{'='*60}{RESET}")
        if verify_ok and not self.errors:
            print(f"{GREEN}{BOLD}✅ BUILD SUCCESSFULLY COMPLETED{RESET}")
            print(f"{GREEN}All checksums updated and verified{RESET}")
            print(f"{GREEN}Signature verification bypass active{RESET}")
        else:
            print(f"{RED}{BOLD}❌ BUILD COMPLETED WITH ERRORS{RESET}")
            if self.errors:
                print(f"{RED}Errors found: {len(self.errors)}{RESET}")
        
        print(f"{BOLD}{'='*60}{RESET}\n")
        
        # Output report
        if self.verbose:
            print(self.generate_report())
        
        return verify_ok and len(self.errors) == 0


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='Fully automated build for LG MEN3 Activator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Usage examples:
  python auto_build.py              # Full automation (update + verify)
  python auto_build.py --update     # Update checksums only
  python auto_build.py --verify     # Verify checksums only
  python auto_build.py --no-backup  # Without creating backups
        """
    )
    
    parser.add_argument('--update', action='store_true',
                       help='Update checksums only')
    parser.add_argument('--verify', action='store_true',
                       help='Verify checksums only')
    parser.add_argument('--no-backup', action='store_true',
                       help='Do not create backups')
    parser.add_argument('--quiet', action='store_true',
                       help='Minimal output')
    
    args = parser.parse_args()
    
    builder = ActivatorBuilder(
        create_backup=not args.no_backup,
        verbose=not args.quiet
    )
    
    try:
        if args.verify:
            # Verify only
            builder.check_files_exist()
            verify_ok, results = builder.verify_checksums()
            sys.exit(0 if verify_ok else 1)
        elif args.update:
            # Update only
            builder.check_files_exist()
            success = builder.update_checksums()
            sys.exit(0 if success else 1)
        else:
            # Full automation
            success = builder.run_full_build()
            sys.exit(0 if success else 1)
            
    except KeyboardInterrupt:
        print(f"\n{RED}Interrupted by user{RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"{RED}Critical error: {e}{RESET}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

