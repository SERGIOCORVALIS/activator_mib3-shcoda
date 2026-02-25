# LG MEN3 ACTIVATOR INSTALLATION GUIDE

## PREPARATION

### 1. Requirements
- LG MEN3 device with firmware MEN3_EU_SK370_P3355L
- SD card or USB drive (formatted in FAT32)
- Backup of current firmware (RECOMMENDED!)

### 2. File Preparation

#### Option A: Separate Activator Installation
1. Copy entire `LG_MEN3_Activator` folder to SD/USB card
2. Make sure structure is preserved:
   ```
   [SD/USB]/
   └── LG_MEN3_Activator/
       ├── Meta/
       ├── Data/
       └── common/
   ```

#### Option B: Integration with Original Firmware
1. Copy contents of `LG_MEN3_Activator` to original firmware folder
2. Update original firmware `main.mnf` (see "Integration" section)

## INSTALLATION

### Step 1: SD/USB Card Preparation
1. Format SD card in FAT32
2. Copy `LG_MEN3_Activator` folder to card root
3. (Optional) Create `common/addFecs.txt` with your FEC codes

### Step 2: Installation via System
1. Insert SD/USB card into device
2. Go to software update menu
3. Select installation from external media
4. Select `LG_MEN3_Activator` or `multi_activator.mnf`
5. Confirm installation
6. **DO NOT DISCONNECT DEVICE** during installation!

### Step 3: Installation Verification
After installation check:
1. Log file: `/tmp/activator.log`
2. Activation marker: `/tmp/activator_marker`
3. FEC codes: `/opt/swup/fecs/activated_fecs.txt`
4. Network services: try connecting via Telnet/FTP

## INTEGRATION WITH ORIGINAL FIRMWARE

### Method 1: Adding to Existing main.mnf

Open `Meta/Normal_release_2/main.mnf` of original firmware and add:

1. In `"Includes"` section:
```json
{
    "PackageName": "activator_device",
    "PackageVersion": "1.0.0"
}
```

2. In `"UpdateOrder"` section (at the end, after ScriptInstaller):
```json
{
    "Type": "parallel",
    "Devices": [
        [],
        [
            "activator_device"
        ]
    ]
}
```

3. Copy metadata:
   - `Meta/Normal_release_2/activator_device/` → to original firmware

4. Copy data:
   - `Data/activator_device.script.module_*/` → to `Data/` of original firmware

### Method 2: Separate Release in multi.mnf

1. Add to `Meta/multi.mnf`:
```json
{
    "PackageName": "Normal_release_2/main_activator.mnf",
    "DisplayName": "LG MEN3 Activator"
}
```

2. Use `main_activator.mnf` as separate release

## FEC CODE CONFIGURATION

### Creating addFecs.txt
Create `common/addFecs.txt` file on SD/USB card with your FEC codes:
```
00030000
00040100
00050000
00060100
...
```

Each FEC code on a new line. Empty lines and lines starting with `#` are ignored.

### Default FEC Codes
If `addFecs.txt` is not found, default codes are used:
- 00030000, 00040100, 00050000
- 00060100, 00060200, 00060300
- 00060800, 00060900
- 00070200, 00070400
- 09400003

## AUTOMATIC SCRIPT EXECUTION

For automatic script execution on boot:

1. Create `delphi.sh` file on SD/USB card
2. Make it executable (chmod +x)
3. Place on SD/USB card root
4. On next boot, script will be automatically executed

Example `delphi.sh`:
```bash
#!/bin/sh
echo "Custom script executed" > /tmp/custom_script.log
# Your commands here
```

## DEBUGGING

### Check Logs
```bash
cat /tmp/activator.log
```

### Check Activation Status
```bash
ls -la /tmp/activator_marker
cat /opt/swup/fecs/activated_fecs.txt
```

### Check Network Services
```bash
# Check inetd
ps aux | grep inetd
cat /etc/inetd.conf

# Test Telnet
telnet localhost 23

# Test FTP
ftp localhost 21
```

### Check Users
```bash
cat /etc/passwd
```

## TROUBLESHOOTING

### Problem: Script Not Executing
**Cause:** Incorrect `activation.sh.sig` signature
**Solution:** 
- Proper script signature required
- Check that `activation.sh.sig` file exists and has correct size (4096 bytes)

### Problem: FEC Codes Not Activating
**Cause:** Incorrect format or path to FEC files
**Solution:**
- Check `addFecs.txt` format (one FEC per line)
- Check logs: `/tmp/activator.log`
- Make sure file is in `common/addFecs.txt` on SD/USB

### Problem: Network Services Not Working
**Cause:** Incorrect paths to daemons or missing daemons
**Solution:**
- Check paths in `/etc/inetd.conf`
- Make sure daemons exist: `/usr/bin/ftpd`, `/usr/bin/telnetd`
- Check logs: `/tmp/activator.log`

### Problem: Installation Not Starting
**Cause:** Incorrect structure or metadata
**Solution:**
- Check folder structure
- Make sure all `.mnf` files are valid (check JSON)
- Check checksums in `installer.txt`

## SECURITY

⚠️ **IMPORTANT:**
1. Always create a backup before installation
2. Do not disconnect device during installation
3. Use only on compatible devices
4. Test on test device before using on main device

## SUPPORT

If problems occur:
1. Check logs: `/tmp/activator.log`
2. Check file structure
3. Verify firmware version compatibility
4. Check checksums and signatures

---

**Version:** 1.0.0  
**Date:** 2024-12-04
