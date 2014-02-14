import web
from Magstim.MagstimInterface import Rapid2
import sys
import argparse
from threading import Lock

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

"""
Holds the interface to the Rapid2 TMS device
"""
STIMULATOR = None

"""
Prevents multi-threaded access to the stimulator
Since the underlying implementation of web.py is unknown, 
    we should control access to the stimulator in this interface
"""
STIMULATOR_LOCK = Lock()

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
        STIMULATOR_LOCK.acquire()
        STIMULATOR.armed = True
        STIMULATOR_LOCK.release()

class tms_disarm:
    """
    Disarms the TMS device
    """
    
    def POST(self):
        STIMULATOR_LOCK.acquire()
        STIMULATOR.armed = False
        STIMULATOR_LOCK.release()

class tms_fire:
    """
    Triggers a TMS pulse
    """
    
    def POST(self):
        STIMULATOR_LOCK.acquire()
        STIMULATOR.trigger()
        STIMULATOR_LOCK.release()

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
    
    # Start the TMS device
    STIMULATOR = Rapid2(port=SERIAL_PORT)
    
    # Set the power level
    powerLevel = int(POWER_THRESHOLD * PERCENT_THRESHOLD / 100);
    if powerLevel > 100:
        powerLevel = 100
    elif powerLevel < 0:
        powerLevel = 0
    STIMULATOR.intensity = powerLevel
    
    # Start the server
    app = web.application(urls, globals())
    app.run()

if __name__ == '__main__':
    do_main()
