import argparse
import sys
import socket


class SMTPEnum():

    def __init__(self, host, port, users):
        self.host = host
        self.port = port

        self.users = []
        with open(users, 'r') as usr:
            self.users = [user.strip('\n') for user in usr.readlines()]
        
        self.run()

    def run(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.connect((self.host, self.port))

            connected = sock.recv(1024)
            connected = connected.decode()
            for user in self.users:
                sock.sendall(f'VRFY {user}\r\n'.encode())
                resp = sock.recv(1024)
                if str(resp.decode()).split(" ")[0] == '252':
                    print(user)
        except Exception as e:
            print(f'Something went wrong: {e}')
        finally:
            sock.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='SMTP Enumerator')
    parser.add_argument('host', type=str, help='Host of the smtp server')
    parser.add_argument('users', type=str, help='File that contains users separated by new line')
    parser.add_argument('-p', type=int, help='Port (default: 25)')
    
    if sys.argv == 1:
        parser.print_help()
        sys.exit(1)
    
    args = parser.parse_args()

    port = args.p if args.p else 25

    smtpenumerator = SMTPEnum(args.host, port, args.users)