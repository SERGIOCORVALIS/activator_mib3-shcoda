LG MEN3 Activator
Based on MST2 Activator by Congo and Duke
Adapted for LG MEN3_EU_SK370_P3355L

==========================================
IMPORTANT: READ BEFORE USE
==========================================

This activator is created for firmware LG MEN3_EU_SK370_P3355L.
It is based on MST2 Activator, but fully adapted for LG MEN3 format.

==========================================
🚀 FULL AUTOMATION (NEW!)
==========================================

After modifying activation.sh simply run:

Windows:   auto_build.bat
           OR python auto_build.py

Linux/Mac: ./auto_build.sh
           OR python3 auto_build.py

Automatically:
✅ Updates all checksums
✅ Bypasses signature verification
✅ Verifies result
✅ Creates backups

For more details: README_AUTOMATION.md or AUTOMATION.txt

STRUCTURE:
----------
LG_MEN3_Activator/
├── Meta/
│   ├── multi_activator.mnf          # Main manifest
│   └── Normal_release_2/
│       ├── main_activator.mnf       # Main activator manifest
│       └── activator_device/        # Activator device metadata
├── Data/
│   └── activator_device.script.module_*/0/
│       ├── activation.sh            # Main activation script
│       ├── activation.sh.sig        # Script signature (required!)
│       └── installer.txt            # Installer metadata
└── common/
    └── addFecs.txt                  # List of FEC codes for activation

INSTALLATION:
-------------
1. Copy the entire LG_MEN3_Activator folder to SD card or USB drive
2. Install as a regular software update through system menu
3. After installation, the activator will automatically execute activation.sh script

IMPORTANT NOTES:
----------------
1. SIGNATURES: The activation.sh.sig file must be properly signed!
   Without proper signature, the script will not be executed by the system.
   Current file contains a stub - a real signature is required.

2. FEC CODES: 
   - If you create common/addFecs.txt on SD/USB card, 
     the activator will use these FEC codes
   - If file is not present, default codes will be used

3. NETWORK SERVICES:
   - Activator enables FTP, Telnet and Login services
   - Configuration files: /etc/inetd.conf, /etc/passwd

4. AUTOMATIC SCRIPT EXECUTION:
   - Place delphi.sh file on SD card
   - On system boot, the script will be automatically executed

5. LOGS:
   - Activation log is saved to /tmp/activator.log
   - Check the log for troubleshooting

INTEGRATION WITH ORIGINAL FIRMWARE:
------------------------------------
To integrate the activator with original firmware MEN3_EU_SK370_P3355L:

1. Copy Meta/Normal_release_2/main_activator.mnf 
   to original firmware as a separate release

2. OR add to original main.mnf:
   - In "Includes" section add:
     {
         "PackageName": "activator_device",
         "PackageVersion": "1.0.0"
     }
   - In "UpdateOrder" section add activator at the end

3. Copy Data/activator_device.script.module_* 
   to Data/ of original firmware

4. Update multi.mnf, adding new release (if using separate one)

SUPPORTED VERSIONS:
-------------------
- MEN3_EU_SK370_P3355L (MUVersion: 1800)
- Variant: FM3-E2-*-*-SK-MQB-PA-*

LIMITATIONS:
------------
- Requires proper activation.sh.sig signature
- Some features may require additional configuration
- Test on test device before using on main device

DEBUGGING:
----------
1. Check /tmp/activator.log after installation
2. Check for marker: /tmp/activator_marker
3. Check FEC codes: /opt/swup/fecs/activated_fecs.txt
4. Check network services: telnet, ftp

SECURITY:
---------
- Always create a backup before installation
- Do not disconnect device during installation
- Use only on compatible devices

VERSION:
--------
1.0.0 - First version for LG MEN3
Based on MST2 Activator v3.0 (Unbroken)

AUTHORS:
--------
Adapted for LG MEN3 based on MST2 Activator by Congo and Duke

==========================================
WARNING: Use at your own risk!
==========================================

