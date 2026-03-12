import os
import sys
import subprocess
import configparser

# Hidden config file in the current directory
CONFIG_FILENAME = ".scp_transfer.conf"

# ──────────────────────────────────────────
# CONFIG FILE FUNCTIONS
# ──────────────────────────────────────────

def get_config_path():
    """Returns the full path to the config file in the current directory."""
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), CONFIG_FILENAME)

def config_exists():
    """Returns True if the hidden config file exists."""
    return os.path.isfile(get_config_path())

def load_config():
    """
    Reads the .conf file and returns a config dict.
    Returns None if the file doesn't exist or is malformed.
    """
    path = get_config_path()
    if not os.path.isfile(path):
        return None

    parser = configparser.ConfigParser()
    try:
        parser.read(path, encoding='utf-8')
        config = {
            'user': parser.get('SCP', 'user'),
            'host': parser.get('SCP', 'host'),
            'path': parser.get('SCP', 'path'),
        }
        return config
    except (configparser.Error, KeyError):
        return None

def save_config(config):
    """
    Writes the config dict to the hidden .conf file.
    Sets the hidden attribute on Windows automatically.
    """
    path = get_config_path()

    # On Windows, remove hidden/read-only attributes before writing
    if os.name == 'nt' and os.path.isfile(path):
        subprocess.run(['attrib', '-H', '-R', path], capture_output=True)

    parser = configparser.ConfigParser()
    parser['SCP'] = {
        'user': config['user'],
        'host': config['host'],
        'path': config['path'],
    }
    with open(path, 'w', encoding='utf-8') as f:
        f.write("# SCP Transfer Utility - Configuration File\n")
        f.write("# Do not edit manually unless you know what you are doing.\n\n")
        parser.write(f)

    # Re-apply hidden attribute on Windows
    if os.name == 'nt':
        subprocess.run(['attrib', '+H', path], capture_output=True)

def delete_config():
    """Deletes the config file if it exists."""
    path = get_config_path()
    if os.path.isfile(path):
        os.remove(path)

# ──────────────────────────────────────────
# SCREEN / UI HELPERS
# ──────────────────────────────────────────

def clear_screen():
    """Clears the terminal screen."""
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def print_header():
    print("=" * 50)
    print("   AUTOMATIC SCP TRANSFER UTILITY")
    print("=" * 50)
    print()

# ──────────────────────────────────────────
# CONFIGURATION SETUP
# ──────────────────────────────────────────

def ask_config(current=None):
    """
    Prompts the user for configuration values.
    If current is provided, uses those as defaults (for 'Change config' flow).
    Returns a config dict.
    """
    default_user = current['user'] if current else "default"
    default_host = current['host'] if current else "x.x.x.x"
    default_path = current['path'] if current else "/"

    print("--- SYSTEM CONFIGURATION ---")
    print("(Press Enter to keep current value)\n")

    user_input = input(f"Remote Username (current: {default_user}): ").strip()
    if not user_input:
        user_input = default_user

    host_input = input(f"Remote Host IP (current: {default_host}): ").strip()
    if not host_input:
        host_input = default_host

    path_input = input(f"Remote Directory Path (current: {default_path}): ").strip()
    if not path_input:
        path_input = default_path

    config = {
        'user': user_input,
        'host': host_input,
        'path': path_input,
    }

    return config

def show_config(config):
    print("\nConfiguration:")
    print(f"  - User : {config['user']}")
    print(f"  - Host : {config['host']}")
    print(f"  - Path : {config['path']}")
    print("-" * 30)

# ──────────────────────────────────────────
# SCP OPERATIONS
# ──────────────────────────────────────────

def send_file(local_filename, remote_user, remote_host, remote_path):
    """
    Sends a local file to the remote server using SCP.
    Returns True if successful, False otherwise.
    """
    clean_remote_path = remote_path.rstrip('/') + '/'
    full_remote_target = f"{remote_user}@{remote_host}:{clean_remote_path}{local_filename.split('/')[-1]}"

    try:
        print(f"\nAttempting to upload '{local_filename}'...")
        result = subprocess.run(
            ['scp', local_filename, full_remote_target],
            capture_output=True,
            text=True,
            timeout=120
        )
        if result.returncode == 0:
            print("\n  File sent successfully.")
            return True
        else:
            print("\n  Error sending file.")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"\n  Connection error or system failure: {e}")
        return False

def receive_file(remote_user, remote_host, remote_path, filename):
    """
    Receives a file from the remote server using SCP.
    Saves it to current directory.
    Returns True if successful, False otherwise.
    """
    clean_remote_path = remote_path.rstrip('/') + '/'
    source_path = f"{remote_user}@{remote_host}:{clean_remote_path}{filename}"

    try:
        print(f"\nAttempting to download '{filename}'...")
        result = subprocess.run(
            ['scp', source_path, './'],
            capture_output=True,
            text=True,
            timeout=120
        )
        if result.returncode == 0:
            print("\n  File received successfully.")
            return True
        else:
            print("\n  Error receiving file.")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"\n  Connection error or system failure: {e}")
        return False

# ──────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────

def main():
    clear_screen()
    print_header()

    # ── First run vs returning user ──
    config = load_config()

    if config is None:
        # First time: ask for values and save them
        print("No configuration found. Let's set it up.\n")
        config = ask_config()
        save_config(config)
        print("\n  Configuration saved.")
        show_config(config)
        input("Press [Enter] to start the menu...")
    else:
        # Config exists: show loaded values and go straight to menu
        print("  Configuration loaded from file.")
        show_config(config)
        input("Press [Enter] to continue...")

    # ── Main menu loop ──
    while True:
        clear_screen()
        print_header()
        print(f"  Connected to: {config['user']}@{config['host']}:{config['path']}")
        print()
        print("=" * 50)
        print("         MAIN MENU")
        print("=" * 50)
        print("  1 - Send file to remote computer")
        print("  2 - Receive file from remote computer")
        print("  3 - Change config settings")
        print("  4 - Exit program")
        print()

        choice = input("Select an option (1-4): ").strip()

        if choice == '1':
            filename = input("\nEnter local filename with extension: ").strip()
            if not os.path.exists(filename):
                print(f"\n  ERROR: File '{filename}' does not exist.")
            else:
                send_file(filename, config['user'], config['host'], config['path'])
            input("\nPress Enter to return to menu...")

        elif choice == '2':
            filename = input("\nEnter remote filename with extension: ").strip()
            receive_file(config['user'], config['host'], config['path'], filename)
            input("\nPress Enter to return to menu...")

        elif choice == '3':
            clear_screen()
            print_header()
            print("--- CHANGE CONFIGURATION ---\n")
            config = ask_config(current=config)
            save_config(config)
            print("\n  Configuration updated and saved.")
            show_config(config)
            input("Press [Enter] to return to menu...")

        elif choice == '4':
            print("\nShutting down script...")
            break

        else:
            print("\n  Invalid option. Please try again.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()