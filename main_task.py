#!/usr/bin/env python

import importlib
import os
import re
import sys
import signal
import time

import pygame

BLACK = (0,0,0)
WHITE = (255,255,255)
LABEL_COLOR = (43,123,123)
RESULT_COLOR = (134,123,21)

class Hell_Player():

    def __init__(self):
        self._serial = self._load_serial()
        self._player = self._load_player()        
        self._running = True
        self._stage = 1
        self._videodir = "/home/pi/escape-pi/"
        
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
        return importlib.import_module('omxplayer', 'escape-pi') \
            .create_player()
        
    def _load_serial(self):     
        return importlib.import_module('serial_com', 'escape-pi') \
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

    def _render_text(self, message, font=None, color=WHITE):
        """Draw the provided message and return as pygame surface of it rendered
        with the configured foreground and background color.
        """
        # Default to small font if not provided.
        if font is None:
            font = self._small_font
        return font.render(message, True, color, BLACK)

    def _animate_countdown(self, seconds=3):
        label1 = self._render_text(' Starting Game in')
        l1w, l1h = label1.get_size()
        sw, sh = self._screen.get_size()
        for i in range(seconds, 0, -1):
            # Each iteration of the countdown rendering changing text.
            label2 = self._render_text(str(i), self._big_font)
            l2w, l2h = label2.get_size()
            # Clear screen and draw text with line1 above line2 and all
            # centered horizontally and vertically.
            self._screen.fill(BLACK)
            self._screen.blit(label1, (sw/2-l1w/2, sh/2-l2h/2-l1h))
            self._screen.blit(label2, (sw/2-l2w/2, sh/2-l2h/2))
            pygame.display.update()
            # Pause for a second between each frame.
            time.sleep(1)


    def PrintResults(self):
        print('print: results')
        label0 = self._render_text('RESULTS', self._big_font, LABEL_COLOR )
        label1 = self._render_text('Footstep Game:')
        label2 = self._render_text('Punch Panda Game:')
        label3 = self._render_text('Kick a sack Game:')

        l0w, l0h = label0.get_size()
        l1w, l1h = label1.get_size()
        l2w, l2h = label2.get_size()
        l3w, l3h = label3.get_size()

        sw, sh = self._screen.get_size()
        self._screen.fill(BLACK)

        self._screen.blit(label0, (sw/2-l0w/2, sh-l0h))
        self._screen.blit(label1, (sw/2-l1w/2, sh/2-l2h/2-l1h))
        self._screen.blit(label2, (sw/2-l2w/2, sh/2-l2h/2))
        pygame.display.update()

    def PrintArrows(self):

        sw, sh = self._screen.get_size()
        self._screen.fill(BLACK)
        # self._screen.blit(label2, (sw/2-l2w/2, sh/2-l2h/2))
        pygame.display.update()
 
    def _blank_screen(self):
        """Render a blank screen filled with the background color."""
        self._screen.fill(BLACK)
        pygame.display.update()
        
    def run(self):   
      
        #self._serial.connect()       
           
        self._animate_countdown()
        self._blank_screen()

        self._player.play(self._videodir + 'test.mp4', loop = False)

        while 1:
            print('playing: ' + self._videodir + 'test.mp4') 
            time.sleep(0.002)

        while self._running:   

            while self._stage == 1:
                if not self._player.is_playing():        
                    self._player.play(self._videodir + 'test.mp4', loop = False)
                    print('playing: ' + self._videodir + 'test.mp4')
                    self._stage=2

            if self._stage == 2:
                if not self._player.is_playing(): 
                    self._stage =3
                    self._blank_screen()

            if self._stage == 3:  

                #inputCMD= self._serial.read() 
                inputCMD= "rez,1222,1222,1222\n"
                command = inputCMD.strip().split(",", 8)
                # rez,1222,1222,1222
                if command[0] == "rez"+"\n":
                    print('arg1: ' + command[1])
                    print('arg2: ' + command[2])
                    print('arg3: ' + command[3])

                
                if inputCMD == "reset"+"\n":
                    inputCMD=""
                    self._player.stop()
                    self._stage=1   
                    
                if inputCMD == "pioff"+"\n":
                    inputCMD=""
                    self._running = False
                    if self._player is not None:
                      self._player.stop()
                    self.Shutdown()
                
                if inputCMD == "piscron"+"\n":
                    inputCMD=""
                    self.ScreenOn()
                    
                if inputCMD == "piscroff"+"\n":
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
        sys.exit(0)
     


# Main entry point.
if __name__ == '__main__':  
    print('Escape PI')
    # Create video looper.
    hell_player = Hell_Player()
    # Configure signal handlers to quit on TERM or INT signal.
    signal.signal(signal.SIGTERM, hell_player.signal_quit)
    signal.signal(signal.SIGINT, hell_player.signal_quit)
    # Run the main loop.
    print('Escape PI - loop')
    hell_player.run()
