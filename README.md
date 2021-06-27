#Configuración del gestor de ventanas Qtile (Arch Linux)
***


##Software utilizado


###Red
####NetworkManager
Es una utilidad de software para simplificar el uso de redes de computadoras en Linux. 
```bash
sudo pacman -S networkmanager
systemctl enable NetworkManager 
```
####Network Manager Applet 
Es un front-end GTK 3 que funciona en entornos Xorg con una bandeja del sistema, muestra una lista de redes disponibles y permite cambiar fácilmente entre ellas. 
```bash
sudo pacman -S network-manager-applet  
```


###Gestor de sesiones
####Lightdm
Es un gestor de sesiones, ligero, rápido y funciona con diversos entornos de escritorio.
```bash
sudo pacman -S lightdm lightdm-gtk-greeter lightdm-gtk-greeter-settings
```
#####Configuración
Si se tiene instalado un gestor de inicio de sesión por ejemplo LY se debe deshabilitar, para después habilitar lightdm. Esto se realiza de la siguiente manera:     
```bash
sudo systemctl disable ly.service
sudo systemctl enable lightdm.service
```
Ademas se debe editar el archivo lightdm.conf (/etc/lightdm), se debe descomentar y agregar lo siguiente:
```ini
# /etc/lightdm/lightdm.conf
# Descomentar esta línea y agregar lo siguiente:
greeter-session = lightdm-gtk-greeter
```
***Nota:*** esta es la configuración si no se desea instalar ningún tema. Si se desea personalizar se debe utilizar Lightdm Greeter Settings.

#####Tema
Se deben instalar los siguiente paquetes:
```bash
sudo pacman -S lightdm-webkit2-greeter
yay -S lightdm-webkit-theme-aether
```
Ademas se deben realizar las siguientes configuraciones:
```ini
# /etc/lightdm/lightdm.conf
# Descomentar esta línea y agregar lo siguiente:
greeter-session = lightdm-webkit2-greeter

# /etc/lightdm/lightdm-webkit2-greeter.conf
webkit_theme = lightdm-webkit-theme-aether
```    


###Fuentes 
```bash
sudo pacman -S powerline-fonts ttf-nerd-fonts-symbols ttf-ubuntu-font-family ttf-dejavu ttf-liberation noto-fonts
```


###Audio
####ALSA
Proporciona controladores de tarjetas de sonido controlados por kernel, por defecto ALSA viene instalado en el kernel, por lo que solo se van a instalar algunas herramientas para activar el sonido, y que sea compatible con OSS(Open Sound System).  
```bash
sudo pacman -S alsa-utils alsa-plugins alsa-oss
```
Ahora se deben agregar los módulos del paquete alsa-oss al kernel, para que tenga compatibilidad con aplicaciones OSS
```bash
sudo modprobe snd_seq_oss snd_pcm_oss snd_mixer_oss
```
Por ultimo se ejecuta el test para comprobar el correcto funcionamiento de los altavoces.
```bash
speaker-test -c 2
```
El paquete alsa-utils, contiene las utilidades alsamixer y amixer. Amixer es un comando de shell para cambiar la configuración de audio, mientras que alsamixer proporciona una interfaz más intuitiva para la configuración de dispositivos de audio.
Ejecutar Alsamixer y aumentar y disminuir el audio desde la terminal:
```bash
# Ejecutar Alsamixer
alsamixer

# Aumentar y disminuir el audio 
amixer -q set Master 5%+
amixer -q set Master 5%-
```
Otra opción seria instalar un programa gráfico para controlar el audio, para lo cual se debe instalar el siguiente paquete:
```bash
sudo pacman -S pavucontrol
```


###Brillo
####Xbacklight
El brillo se puede configurar con el paquete xorg-xbacklight, cabe resaltar que dicho paquete solo funciona con Intel.  
```bash
sudo pacman -S xorg-xbacklight
```
Aumentar y disminuir el brillo desde la terminal:
```bash
xbacklight -inc 5
xbacklight -dec 5
```
####Brightnessctl
Es una herramienta que sirve para el control del brillo.  
```bash
sudo pacman -S brightnessctl
```
Aumentar y disminuir el brillo desde la terminal:
```bash
brightnessctl set +10%
brightnessctl set 10%-
```


###Monitores
####Xrandr
Es una utilidad de configuración oficial para la extensión RandR, cabe resaltar que se puede utilizar para establecer el tamaño, la orientación o el reflejo de las salidas de una o más pantallas.  
```bash
sudo pacman -S xrandr
```
Comandos necesarios para establecer una configuración básica.
```bash
# Muestra todas las salidas y resoluciones disponibles
xrandr
# Formato común para un portátil con monitor extra
xrandr --output eDP-1 --primary --mode 1366x768 --pos 0x1080 --output HDMI-1 --mode 1366x768 --pos 0x0
```
####Arandr
Es una herramienta que está diseñada para proporcionar una interfaz visual simple para XRandR, las posiciones relativas del monitor se muestran gráficamente y se pueden cambiar arrastrando y soltando.  
```bash
sudo pacman -S arandr
```
####Lxrandr
Es el administrador de pantalla estándar de LXDE, gestiona la resolución de pantalla y monitores externos.  
```bash
sudo pacman -S lxrandr
```


###Transparencia
####Picom
Sirve para establecer la opacidad (transparencia) para ventanas enfocadas y desenfocadas.
```bash
sudo pacman -S picom
```


###Fondos
####Nitrogen 
Es un navegador y configurador de fondos de escritorio rápido y ligero para Xorg.
```bash
sudo pacman -S nitrogen
```
####Feh 
Es un potente y ligero visor de imágenes que también puede ser utilizado para gestionar el fondo de pantalla.
```bash
sudo pacman -S feh
```


###Menú 
####Rofi
Es un selector de ventanas, diálogo de ejecución, lanzador de ssh y reemplazo de dmenu.
```bash
sudo pacman -S rofi
```
#####Tema
Para cambiar el tema que tiene establecido por defecto, se debe ejecutar el siguiente comando:
```bash
rofi-theme-selector
```