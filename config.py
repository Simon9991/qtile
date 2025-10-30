from libqtile import bar, hook, layout, qtile, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen, ScratchPad, DropDown
from libqtile.lazy import lazy
import os
import subprocess

mod = "mod4"
terminal = "ghostty"
myTerm = terminal

# =============== THEME: TOKYONIGHT (Night) ===============
colors = {
    "bg": "#1a1b26",
    "bg_alt": "#16161e",
    "fg": "#c0caf5",
    "muted": "#565f89",
    "accent": "#7aa2f7",
    "accent2": "#f7768e",
    "green": "#9ece6a",
    "yellow": "#e0af68",
    "magenta": "#ad8ee6",
    "cyan": "#0db9d7",
    "music": "#0891b2",
    "music2": "#5e81ac",
    "line": "#444b6a",
    "black2": "#24283b",
}


def C(name):
    return colors[name]


# Global look
widget_defaults = dict(
    font="JetBrainsMono Nerd Font",
    fontsize=13,
    padding=8,
    background=C("bg"),
    foreground=C("fg"),
)
extension_defaults = widget_defaults.copy()

# =============== KEYS ===============
keys = [
    Key([mod], "h", lazy.layout.left(), desc="Focus left"),
    Key([mod], "l", lazy.layout.right(), desc="Focus right"),
    Key([mod], "j", lazy.layout.down(), desc="Focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Focus next"),
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move up"),
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Normalize sizes"),
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(), desc="Toggle split"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Terminal"),
    Key([mod], "Tab", lazy.next_layout(), desc="Next layout"),
    Key([mod], "q", lazy.window.kill(), desc="Kill window"),
    Key([mod], "f", lazy.window.toggle_fullscreen(), desc="Fullscreen"),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Quit Qtile"),
    Key([mod], "d", lazy.spawn("rofi -show drun -show-icons"), desc="Launcher"),
    Key(
        [mod],
        "v",
        lazy.spawn(
            "rofi -modi 'clipboard:greenclip print' -show clipboard -run-command '{cmd}'"
        ),
        desc="Clipboard history",
    ),
    # Screenshots
    Key(
        ["control"],
        "F12",
        lazy.spawn("/home/simon/.local/bin/screenshot-area"),
        desc="Shot area",
    ),
    Key(
        ["control"],
        "F12",
        lazy.spawn("/home/simon/.local/bin/screenshot-area"),
        desc="Shot area",
    ),
    Key([mod, "control"], "Print", lazy.spawn("peek"), desc="Screen recorder"),
    # Audio (PipeWire)
    Key([mod], "F12", lazy.spawn("wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%+")),
    Key([mod], "F11", lazy.spawn("wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%-")),
    # Media controls
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous"), desc="Previous track"),
    Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause"), desc="Play/Pause"),
    Key([], "XF86AudioNext", lazy.spawn("playerctl next"), desc="Next track"),
    # Scratchpads
    Key(
        [mod],
        "grave",
        lazy.group["scratch"].dropdown_toggle("term"),
        desc="Scratch terminal",
    ),
    Key(
        [mod, "shift"],
        "b",
        lazy.group["scratch"].dropdown_toggle("btop"),
        desc="btop scratch",
    ),
    Key(
        [mod],
        "c",
        lazy.group["scratch"].dropdown_toggle("calc"),
        desc="Calculator",
    ),
    Key(
        [mod],
        "n",
        lazy.group["scratch"].dropdown_toggle("notes"),
        desc="Notes/Todo",
    ),
    Key(
        [mod],
        "m",
        lazy.group["scratch"].dropdown_toggle("music"),
        desc="Music player",
    ),
]

# Optional: Wayland VT switch guard (harmless on X11)
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )

# =============== GROUPS ===============
groups = [Group(i) for i in "12345678"]
# Workspace 9: Discord/Vesktop auto-assign
groups.append(
    Group("9", matches=[Match(wm_class=["discord", "vesktop", "Discord", "Vesktop"])])
)
for i in groups:
    keys.extend(
        [
            Key([mod], i.name, lazy.group[i.name].toscreen(), desc=f"Go to {i.name}"),
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name),
                desc=f"Send to {i.name}",
            ),
        ]
    )

# ScratchPad
groups += [
    ScratchPad(
        "scratch",
        [
            DropDown(
                "term",
                myTerm,
                opacity=0.95,
                height=0.45,
                width=0.6,
                x=0.2,
                y=0.1,
                on_focus_lost_hide=True,
            ),
            DropDown(
                "btop",
                f"{myTerm} -e btop",
                opacity=0.95,
                height=0.6,
                width=0.7,
                x=0.15,
                y=0.05,
                on_focus_lost_hide=True,
            ),
            DropDown(
                "calc",
                "qalculate-gtk",
                opacity=0.95,
                height=0.5,
                width=0.4,
                x=0.3,
                y=0.2,
                on_focus_lost_hide=True,
            ),
            DropDown(
                "notes",
                f"{myTerm} -e nvim /home/simon/notes.md",
                opacity=0.95,
                height=0.6,
                width=0.6,
                x=0.2,
                y=0.15,
                on_focus_lost_hide=True,
            ),
            DropDown(
                "music",
                f"{myTerm} -e sh -c 'playerctl metadata --format \"Now playing: {{artist}} - {{title}}\" && exec zsh'",
                opacity=0.95,
                height=0.5,
                width=0.5,
                x=0.25,
                y=0.2,
                on_focus_lost_hide=True,
            ),
        ],
    )
]

# =============== LAYOUTS ===============
layout_theme = {
    "border_width": 0,
    "margin": [6, 6, 6, 6],
    "border_focus": C("accent"),
    "border_normal": C("black2"),
}
layouts = [
    layout.Columns(**layout_theme),
    layout.MonadTall(**layout_theme),
    layout.Max(),
]

floating_layout = layout.Floating(
    border_focus=C("accent2"),
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),
        Match(wm_class="makebranch"),
        Match(wm_class="maketag"),
        Match(wm_class="ssh-askpass"),
        Match(title="branchdialog"),
        Match(title="pinentry"),
    ],
)


# =============== BAR ===============
def sep(pad=6):
    return widget.Sep(linewidth=1, padding=pad, foreground=C("line"), size_percent=70)


# Workspace icon mapping
workspace_icons = {
    "1": "󰈹",  # Browser
    "2": "",  # Code
    "3": "",  # Terminal
    "4": "",  # Files
    "5": "󰙯",  # Social
    "6": "",  # Music
    "7": "",  # Games
    "8": "",  # Video
    "9": "󰙯",  # Discord/Chat (auto-assigned)
}

# App-specific icons for dynamic labeling
app_icons = {
    "discord": "󰙯",
    "vesktop": "󰙯",
    "google-chrome": "󰊯",
    "chrome": "󰊯",
    "firefox": "",
    "obsidian": "",
    "code": "",
    "zed": "",
}


def get_workspace_icon(text):
    """Convert workspace number to icon"""
    return workspace_icons.get(text, text)


screens = [
    Screen(
        top=bar.Bar(
            [
                widget.Spacer(length=8),
                widget.GroupBox(
                    fontsize=15,
                    margin_y=3,
                    margin_x=6,
                    padding_y=1,
                    padding_x=6,
                    # borderwidth=2,
                    # rounded=True,
                    active=C("fg"),
                    inactive=C("muted"),
                    highlight_method="block",
                    this_current_screen_border=C("accent"),
                    this_screen_border=C("magenta"),
                    other_current_screen_border=C("accent"),
                    other_screen_border=C("magenta"),
                    disable_drag=True,
                    background=C("bg_alt"),
                    parse_text=get_workspace_icon,
                ),
                widget.Spacer(length=6),
                sep(),
                # widget.CurrentLayoutIcon(scale=0.7, background=C("bg")),
                widget.CurrentLayout(foreground=C("muted"), padding=6),
                sep(),
                widget.WindowName(
                    foreground=C("accent"),
                    max_chars=80,
                    width=bar.CALCULATED,
                    empty_group_string="Desktop",
                ),
                widget.Spacer(length=bar.STRETCH),
                widget.GenPollText(
                    update_interval=300,
                    func=lambda: subprocess.check_output(
                        "printf $(uname -r)", shell=True, text=True
                    ).strip(),
                    foreground=C("accent2"),
                    fmt="  {}",
                ),
                sep(),
                widget.CPU(
                    format="  {load_percent}%",
                    foreground=C("yellow"),
                    mouse_callbacks={
                        "Button1": lambda: qtile.cmd_spawn(myTerm + " -e btop")
                    },
                ),
                sep(),
                widget.Memory(
                    format="  {MemPercent}%",
                    measure_mem="G",
                    foreground=C("green"),
                    mouse_callbacks={
                        "Button1": lambda: qtile.cmd_spawn(myTerm + " -e btop")
                    },
                ),
                sep(),
                widget.DF(
                    partition="/",
                    visible_on_warn=False,
                    update_interval=60,
                    format="  {uf}{m} free",
                    foreground=C("magenta"),
                    mouse_callbacks={"Button1": lambda: qtile.cmd_spawn("notify-disk")},
                ),
                sep(),
                widget.Wttr(
                    location={"Daejeon": "Daejeon"},
                    format="%C · %f · %p · %m %M",
                    units="m",
                    update_interval=600,  # 10 minutes
                    foreground=C("music"),
                    mouse_callbacks={
                        "Button1": lambda: qtile.cmd_spawn(
                            "xdg-open https://wttr.in/Daejeon"
                        )
                    },
                ),
                sep(),
                widget.Volume(
                    fmt="  {}",
                    foreground=C("accent"),
                    mouse_callbacks={
                        "Button3": lambda: qtile.cmd_spawn(myTerm + " -e pulsemixer")
                    },
                ),
                sep(),
                widget.Clock(
                    format="  %a, %b %d    %H:%M",
                    foreground=C("fg"),
                    mouse_callbacks={"Button1": lambda: qtile.cmd_spawn("notify-date")},
                ),
                widget.Systray(padding=6),
                widget.Spacer(length=8),
            ],
            32,
            margin=[0, 0, 8, 0],
            background=C("bg") + "cc",
        ),
    ),
]

# =============== MOUSE ===============
mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
reconfigure_screens = True
auto_fullscreen = True
auto_minimize = True
focus_on_window_activation = "smart"
wl_input_rules = None
wl_xcursor_theme = "Bibata-Modern-Classic"
wl_xcursor_size = 24
wmname = "LG3D"


# =============== HOOKS ===============
@hook.subscribe.startup_once
def _autostart():
    home = os.path.expanduser("~")
    autostart = os.path.join(home, ".config", "qtile", "autostart.sh")
    if os.path.exists(autostart):
        subprocess.Popen([autostart])
