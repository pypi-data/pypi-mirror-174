from win32gui import GetWindowText, GetForegroundWindow
import psutil
from ctypes import wintypes, windll, byref, c_ulong

def getInfo():
    thiswin = ''
    wintext = getTitle()
    pid = wintypes.DWORD()
    active = windll.user32.GetForegroundWindow()  # Don't delete it
    windll.user32.GetWindowThreadProcessId(active, byref(pid))
    if active == 0 or active == 67370 or active == 1901390:
        thiswin = 'LockApp.exe'
    # 10553666 - return code for unlocked workstation1
    # 0 - return code for locked workstation1
    #
    # 132782 - return code for unlocked workstation2
    # 67370 -  return code for locked workstation2
    #
    # 3216806 - return code for unlocked workstation3
    # 1901390 - return code for locked workstation3
    #
    # 197944 - return code for unlocked workstation4
    # 0 -  return code for locked workstation4
    else:
        pid = pid.value
        for item in psutil.process_iter():
            if pid == item.pid:
                thiswin = item.name()
    if thiswin == 'LockApp.exe' and type(pid) == c_ulong:
        wintext = 'LockScr'
        pid = -1
    return {'App1': thiswin, 'App2': thiswin, 'Title': wintext, 'PID': pid, 'PName': thiswin}

def getTitle():
    return GetWindowText(GetForegroundWindow())
