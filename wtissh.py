import os
import datetime
import time
import re

try:
    import paramiko
except ImportError:
    print("The 'paramiko' modules is required for this code.")
    exit(1)

# Global session log file
session_log_file = None

# Load devices
def load_devices(filename):
    devices = []
    with open(filename, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 3:
                devices.append({'ip': parts[0], 'username': parts[1], 'password': parts[2]})
    return devices

# Create outputs folder and session log
def create_session_log():
    global session_log_file
    folder = "outputs"
    os.makedirs(folder, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
    session_log_file = os.path.join(folder, f"Results_{timestamp}.txt")
    with open(session_log_file, 'w', encoding='utf-8') as f:
        f.write(f"Session started at {timestamp}\n\n")

# Append output to session log
def append_to_session_log(content):
    global session_log_file
    with open(session_log_file, 'a', encoding='utf-8') as f:
        f.write(content)

# Wait for output to start and stop
def wait_for_output(channel, initial_timeout=6, idle_timeout=2):
    buffer = ''
    start_time = time.time()
    last_data_time = None

    while True:
        if channel.recv_ready():
            data = channel.recv(4096).decode('utf-8', errors='ignore')
            buffer += data
            last_data_time = time.time()
        else:
            now = time.time()
            if last_data_time:
                if now - last_data_time >= idle_timeout:
                    break
            elif now - start_time >= initial_timeout:
                break
            time.sleep(0.05)  # faster checking
    return buffer

# Run commands on a device
def run_commands_on_device(device, commands, save_output):
    ip = device['ip']
    username = device['username']
    password = device['password']

    print(f"[→] Running on {ip}...")

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(
            hostname=ip,
            username=username,
            password=password,
            timeout=5,
            allow_agent=False,
            look_for_keys=False,
        )
        channel = client.invoke_shell()
        channel.settimeout(2)

        # Flush initial banner
        try:
            while channel.recv_ready():
                channel.recv(4096)
        except Exception:
            pass

        # Send Enter to wake up prompt
        channel.send('\r')
        time.sleep(1)
        wait_for_output(channel)

        full_output = ""

        for cmd in commands:
            channel.send(cmd + '\r')
            time.sleep(0.2)  # Small pause after sending
            output = wait_for_output(channel)

            full_output += f"\n\n===== Command: {cmd} =====\n{output}\n"

        # Save to log if enabled
        if save_output:
            cleaned_output = clean_output(f"\n\n===== Device: {ip} =====\n{full_output}\n")
            append_to_session_log(cleaned_output)

        print(f"[✔] Done {ip}")

    except Exception as e:
        print(f"[✖] Failed {ip}: {e}")

    finally:
        client.close()

def clean_output(text):
    # Normalize line endings
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    # Remove multiple consecutive newlines
    cleaned = re.sub(r'\n+', '\n', text)
    return cleaned.strip()

# Main
def main():
    devices = load_devices('terminal_devices.txt')

    if not devices:
        print("No devices found in terminal_devices.txt")
        return

    print(f"Devices loaded: {len(devices)} devices.\n")

    # Predefined command list
    commands = [
        '/bash free',
        '/bash df -h',
        '/j*',
        '/bash uptime',
    ]

    save_output = input("\nSave output to file? (y/n): ").strip().lower() == 'y'

    if save_output:
        create_session_log()

    # ✅ Only after commands are entered, start testing devices:
    for idx, device in enumerate(devices, start=1):
        print(f"\n[→] Testing device {idx} of {len(devices)} ({device['ip']})...")
        run_commands_on_device(device, commands, save_output)

if __name__ == "__main__":
    main()
