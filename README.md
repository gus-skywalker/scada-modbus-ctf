# HOW TO

# Docker Build
docker build -t my_vnc_image .

# X86_64
docker run -it -p 5020:5020 -p 5900:5900 my_vnc_image /bin/bash

# ARM
docker run --platform linux/amd64 -it --rm -p 5020:5020 -p 5900:5900 my_vnc_image

# Virtual Networking Computing (VNC) Connection
localhost:5900
passwd: 123456

