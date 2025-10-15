#!/usr/bin/env bash

# Kill any previous compositor or wallpaper daemon
pkill picom

# compositor
picom --config "$HOME/.config/picom/picom.conf" &

# wallpaper
xwallpaper --zoom "$HOME/Pictures/wallpapers/current.jpg" &

