#!/bin/bash

# Remove any existing X lock file
rm -f /tmp/.X99-lock

# Navegar para o diretório correto e iniciar o script da aplicação
cd /app/plants/oil-refinery
./start.sh

# Manter o contêiner ativo apenas se não houver logs
tail -f /dev/null