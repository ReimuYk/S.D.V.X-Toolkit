import win32gui
import win32api
import win32con
import time, math, random

# global value
display_value = 1234

# config values
num_spa = 150
num_w = 20
off_x = 30
off_y = 30
off_padding = 10

# pre-calculated
num_xy = [{'x0':0,              'y0':0,                 'x1':2*num_w+num_spa,   'y1':num_w},
          {'x0':0,              'y0':0,                 'x1':num_w,             'y1':2*num_w+num_spa},
          {'x0':num_w+num_spa,  'y0':0,                 'x1':2*num_w+num_spa,   'y1':2*num_w+num_spa},
          {'x0':0,              'y0':num_w+num_spa,     'x1':2*num_w+num_spa,   'y1':2*num_w+num_spa},
          {'x0':0,              'y0':num_w+num_spa,     'x1':num_w,             'y1':3*num_w+2*num_spa},
          {'x0':num_w+num_spa,  'y0':num_w+num_spa,     'x1':2*num_w+num_spa,   'y1':3*num_w+2*num_spa},
          {'x0':0,              'y0':2*num_w+2*num_spa, 'x1':2*num_w+num_spa,   'y1':3*num_w+2*num_spa}]

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
        return None
    
            
    dc, ps=win32gui.BeginPaint(hwnd)
    win32gui.SetGraphicsMode(dc, win32con.GM_ADVANCED)
    l,t,r,b=win32gui.GetClientRect(hwnd)
    print(l,t,r,b) # for debug

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

def f():
    global display_value
    wc = win32gui.WNDCLASS()
    wc.lpszClassName = 'test_win32gui_2'
    wc.style =  win32con.CS_GLOBALCLASS|win32con.CS_VREDRAW | win32con.CS_HREDRAW
    wc.hbrBackground = win32con.COLOR_WINDOW+1
    wc.lpfnWndProc=wndproc_2
    class_atom=win32gui.RegisterClass(wc)       
    hwnd = win32gui.CreateWindowEx(0, class_atom,'SDVX-Scoreboard',
        win32con.WS_CAPTION|win32con.WS_VISIBLE|win32con.WS_THICKFRAME|win32con.WS_SYSMENU,
        100,100,1000,500, 0, 0, 0, None)
    s=win32gui.GetWindowLong(hwnd,win32con.GWL_EXSTYLE)
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, s|win32con.WS_EX_LAYERED)
    win32gui.SetLayeredWindowAttributes(hwnd, 0, 60, win32con.LWA_ALPHA)
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

    # refresh & display
##    win32gui.InvalidateRect(hwnd, None, True)
##    win32gui.PumpWaitingMessages()
    for i in range(10):
        win32gui.InvalidateRect(hwnd, None, True)
        win32gui.PumpWaitingMessages()
        display_value += 1
        time.sleep(0.3)
##    win32gui.DestroyWindow(hwnd)
##    win32gui.UnregisterClass(class_atom,None)


f()
