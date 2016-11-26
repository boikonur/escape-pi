 INSTALLATION INSTRUCTIONS


<!--
 Add Restfull communication.
Video played once.
Serial port both direction
 -->

sudo apt-get update
sudo apt-get -y install build-essential python-dev python-pip python-pygame supervisor git omxplayer




<!-- install hello video -->
git clone https://github.com/adafruit/pi_hello_video.git
cd pi_hello_video
./rebuild.sh
cd hello_video
sudo make install

<!-- not going blank -->
his is an X power-saving thing.

Firstly, you may need to install xset, a lightweight application that controls some X settings.

apt-get install x11-xserver-utils
Now open up your ~/.xinitrc file (if you don't have one then create it) and enter this:

xset s off         # don't activate screensaver
xset -dpms         # disable DPMS (Energy Star) features.
xset s noblank     # don't blank the video device

exec /etc/alternatives/x-session-manager      # start lxde



<!-- for video edit -->
https://handbrake.fr/

<!-- Once a video is loaded click the Video tab and adjust the settings to: -->
RF = 18
Profile = high
Level = 5.0