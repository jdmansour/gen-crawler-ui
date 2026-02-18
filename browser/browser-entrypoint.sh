#!/bin/sh
set -e

# Start Xvfb (virtual display)
Xvfb :99 -screen 0 1920x1080x24 -nolisten tcp &
export DISPLAY=:99
sleep 1

# Start Chrome with CDP on internal port 9223 (binds to 127.0.0.1 only)
chrome \
    --no-sandbox \
    --disable-gpu \
    --disable-dev-shm-usage \
    --no-first-run \
    --no-default-browser-check \
    --force-device-scale-factor=2 \
    --remote-debugging-port=9223 \
    --remote-allow-origins=* \
    --disable-extensions-except=$UBOL_EXT_PATH,$ISDCAC_EXT_PATH \
    --load-extension=$UBOL_EXT_PATH,$ISDCAC_EXT_PATH &

# Wait for Chrome to be ready
echo "Waiting for Chrome CDP on 127.0.0.1:9223..."
until curl -sf http://127.0.0.1:9223/json/version > /dev/null 2>&1; do
    sleep 0.5
done
echo "Chrome CDP is ready, starting socat proxy on 0.0.0.0:9222"

# Forward external port 9222 to Chrome's internal port 9223
exec socat TCP-LISTEN:9222,fork,reuseaddr,bind=0.0.0.0 TCP:127.0.0.1:9223
