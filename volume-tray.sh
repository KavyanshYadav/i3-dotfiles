#!/bin/bash

# Terminate already running pasystray instances
killall -q pasystray

# Wait until the processes have been shut down
while pgrep -u $UID -x pasystray >/dev/null; do sleep 0.5; done

# Launch pasystray
pasystray &
