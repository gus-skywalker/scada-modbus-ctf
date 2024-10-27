#!/bin/bash

# Remove any existing X lock file
rm -f /tmp/.X99-lock

# Start Xvfb
Xvfb :99 -screen 0 1024x768x24 &
export DISPLAY=:99

# Check if Xvfb started successfully
# if ! xset q &>/dev/null; then
#     echo "Error: DISPLAY :99 not accessible."
#     exit 1
# fi

# Start fluxbox
fluxbox &

# Start x11vnc
x11vnc -forever -usepw -display :99 &

# Navegar para o diretório correto e iniciar o script da aplicação
cd /app/plants/oil-refinery
./start.sh

# Manter o contêiner ativo apenas se não houver logs
tail -f /dev/null
