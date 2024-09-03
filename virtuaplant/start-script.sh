#!/bin/bash

# Start Xvfb
Xvfb :99 -screen 0 1024x768x24 &
export DISPLAY=:99

# Start fluxbox
fluxbox &

# Start x11vnc
x11vnc -forever -usepw -display :99 &

# Executar o script Python
cd /app/plants/oil-refinery
./start.sh

# Manter o container ativo
tail -f /dev/null

# docker run -it --rm --shm-size=256m -p 5020:5020 -p 5900:5900 my_vnc_image
