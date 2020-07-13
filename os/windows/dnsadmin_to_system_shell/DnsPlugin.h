#define DNSPLUGIN_API extern "C" __declspec(dllexport)

DNSPLUGIN_API int DnsPluginInitialize(PVOID, PVOID);
DNSPLUGIN_API int DnsPluginCleanup();
DNSPLUGIN_API int DnsPluginQuery(PVOID, PVOID,PVOID,PVOID);
