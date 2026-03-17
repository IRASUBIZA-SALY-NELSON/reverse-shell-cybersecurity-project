#!/bin/bash
# Save as listener.sh and run: bash listener.sh

LHOST=$(hostname -I | awk '{print $1}')
LPORT=4444

echo "[+] Starting listener on $LHOST:$LPORT"
echo "[+] Run: nc -lvnp $LPORT"

while true; do
    nc -lvnp $LPORT
done
