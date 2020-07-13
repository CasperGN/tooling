# SMTP Misc

## smtp_enum.py

Recently came across a need to enumerate through an open port 25 which users were valid through their mail address. Hence the script. 
  
```
[cgn@localhost scripts]$ python smtp_enum.py -h
usage: SMTP Enumerator [-h] [-p P] host users

positional arguments:
  host        Host of the smtp server
  users       File that contains users separated by new line

optional arguments:
  -h, --help  show this help message and exit
  -p P        Port (default: 25)
```