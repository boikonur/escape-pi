import serial
import time

class SerialCom():
      """ Wrapper class for managing the serial connection with host"""
      def __init__(self):
        self.ser = None
       
      def connect(self):
          """ Connect or disconnect Return connection status."""
          try:
            if self.ser == None:
                self.ser = serial.Serial('/dev/ttyS0', 9600, timeout=1)
                print "Successfully connected on /dev/ttyS0"
                self.ser.flushInput()
                self.ser.flushOutput()
                time.sleep(.1)
                
                self.write("UP") 
                
                return True
            else:
                if self.ser.isOpen():
                    self.ser.close()
                    print "Disconnected."
                    return False
                else:
                    self.ser.open()
                    print "Connected."
                    return True
          except serial.SerialException, e:
            return False


      def flushInput(self)
        self.ser.flushInput()
        time.sleep(.1)
        
      def isConnected(self):
          '''Is the computer connected'''
          try:
            return self.ser.isOpen()
          except:
            return False

      def write(self, command):
          """ Sends command , appending a carraige return. """
          try:
            self.ser.write(command + '\r')
          except Exception, e:
            print "Error sending message %s to host:\n%s" % (command, e)

      def read(self):
          """ Reads specified number of characters from the serial port. """
          return self.ser.readline()
              
      def disconnect(self):
          self.ser.close();
 
def create_serial():
    return SerialCom()