import subprocess
import re

# Run "arp -a" to get a list of devices
arp_output = subprocess.check_output("arp -a", shell=True, text=True)

# Find all IP addresses in the arp output
ip_addresses = re.findall(r'\d+\.\d+\.\d+\.\d+', arp_output)

# Print all found IPs (even the ones we won't ping)
print("🔍 Found IPs on the network:")
for ip in ip_addresses:
    print(f" - {ip}")

# Define a list of known "bad" addresses we don't want to ping
excluded_ips = {"10.0.0.255", "255.255.255.255"}

# Filter out only the valid IPs for pinging
valid_ips = [ip for ip in ip_addresses if ip.startswith("10.") and ip not in excluded_ips]

# Print valid IPs before pinging
print("\n✅ Pinging these IPs:")
for ip in valid_ips:
    print(f" - {ip}")

# If there are valid IPs, open CMD and ping them
if valid_ips:
    ping_commands = " & ".join([f"ping -n 4 {ip}" for ip in valid_ips])
    subprocess.Popen(["cmd", "/k", ping_commands], creationflags=subprocess.CREATE_NEW_CONSOLE)
else:
    print("\n⚠️ No valid IPs to ping.")
