#!/bin/sh
# Tailscale status widget for tmux status bar.
# Outputs: green lock + name + IP when connected; red lock + "down" when not.
command -v tailscale >/dev/null 2>&1 || exit 0
TS_JSON=$(tailscale status --json 2>/dev/null) python3 -c '
import os, json
try:
    d = json.loads(os.environ.get("TS_JSON", "{}"))
    if d.get("BackendState") == "Running":
        node = d.get("Self", {})
        ips = node.get("TailscaleIPs", [])
        ip4 = next((ip for ip in ips if ":" not in ip), "?")
        name = node.get("HostName", "?")
        print("#[fg=#a6e3a1]\uf023 #[fg=#cdd6f4] " + name + "  " + ip4 + "#[default]")
    else:
        print("#[fg=#f38ba8]\uf023  down#[default]")
except Exception:
    pass
' 2>/dev/null
