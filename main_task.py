#!/usr/bin/env python

import importlib
import os
import re
import sys
import signal
import time

import pygame
# loop1 ->|-> vid1 -> loop2>|-> vid2->loop3->|-> vid3->loop4->|-> vid4->exit
class Hell_Player():

    def __init__(self):
        self._serial = self._load_serial()
        self._player = self._load_player()        
        self._running = True
        self._vid = False
        self._stage = 1
        self._videos = "/video/"
        self._movie = ""
        
        # Initialize pygame and display a blank screen.
        pygame.display.init()
        pygame.font.init()
        pygame.mouse.set_visible(False)
        
        size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        self._screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
        self._blank_screen()            
        self._small_font = pygame.font.Font(None, 50)
        self._big_font   = pygame.font.Font(None, 250)
        
    def _load_player(self):     
        return importlib.import_module('hello_video', 'hell_player') \
            .create_player()
        
    def _load_serial(self):     
        return importlib.import_module('serial_com', 'hell_player') \
            .create_serial()
    
    def Shutdown(self):  
        os.system("sudo shutdown -h now")  
        
    def ScreenOn(self):  
        os.system("/opt/vc/bin/tvservice -p")  
   
    def ScreenOff(self):  
        os.system("/opt/vc/bin/tvservice -o")  
        
        #chmod u+s /opt/vc/bin/tvservice
        #chmod u+s /bin/chvt
        #/opt/vc/bin/tvservice -p && /opt/vc/bin/tvservice -o
        #Turning the power back on:
        #/opt/vc/bin/tvservice -p && chvt 1 && chvt 7

    def _render_text(self, message, font=None):
        """Draw the provided message and return as pygame surface of it rendered
        with the configured foreground and background color.
        """
        # Default to small font if not provided.
        if font is None:
            font = self._small_font
        return font.render(message, True, (255,255,255), (0,0,0))

    def PrintResults(self):

        label1 = self._render_text('Test')
        l1w, l1h = label1.get_size()
        sw, sh = self._screen.get_size()
        self._screen.fill((0, 0, 0))
        self._screen.blit(label1, (sw/2-l1w/2, sh/2-l2h/2-l1h))
        self._screen.blit(label2, (sw/2-l2w/2, sh/2-l2h/2))
        pygame.display.update()

    def PrintArrows(self):
        label1 = self._render_text('Test2')
        l1w, l1h = label1.get_size()
        sw, sh = self._screen.get_size()
        self._screen.fill((0, 0, 0))
        self._screen.blit(label1, (sw/2-l1w/2, sh/2-l2h/2-l1h))
        self._screen.blit(label2, (sw/2-l2w/2, sh/2-l2h/2))
        pygame.draw.polygon(window, (0, 0, 0), ((0, 100), (0, 200), (200, 200), (200, 300), (300, 150), (200, 0), (200, 100)))

        pygame.display.update()
 
    def _blank_screen(self):
        """Render a blank screen filled with the background color."""
        self._screen.fill((0, 0, 0))
        pygame.display.update()
        
    def run(self):   
      
        self._serial.connect();
        
        
        while self._running:              
                              
              if self._vid is True:
                self._movie = "vid" + str(self._stage) + ".h264"              
              else:
                self._movie = "loop" + str(self._stage) + ".h264"                     
                            
              if not self._player.is_playing():
                  self._blank_screen()
                  self._player.play(self._videos + self._movie, loop = self._vid!=True)
                  print('Playing: {0}'.format(self._movie))                
           
              else:
                
                if self._vid is True:
                    self._vid=False
                    self._stage+=1
                    if self._stage>4:
                      self._stage=4
                else:
                  inputCMD= self._serial.read()
                           
                
                if inputCMD == "pi1"+"\n":
                    inputCMD=""
                    self._player.stop()
                    self._vid=True;
                    self._movie = "vid" + str(self._stage) + ".h264"
                    self._stage=1
                

                if inputCMD == "pi2"+"\n":
                    inputCMD=""
                    self._player.stop()
                    self._vid=True;
                    self._movie = "vid" + str(self._stage) + ".h264"
                    self._stage=2
                

                if inputCMD == "pi3"+"\n":
                    inputCMD=""
                    self._player.stop()
                    self._vid=True;
                    self._movie = "vid" + str(self._stage) + ".h264"
                    self._stage=3

                if inputCMD == "pi4"+"\n":
                    inputCMD=""
                    self._player.stop()
                    self._vid=True;
                    self._movie = "vid" + str(self._stage) + ".h264"
                    self._stage=4
                

                if inputCMD == "re"+"\n":
                    inputCMD=""
                    self._player.stop()
                    self._vid=False;
                    self._stage=1   
                    
                if inputCMD == "off1"+"\n":
                    inputCMD=""
                    self._running = False
                    if self._player is not None:
                      self._player.stop()
                    self.Shutdown()
                
                if inputCMD == "tv1"+"\n":
                    inputCMD=""
                    self.ScreenOn()
                    
                if inputCMD == "tv0"+"\n":
                    inputCMD=""
                    self.ScreenOff()
                            
              
                
            # Give the CPU some time to do other tasks.
                time.sleep(0.002)

    def signal_quit(self, signal, frame):
        """Shut down the program, meant to by called by signal handler."""
        self._running = False
        if self._player is not None:
            self._player.stop()
        pygame.quit()
     


# Main entry point.
if __name__ == '__main__':  
    print('Hell Player')
    # Create video looper.
    hell_player = Hell_Player()
    # Configure signal handlers to quit on TERM or INT signal.
    signal.signal(signal.SIGTERM, hell_player.signal_quit)
    signal.signal(signal.SIGINT, hell_player.signal_quit)
    # Run the main loop.
    hell_player.run()
