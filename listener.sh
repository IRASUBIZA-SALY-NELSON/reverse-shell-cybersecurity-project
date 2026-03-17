#!/bin/bash
LHOST=$(hostname -I | awk '{print $1}')
LPORT=4444
echo "[+] Listener: $LHOST:$LPORT"
echo "[+] Run game in other terminal..."
nc -lvnp $LPORT
