import argparse
import requests

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            description='Triggers the TMS machine via a server on the given port')
    parser.add_argument('port', type=int)
    args = parser.parse_args()
    
    requests.post('http://localhost:%d/TMS/fire' % args.port)
