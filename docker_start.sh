#!/usr/bin/env bash

set -e

# generate the deovr json file once on startup then loop
python /syndra/main.py &

# start nginx
nginx -g 'daemon off;'
