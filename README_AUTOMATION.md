# FULL AUTOMATION LG MEN3 ACTIVATOR

## 🚀 Quick Start

### Simply run:
```bash
python auto_build.py
```

This automatically:
- ✅ Checks for all files
- ✅ Creates backups
- ✅ Updates all checksums
- ✅ Removes ExtraFiles section (signature bypass)
- ✅ Verifies result
- ✅ Generates report

---

## 📋 Operation Modes

### 1. Full automation (default)
```bash
python auto_build.py
```
Performs all steps: check → update → verify result

### 2. Update checksums only
```bash
python auto_build.py --update
```
Updates checksums without verification

### 3. Verify checksums only
```bash
python auto_build.py --verify
```
Verifies current checksums without changes

### 4. Without backups
```bash
python auto_build.py --no-backup
```
Does not create backups before changes

### 5. Minimal output
```bash
python auto_build.py --quiet
```
Outputs only critical information

---

## 🪟 Usage on Windows

### Via command line:
```cmd
auto_build.bat
```

### With parameters:
```cmd
auto_build.bat --update
auto_build.bat --verify
auto_build.bat --no-backup
```

### Double-click:
Simply double-click `auto_build.bat` for full automation

---

## 🐧 Usage on Linux/Mac

### Make script executable:
```bash
chmod +x auto_build.sh
```

### Run:
```bash
./auto_build.sh
```

### With parameters:
```bash
./auto_build.sh --update
./auto_build.sh --verify
```

---

## 🔄 Typical Usage Scenarios

### After modifying activation.sh:
```bash
python auto_build.py
```
Automatically updates all checksums and verifies result

### Before installation (verification):
```bash
python auto_build.py --verify
```
Make sure all checksums are correct

### Quick update without backups:
```bash
python auto_build.py --update --no-backup
```

---

## 📁 Backup Structure

Backups are saved in `.backups/` folder:
```
.backups/
├── installer.txt.20251204_213528.bak
└── 1.0.0.mnf.20251204_213528.bak
```

Filename format: `filename.YYYYMMDD_HHMMSS.bak`

---

## ✅ What is Automatically Verified

1. **File presence:**
   - `activation.sh`
   - `installer.txt`
   - `1.0.0.mnf`

2. **Checksums:**
   - SHA256 for `activation.sh` in `installer.txt`
   - SHA256 for `installer.txt` in `1.0.0.mnf`
   - `activation.sh` file size

3. **Signature bypass:**
   - Absence of `ExtraFiles` section in `installer.txt`

---

## 📊 Example Output

```
============================================================
LG MEN3 ACTIVATOR - FULL AUTOMATION
============================================================

[21:35:28] 📋 Checking for files...
[21:35:28] ✅ File found: activation.sh
[21:35:28] ✅ File found: installer.txt
[21:35:28] ✅ File found: 1.0.0.mnf
[21:35:28] 📋 Updating checksums...
[21:35:28] ℹ️  Creating backups...
[21:35:28] ℹ️  Backup created: installer.txt.20251204_213528.bak
[21:35:28] ℹ️  Backup created: 1.0.0.mnf.20251204_213528.bak
[21:35:28] ℹ️  Calculating SHA256 for activation.sh...
[21:35:28] ℹ️  Size: 5905 bytes
[21:35:28] ℹ️  SHA256: 603bed2ce661777b3531bef8cf1dc9489de6ae03a0f545c33632629fc37e45fd
[21:35:28] ℹ️  Updating installer.txt...
[21:35:28] ✅ ExtraFiles section absent (bypass active)
[21:35:28] ✅ installer.txt updated
[21:35:28] ℹ️  Calculating SHA256 for installer.txt...
[21:35:28] ℹ️  SHA256 installer.txt: 9a29ddde44dbe2112d971a0cbcf7f24acc30cd84ab1bb8e8ad44ba6e6a330961
[21:35:28] ℹ️  Updating 1.0.0.mnf...
[21:35:28] ✅ 1.0.0.mnf updated
[21:35:28] 📋 Verifying checksums...
[21:35:28] ℹ️  Verifying activation.sh in installer.txt...
[21:35:28] ✅ activation.sh checksum matches
[21:35:28] ✅ ExtraFiles section removed (signature bypass active)
[21:35:28] ℹ️  Verifying installer.txt in .mnf...
[21:35:28] ✅ installer.txt checksum matches

============================================================
✅ BUILD SUCCESSFULLY COMPLETED
All checksums updated and verified
Signature verification bypass active
============================================================
```

---

## ⚙️ IDE Integration

### Visual Studio Code
Add to `.vscode/tasks.json`:
```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Auto Build Activator",
            "type": "shell",
            "command": "python",
            "args": ["auto_build.py"],
            "group": "build",
            "presentation": {
                "reveal": "always",
                "panel": "new"
            }
        }
    ]
}
```

### PyCharm
Create Run Configuration:
- Script: `auto_build.py`
- Working directory: project
- Parameters: (leave empty for full automation)

---

## 🔧 Requirements

- Python 3.6+
- Python standard library (json, hashlib, pathlib, shutil)

Optional (for colored output):
```bash
pip install colorama
```

---

## 🐛 Troubleshooting

### Error: "File not found"
Make sure you're running the script from project root folder:
```
LG_MEN3_Activator/
├── auto_build.py
├── Data/
└── Meta/
```

### Error: "Permission denied" (Linux/Mac)
```bash
chmod +x auto_build.sh
chmod +x auto_build.py
```

### Error: "Module not found: colorama"
Colored output is optional. Script works without colorama, but without colors.

---

## 📝 Comparison with Old Scripts

| Function | calculate_checksums.py | verify_checksums.py | **auto_build.py** |
|----------|----------------------|-------------------|-------------------|
| Update checksums | ✅ | ❌ | ✅ |
| Verify checksums | ❌ | ✅ | ✅ |
| Backups | ❌ | ❌ | ✅ |
| Signature bypass | ✅ | ✅ | ✅ |
| Report | ❌ | ❌ | ✅ |
| Automation | ❌ | ❌ | ✅ |
| Operation modes | ❌ | ❌ | ✅ |

**Recommendation:** Use `auto_build.py` for all tasks!

---

## 🎯 Recommended Workflow

1. **Edit `activation.sh`**
2. **Run:** `python auto_build.py`
3. **Check output:** Everything should be ✅
4. **Done!** Package is ready for installation

---

## 📞 Support

If problems occur:
1. Check that all files are in place
2. Run with `--verify` for diagnostics
3. Check logs in script output

---

**Version:** 1.0.0  
**Date:** 2025-12-04  
**Status:** ✅ Fully automated
