#!/bin/bash

# Configurar o arquivo .Xauthority
touch ~/.Xauthority
xauth add :1 . $(mcookie)

# Limpar locks e matar sessões VNC existentes
rm -f /tmp/.X11-unix/X1
rm -f /tmp/.X1-lock
vncserver -kill :1 2 > /dev/null || true

# Configurar senha do VNC (executar apenas se não estiver configurada)
if [ ! -f ~/.vnc/passwd ]; then
    echo "Configurando senha para o TightVNC..."
    mkdir -p ~/.vnc
    echo "password" | vncpasswd -f > ~/.vnc/passwd
    chmod 600 ~/.vnc/passwd
fi

# Iniciar o servidor VNC no display :1
vncserver :1 -geometry 640x480 -depth 24

# Manter o script ativo para evitar reinicializações
tail -f /dev/null
