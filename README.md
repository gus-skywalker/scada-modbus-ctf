# HOW TO

# Docker Build
docker build -t my_novnc_image .

# X86_64
docker run -d -p 5020:5020 -p 5901:5901 -p 6080:6080 --name my_novnc_container my_novnc_image

# ARM
docker run -d --platform linux/amd64 -p 5020:5020 -p 5901:5901 -p 6080:6080 --name my_novnc_container my_novnc_image

# Virtual Networking Computing (VNC) Connection
localhost:5900
passwd: 123456

# noVNC
http://localhost:6080/vnc.html


# file .vnc/xstartup
#!/bin/sh
xrdb $HOME/.Xresources
xsetroot -solid black
xrandr -s 640x480
cd ~/virtuaplant/plants/oil-refinery
while true; do
 ~/virtuaplant_venv/bin/python ./oil_world.py -t 0.0.0.0
done

 # vnc.service
[Unit]
Description=VNC Service
After=network.target

[Service]
Type=forking
User=plant
ExecStartPre=-/usr/bin/vncserver -kill :1 > /dev/null 2>&1
ExecStart=/usr/bin/vncserver -depth 16 -geometry 640x480 :1
ExecStop=/usr/bin/vncserver -kill :1

[Install]
WantedBy=multi-user.target

# vncproxy.service
[Unit]
Description=VNC proxy service
After=network.target

[Service]
Type=simple
Restart=always
RestartSec=1
User=plant
ExecStart=/home/plant/noVNC/utils/launch.sh --vnc localhost:5901

[Install]
WantedBy=multi-user.target
