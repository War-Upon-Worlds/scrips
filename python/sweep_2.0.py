import subprocess
import re

# Run "arp -a" to get a list of devices
arp_output = subprocess.check_output("arp -a", shell=True, text=True)

# Find all IP addresses in the ARP output
ip_addresses = re.findall(r'\d+\.\d+\.\d+\.\d+', arp_output)

# Define a list of known "bad" addresses we don't want to ping
excluded_ips = {"10.0.0.255", "255.255.255.255"}

# Filter only the valid IPs (ignoring broadcast/multicast addresses)
valid_ips = [ip for ip in ip_addresses if ip.startswith("10.") and ip not in excluded_ips]

# Prepare the command to run in a new CMD window
cmd_script = 'echo Found IPs on the network: & '
cmd_script += ' & '.join([f'echo - {ip}' for ip in ip_addresses])  # Print all found IPs
cmd_script += ' & echo. & echo Valid IPs to ping: & '
cmd_script += ' & '.join([f'echo - {ip}' for ip in valid_ips])  # Print valid IPs
cmd_script += ' & echo. & echo Pinging valid IPs... & '
cmd_script += ' & '.join([f'ping -n 4 {ip}' for ip in valid_ips]) if valid_ips else 'echo No valid IPs to ping.'

# Open a new CMD window and execute the script
subprocess.Popen(["cmd", "/k", cmd_script], creationflags=subprocess.CREATE_NEW_CONSOLE)
