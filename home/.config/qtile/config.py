# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile.config import Key, Screen, Group, Drag, Click
from libqtile.lazy import lazy
from libqtile import layout, bar, widget, hook

from typing import List  # noqa: F401
import os
import subprocess

mod = "mod4"

@hook.subscribe.screen_change
def set_screens(qtile, event):
    xrandr_state = subprocess.check_output(["xrandr"])
    if b"DP-1 connected" in xrandr_state:
        xrandr_command = [
            "xrandr",
            "--output", "eDP-1", "--off",
        ]
    else:
        xrandr_command = [
            "xrandr",
            "--output", "eDP-1", "--auto",
        ]
    subprocess.call(xrandr_command)
    qtile.cmd_restart()

keys = [
    # Switch between windows in current stack pane(only pointer is moved around)
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod], "l", lazy.layout.right()),

    # Move windows up or down in current stack(windows are sheffuled)
    Key([mod, "control"], "k", lazy.layout.shuffle_down()),
    Key([mod, "control"], "j", lazy.layout.shuffle_up()),

    # Swap panes of split stack
    Key([mod, "shift"], "space", lazy.layout.rotate()),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split()),

    Key([mod], "Return", lazy.spawn("gnome-terminal")),
    Key([], "Scroll_Lock", lazy.spawn("i3lock -d")),
    Key([mod], "e", lazy.spawn("emacs")),
    Key([mod], "c", lazy.spawn("google-chrome")),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout()),

    Key([mod], "x", lazy.window.kill()),
    Key([mod], "f", lazy.window.toggle_fullscreen()),
    Key([mod, "control"], "f", lazy.window.toggle_floating()),

    Key([mod, "control"], "r", lazy.restart()),
    Key([mod, "control"], "q", lazy.shutdown()),
    Key([mod], "r", lazy.spawncmd()),
]

groups = [Group(i) for i in "1234567890"]

for i in groups:
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], i.name, lazy.group[i.name].toscreen()),
        # mod1 + shift + letter of group = switch to & move focused window to group
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name)),
    ])

emacs_purple='#7359B5'
border_width = 2
border = dict(
    border_focus=emacs_purple,
    border_width=border_width
)

layouts = [
    layout.MonadTall(name="monadtall", **border),
    layout.Max(),
    layout.Stack(num_stacks=2),
    layout.Columns(name="columns", **border),
    #layout.Tile(**border),
    #layout.Bsp(name="bsp", margin=20, **border),
    #layout.Matrix(name="matrix", **border),
    #layout.MonadWide(name="monadwide", **border),
    #layout.RatioTile(name="ratiotile", **border),
    #layout.TreeTab(name="treetab", border_width=border_width),
    #layout.VerticalTile(name="verticaltile", **border),
    #layout.Zoomy(name="zoomy"),
]

widget_defaults = dict(
    font='sans',
    fontsize=14,
    padding=3,
)
extension_defaults = widget_defaults.copy()

prompt = "{} $ ".format(os.environ["USER"])
screens = [
    Screen(
        bottom=bar.Bar(
            [
                widget.Prompt(prompt=prompt),
                widget.CurrentLayout(),
                widget.CurrentLayoutIcon(scale=0.6, padding=-4),
                widget.Spacer(width=10),
                widget.GroupBox(center_aligned=True),
                widget.Systray(),
                widget.TextBox('Vol:'),
                widget.Volume(),
                widget.Notify(fmt=" 🔥 {} "),
                widget.Battery(),
                widget.Clock(format='%m-%d %a %H:%M %p',
                             update_interval=60),
            ],
            28,
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List

follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    {'wmclass': 'confirm'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'file_progress'},
    {'wmclass': 'notification'},
    {'wmclass': 'splash'},
    {'wmclass': 'toolbar'},
    {'wmclass': 'confirmreset'},  # gitk
    {'wmclass': 'makebranch'},  # gitk
    {'wmclass': 'maketag'},  # gitk
    {'wname': 'branchdialog'},  # gitk
    {'wname': 'pinentry'},  # GPG key password entry
    {'wmclass': 'ssh-askpass'},  # ssh-askpass
])
auto_fullscreen = True
focus_on_window_activation = "smart"

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

# callback entrance, e.g. def main(qtile_instance): pass
def main(qtile):
    subprocess.run(["ibus-daemon", "-drx"])

