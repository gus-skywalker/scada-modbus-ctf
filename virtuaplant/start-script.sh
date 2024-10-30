#!/bin/bash

# Configuração de .Xauthority e VNC
touch ~/.Xauthority
xauth add :1 . $(mcookie)

# Limpar locks e matar sessões VNC existentes
rm -f /tmp/.X11-unix/X1
rm -f /tmp/.X1-lock
vncserver -kill :1 2> /dev/null || true

# Configurar senha do VNC 
echo "Configurando senha para o TightVNC..."
mkdir -p ~/.vnc
echo "password" | vncpasswd -f > ~/.vnc/passwd
chmod 600 ~/.vnc/passwd

# Iniciar o servidor VNC no display :1
vncserver :1 -geometry 640x480 -depth 24

# Iniciar o noVNC para conectar ao TightVNC na porta 5901 e expor na porta 6080
/app/noVNC/utils/novnc_proxy --vnc localhost:5901 --listen 80 &

# Função para iniciar e monitorar `oil_world.py`
start_oil_world() {
    cd /app/plants/oil-refinery

    while true; do
        echo "Iniciando o processo oil_world.py"
        ./oil_world.py -t localhost &

        # Pegar o PID do processo `oil_world.py`
        OIL_WORLD_PID=$!

        # Aguardar o script `oil_world.py` estar ativo na porta 5020
        echo "Aguardando o script oil_world.py iniciar completamente na porta 5020..."
        while ! timeout 1 bash -c "</dev/tcp/localhost/5020"; do
            sleep 1
        done
        echo "oil_world.py iniciado e ativo na porta 5020."

        # Monitorar o processo e reiniciar se ele falhar
        wait $OIL_WORLD_PID
        echo "oil_world.py parou. Reiniciando em 1 segundos..."
        sleep 1
    done
}

# Iniciar o processo `oil_world.py` e aguardar sua inicialização
start_oil_world &

# Aguardar a disponibilidade da porta 5020 antes de continuar
echo "Aguardando disponibilidade da porta 5020 para iniciar outros processos..."
while ! timeout 1 bash -c "</dev/tcp/localhost/5020"; do
    sleep 1
done
echo "Porta 5020 disponível. Iniciando outros processos..."

# Função para iniciar e monitorar `flag_manager.py`
start_flag_manager() {
    cd /app/plants/oil-refinery
    while true; do
        echo "Iniciando flag_manager.py"
        ./flag_manager.py || echo "Erro ao iniciar flag_manager.py"
        echo "flag_manager.py parou. Reiniciando em 1 segundos..."
        sleep 1
    done
}

# Função para iniciar e monitorar `plant_manager.py`
start_plant_manager() {
    cd /app/plants/oil-refinery
    while true; do
        echo "Iniciando plant_manager.py"
        ./plant_manager.py || echo "Erro ao iniciar plant_manager.py"
        echo "plant_manager.py parou. Reiniciando em 1 segundo..."
        sleep 1
    done
}

# Iniciar `flag_manager.py` e `plant_manager.py` com monitoramento
start_flag_manager &
start_plant_manager &

# Manter o container ativo
tail -f /dev/null
