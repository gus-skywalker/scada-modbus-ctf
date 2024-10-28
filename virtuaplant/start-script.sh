#!/bin/bash

# Start Xvfb
rm -f /tmp/.X99-lock
Xvfb :99 -screen 0 1024x768x24 &
export DISPLAY=:99
sleep 3

# Start fluxbox
fluxbox &
sleep 3

# Start x11vnc
x11vnc -forever -nopw -display :99 -rfbport 5901 &
sleep 3

# Start noVNC in a loop to ensure it restarts if it crashes
while true; do
    /app/noVNC/utils/novnc_proxy --vnc localhost:5901 --listen 6080
    echo "noVNC proxy crashed. Restarting in 5 seconds..."
    sleep 5
done &

# Executar o script Python
cd /app/plants/oil-refinery
./oil_world.py -t localhost

# Manter o container ativo
tail -f /dev/null
