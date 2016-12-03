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
RESULT_COLOR = (134,67,21)
RESULT_BAD_COLOR = (252,134,134)
RESULT_GOOD_COLOR = (134,252,162)
TITLE_COLOR = (85,23,47)

OPTION_COLOR1= (252,134,134)
OPTION_COLOR2= (134,252,162)

class Hell_Player():

    def __init__(self):
        self._serial = self._load_serial()
        self._player = self._load_player()        
        self._running = True
        self._stage = 2
        self._videodir = "/home/pi/escape-pi/"
        self._highscore = 6000
        
        # Initialize pygame and display a blank screen.
        pygame.display.init()
        pygame.font.init()
        pygame.mouse.set_visible(False)

        pygame.mixer.init()
        pygame.mixer.music.load("gong.wav")       
        pygame.mixer.music.set_volume(10)
        
        #fadeout()  #time
        #set_volume()  #from 0.0 to 1.0

        
        size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        self._screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
        self._blank_screen()            
        self._small_font = pygame.font.Font(None, 50)
        self._mid_font = pygame.font.Font(None, 100)
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


    def PrintResults(self, results=[0,0,0]):
        print('print: results')
        label0 = self._render_text('RESULT', self._big_font, LABEL_COLOR )
        label1 = self._render_text('1: Footstep Game:', self._small_font,  TITLE_COLOR)
        label2 = self._render_text('2: Punch Panda Game:', self._small_font,  TITLE_COLOR)
        label3 = self._render_text('3: Kick a sack Game:',  self._small_font, TITLE_COLOR)

        if (results[0] > self._highscore):
            res_string1 = self._render_text(str(results[0]), self._small_font, RESULT_GOOD_COLOR)
        else:   
            res_string1 = self._render_text(str(results[0]), self._small_font, RESULT_BAD_COLOR)

        if (results[0] > self._highscore):
            res_string2 = self._render_text(str(results[1]), self._small_font, RESULT_GOOD_COLOR)
        else:
            res_string2 = self._render_text(str(results[1]), self._small_font, RESULT_BAD_COLOR)

        if (results[0] > self._highscore):
            res_string3 = self._render_text(str(results[2]), self._small_font, RESULT_GOOD_COLOR)
        else:
            res_string3 = self._render_text(str(results[2]), self._small_font, RESULT_BAD_COLOR)

        l0w, l0h = label0.get_size()
        l1w, l1h = label1.get_size()
        l2w, l2h = label2.get_size()
        l3w, l3h = label3.get_size()

        r1w, r1h = res_string1.get_size()
        r2w, r2h = res_string2.get_size()
        r3w, r3h = res_string3.get_size()

        sw, sh = self._screen.get_size()
        self._screen.fill(BLACK)

        self._screen.blit(label0, (sw/2-l0w/2, l0h/3))

        self._screen.blit(label1, (sw/5, sh/3))
        self._screen.blit(label2, (sw/5, sh/3+l1h*2))
        self._screen.blit(label3, (sw/5, sh/3+l1h*2 +l2h*2))

        self._screen.blit(res_string1, (sw/2+sw/4, sh/3))
        self._screen.blit(res_string2, (sw/2+sw/4, sh/3+l1h*2))
        self._screen.blit(res_string3, (sw/2+sw/4, sh/3+l1h*2 +l2h*2))


        pygame.display.update()
        pygame.mixer.music.play()

    def PrintEndScreen(self):
        print('print: End Screen')

        label0 = self._render_text('SUCCESS', self._big_font, LABEL_COLOR )
        label1 = self._render_text('Finish Game?', self._mid_font, WHITE )
        label2 = self._render_text('NO', self._big_font,  OPTION_COLOR1)
        label3 = self._render_text('YES',  self._big_font, OPTION_COLOR2)
        
    
        l0w, l0h = label0.get_size()
        l1w, l1h = label1.get_size()
        l2w, l2h = label2.get_size()
        l3w, l3h = label3.get_size()

        sw, sh = self._screen.get_size()
        self._screen.fill(BLACK)

        self._screen.blit(label0, (sw/2-l0w/2, l0h/3))

        self._screen.blit(label1, (sw/2-l1w/2, sh/2+l1h/2))

        self._screen.blit(label2, (sw/4-l2w/2, 3*sh/4))
        self._screen.blit(label3, (3*sw/4-l3w/2, 3*sh/4))

        pygame.display.update()
        pygame.mixer.music.play()
        
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
      
        self._serial.connect()       
           
        self._animate_countdown()
        self._blank_screen()
     
        while self._running:   

            if self._stage == 1:
                if not self._player.is_playing():        
                    self._player.play(self._videodir + 'test.mp4', loop = False)
                    print('playing: ' + self._videodir + 'test.mp4')
                    self._stage=2

            if self._stage == 2:
                if not self._player.is_playing(): 
                    print('movie finished, printing result screen')
                    self._blank_screen()
                    self.PrintResults()
                    self._stage =3
 		    #inputCMD= 'rez,1222,22222,3333\n'
        
            if self._stage == 3:  
                #inputCMD= 'rez,1222,22222,3333\n'
                inputCMD= self._serial.read() 
                command = inputCMD.strip().split(",", 8)
             
                if command[0] == "rez":
                    print('arg1: ' + command[1])
                    print('arg2: ' + command[2])
                    print('arg3: ' + command[3])
                    self.PrintResults([command[1],command[2],command[3]])


                    inputCMD=""
                    command=[]
                
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
            
            if self._stage == 4:
                self.PrintEndScreen()
                self._stage = 5

            #if self._stage == 5:

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
    hell_player.run()
