import web
from Magstim.MagstimInterface import Rapid2
import sys
import argparse
import time
from threading import Lock, Thread

"""
Where the TMS machine is connected to this computer
"""
SERIAL_PORT = 'COM1'

"""
"""
POWER_THRESHOLD = 80;

"""
"""
PERCENT_THRESHOLD = 110;

urls = (
    '/', 'index', 
    '/TMS/arm', 'tms_arm', 
    '/TMS/disarm', 'tms_disarm', 
    '/TMS/fire', 'tms_fire'
)

class index:
    """
    Returns a readme with how to use this API
    """
    
    def GET(self):
        with open('README.md', 'r') as f:
            return f.read()

class tms_arm:
    """
    Arms the TMS device
    """
    
    def POST(self):
        web.STIMULATOR_LOCK.acquire()
        web.STIMULATOR.armed = True
        web.STIMULATOR_LOCK.release()

class tms_disarm:
    """
    Disarms the TMS device
    """
    
    def POST(self):
        web.STIMULATOR_LOCK.acquire()
        web.STIMULATOR.armed = False
        web.STIMULATOR_LOCK.release()

class tms_fire:
    """
    Triggers a TMS pulse
    """
    
    def POST(self):
        web.STIMULATOR_LOCK.acquire()
        web.STIMULATOR.trigger()
        web.STIMULATOR_LOCK.release()
        
class maintain_communication(Thread):
    def run(self):
        while True:
            web.STIMULATOR_LOCK.acquire()
            web.STIMULATOR.remocon = True
            web.STIMULATOR_LOCK.release()
            
            time.sleep(0.25)

# Report all errors to the client
web.internalerror = web.debugerror

def do_main():
    # Take only a port as an argument
    parser = argparse.ArgumentParser(
            description='Opens a server to control the TMS machine on the given port')
    parser.add_argument('port', type=int)
    args = parser.parse_args()
    
    # Make sure that the server only listens to localhost
    # This is because we cannot allow outside computer to access the TMS
    sys.argv[1] = '127.0.0.1:%d' % args.port

    # Initialize the shared state between web threads
    web.STIMULATOR = Rapid2(port=SERIAL_PORT)
    web.STIMULATOR_LOCK = Lock()
    web.STIMULATOR.remocon = True
    
    # Set the power level
    powerLevel = int(POWER_THRESHOLD * PERCENT_THRESHOLD / 100);
    if powerLevel > 100:
        powerLevel = 100
    elif powerLevel < 0:
        powerLevel = 0
    web.STIMULATOR.intensity = powerLevel
    
    # Start the server
    app = web.application(urls, globals())
    app.run()

if __name__ == '__main__':
    do_main()
