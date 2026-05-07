import ctypes
import os

MEM_COMMIT = 0x00001000
MEM_RESERVE = 0x00002000
PAGE_READWRİTE = 0x04
PROCESS_ALL_ACCES = (0x000F0000 | 0x00100000 | 0xFFFF)


dll_path = input("Dll path: ")
pid = int(input("Process ID(PID): "))


def inject_dll(pid, dll_path):
    dll_len = len(dll_path)

    handle = ctypes.windll.kernel32.OpenProcess(PROCESS_ALL_ACCES, False, pid)
    if not handle:
        print("Acilamadi")
        return
    
    arg_address = ctypes.windll.kernel32.VirtualAllocEx(handle, 0, dll_len, MEM_COMMIT | MEM_RESERVE, PAGE_READWRİTE)

    written = ctypes.c_int(0)
    ctypes.windll.kernel32.WriteProcessMemory(handle, arg_address, dll_path.encode('ascii'), dll_len, ctypes.byref(written))

    kernel32_handle = ctypes.windll.kernel32.GetModuleHandleA(b"kernel32.dll")
    load_library_address = ctypes.windll.kernel32.GetProcAddress(kernel32_handle, b"LoadLibraryA")

    thread_id = ctypes.c_ulong(0)
    if not ctypes.windll.kernel32.Create.RemoteThread(handle,None,0,load_library_address,arg_address,0,ctypes.byref(thread_id)):
        print("Thread olusturulamadi")
        return
    
    print("Dll injected")