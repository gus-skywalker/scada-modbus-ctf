# Use a base image with Python 2.7
FROM --platform=linux/amd64 python:2.7

# Install system dependencies
RUN apt-get update && \
    apt-get install -y \
    gcc \
    build-essential \
    cmake \
    libglib2.0-dev \
    libgtk-3-dev \
    libsdl1.2-dev \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libgirepository1.0-dev \
    libx11-dev \
    libxext-dev \
    libxi-dev \
    libxrandr-dev \
    libxinerama-dev \
    libxcursor-dev \
    libxfixes-dev \
    libxss-dev \
    libxtst-dev \
    python-pygame \
    python-gobject \
    python-pip \
    python-dev \
    libffi-dev \
    libportmidi-dev \
    git \
    unzip \
    curl \
    x11vnc \
    fluxbox \
    xvfb \
    xterm \
    supervisor \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Remover ALSA se som não for necessário
RUN apt-get remove -y alsa-utils libasound2

# Update pip and install setuptools
RUN pip install --upgrade pip setuptools

# Install PyGObject and necessary libraries
RUN apt-get update && \
    apt-get install -y python-gi gir1.2-gtk-3.0

# Set the working directory
WORKDIR /app

# Copy application code and script
COPY virtuaplant .

# Make the script executable
RUN chmod +x start-script.sh

# Install Python dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Install additional Python dependencies
RUN pip install --no-cache-dir Twisted==15.0.0 pymunk==4.0.0 pymodbus==1.2.0 pyasn1==0.1.7 pycrypto==2.6.1

# Install PyGObject and pygame
RUN pip install --no-cache-dir PyGObject pygame

# Variáveis de ambiente para o servidor Modbus
ENV MODBUS_HOST=localhost
ENV MODBUS_PORT=5020
ENV DISPLAY=:99

# Instalação global do NumPy para o websockify
# RUN pip install numpy==1.16.6

# Install noVNC (websockify will be installed automatically)
RUN git clone https://github.com/novnc/noVNC.git /app/noVNC

# Configure Xvfb and VNC server
RUN mkdir ~/.vnc

# Expose necessary ports
EXPOSE 5020 5901

# Start the VNC server, noVNC, and the application using the script
# ENTRYPOINT ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
# ENTRYPOINT ["sh", "-c", "Xvfb :1 -screen 0 1024x768x24 & export DISPLAY=:1 && fluxbox & sleep 5 && x11vnc -forever -nopw -display :1 -rfbport 5901 & /app/noVNC/utils/novnc_proxy --vnc localhost:5901 --listen 6080 & sleep 5 && cd /app/plants/oil-refinery && ./start.sh && tail -f /dev/null"]
ENTRYPOINT ["/app/start-script.sh"]