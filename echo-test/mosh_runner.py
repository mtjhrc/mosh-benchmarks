#!/usr/bin/env python3

import os
import sys
import re
import subprocess
from os.path import abspath

# Note:
# This script assumes ../bin/create_ns.sh has been run.
# This script has to be ran using sudo, 
# (or as root and with the SUDO_USER env variable set)
assert len(sys.argv) == 3
mode = sys.argv[1]
assert mode in ("UDP", "TCP")
output_dir = sys.argv[2]

user = os.environ["SUDO_USER"]

test_bin = abspath("build/echo-test")
termrec_bin = abspath("../prefix/bin/termrec")
mosh_server_bin = abspath("../bin/mosh-server")
mosh_client_bin = abspath("../bin/mosh-client")

CONNECT_RE = re.compile("^MOSH CONNECT (?:TCP )?(\\d+) (\\S+)$");

server_cmd = ["ip", "netns", "exec", "ns_server",
              "sudo", "-E","-u", user, "--",
              mosh_server_bin, 
              "new", 
              "-i", 
              "0.0.0.0",
              "-m",
              mode
             ]

print("Running server:")
print(" ".join(server_cmd))

common_env = {
    "PATH": os.environ["PATH"],
    "LANG": "en_US.UTF-8",
    "LC_ALL": "en_US.UTF-8",
    "TERM": "xterm-256color"
}

if value := os.environ.get("MOSH_TCP_THIN"):
    common_env["MOSH_TCP_THIN"] = value

# set the "SHELL" to be our test program 
server_env = common_env.copy()
server_env["SHELL"] = test_bin
server_proc = subprocess.Popen(server_cmd, stdout = subprocess.PIPE, env = server_env, text = True)

port = None
key = None
server_output = []
for line in server_proc.stdout:
    search = CONNECT_RE.search(line)
    if search:
        print("Found connection string:", search.group(0))
        port = search.group(1)
        key = search.group(2)
        break
    else:
        server_output.append(line)

assert key is not None and port is not None, f"Didn't find connect string:\n {'\n'.join(server_output)}"
print("Started mosh server")

client_cmd = ["ip", "netns", "exec", "ns_client",
        "sudo", "-E", "-u", user, "--",
        termrec_bin, "record", "--child-stderr", "/dev/null", "-i", "build/input.termrec", "-d", output_dir, "--",
        mosh_client_bin, "10.0.0.1", port
    ]
print("Running client:")
print(" ".join(client_cmd))
client_env = common_env.copy()
client_env["MOSH_TRANSPORT_MODE"] = mode
client_env["MOSH_KEY"] = key
#client_env["RUST_LOG"] = "trace"
os.execvpe(client_cmd[0], client_cmd, client_env)        
