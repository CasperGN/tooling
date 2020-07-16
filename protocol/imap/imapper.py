import imaplib
import argparse
import sys
import time


class IMAPPER():


    def __init__(self, host, user, passwd, port=143):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.port = port

        self.mail = ''

        self.folders = []
        self.fetched = {}

        self.run()

        for folder in self.folders:
            self.fetch(folder)

   

    def run(self):
        self.mail = imaplib.IMAP4(self.host, self.port)
        self.mail.login(self.user, self.passwd)
        print('[+] Login succesfull')

        # mail.list returns a tuple, first is if it was a success
        _, folders = self.mail.list()
        print(f'[+] Folders: {folders}')
        
        for folder in folders:
            foldersplit = folder.decode().split(' ')[2:]
            realfolder = ''
            if 'INBOX' not in foldersplit[0]:
                for item in foldersplit[1:]:
                    realfolder += item            
            else:
                for item in foldersplit:
                    realfolder += item
                    if item != foldersplit[-1]:
                        realfolder += ' '
            self.folders.append(realfolder)
        

    def fetch(self, folder):
        ok, _ = self.mail.select(f'{folder}')
        if ok == "OK":
            _, data = self.mail.search(None, 'ALL')
            if data:
                if data[0] is not None:
                    for num in data[0].split():
                        _, data = self.mail.fetch(num, '(RFC822)')                
                        print(f'Fetch from {folder}:\nMessage: {num}\n{data[0][1]}\n')
            self.mail.close()
        return


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Imapper')
    parser.add_argument('imaphost', type=str, help='Host/IP of the IMAP server')
    parser.add_argument('user', type=str, help='User to login with')
    parser.add_argument('password', type=str, help='Password of the user')
    parser.add_argument('-p', type=int, help='Port to connect to (Default: 143)')

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    if args.p:
        imapper = IMAPPER(args.imaphost, args.user, args.password, args.p)
    else:
        imapper = IMAPPER(args.imaphost, args.user, args.password)