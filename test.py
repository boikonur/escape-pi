#!/usr/bin/env python

import importlib
import os
import re
import sys
import signal
import time



class test_Player():

    def __init__(self):
    
        self._player = self._load_player()        
 
        self._videodir = "/home/pi/escape-pi/"
        
     
        
    def _load_player(self):     
        return importlib.import_module('omxplayer', 'escape-pi') \
            .create_player()
        
  
        
    def run(self):   
      
        #self._serial.connect()       
           
     
        self._player.play(self._videodir + 'test.mp4', loop = False)

        while 1:
            time.sleep(1)
           
                

      

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
    hell_player = test_Player()
    # Configure signal handlers to quit on TERM or INT signal.
    signal.signal(signal.SIGTERM, hell_player.signal_quit)
    signal.signal(signal.SIGINT, hell_player.signal_quit)
    # Run the main loop.
    hell_player.run()
