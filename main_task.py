#!/usr/bin/env python
# -*- coding: utf-8 -*-
import importlib
import os
import re
import sys
import signal
import time

import pygame

import requests

BLACK = (0,0,0)
WHITE = (255,255,255)
LABEL_COLOR = (43,170,170)
RESULT_COLOR = (134,67,21)
RESULT_BAD_COLOR = (252,120,120)
RESULT_GOOD_COLOR = (134,252,162)
TITLE_COLOR1 = (255,216,50)
TITLE_COLOR2 = (255,100,50)
TITLE_COLOR3 = (255,25,25)

HIGHSCORE_COLOR=(30, 250, 30)
OPTION_COLOR1= (252,134,134)
OPTION_COLOR2= (134,252,162)
FAIL_LABEL_COLOR = (160, 30, 30)

FAIL_TEXT_BG = u'ПРОВАЛ'
START_TEXT_BG = u'Играта започва след:'
RESULT_TEXT_BG = u'РЕЗУЛТАТ'

START_TEXT_EN = u'Starting in:'
RESULT_TEXT_EN = u'RESULTS'
FAIL_TEXT_EN = u'FAILURE'

GAME_NAME0_BG = u'Изпитание за наблюдателност'
GAME_NAME1_BG = u'Изпитание за сила'
GAME_NAME2_BG  = u'Изпитание за координация'
GAME_NAME3_BG = u'Изпитание за бързина'
GAME_NAME4_BG  = u'Изпитание за ловкост'
GAME_NAME5_BG  = u'Изпитание за точност'

GAME_NAME0_EN = u'Izpitanie Nabludatelnost'
GAME_NAME1_EN = u'Izpitanie za Sila'
GAME_NAME2_EN  = u'Izpitanie za Koordinaciq'
GAME_NAME3_EN = u'Izpitanie za burzina'
GAME_NAME4_EN  = u'Izpitanie za Lovkost'
GAME_NAME5_EN  = u'Izpitanie za Tochnost'

SUCCESS_TEXT_BG  = u'ФИНАЛ'
FIN_QURY_TEXT_BG  = u'Край?'
NO_TEXT_BG  = u'НЕ'
YES_TEXT_BG  = u'ДА'

SUCCESS_TEXT_EN  = u'SUCCESS'
FIN_QURY_TEXT_EN  = u'Finish?'
NO_TEXT_EN  = u'NO'
YES_TEXT_EN  = u'YES'

GAME1_MIN_POINTS = 1
GAME2_MIN_POINTS = 3
GAME3_MIN_POINTS = 3
GAME4_MIN_POINTS = 3
GAME5_MIN_POINTS = 5
GAME6_MIN_POINTS = 5


class Hell_Player():

    def __init__(self):
        self._serial = self._load_serial()
        self._player = self._load_player()        
        self._running = True
        self._stage = 0
        self._prevstage = 1
        self._videodir = "/home/pi/escape-pi/"
        self._highscore = 0
        self._language = 'bg'
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
        self._small_font = pygame.font.Font(None, 60)
        self._mid_font = pygame.font.Font(None, 100)
        self._big_font   = pygame.font.Font(None, 250)
        
    def _load_player(self):     
        return importlib.import_module('omxplayer', 'escape-pi').create_player()
        
    def _load_serial(self):     
        return importlib.import_module('serial_com', 'escape-pi').create_serial()
    
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
        if font is None:
            font = self._small_font
        return font.render(message, True, color, BLACK)

    def _animate_countdown(self, seconds=3):
        label1 = self._render_text(START_TEXT_BG)
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
        self._screen.fill(BLACK)

    def PrintResults(self, results=[0,0,0,0,0,0]):
        print('print: results')

        if self._language == 'bg':
            label0 = self._render_text(RESULT_TEXT_BG, self._big_font,   LABEL_COLOR)
            label1 = self._render_text(GAME_NAME0_BG, self._small_font,  TITLE_COLOR1)
            label2 = self._render_text(GAME_NAME1_BG, self._small_font,  TITLE_COLOR2)
            label3 = self._render_text(GAME_NAME2_BG, self._small_font,  TITLE_COLOR2)
            label4 = self._render_text(GAME_NAME3_BG, self._small_font,  TITLE_COLOR2)
            label5 = self._render_text(GAME_NAME4_BG, self._small_font,  TITLE_COLOR3)
            label6 = self._render_text(GAME_NAME5_BG, self._small_font,  TITLE_COLOR3)
        else:
            label0 = self._render_text(RESULT_TEXT_EN, self._big_font,    LABEL_COLOR)
            label1 = self._render_text(GAME_NAME0_EN, self._small_font,  TITLE_COLOR1)
            label2 = self._render_text(GAME_NAME1_EN, self._small_font,  TITLE_COLOR2)
            label3 = self._render_text(GAME_NAME2_EN, self._small_font,  TITLE_COLOR2)
            label4 = self._render_text(GAME_NAME3_EN, self._small_font,  TITLE_COLOR3)
            label5 = self._render_text(GAME_NAME4_EN, self._small_font,  TITLE_COLOR3)
            label6 = self._render_text(GAME_NAME5_EN, self._small_font,  TITLE_COLOR3)

        if (int(results[0]) > GAME1_MIN_POINTS):
            res_string1 = self._render_text(str(results[0]), self._small_font, RESULT_GOOD_COLOR)
        else:   
            res_string1 = self._render_text(str(results[0]), self._small_font, RESULT_BAD_COLOR)

        if (int(results[1]) > GAME2_MIN_POINTS):
            res_string2 = self._render_text(str(results[1]), self._small_font, RESULT_GOOD_COLOR)
        else:
            res_string2 = self._render_text(str(results[1]), self._small_font, RESULT_BAD_COLOR)

        if (int(results[2]) > GAME3_MIN_POINTS):
            res_string3 = self._render_text(str(results[2]), self._small_font, RESULT_GOOD_COLOR)
        else:
            res_string3 = self._render_text(str(results[2]), self._small_font, RESULT_BAD_COLOR)

        if (int(results[3]) > GAME4_MIN_POINTS):
            res_string4 = self._render_text(str(results[3]), self._small_font, RESULT_GOOD_COLOR)
        else:
            res_string4 = self._render_text(str(results[3]), self._small_font, RESULT_BAD_COLOR)

        if (int(results[4]) > GAME5_MIN_POINTS):
            res_string5 = self._render_text(str(results[4]), self._small_font, RESULT_GOOD_COLOR)
        else:
            res_string5 = self._render_text(str(results[4]), self._small_font, RESULT_BAD_COLOR)

        if (int(results[5]) > GAME6_MIN_POINTS):
            res_string6 = self._render_text(str(results[5]), self._small_font, RESULT_GOOD_COLOR)
        else:
            res_string6 = self._render_text(str(results[5]), self._small_font, RESULT_BAD_COLOR)

        l0w, l0h = label0.get_size()

        l1w, l1h = label1.get_size()
        l2w, l2h = label2.get_size()
        l3w, l3h = label3.get_size()
        l4w, l4h = label4.get_size()
        l5w, l5h = label5.get_size()
        l6w, l6h = label6.get_size()

        r1w, r1h = res_string1.get_size()
        r2w, r2h = res_string2.get_size()
        r3w, r3h = res_string3.get_size()
        r4w, r4h = res_string4.get_size()
        r5w, r5h = res_string5.get_size()
        r6w, r6h = res_string6.get_size()

        sw, sh = self._screen.get_size()
        self._screen.fill(BLACK)

        self._screen.blit(label0, (sw/2-l0w/2, l0h/3))

        self._screen.blit(label1, (sw/5, sh/3))
        self._screen.blit(label2, (sw/5, sh/3+l1h*2))
        self._screen.blit(label3, (sw/5, sh/3+l1h*2 +l2h*2))
        self._screen.blit(label4, (sw/5, sh/3+l1h*2 +l2h*2 + l3h*2))
        self._screen.blit(label5, (sw/5, sh/3+l1h*2 +l2h*2 + l3h*2 +l4h*2))
        self._screen.blit(label6, (sw/5, sh/3+l1h*2 +l2h*2 + l3h*2 +l4h*2+l5h*2))

        self._screen.blit(res_string1, (sw/2+sw/4, sh/3))
        self._screen.blit(res_string2, (sw/2+sw/4, sh/3+l1h*2))
        self._screen.blit(res_string3, (sw/2+sw/4, sh/3+l1h*2 +l2h*2))
        self._screen.blit(res_string4, (sw/2+sw/4, sh/3+l1h*2 +l2h*2 +l3h*2))
        self._screen.blit(res_string5, (sw/2+sw/4, sh/3+l1h*2 +l2h*2 +l3h*2 +l4h*2))
        self._screen.blit(res_string6, (sw/2+sw/4, sh/3+l1h*2 +l2h*2 +l3h*2 +l4h*2 +l5h*2))

        pygame.display.update()
        pygame.mixer.music.play()

    def PrintEndScreen(self):
        print('print: End Screen')
        if self._language == 'bg':
            label0 = self._render_text(SUCCESS_TEXT_BG, self._big_font, LABEL_COLOR )
            label1 = self._render_text(FIN_QURY_TEXT_BG, self._mid_font, WHITE )
            label3 = self._render_text(NO_TEXT_BG, self._big_font,  OPTION_COLOR1)
            label4 = self._render_text(YES_TEXT_BG,  self._big_font, OPTION_COLOR2)
        else:
            label0 = self._render_text(SUCCESS_TEXT_EN, self._big_font, LABEL_COLOR )
            label1 = self._render_text(FIN_QURY_TEXT_EN, self._mid_font, WHITE )
            label3 = self._render_text(NO_TEXT_EN, self._big_font,  OPTION_COLOR1)
            label4 = self._render_text(YES_TEXT_EN,  self._big_font, OPTION_COLOR2)
           
        label2 = self._render_text(unicode(self._highscore), self._big_font, HIGHSCORE_COLOR )
    
        l0w, l0h = label0.get_size()
        l1w, l1h = label1.get_size()
        l2w, l2h = label2.get_size()
        l3w, l3h = label3.get_size()
        l4w, l4h = label4.get_size()

        sw, sh = self._screen.get_size()
        self._screen.fill(BLACK)

        self._screen.blit(label0, (sw/2-l0w/2, l0h/3))

        self._screen.blit(label1, (sw/2-l1w/2, sh/2+l1h/2))
        self._screen.blit(label2, (sw/2-l2w/2, sh/2-l2h))

        self._screen.blit(label3, (sw/4-l2w/2, 3*sh/4))
        self._screen.blit(label4, (3*sw/4-l3w/2, 3*sh/4))

        pygame.display.update()
        pygame.mixer.music.play()
       
    def PrintFailure(self):
        print('print: End Screen')
        if self._language == 'bg':
            label0 = self._render_text(FAIL_TEXT_BG, self._big_font, FAIL_LABEL_COLOR )    
        else:
            label0 = self._render_text(FAIL_TEXT_EN, self._big_font, FAIL_LABEL_COLOR )
          
        l0w, l0h = label0.get_size()
        sw, sh = self._screen.get_size()

        self._screen.fill(BLACK)
        self._screen.blit(label0, (sw/2-l0w/2, sh/2-l0h/2))
        pygame.display.update()

    def _blank_screen(self):
        """Render a blank screen filled with the background color."""
        self._screen.fill(BLACK)
        pygame.display.update()

    def _service_screen(self):
        """Render a blank screen filled with the background color."""
        sw, sh = self._screen.get_size()
        self._screen.fill(BLACK)        
        service_text1 = self._render_text(u'Бутон 1 и 3 за  Език (20сек.)', self._small_font, RESULT_BAD_COLOR)
        service_text2 = self._render_text(u'Бутон 1 и 2 за  Изключване (20сек.)', self._small_font, RESULT_BAD_COLOR)

        l0w, l0h = service_text1.get_size()
        l1w, l1h = service_text2.get_size()
        self._screen.blit(service_text1, (sw/2-l0w/2, sh/3))
        self._screen.blit(service_text2, (sw/2-l1w/2, sh/3+2*l0h))
        pygame.display.update()

    def _post_request(self):
        url = 'http://requestb.in/znx6gnzn'
        headers = {'Content-Type' : 'application/json'}
        login_payload = {'device_info': {'app-id': 'fc', 'os-type': 'os'}}

        #authentication = (login, password)  # Anyone who sees your authorization will be able to get this anyway

        #response = requests.post(url, data=login_payload, auth=authentication, headers=headers))
        responce = requests.post(url, data=login_payload, headers=headers)
        print 'POST Code:' + str(responce.status_code)
        print 'POST Content:' + str(responce.content)
        
    def run(self):   
      
        self._serial.connect()  
                 
        self._blank_screen()

        #self._post_request()

        while self._running:   

            if self._prevstage != self._stage:
                self._prevstage = self._stage
                print("STAGE:" +  str(self._stage))

            inputCMD= self._serial.read() 

            if inputCMD == "lang_bg"+"\n":
                    inputCMD=""
                    self._language='bg'
                    pygame.mixer.music.play()

            if inputCMD == "lang_en"+"\n":
                    inputCMD=""
                    self._language='en'
                    pygame.mixer.music.play()
                    
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

            if inputCMD == "failgame"+ "\n":
                inputCMD=""
                self._stage == 0
                self.PrintFailure()
              #  self._post_request()
            
            if inputCMD == "reset"+"\n":
                    inputCMD=""
                    print("Reset CMD")
                    self._player.stop()
                    self._highscore = 0
                    self._stage = 0  
                    self._blank_screen()
                    #self.ScreenOff()
                   #self._post_request()

            if inputCMD == "replay"+"\n":
                    inputCMD=""
                    print("Replay CMD")               
                    self._blank_screen()
                    self._stage == 3
                    #self.ScreenOff()
                   #self._post_request()     
            
            if inputCMD == "startgame"+"\n":
                inputCMD=""
                #self.ScreenOn()
                self._animate_countdown()
                self._stage = 1

            #stage game
            # if self._stage == 0:
            #     self._stage == 1

            if self._stage == 1:
                if not self._player.is_playing():        
                    self._player.play(self._videodir + 'test.mp4', loop = False)
                    print('playing: ' + self._videodir + 'test.mp4')
                    self._stage = 2

            if self._stage == 2:
                if not self._player.is_playing(): 
                    print('movie finished, printing result screen')
                    self._blank_screen()
                    self.PrintResults()
                    self._stage = 3
 		         
            if self._stage == 3:  
                command = inputCMD.strip().split(",", 10)
             
                if command[0] == "rez":
                    print("Incomming results")
                    for idx, word in enumerate(command):
                        print('arg' + str(idx) +':'+ word)
            
                    self._highscore= int(command[1])+int(command[2])+int(command[3])+int(command[4])+int(command[5])+int(command[6])
                    self.PrintResults([command[1],command[2],command[3],command[4],command[5],command[6]])

                    if int(command[5]) > GAME5_MIN_POINTS and int(command[6]) > GAME6_MIN_POINTS:
                       print("All Games are won")
                       self._stage=4                  
                    
                    inputCMD=""
                    command=[]          

            if self._stage == 4:
                self.PrintEndScreen()
                self._stage = 5

            if self._stage == 5:
                command = inputCMD.strip().split(",", 10)
                if command[0] == "rez":
                    self._stage = 3

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
