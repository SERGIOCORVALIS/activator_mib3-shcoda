#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to verify checksums in installer.txt and .mnf files
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

def verify_checksums():
    """Verify all checksums"""
    print("=== LG MEN3 Activator - Checksum Verification ===\n")
    
    errors = []
    warnings = []
    
    # 1. Verify activation.sh checksum in installer.txt
    print("1. Verifying activation.sh checksum in installer.txt...")
    if not SCRIPT_PATH.exists():
        errors.append(f"File {SCRIPT_PATH} not found!")
        print(f"   ❌ ERROR: File not found!")
    else:
        actual_hash = calculate_sha256(SCRIPT_PATH)
        file_size = SCRIPT_PATH.stat().st_size
        
        if not INSTALLER_PATH.exists():
            errors.append(f"File {INSTALLER_PATH} not found!")
            print(f"   ❌ ERROR: installer.txt not found!")
        else:
            with open(INSTALLER_PATH, 'r', encoding='utf-8') as f:
                installer_data = json.load(f)
            
            expected_hash = installer_data['Scripts'][0]['CheckSum'][0]
            expected_size = installer_data['Scripts'][0]['Length']
            
            print(f"   File size: {file_size} bytes (expected: {expected_size})")
            print(f"   Actual hash:   {actual_hash}")
            print(f"   Expected hash: {expected_hash}")
            
            if actual_hash == expected_hash:
                print("   ✅ Checksum matches!")
            else:
                errors.append("activation.sh checksum mismatch in installer.txt")
                print("   ❌ Checksum mismatch!")
            
            if file_size != expected_size:
                warnings.append("activation.sh size mismatch in installer.txt")
                print("   ⚠️  Size mismatch!")
            
            # Check for ExtraFiles section
            if 'ExtraFiles' in installer_data['Scripts'][0]:
                warnings.append("ExtraFiles section still present in installer.txt (signature check may fail)")
                print("   ⚠️  ExtraFiles section found (should be removed to bypass signature check)")
            else:
                print("   ✅ ExtraFiles section removed (signature bypass active)")
    
    # 2. Verify installer.txt checksum in .mnf
    print("\n2. Verifying installer.txt checksum in .mnf...")
    if not INSTALLER_PATH.exists():
        errors.append(f"File {INSTALLER_PATH} not found!")
        print(f"   ❌ ERROR: installer.txt not found!")
    else:
        actual_installer_hash = calculate_sha256(INSTALLER_PATH)
        
        if not MNF_PATH.exists():
            errors.append(f"File {MNF_PATH} not found!")
            print(f"   ❌ ERROR: .mnf file not found!")
        else:
            with open(MNF_PATH, 'r', encoding='utf-8') as f:
                mnf_data = json.load(f)
            
            expected_installer_hash = mnf_data['HWIndex'][0]['CheckSum'][0]
            
            print(f"   Actual hash:   {actual_installer_hash}")
            print(f"   Expected hash: {expected_installer_hash}")
            
            if actual_installer_hash == expected_installer_hash:
                print("   ✅ Checksum matches!")
            else:
                errors.append("installer.txt checksum mismatch in .mnf")
                print("   ❌ Checksum mismatch!")
    
    # Summary
    print("\n" + "="*50)
    if errors:
        print("❌ VERIFICATION FAILED")
        print(f"\nErrors found: {len(errors)}")
        for error in errors:
            print(f"  - {error}")
    else:
        print("✅ VERIFICATION PASSED")
    
    if warnings:
        print(f"\nWarnings: {len(warnings)}")
        for warning in warnings:
            print(f"  ⚠️  {warning}")
    
    print("\n" + "="*50)
    
    return len(errors) == 0

if __name__ == "__main__":
    success = verify_checksums()
    exit(0 if success else 1)

