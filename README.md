# SCP Transfer Utility

A lightweight Python CLI tool for transferring files to and from a remote server via SCP. Saves connection settings to a hidden local config file so you only configure it once.

##  Features

- **Send & Receive files** via SCP with a simple numbered menu.
- **Persistent configuration**: saves `user`, `host`, and `path` to a hidden `.scp_transfer.conf` file after first run.
- **Auto-load**: on subsequent runs, configuration is loaded automatically — no re-typing needed.
- **Change settings anytime** from the main menu without restarting the script.
- **Cross-platform**: works on Windows and Linux/macOS. On Windows, the config file is automatically marked as hidden via `attrib +H`.
- **No external dependencies**: uses only Python standard library modules.

##  Prerequisites

No external libraries required. Standard library only:
- `os`
- `sys`
- `subprocess`
- `configparser`

**Python Version:** Compatible with Python 3.x

**System requirement:** `scp` must be available in your system PATH (comes with OpenSSH, installed by default on Linux/macOS and available on Windows 10+).

##  Installation

1. Download or clone `scp_transfer.py` to any folder.
2. Open a terminal in that folder.
3. Run the script:
```bash
python scp_transfer.py
```

##  Usage

### First Run

On the first execution, the script will prompt you for connection details:
```
Remote Username (current: default): myuser
Remote Host IP (current: x.x.x.x): 192.168.1.100
Remote Directory Path (current: /): /home/myuser/transfers/
```

These values are saved to `.scp_transfer.conf` in the same directory as the script. On Windows, the file is automatically hidden.

### Subsequent Runs

The script detects the config file and loads it automatically, taking you straight to the main menu.

### Main Menu
```
==================================================
         MAIN MENU
==================================================
  1 - Send file to remote computer
  2 - Receive file from remote computer
  3 - Change config settings
  4 - Exit program
```

- **Option 1**: enter a local filename (e.g. `report.pdf`) and it will be uploaded to the configured remote path.
- **Option 2**: enter a remote filename and it will be downloaded to the current directory.
- **Option 3**: re-prompts all config fields showing current values as defaults. Saves and overwrites the `.conf` file.
- **Option 4**: exits the script.

##  Config File

The config file is stored as `.scp_transfer.conf` in the script's directory. Example contents:
```ini
# SCP Transfer Utility - Configuration File
# Do not edit manually unless you know what you are doing.

[SCP]
user = myuser
host = 192.168.1.100
path = /home/myuser/transfers/
```

You can edit it manually if needed, but using **Option 3** from the menu is the recommended way.

On Windows, the file is hidden automatically using `attrib +H`. Before overwriting it, the script temporarily removes the hidden/read-only attribute and restores it after saving.

##  Troubleshooting

| Issue | Possible Cause | Solution |
|-------|----------------|----------|
| `scp: command not found` | OpenSSH not installed or not in PATH | Install OpenSSH or add it to your system PATH |
| `PermissionError` on config file | File locked by another process | Close any editor that may have the file open |
| Connection timeout | Host unreachable or firewall blocking port 22 | Verify the host IP and that SSH port 22 is open |
| File not found on send | Wrong filename or path | Ensure the file exists in the current working directory |
| Config not loading | Malformed `.conf` file | Delete `.scp_transfer.conf` and re-run to reconfigure |

##  License

This project is open-source and free to use for personal and commercial purposes.

---

*Developed for simple, scriptable file transfers over SSH.*
