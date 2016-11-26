# Copyright 2015 Adafruit Industries.
# Author: Tony DiCola
# License: GNU GPLv2, see LICENSE.txt
import os
import subprocess
import time


class OMXPlayer():

    def __init__(self):

        self._process = None 
        
 
        print("omx: constructor")
       

    def play(self, movie, loop=False, vol=0):
       
        print("omx: play")
        self.stop(3)  # Up to 3 second delay to let the old player stop.
        # Assemble list of arguments.
        args = ['/usr/bin/omxplayer']
        args.extend(['-o', 'hdmi'])   #('hdmi', 'local', 'both')
        args.extend('--no-osd --audio_fifo 0.01 --video_fifo 0.01') # video FIFO buffers are kept low to reduce clipping ends of movie at loop.
        if vol is not 0:
            args.extend(['--vol', str(vol)])
        if loop:
            args.append('--loop')         # Add loop parameter if necessary.
        args.append(movie)                # Add movie file path.
        # Run omxplayer process and direct standard output to /dev/null.
        #self._process = subprocess.Popen(args, stdout=open(os.devnull, 'wb'), close_fds=True)
        print(str(args))
        self._process = subprocess.Popen(args)
        print("popen: " +str( self._process.pid) + " ret code: " +str(self._process.returncode))
 

    def is_playing(self):
        """Return true if the video player is running, false otherwise."""
        if self._process is None:
            return False
        self._process.poll()
        return self._process.returncode is None

    def stop(self, block_timeout_sec=None):
        """Stop the video player.  block_timeout_sec is how many seconds to
        block waiting for the player to stop before moving on.
        """
        # Stop the player if it's running.
        if self._process is not None and self._process.returncode is None:
            # There are a couple processes used by omxplayer, so kill both
            # with a pkill command.
            subprocess.call(['pkill', '-9', str(self._process.pid)])
        # If a blocking timeout was specified, wait up to that amount of time
        # for the process to stop.
        start = time.time()
        while self._process is not None and self._process.returncode is None:
            if (time.time() - start) >= block_timeout_sec:
                break
            time.sleep(0)
        # Let the process be garbage collected.
        self._process = None


def create_player():
    """Create new video player based on omxplayer."""
    return OMXPlayer()