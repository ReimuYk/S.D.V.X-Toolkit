import win32gui
import win32api
import win32con
import time, math, random
import win32process
import ctypes

# global value
display_value = 9876
DLL = ctypes.windll.LoadLibrary(".\\kernel32.dll")
PROCESS = None
total_notes = 0
score = 0
critical_note = 0
near_note = 0
error_note = 0

# config values
num_spa = 10
num_w = 5
off_x = 3
off_y = 3
off_padding = 10
alpha_level = 200
score_addr = 0x18810EF8
critical_addr = 0x18810F0C
near_addr = 0x18810F10
error_addr = 0x18810F14

# pre-calculated
num_xy = [{'x0':0,              'y0':0,                 'x1':2*num_w+num_spa,   'y1':num_w},
          {'x0':0,              'y0':0,                 'x1':num_w,             'y1':2*num_w+num_spa},
          {'x0':num_w+num_spa,  'y0':0,                 'x1':2*num_w+num_spa,   'y1':2*num_w+num_spa},
          {'x0':0,              'y0':num_w+num_spa,     'x1':2*num_w+num_spa,   'y1':2*num_w+num_spa},
          {'x0':0,              'y0':num_w+num_spa,     'x1':num_w,             'y1':3*num_w+2*num_spa},
          {'x0':num_w+num_spa,  'y0':num_w+num_spa,     'x1':2*num_w+num_spa,   'y1':3*num_w+2*num_spa},
          {'x0':0,              'y0':2*num_w+2*num_spa, 'x1':2*num_w+num_spa,   'y1':3*num_w+2*num_spa}]
window_width = (2*off_x) + (8*num_w + 4*num_spa) + (3*off_padding) + 16
window_height = (2*off_y) + (3*num_w + 2*num_spa) + 39

def OnPaint_2(hwnd, msg, wp, lp):
    global display_value
    def num2vertices(num, off_x=30, off_y=30, red=0xff00, green=0, blue=0, alpha=0):
        global num_xy
        lines = [(
            {'x':p['x0']+off_x, 'y':p['y0']+off_y, 'Red':red, 'Green':green, 'Blue':blue, 'Alpha':alpha},
            {'x':p['x1']+off_x, 'y':p['y1']+off_y, 'Red':red, 'Green':green, 'Blue':blue, 'Alpha':alpha},
            ) for p in num_xy]
        if num==9:
            return [lines[0], lines[1], lines[2], lines[3], lines[5], lines[6]]
        if num==8:
            return lines
        if num==7:
            return [lines[0], lines[2], lines[5]]
        if num==6:
            return [lines[0], lines[1], lines[3], lines[4], lines[5], lines[6]]
        if num==5:
            return [lines[0], lines[1], lines[3], lines[5], lines[6]]
        if num==4:
            return [lines[1], lines[2], lines[3], lines[5]]
        if num==3:
            return [lines[0], lines[2], lines[3], lines[5], lines[6]]
        if num==2:
            return [lines[0], lines[2], lines[3], lines[4], lines[6]]
        if num==1:
            return [lines[2], lines[5]]
        if num==0:
            return [lines[0], lines[1], lines[2], lines[4], lines[5], lines[6]]
        return [lines[3]]
            
    dc, ps=win32gui.BeginPaint(hwnd)
    win32gui.SetGraphicsMode(dc, win32con.GM_ADVANCED)
    l,t,r,b=win32gui.GetClientRect(hwnd)

    # 1st num
    val1 = display_value // 1000
    off_x1 = off_x
    for vertices in num2vertices(val1, off_x1, off_y):
        mesh=((0,1),)
        win32gui.GradientFill(dc,vertices, mesh, win32con.GRADIENT_FILL_RECT_H)
    # 2nd num
    val2 = (display_value // 100) % 10
    off_x2 = off_x + (2*num_w + num_spa) + (off_padding)
    for vertices in num2vertices(val2, off_x2, off_y):
        mesh=((0,1),)
        win32gui.GradientFill(dc,vertices, mesh, win32con.GRADIENT_FILL_RECT_H)
    # 3rd num
    val3 = (display_value // 10) % 10
    off_x3 = off_x + (4*num_w + 2*num_spa) + (2*off_padding)
    for vertices in num2vertices(val3, off_x3, off_y):
        mesh=((0,1),)
        win32gui.GradientFill(dc,vertices, mesh, win32con.GRADIENT_FILL_RECT_H)
    # 4th num
    val4 = display_value % 10
    off_x4 = off_x + (6*num_w + 3*num_spa) + (3*off_padding)
    for vertices in num2vertices(val4, off_x4, off_y):
        mesh=((0,1),)
        win32gui.GradientFill(dc,vertices, mesh, win32con.GRADIENT_FILL_RECT_H)
        
    win32gui.EndPaint(hwnd, ps)
    return 0
wndproc_2={win32con.WM_PAINT:OnPaint_2}

def process_init():
    global PROCESS
    HANDLE = win32gui.FindWindow(None,'SOUND VOLTEX IV HEAVENLY HAVEN 1')
    if HANDLE==0:
        print("Warning: PROCESS NOT AVAILABLE")
        return
    hid,pid = win32process.GetWindowThreadProcessId(HANDLE)
    PROCESS = win32api.OpenProcess(win32con.PROCESS_VM_READ|
                                   win32con.PROCESS_VM_WRITE|
                                   win32con.PROCESS_VM_OPERATION,True,pid)

def VMREAD(addr):
    base = ctypes.c_int()
    DLL.ReadProcessMemory(int(PROCESS),addr,ctypes.byref(base),4,None)
##    print("0x%X"%addr,end='\t')
##    print(base)
    return base.value

def update_display_value():
    global display_value, score, total_notes, critical_note, near_note, error_note
    t_score = VMREAD(score_addr)
    t_critical = VMREAD(critical_addr)
    t_near = VMREAD(near_addr)
    t_error = VMREAD(error_addr)

    # new play count when score decreases
    if t_score < score:
        dispaly_value = 9999
        score = 0
        total_notes = 0
        critical_note = 0
        near_note = 0
        error_note = 0
        return

    # confirm total_notes when two same VMREAD non-zero result
    if total_notes == 0:
        if t_score != 0 and t_score == score and t_critical == critical_note \
           and t_near == near_note and t_error == error_note:
            total_notes = round(10000000/(2*score/(2*critical_note+near_note)))
        score = t_score
        critical_note = t_critical
        near_note = t_near
        error_note = t_error
        return

    # confirm display value
    score = t_score
    critical_note = t_critical
    near_note = t_near
    error_note = t_error
    display_value = int((1-(near_note+2*error_note)/(2*total_notes))*10000)

def run():
    global display_value
    wc = win32gui.WNDCLASS()
    wc.lpszClassName = 'sdvx_scoreboard'
    wc.style =  win32con.CS_GLOBALCLASS|win32con.CS_VREDRAW | win32con.CS_HREDRAW
    wc.hbrBackground = win32con.COLOR_WINDOW+1
    wc.lpfnWndProc=wndproc_2
    class_atom=win32gui.RegisterClass(wc)       
    hwnd = win32gui.CreateWindowEx(0, class_atom,'SDVX-Scoreboard',
        win32con.WS_CAPTION|win32con.WS_VISIBLE|win32con.WS_THICKFRAME|win32con.WS_SYSMENU,
        100,100,window_width,window_height, 0, 0, 0, None)
    s=win32gui.GetWindowLong(hwnd,win32con.GWL_EXSTYLE)
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, s|win32con.WS_EX_LAYERED)
    win32gui.SetLayeredWindowAttributes(hwnd, 0, alpha_level, win32con.LWA_ALPHA)
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

    process_init()
    while True:
        time.sleep(0.2)
        update_display_value()
        win32gui.InvalidateRect(hwnd, None, True)
        win32gui.PumpWaitingMessages()

run()
