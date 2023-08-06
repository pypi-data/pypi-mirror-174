from sys import platform
import re
from subprocess import PIPE, Popen, check_output
from psutil import Process, process_iter

def getInfo():
    if platform == 'win32':
        return winApp()
    elif platform == 'linux':
        return linApp()


def linApp():
    title = linTitle()
    if title != 'LockScr':
        names = linAppName()
        p = Process(int(check_output(["xdotool", "getactivewindow", "getwindowpid"]).decode("utf-8").strip()))
        pid = p.pid
        p = p.name()
    else:
        names = {'App1': 'LockScr', 'App2': 'LockScr'}
        p = 'LockScr'
        pid = -1
    return {'App1': names['App1'], 'App2': names['App2'], 'Title': title, 'PID': pid, 'PName': p}


def linTitle():
    root = Popen(['xprop', '-root', '_NET_ACTIVE_WINDOW'], stdout=PIPE)
    stdout, stderr = root.communicate()
    res = None
    m = re.search(b'^_NET_ACTIVE_WINDOW.* ([\w]+)$', stdout)
    if m is not None:
        window_id = m.group(1)
        if window_id != b'0x0':
            window = Popen(['xprop', '-id', window_id, 'WM_NAME'], stdout=PIPE)
            stdout, stderr = window.communicate()
        else:
            return 'LockScr'
    match = re.match(b"WM_NAME\(\w+\) = (?P<name>.+)$", stdout)
    if match is not None:
        res = (match.group("name").strip(b'"')).decode('utf-8')
    return res


def linAppName():
    root = Popen(['xprop', '-root', '_NET_ACTIVE_WINDOW'], stdout=PIPE)
    stdout, stderr = root.communicate()
    m = re.search(b'^_NET_ACTIVE_WINDOW.* ([\w]+)$', stdout)
    window_id = m.group(1)

    if m is not None:
        appname1, appname2 = None, None
        process = Popen(['xprop', '-id', window_id, 'WM_CLASS'], stdout=PIPE)
        stdout, stderr = process.communicate()
        pmatch = re.match(b'WM_CLASS\(\w+\) = (?P<name>.+)$', stdout)
        if pmatch is not None:
            appname1, appname2 = pmatch.group('name').decode('UTF-8').split(', ')
            appname1 = appname1.strip('"')
            appname2 = appname2.strip('"')

        return {'App1': appname1,
                'App2': appname2}

    return {'App1': None,
            'App2': None}
def winApp():
    from ctypes import wintypes, windll, byref, c_ulong
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
        for item in process_iter():
            if pid == item.pid:
                thiswin = item.name()
    if thiswin == 'LockApp.exe' and type(pid) == c_ulong:
        wintext = 'LockScr'
        pid = -1
    return {'App1': thiswin, 'App2': thiswin, 'Title': wintext, 'PID': pid, 'PName': thiswin}

def getTitle():
    from win32gui import GetWindowText, GetForegroundWindow
    return GetWindowText(GetForegroundWindow())
