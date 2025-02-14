import subprocess

# Command to execute
commands = "ping /? & ping -n 4 10.0.0.1"

# Open a new command prompt and execute the ping command
subprocess.run(["cmd", "/k", commands])
