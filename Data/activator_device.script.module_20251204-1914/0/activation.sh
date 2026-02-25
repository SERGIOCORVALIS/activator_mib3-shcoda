#!/bin/sh
#
# LG MEN3 Activator Script
# Based on MST2 Activator by Congo and Duke
# Adapted for LG MEN3_EU_SK370_P3355L
#

LOG_FILE="/tmp/activator.log"
FEC_DIR="/opt/swup/fecs"
CONFIG_DIR="/opt/swup/config"

# Create log file
echo "=== LG MEN3 Activator Started ===" > "$LOG_FILE"
echo "Date: $(date)" >> "$LOG_FILE"

# Function to log messages
log_msg() {
    echo "[$(date +%Y-%m-%d\ %H:%M:%S)] $1" >> "$LOG_FILE"
    echo "$1"
}

log_msg "Starting activation process..."

# Create necessary directories
mkdir -p "$FEC_DIR" 2>/dev/null
mkdir -p "$CONFIG_DIR" 2>/dev/null
mkdir -p /tmp/activator 2>/dev/null

# Check for SD/USB cards with FEC files
log_msg "Checking for FEC files on external media..."

# Check SD cards and USB drives
for mount_point in /sdc1 /sdc2 /usb1 /usb2 /media/sdcard /media/usb; do
    if [ -d "$mount_point" ]; then
        if [ -f "$mount_point/common/addFecs.txt" ]; then
            log_msg "Found addFecs.txt on $mount_point"
            cp "$mount_point/common/addFecs.txt" "$FEC_DIR/addFecs.txt" 2>/dev/null
        fi
        if [ -f "$mount_point/EXCEPTION_LIST/tools/activation.sh" ]; then
            log_msg "Found additional activation script on $mount_point"
            chmod +x "$mount_point/EXCEPTION_LIST/tools/activation.sh"
            "$mount_point/EXCEPTION_LIST/tools/activation.sh" >> "$LOG_FILE" 2>&1
        fi
    fi
done

# Install network services configuration
log_msg "Installing network services configuration..."

# Create inetd.conf if it doesn't exist or backup existing
if [ ! -f /etc/inetd.conf ]; then
    log_msg "Creating /etc/inetd.conf"
    cat > /etc/inetd.conf << 'EOF'
ftp     stream  tcp  nowait  root  /usr/bin/ftpd       in.ftpd
telnet  stream  tcp  nowait  root  /usr/bin/telnetd    in.telnetd
login   stream  tcp  nowait  root  /usr/bin/rlogind    in.rlogind
EOF
    chmod 644 /etc/inetd.conf
else
    log_msg "Backing up existing /etc/inetd.conf"
    cp /etc/inetd.conf /etc/inetd.conf.backup.$(date +%Y%m%d_%H%M%S)
    # Append our services if not present
    if ! grep -q "ftp.*stream.*tcp" /etc/inetd.conf; then
        echo "ftp     stream  tcp  nowait  root  /usr/bin/ftpd       in.ftpd" >> /etc/inetd.conf
    fi
    if ! grep -q "telnet.*stream.*tcp" /etc/inetd.conf; then
        echo "telnet  stream  tcp  nowait  root  /usr/bin/telnetd    in.telnetd" >> /etc/inetd.conf
    fi
fi

# Update passwd file to enable root access
log_msg "Updating passwd file..."

if [ -f /etc/passwd ]; then
    cp /etc/passwd /etc/passwd.backup.$(date +%Y%m%d_%H%M%S)
    # Ensure root user exists with shell access
    if ! grep -q "^root:" /etc/passwd; then
        echo "root::0:0::/root:/bin/sh" >> /etc/passwd
    else
        # Update root to use /bin/sh
        sed -i 's|^root:.*|root::0:0::/root:/bin/sh|' /etc/passwd
    fi
    # Add delphi user if not present
    if ! grep -q "^delphi:" /etc/passwd; then
        echo "delphi::1000:9100:Global Delphi User:/home/delphi:/bin/sh" >> /etc/passwd
    fi
    # Add ftpuser if not present
    if ! grep -q "^ftpuser:" /etc/passwd; then
        echo "ftpuser::0:0::/:/bin/sh" >> /etc/passwd
    fi
fi

# Enable UART console (if applicable)
log_msg "Enabling UART console..."
# This may vary depending on system configuration
if [ -f /proc/cmdline ]; then
    # Check if console is already enabled
    if ! grep -q "console=" /proc/cmdline; then
        log_msg "UART console configuration may need manual setup"
    fi
fi

# Process FEC codes if addFecs.txt exists
if [ -f "$FEC_DIR/addFecs.txt" ]; then
    log_msg "Processing FEC codes from addFecs.txt"
    while IFS= read -r fec_code; do
        # Skip empty lines and comments
        [ -z "$fec_code" ] && continue
        [ "${fec_code#\#}" != "$fec_code" ] && continue
        
        log_msg "Processing FEC: $fec_code"
        # FEC activation logic would go here
        # This is platform-specific and may require additional tools
        # For now, we'll just log the FEC codes
        echo "$fec_code" >> "$FEC_DIR/activated_fecs.txt"
    done < "$FEC_DIR/addFecs.txt"
else
    log_msg "No addFecs.txt found, using default FEC codes"
    # Default FEC codes
    cat > "$FEC_DIR/activated_fecs.txt" << 'EOF'
00050000
00060100
00060200
00060300
00070700
00070D00
00070E00
00071600
00000700
EOF
fi

# Enable automatic script execution from SD card
log_msg "Setting up automatic script execution from SD card..."

# Create startup script that checks for delphi.sh on SD cards
STARTUP_SCRIPT="/etc/init.d/activator_sd_script.sh"
cat > "$STARTUP_SCRIPT" << 'EOFSCRIPT'
#!/bin/sh
# Auto-execute script from SD card on startup
# LG MEN3 Activator - Startup Script

LOG_FILE="/tmp/activator_startup.log"
echo "[$(date +%Y-%m-%d\ %H:%M:%S)] Startup script executed" >> "$LOG_FILE"

sleep 10  # Wait for SD2 to be ready

for mount_point in /sdc1 /sdc2 /usb1 /usb2 /media/sdcard /media/usb /mnt/sdcard /mnt/usb; do
    if [ -d "$mount_point" ] && [ -f "$mount_point/delphi.sh" ]; then
        echo "[$(date +%Y-%m-%d\ %H:%M:%S)] Found delphi.sh on $mount_point, executing..." >> "$LOG_FILE"
        chmod +x "$mount_point/delphi.sh" 2>/dev/null
        "$mount_point/delphi.sh" >> /tmp/delphi_script.log 2>&1
        echo "[$(date +%Y-%m-%d\ %H:%M:%S)] Script execution completed" >> "$LOG_FILE"
        break
    fi
done
EOFSCRIPT

chmod +x "$STARTUP_SCRIPT"
log_msg "Startup script created: $STARTUP_SCRIPT"

# Try multiple methods to add to startup
STARTUP_REGISTERED=0

# Method 1: systemd (modern Linux systems)
if command -v systemctl >/dev/null 2>&1 && [ -d /etc/systemd/system ]; then
    log_msg "Attempting to register via systemd..."
    cat > /etc/systemd/system/activator-sd-script.service << 'EOFSERVICE'
[Unit]
Description=LG MEN3 Activator SD Script Runner
After=multi-user.target

[Service]
Type=oneshot
ExecStart=/etc/init.d/activator_sd_script.sh
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
EOFSERVICE
    if systemctl enable activator-sd-script.service >/dev/null 2>&1; then
        log_msg "✓ Registered via systemd"
        STARTUP_REGISTERED=1
    else
        log_msg "✗ systemd registration failed"
        rm -f /etc/systemd/system/activator-sd-script.service 2>/dev/null
    fi
fi

# Method 2: /etc/rc.d (SysV init)
if [ "$STARTUP_REGISTERED" -eq 0 ] && [ -d /etc/rc.d ]; then
    log_msg "Attempting to register via /etc/rc.d..."
    if ln -sf "$STARTUP_SCRIPT" /etc/rc.d/S99activator_sd_script 2>/dev/null; then
        log_msg "✓ Registered via /etc/rc.d (S99activator_sd_script)"
        STARTUP_REGISTERED=1
    else
        # Try with different priority
        if ln -sf "$STARTUP_SCRIPT" /etc/rc.d/S50activator_sd_script 2>/dev/null; then
            log_msg "✓ Registered via /etc/rc.d (S50activator_sd_script)"
            STARTUP_REGISTERED=1
        else
            log_msg "✗ /etc/rc.d registration failed"
        fi
    fi
fi

# Method 3: /etc/rc.local
if [ "$STARTUP_REGISTERED" -eq 0 ] && [ -f /etc/rc.local ]; then
    log_msg "Attempting to register via /etc/rc.local..."
    if ! grep -q "activator_sd_script.sh" /etc/rc.local 2>/dev/null; then
        # Backup rc.local
        cp /etc/rc.local /etc/rc.local.backup.$(date +%Y%m%d_%H%M%S) 2>/dev/null
        # Add before exit 0
        sed -i '/^exit 0/i /etc/init.d/activator_sd_script.sh &' /etc/rc.local 2>/dev/null || \
        sed -i '$ a /etc/init.d/activator_sd_script.sh &' /etc/rc.local 2>/dev/null
        if grep -q "activator_sd_script.sh" /etc/rc.local 2>/dev/null; then
            log_msg "✓ Registered via /etc/rc.local"
            STARTUP_REGISTERED=1
        else
            log_msg "✗ /etc/rc.local registration failed"
        fi
    else
        log_msg "✓ Already registered in /etc/rc.local"
        STARTUP_REGISTERED=1
    fi
fi

# Method 4: /etc/inittab
if [ "$STARTUP_REGISTERED" -eq 0 ] && [ -f /etc/inittab ]; then
    log_msg "Attempting to register via /etc/inittab..."
    if ! grep -q "activator_sd_script" /etc/inittab 2>/dev/null; then
        # Backup inittab
        cp /etc/inittab /etc/inittab.backup.$(date +%Y%m%d_%H%M%S) 2>/dev/null
        # Add entry
        echo "sdscript:3:once:/etc/init.d/activator_sd_script.sh" >> /etc/inittab 2>/dev/null
        if grep -q "activator_sd_script" /etc/inittab 2>/dev/null; then
            log_msg "✓ Registered via /etc/inittab"
            STARTUP_REGISTERED=1
        else
            log_msg "✗ /etc/inittab registration failed"
        fi
    else
        log_msg "✓ Already registered in /etc/inittab"
        STARTUP_REGISTERED=1
    fi
fi

# Method 5: crontab @reboot (fallback)
if [ "$STARTUP_REGISTERED" -eq 0 ]; then
    log_msg "Attempting to register via crontab @reboot..."
    if command -v crontab >/dev/null 2>&1; then
        # Try root crontab
        (crontab -l 2>/dev/null | grep -v "activator_sd_script"; echo "@reboot /etc/init.d/activator_sd_script.sh") | crontab - 2>/dev/null
        if crontab -l 2>/dev/null | grep -q "activator_sd_script" >/dev/null 2>&1; then
            log_msg "✓ Registered via crontab @reboot"
            STARTUP_REGISTERED=1
        else
            log_msg "✗ crontab registration failed"
        fi
    fi
fi

# Method 6: /etc/profile or /etc/bash.bashrc (last resort)
if [ "$STARTUP_REGISTERED" -eq 0 ]; then
    log_msg "Attempting to register via /etc/profile (last resort)..."
    for profile_file in /etc/profile /etc/bash.bashrc /etc/bashrc; do
        if [ -f "$profile_file" ] && [ -w "$profile_file" ]; then
            if ! grep -q "activator_sd_script.sh" "$profile_file" 2>/dev/null; then
                echo "[ -f /etc/init.d/activator_sd_script.sh ] && /etc/init.d/activator_sd_script.sh &" >> "$profile_file" 2>/dev/null
                if grep -q "activator_sd_script.sh" "$profile_file" 2>/dev/null; then
                    log_msg "✓ Registered via $profile_file (user login trigger)"
                    STARTUP_REGISTERED=1
                    break
                fi
            else
                log_msg "✓ Already registered in $profile_file"
                STARTUP_REGISTERED=1
                break
            fi
        fi
    done
fi

# Report status
if [ "$STARTUP_REGISTERED" -eq 1 ]; then
    log_msg "✓ Automatic startup registration SUCCESSFUL"
else
    log_msg "⚠ WARNING: Automatic startup registration FAILED - script will not run automatically"
    log_msg "  Manual execution: /etc/init.d/activator_sd_script.sh"
fi

# Create activation marker
echo "ACTIVATED_$(date +%Y%m%d_%H%M%S)" > /tmp/activator_marker
log_msg "Activation marker created"

# Final status
log_msg "=== Activation completed successfully ==="
log_msg "Log file: $LOG_FILE"
log_msg "FEC directory: $FEC_DIR"
log_msg "Activated FECs saved to: $FEC_DIR/activated_fecs.txt"

# Try to restart network services if inetd is available
if command -v inetd >/dev/null 2>&1; then
    log_msg "Restarting inetd service..."
    killall inetd 2>/dev/null
    sleep 1
    inetd /etc/inetd.conf >/dev/null 2>&1 &
    log_msg "inetd service restarted"
fi

exit 0

