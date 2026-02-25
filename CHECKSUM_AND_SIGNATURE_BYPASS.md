# CHECKSUM VERIFICATION AND SIGNATURE BYPASS

## CURRENT STATUS

### ✅ Checksums updated:

1. **activation.sh**
   - Size: 5905 bytes
   - SHA256: `603bed2ce661777b3531bef8cf1dc9489de6ae03a0f545c33632629fc37e45fd`
   - Updated in: `installer.txt`

2. **installer.txt**
   - SHA256: `9a29ddde44dbe2112d971a0cbcf7f24acc30cd84ab1bb8e8ad44ba6e6a330961`
   - Updated in: `script.module/1.0.0.mnf`

3. **CheckSumSize**: 524288 bytes (block size for verification)

---

## SIGNATURE BYPASS METHODS

### Method 1: Remove ExtraFiles Section (IMPLEMENTED)

**Current approach:**
- `calculate_checksums.py` script automatically removes `ExtraFiles` section from `installer.txt`
- `ExtraFiles` section usually contains references to signature files (`.sig`)

**How it works:**
```json
// BEFORE (with signature verification):
{
    "Scripts": [{
        "Path": "...",
        "ExtraFiles": [
            {
                "Path": ".../activation.sh.sig",
                "CheckSum": [...]
            }
        ]
    }]
}

// AFTER (without signature verification):
{
    "Scripts": [{
        "Path": "...",
        // ExtraFiles removed
    }]
}
```

**Advantages:**
- ✅ Simple and fast method
- ✅ Does not require system file modification
- ✅ Automatically executed by script

**Disadvantages:**
- ⚠️ May not work if system checks for signature in another location
- ⚠️ Some firmware versions may require signature mandatorily

---

### Method 2: Using Signature Stub

**Current state:**
- `activation.sh.sig` file exists but contains zero bytes (stub)

**If system requires signature file presence:**
1. Create signature file 4096 bytes with zero bytes:
   ```bash
   dd if=/dev/zero of=activation.sh.sig bs=1 count=4096
   ```

2. Update signature file checksum in `installer.txt` (if ExtraFiles section is present)

**Limitations:**
- ⚠️ Works only if system does not check signature content
- ⚠️ Most systems check cryptographic signature validity

---

### Method 3: Using Signature from Another Script

**If other scripts found in firmware:**

1. Find existing script with valid signature in LG MEN3 firmware
2. Copy `.sig` file from that script
3. Rename to `activation.sh.sig`
4. Update checksums

**Important:**
- ⚠️ Signature must be for the same script type
- ⚠️ Size and format must match
- ⚠️ May not work if signature is bound to specific file

---

### Method 4: System Verification Modification (Advanced)

**If system checks signature at firmware level:**

1. **Study verification mechanism:**
   - Find executable file that verifies signatures
   - Usually part of ScriptInstaller or UpdateManager

2. **Possible verification locations:**
   - `/usr/bin/scriptinstaller`
   - `/opt/swup/bin/*`
   - Libraries in `/usr/lib/` or `/opt/swup/lib/`

3. **Bypass methods:**
   - Binary file patching (replace verification with NOP)
   - Using LD_PRELOAD to intercept verification functions
   - System configuration file modification

**Requirements:**
- ⚠️ Requires root access to system
- ⚠️ Knowledge of firmware structure needed
- ⚠️ May compromise system integrity

---

### Method 5: Using Developer/Debug Mode

**If system supports developer mode:**

1. Enable developer/debug mode in system
2. In this mode, signature verification may be disabled
3. Install activator in developer mode

**Limitations:**
- ⚠️ Not all systems have such mode
- ⚠️ May require special keys or access

---

## CHECKSUM VERIFICATION

### Automatic verification:

```bash
# Python
python calculate_checksums.py

# PowerShell
.\calculate_checksums.ps1
```

### Manual verification:

```bash
# SHA256 for activation.sh
sha256sum Data/activator_device.script.module_20251204-1914/0/activation.sh

# SHA256 for installer.txt
sha256sum Data/activator_device.script.module_20251204-1914/0/installer.txt
```

### Current values:

| File | SHA256 Hash |
|------|-------------|
| activation.sh | `603bed2ce661777b3531bef8cf1dc9489de6ae03a0f545c33632629fc37e45fd` |
| installer.txt | `9a29ddde44dbe2112d971a0cbcf7f24acc30cd84ab1bb8e8ad44ba6e6a330961` |

---

## RECOMMENDATIONS

### For most cases:

1. ✅ **Use Method 1** (remove ExtraFiles) - already implemented
2. ✅ Run `calculate_checksums.py` after each `activation.sh` modification
3. ✅ Verify that all checksums are updated

### If Method 1 doesn't work:

1. Check system logs for signature verification errors
2. Study structure of other scripts in firmware
3. Try Method 3 (using signature from another script)
4. Consider Method 4 only with root access and knowledge

### Important notes:

- ⚠️ Always create backups before modification
- ⚠️ Test on test system before using in production
- ⚠️ Some methods may compromise update system integrity

---

## FILE STRUCTURE

```
LG_MEN3_Activator/
├── Data/
│   └── activator_device.script.module_20251204-1914/
│       └── 0/
│           ├── activation.sh          # Main activation script
│           ├── activation.sh.sig      # Signature file (stub)
│           └── installer.txt          # Installer configuration (without ExtraFiles)
├── Meta/
│   └── Normal_release_2/
│       └── activator_device/
│           └── script.module/
│               └── 1.0.0.mnf          # Manifest with installer.txt checksum
└── calculate_checksums.py             # Automatic update script
```

---

## UPDATE AFTER CHANGES

After any modification of `activation.sh`:

1. Run `python calculate_checksums.py`
2. Script automatically:
   - Calculates new SHA256 for `activation.sh`
   - Updates `installer.txt`
   - Removes `ExtraFiles` section (if present)
   - Calculates new SHA256 for `installer.txt`
   - Updates `1.0.0.mnf`

---

## ADDITIONAL INFORMATION

See also:
- `SIGNATURE_INFO.txt` - Signature information
- `INSTALLATION_GUIDE.md` - Installation guide
- `ReadMe.txt` - General information

---

**Last update:** After running `calculate_checksums.py`
**Status:** Checksums are current, signature verification bypassed via ExtraFiles removal
