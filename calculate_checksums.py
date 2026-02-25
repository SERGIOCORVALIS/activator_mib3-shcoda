#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to calculate SHA256 checksums and update installer.txt and .mnf files
for LG MEN3 Activator
"""

import os
import json
import hashlib
from pathlib import Path

# File paths
BASE_DIR = Path(__file__).parent
SCRIPT_PATH = BASE_DIR / "Data" / "activator_device.script.module_20251204-1914" / "0" / "activation.sh"
INSTALLER_PATH = BASE_DIR / "Data" / "activator_device.script.module_20251204-1914" / "0" / "installer.txt"
MNF_PATH = BASE_DIR / "Meta" / "Normal_release_2" / "activator_device" / "script.module" / "1.0.0.mnf"

def calculate_sha256(file_path):
    """Calculate SHA256 hash of a file"""
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

def main():
    print("=== LG MEN3 Activator - Checksum Calculation ===\n")
    
    # Check if script file exists
    if not SCRIPT_PATH.exists():
        print(f"ERROR: File {SCRIPT_PATH} not found!")
        return 1
    
    # 1. Calculate checksum for activation.sh
    print("1. Calculating checksum for activation.sh...")
    file_size = SCRIPT_PATH.stat().st_size
    script_hash = calculate_sha256(SCRIPT_PATH)
    print(f"   File size: {file_size} bytes")
    print(f"   SHA256 hash: {script_hash}")
    
    check_sum_size = 524288
    
    # 2. Update installer.txt
    print("\n2. Updating installer.txt...")
    with open(INSTALLER_PATH, 'r', encoding='utf-8') as f:
        installer_data = json.load(f)
    
    # Update checksums
    installer_data['Scripts'][0]['Length'] = file_size
    installer_data['Scripts'][0]['CheckSum'] = [script_hash]
    installer_data['Scripts'][0]['CheckSumSize'] = check_sum_size
    
    # Remove ExtraFiles section to bypass signature verification
    print("   Removing ExtraFiles section to bypass signature check...")
    if 'ExtraFiles' in installer_data['Scripts'][0]:
        del installer_data['Scripts'][0]['ExtraFiles']
    
    # Save updated installer.txt
    with open(INSTALLER_PATH, 'w', encoding='utf-8') as f:
        json.dump(installer_data, f, indent=4, ensure_ascii=False)
    print("   installer.txt updated!")
    
    # 3. Calculate checksum for installer.txt
    print("\n3. Calculating checksum for installer.txt...")
    installer_hash = calculate_sha256(INSTALLER_PATH)
    print(f"   SHA256 hash installer.txt: {installer_hash}")
    
    # 4. Update script.module/1.0.0.mnf
    print("\n4. Updating script.module/1.0.0.mnf...")
    with open(MNF_PATH, 'r', encoding='utf-8') as f:
        mnf_data = json.load(f)
    
    # Update checksums
    mnf_data['HWIndex'][0]['InstallerFile'] = "activator_device.script.module_20251204-1914/0/installer.txt"
    mnf_data['HWIndex'][0]['CheckSum'] = [installer_hash]
    mnf_data['HWIndex'][0]['CheckSumSize'] = check_sum_size
    
    # Save updated .mnf file
    with open(MNF_PATH, 'w', encoding='utf-8') as f:
        json.dump(mnf_data, f, indent=4, ensure_ascii=False)
    print("   1.0.0.mnf updated!")
    
    print("\n=== DONE ===")
    print("\nResults:")
    print(f"  - activation.sh: {script_hash}")
    print(f"  - installer.txt: {installer_hash}")
    print(f"  - activation.sh size: {file_size} bytes")
    print("\nIMPORTANT:")
    print("  - ExtraFiles section removed from installer.txt to bypass signature check")
    print("  - If system requires signature, different approach may be needed")
    print()
    
    return 0

if __name__ == "__main__":
    exit(main())

