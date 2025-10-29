#!/usr/bin/env bash

# Kill any previous compositor or wallpaper daemon
pkill -9 picom
sleep 0.5

# compositor
picom --config "$HOME/.config/picom/picom.conf" &

# wallpaper
xwallpaper --zoom "$HOME/Pictures/wallpapers/current.jpg" &

# clipboard manager
pkill greenclip
greenclip daemon &

