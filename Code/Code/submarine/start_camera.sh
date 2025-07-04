#!/bin/bash
# start_camera.sh
/usr/local/bin/mjpg_streamer -o "output_http.so -p 8080" -i "input_uvc.so -n -f 10 -r 1280x720"