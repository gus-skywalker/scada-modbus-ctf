# HOW TO

# Docker Build
docker build -t my_novnc_image .

# X86_64
docker run -d -p 5020:5020 -p 5900:5900 -p 6080:6080 --name my_novnc_container my_novnc_image

# ARM
docker run -d --platform linux/amd64 -p 5020:5020 -p 5900:5900 -p 6080:6080 --name my_novnc_container my_novnc_image

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

 