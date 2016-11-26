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




<!-- for video edit -->
https://handbrake.fr/

<!-- Once a video is loaded click the Video tab and adjust the settings to: -->
RF = 18
Profile = high
Level = 5.0