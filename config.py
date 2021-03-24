import os
import re
import socket
import subprocess
from libqtile import qtile
from libqtile.config import Click, Drag, Group, KeyChord, Key, Match, Screen
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from libqtile.lazy import lazy
from typing import List  # noqa: F401


mod = "mod4"
alt = "mod1" 
terminal = "terminator"

keys = [
    #----- VENTANAS -----
    #Desplazamiento entre ventanas.
    Key([mod], "Left",
        lazy.layout.left(),
        desc="Move focus to left"
        ),
    Key([mod], "Right",
        lazy.layout.right(),
        desc="Move focus to right"
        ),
    Key([mod], "Down",
        lazy.layout.down(),
        desc="Move focus down"
        ),
    Key([mod], "Up",
        lazy.layout.up(),
        desc="Move focus up"
        ),
    Key([mod], "Tab",
        lazy.layout.next(),
        desc="Move window focus to other window"
        ),
    #Moviento de ventanas (Izquierda, Derecha, Abajo Arriba).
    Key([mod, "shift"], "Left",
        lazy.layout.shuffle_left(),
        desc="Move window to the left"
        ),
    Key([mod, "shift"], "Right",
        lazy.layout.shuffle_right(),
        desc="Move window to the right"
        ),
    Key([mod, "shift"], "Down",
        lazy.layout.shuffle_down(),
        desc="Move window down"
        ),
    Key([mod, "shift"], "Up",
        lazy.layout.shuffle_up(),
        desc="Move window up"
        ),
    #Modificar el tamaño de las ventanas (Funciona en el layout "Columns").
    Key([mod, "control"], "Left",
        lazy.layout.grow_left(),
        desc="Grow window to the left"
        ),
    Key([mod, "control"], "Right",
        lazy.layout.grow_right(),
        desc="Grow window to the right"
        ),
    Key([mod, "control"], "Down",
        lazy.layout.grow_down(),
        desc="Grow window down"
        ),
    Key([mod, "control"], "Up",
        lazy.layout.grow_up(),
        desc="Grow window up"
        ),
    #Otros
    Key([mod], "n",
        lazy.layout.normalize(),
        desc="Reset all window sizes"
        ),
    Key([mod], "m",
             lazy.layout.maximize(),
             desc='toggle window between minimum and maximum sizes'
             ),
    Key([mod, "control"], "f",
             lazy.window.toggle_floating(),
             desc='toggle floating'
             ),
    Key([mod], "f",
        lazy.window.toggle_fullscreen(),
        desc='toggle fullscreen'
        ),

    #Alternar entre lados divididos y no divididos de la pila.
    #Split = se muestran todas las ventanas
    Key([mod, "shift"], "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"
        ),
    #Dar vuelta al diseño Monadtall/Monadwide
    Key([mod, "shift"], "f",
        lazy.layout.flip(),
        desc="Flip Layout For Monadtall/Monadwide"
        ),
    #Reducir el tamaño de la ventana (diseño MondadTall)
    Key([mod, "shift"], "j",
        lazy.layout.shrink(),
        lazy.layout.decrease_nmaster(),
        desc='Shrink window (MonadTall), decrease number in master pane (Tile)'
        ),
    #Incrementar el tamaño de la ventana (diseño MondadTall)
    Key([mod, "shift"], "l",
        lazy.layout.grow(),
        lazy.layout.increase_nmaster(),
        desc='Expand window (MonadTall), increase number in master pane (Tile)'
        ),
    
    #----- LAYOUTS -----
    #Alternar entre los diferentes Layouts
    Key([mod, "shift"], "Tab",
        lazy.next_layout(),
        desc="Toggle between layouts"
        ),
    
    #----- SCREENS -----
    #Cambiar el enfoque a un monitor específico
    Key([mod, alt], "o",
        lazy.to_screen(0),
        desc='Keyboard focus to monitor 1'
        ),
    Key([mod, alt], "p",
        lazy.to_screen(1),
        desc='Keyboard focus to monitor 2'
        ),
    # Cambiar el enfoque de los monitores
    Key([mod, alt], "Right",
        lazy.next_screen(),
        desc='Move focus to next monitor'
        ),
    Key([mod, alt], "Left",
        lazy.prev_screen(),
        desc='Move focus to prev monitor'
        ),

    #----- BOTONES CON FUNCION ESPECIAL -----
    #Control del brillo
    Key([], "XF86MonBrightnessUp",
            lazy.spawn("xbacklight -inc 5"),
            desc="Increase Brightness"
        ),
    Key([], "XF86MonBrightnessDown",
            lazy.spawn("xbacklight -dec 5"),
            desc="Decrease Brightness"
        ),
    #Control del audio
    Key([], "XF86AudioMute",
            lazy.spawn("amixer -q set Master toggle"),
            desc="Mute"
        ),
    Key([], "XF86AudioRaiseVolume",
            lazy.spawn("amixer -q set Master 5%+"),
            desc="Increase Volume"
        ),
    Key([], "XF86AudioLowerVolume",
            lazy.spawn("amixer -q set Master 5%-"),
            desc="Decrease Volume"
        ),
    Key([], "XF86AudioPlay",
            lazy.spawn("playerctl play-pause"),
            desc="Play"
        ),
    Key([], "XF86AudioNext",
            lazy.spawn("playerctl next"),
            desc="Next"
        ),
    Key([], "XF86AudioPrev",
            lazy.spawn("playerctl previous"),
            desc="Previous"
        ),
    Key([], "XF86AudioStop",
            lazy.spawn("playerctl stop"),
            desc="Stop"
        ),
    #Captura de pantalla
    Key([], "Print",
            lazy.spawn(
                "scrot 'ArchLinux-%Y-%m-%d-%s_screenshot_$wx$h.jpg' -e 'mv $f $$(xdg-user-dir)'"),
            desc="Screenshot"
        ),
    Key([alt], "Print",
        lazy.spawn('xfce4-screenshooter'),
        desc="Xfce4-Screenshot"
        ),

    #-----CONTROL QTILE-----
    #Reiniciar Qtile
    Key([mod, "control"], "r",
        lazy.restart(),
        desc="Restart Qtile"
        ),
    #Cerrar Qtile
    Key([mod, "control"], "q",
        lazy.shutdown(),
        desc="Shutdown Qtile"
        ),

    #----- APLICACIONES -----
    #Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt wigdet"),

    #Ejecutar Terminator
    Key([mod], "Return",
        lazy.spawn(terminal),
        desc="Launch terminal"
        ),
    #Ejecutrar Rofi
    Key([mod], "r",
        lazy.spawn('rofi -show drun -show-icons'),
        desc="Launch Rofi"
        ),
    #Cerrar la ventana activa
    Key([mod], "w",
        lazy.window.kill(),
        desc="Kill focused window"
        ),
]

group_names = [("TER", {'layout': 'monadtall'}),
               ("WWW", {'layout': 'treetab'}),
               ("DEV", {'layout': 'monadtall'}),
               ("MIC", {'layout': 'monadtall'}),
               ("DIR", {'layout': 'monadtall'})
               ]

groups = [Group(name, **kwargs) for name, kwargs in group_names]

for i, (name, kwargs) in enumerate(group_names, 1):
    keys.append(Key([mod], str(i), lazy.group[name].toscreen()))          # Cambiar a otro grupo
    keys.append(Key([mod, "shift"], str(i), lazy.window.togroup(name)))   # Enviar la ventana actual a otro grupo

colors = [["#282c34", "#282c34"], # 0 Fondo del panel principal (Color: Shark)
          ["#3d3f4b", "#434758"], # 1 Fondo para la pestaña del grupo actual (Color: Gun Powder)
          ["#ffffff", "#ffffff"], # 2 Color de la fuente para los nombres de los grupos (Color: White)
          ["#ff5555", "#ff5555"], # 3 Color de la línea del borde de la pestaña actual (Color: Persimmon)
          ["#74438f", "#74438f"], # 4 Color #1 de la línea de borde para 'otras pestañas' y color para 'widgets impares' (Color: Affair)
          ["#4f76c7", "#4f76c7"], # 5 Color #1 para los 'widgets pares'(Color: Indigo)
          ["#e1acff", "#e1acff"], # 6 Nombre de la ventana (Color: Mauve)
          ["#141414", "#141414"], # 7  (Color: Cod Gray)
          ["#90C435", "#90C435"], # 8  (Color: Atlantis)
          ["#000000", "#000000"], # 9  (Color: Black)
          ["#384323", "#384323"], # 10 (Color: Woodland)
          ["#a0a0a0", "#a0a0a0"], # 11 (Color: Silver Chalice)
          ["#ed5752", "#ed5752"], # 12 (Color: Raspberry)
          ["#92aac7", "#92aac7"], # 13 (Color: Bluebell)
          ["#659623", "#659623"], # 14 (Color: Olive Drab)
          ["#364A1B", "#364A1B"], # 15 (Color: Thatch Green)
          ["#31a9b8", "#31a9b8"], # 16 (Color: Pelorous)
          ["#cf3721", "#cf3721"], # 17 (Color: Punch)
          ["#ed8c72", "#ed8c72"], # 18 (Color: Apricot)
          ["#31a9b8", "#31a9b8"], # 19 (Color: Pelorous)
          ["#c99e10", "#c99e10"], # 20 (Color: Pizza)
          ["#8d230f", "#8d230f"], # 21 (Color: Tamarillo)
          ["#34675c", "#7da3a1"], # 22 (Color: Stromboli, Sea Nymph)
          ["#2c7873", "#6fb98f"], # 23 (Color: Paradiso, Silver Tree)
          ["#021c1e", "#004445"], # 24 (Color: Holly, Cyprus)
          ] 
          
layout_theme = {"border_width": 2,
                "margin": 3,
                "border_focus": "#cf3721", #(Color: Apricot)
                "border_normal": "#1D2330" #
                }

layouts = [
    #layout.MonadWide(**layout_theme),
    #layout.Bsp(**layout_theme),
    #layout.Stack(stacks=2, **layout_theme),
    #layout.Columns(**layout_theme),
    #layout.RatioTile(**layout_theme),
    #layout.VerticalTile(**layout_theme),
    #layout.Matrix(**layout_theme),
    #layout.Zoomy(**layout_theme),
    #layout.Tile(shift_windows=True, **layout_theme),
    #layout.Stack(num_stacks=2),
    layout.MonadTall(**layout_theme),
    layout.TreeTab(
        font="Ubuntu",
        fontsize=10,
        sections=["PRINCIPAL"],
        section_fontsize=11,
        bg_color=colors[7],
        active_bg=colors[17],  # colors[8],
        active_fg=colors[2],  # colors[9],
        inactive_bg=colors[16],  # colors[10],
        inactive_fg=colors[0],  # colors[11],
        padding_y=5,
        section_top=10,
        panel_width=180
    ),
    layout.Max(**layout_theme),
    layout.Floating(**layout_theme)
]

prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())

##### DEFAULT WIDGET SETTINGS #####
widget_defaults = dict(
    font="Ubuntu Mono",
    fontsize = 12,
    padding = 2,
    background=colors[2]
)
extension_defaults = widget_defaults.copy()


def init_widgets_list():
    widgets_list = [
        # ----- Separador -----
        widget.Sep(
            linewidth=0,
            padding=6,
            foreground=colors[2],
            background=colors[0]
        ),
        # ----- Imagen (Icono de Python) -----
        widget.Image(
            filename="~/.config/qtile/icons/python.png",
            scale="False",
            mouse_callbacks={'Button1': lambda: qtile.cmd_spawn(
                'rofi -show drun -show-icons')}
        ),
        # ----- Separador -----
        widget.Sep(
            linewidth=0,
            padding=6,
            foreground=colors[2],
            background=colors[0]
        ),
        # ----- Grupos -----
        widget.GroupBox(
            font="Ubuntu Bold",
            fontsize=9,
            margin_y=3,
            margin_x=0,
            padding_y=5,
            padding_x=3,
            borderwidth=3,
            active=colors[2],
            inactive=colors[2],
            rounded=False,
            highlight_color=colors[1],
            highlight_method="line",
            this_current_screen_border=colors[17],
            this_screen_border=colors[16],
            other_current_screen_border=colors[17],
            other_screen_border=colors[16],
            foreground=colors[2],
            background=colors[0],
            urgent_alert_method = 'border',
            urgent_border = colors[17]
        ),
        # ----- Prompt -----
        widget.Prompt(
            prompt=prompt,
            font="Ubuntu Mono",
            padding=10,
            foreground=colors[3],
            background=colors[1]
        ),
        # ----- Separador -----
        widget.Sep(
            linewidth=0,
            padding=20,
            foreground=colors[2],
            background=colors[0]
        ),
        # ----- Nombres de Ventanas -----
        widget.WindowName(
            foreground=colors[2],
            background=colors[0],
            padding=0
        ),
        # ----- Separador -----
        widget.Sep(
            linewidth=0,
            padding=6,
            foreground=colors[0],
            background=colors[0]
        ),
        # ----- Texto (inicio Caja de Widgets) -----
        widget.TextBox(
            text='',
            background=colors[0],
            foreground=colors[16],
            padding=0,
            fontsize=37
        ),
        # ----- Caja de Widgets -----
        widget.WidgetBox(
            background = colors[16],
            text_closed = '🞀 ',
            text_open = '🞂',
            fontsize = 15,  
            widgets=[
                # ----- Texto (inicio de Temperatura PC) -----
                widget.TextBox(
                    text='',
                    background=colors[16],
                    foreground=colors[16],
                    padding=0,
                    fontsize=37
                ),
                # ----- Texto (Icono de Temperatura PC) -----
                widget.TextBox(
                    text=" 🌡",
                    padding=2,
                    foreground=colors[2],
                    background=colors[16],
                    fontsize=11
                ),
                # ----- Temperatura PC -----
                widget.ThermalSensor(
                    foreground=colors[2],
                    background=colors[16],
                    threshold=90,
                    padding=5
                ),
                # ----- Texto (inicio Actualizaciones) -----
                widget.TextBox(
                    text='',
                    background=colors[16],
                    foreground=colors[17],
                    padding=0,
                    fontsize=37
                ),
                # ----- Texto (Icono de Actualizaciones) -----
                widget.TextBox(
                    text=" ⟳",
                    padding=2,
                    foreground=colors[2],
                    background=colors[17],
                    fontsize=14
                ),
                # ----- Actualizaciones -----
                widget.CheckUpdates(
                    update_interval=900,
                    distro="Arch",
                    background=colors[17],
                    foreground=colors[2],
                    #colour_have_updates=colors[3],
                    # #colour_no_updates=colors[2],
                    display_format="{updates} Updates",
                    #mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(terminal + '-e sudo pacman -Syu')}
                    execute="terminator -x sudo pacman -Syyu"
                ),
                # ----- Texto (inicio de Red Cableada) -----
                widget.TextBox(
                    text='',
                    background=colors[17],
                    foreground=colors[16],
                    padding=0,
                    fontsize=37
                ),
                # ----- Red Cableada -----
                widget.Net(
                    interface="eno1",
                    format='{down} ↓↑ {up}',
                    foreground=colors[2],
                    background=colors[16],
                    #padding = 5
                ),
            ]
        ),
        # ----- Texto (inicio Iconos Layout) -----
        widget.TextBox(
            text='',
            background=colors[16],
            foreground=colors[17],
            padding=0,
            fontsize=37
        ),
        # ----- Iconos Layout -----
        widget.CurrentLayoutIcon(
            custom_icon_paths=[os.path.expanduser("~/.config/qtile/icons")],
            foreground=colors[0],
            background=colors[17],
            padding=0,
            scale=0.7
        ),
        # ----- Layouts -----
        widget.CurrentLayout(
            foreground=colors[2],
            background=colors[17],
            padding=5
        ),
        # ----- Texto (inicio de Volumen) -----
        widget.TextBox(
            text='',
            background=colors[17],
            foreground=colors[16],
            padding=0,
            fontsize=37
        ),
        # ----- Texto (Icono de Volumen) -----
        widget.TextBox(
            text=" Vol:",
            foreground=colors[2],
            background=colors[16],
            padding=0
        ),
        # ----- Volumen -----
        widget.Volume(
            foreground=colors[2],
            background=colors[16],
            padding=5
        ),
        # ----- Texto (inicio de Brillo) -----
        widget.TextBox(
            text='',
            background=colors[16],
            foreground=colors[17],
            padding=0,
            fontsize=37
        ),
        # ----- Texto (Icono de Brillo) -----
         widget.TextBox(
            text="☀",
            foreground=colors[2],
            background=colors[17],
            padding=0,
            fontsize=18
        ),
        # ----- Brillo -----
        widget.Backlight(
            backlight_name = 'intel_backlight',
            brightness_file = '/sys/class/backlight/intel_backlight/brightness',
            foreground=colors[2],
            background=colors[17],
            padding=5
        ),
        # ----- WLAN -----
        #widget.Wlan(
        #    interface="wlan0",
        #    format='I:{essid} S:{percent:2.0%}',
        #    foreground=colors[2],
        #    background=colors[17],
        #    padding=0
        #),
        # ----- Texto (inicio de Bandeja del Sistema) -----
        widget.TextBox(
            text='',
            background=colors[17],
            foreground=colors[16],
            padding=0,
            fontsize=37
        ),
        # ----- Bandeja del Sistema -----
        widget.Systray(
            background=colors[16],
            padding=10
        ),
        # ----- Texto (inicio del Reloj y Fecha) -----
        widget.TextBox(
            text='',
            background=colors[16],
            foreground=colors[17],
            padding=0,
            fontsize=37
        ),
        # ----- Texto (Reloj y Fecha) -----
        widget.Clock(
            foreground=colors[2],
            background=colors[17],
            format="%a, %x - %X"
        ),
    ]
    return widgets_list

def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    del widgets_screen1[7:8]               # Elimina los widgets no deseados (bandeja del sistema) en los monitores
    return widgets_screen1

def init_widgets_screen2():
    widgets_screen2 = init_widgets_list()
    return widgets_screen2                 # En el monitor 2 se mostraran todos los widgets en widgets_list 

def init_screens():
    return [Screen(top=bar.Bar(widgets=init_widgets_screen1(), opacity=1.0, size=20)),
            Screen(top=bar.Bar(widgets=init_widgets_screen2(), opacity=1.0, size=20)),]
            #Screen(top=bar.Bar(widgets=init_widgets_screen1(), opacity=1.0, size=20))]

if __name__ in ["config", "__main__"]:
    screens = init_screens()
    widgets_list = init_widgets_list()
    widgets_screen1 = init_widgets_screen1()
    widgets_screen2 = init_widgets_screen2()

def window_to_prev_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i - 1].name)

def window_to_next_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i + 1].name)

def window_to_previous_screen(qtile):
    i = qtile.screens.index(qtile.current_screen)
    if i != 0:
        group = qtile.screens[i - 1].group.name
        qtile.current_window.togroup(group)

def window_to_next_screen(qtile):
    i = qtile.screens.index(qtile.current_screen)
    if i + 1 != len(qtile.screens):
        group = qtile.screens[i + 1].group.name
        qtile.current_window.togroup(group)

def switch_screens(qtile):
    i = qtile.screens.index(qtile.current_screen)
    group = qtile.screens[i - 1].group
    qtile.current_screen.set_group(group)

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False

floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    # default_float_rules include: utility, notification, toolbar, splash, dialog,
    # file_progress, confirm, download and error.
    *layout.Floating.default_float_rules,
    Match(title='Confirmation'),  # tastyworks exit box
    Match(title='Qalculate!'),  # qalculate-gtk
    #{'wmclass': 'Arandr'},
    #Match(wm_class='kdenlive'),  # kdenlive
    Match(wm_class='pinentry-gtk-2'),  # GPG key password entry
])
auto_fullscreen = True
focus_on_window_activation = "smart"

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
