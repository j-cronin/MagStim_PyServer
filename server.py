import web
import Magstim
import sys
import argparse

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
    
    """
    
    def POST(self):
        pass

class tms_disarm:
    """
    
    """
    
    def POST(self):
        pass

class tms_fire:
    """
    
    """
    
    def POST(self):
        pass

# Report all errors to the client
web.internalerror = web.debugerror

if __name__ == '__main__':
    # Take only a port as an argument
    parser = argparse.ArgumentParser(
            description='Opens a server to control the TMS machine on the given port')
    parser.add_argument('port', type=int)
    args = parser.parse_args()
    
    # Make sure that the server only listens to localhost
    # This is because we cannot allow outside computer to access the TMS
    sys.argv[1] = '127.0.0.1:%d' % args.port
    
    # Start the server
    app = web.application(urls, globals())
    app.run()

