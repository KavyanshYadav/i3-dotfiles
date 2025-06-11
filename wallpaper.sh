#!/bin/bash

# Define paths to your wallpapers
WALLPAPER1="/home/aufvim/wallpaper.png"
WALLPAPER2="/path/to/wallpaper_monitor2.jpg"

# Run your calendar script to generate a dynamic wallpaper for one monitor
# Assuming calendar.py generates to a specific known path, e.g., ~/Pictures/calendar_wallpaper.png
/usr/bin/python3 ./calander.py --ratio16x9
CALENDAR_WALLPAPER="/home/aufvim/life_calendar_16x9.png" # Adjust path as needed

# Determine which monitor gets which wallpaper.
# The order of images in feh corresponds to the order xrandr lists active outputs.
# You might need to adjust this order based on your xrandr output.

# Example: Monitor 1 (e.g., laptop screen) gets calendar, Monitor 2 (e.g., external) gets static.
# Replace HDMI-1 and eDP-1 with your actual monitor names from xrandr
MONITOR1_NAME="eDP-1"    # Your primary monitor (e.g., laptop screen)
MONITOR2_NAME="HDMI-1-0" # Your second monitor

# Check if monitors are connected. feh will complain if they're not.
#<F15>if xrandr | grep -q "$MONITOR1_NAME connected"; then
#  feh --bg-fill "$CALENDAR_WALLPAPER" --output "$MONITOR1_NAME"
#fi

#if xrandr | grep -q "$MONITOR2_NAME connected"; then
#  feh --bg-fill "$WALLPAPER1" --output "$MONITOR2_NAME"
#fi

# Alternative: if feh --no-xinerama is available and works for you
# This might apply wallpapers independently to each screen if xinerama is not used.
# However, for different images per monitor, specifying --output is more explicit.
#feh --no-xinerama --bg-fill "$CALENDAR_WALLPAPER" "$WALLPAPER1" # This might put them side-by-side on a single virtual screen. Test carefully.

# The most robust way is to use --output for each monitor:
feh --bg-fill "$CALENDAR_WALLPAPER" --output "$MONITOR1_NAME" --bg-fill "$WALLPAPER1" --output "$MONITOR2_NAME"
# This command sets the background for specific outputs directly.
