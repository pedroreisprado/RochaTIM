import subprocess
import time
import win32gui
import win32con
import pygetwindow as gw
# from functions.logger import logger

def openProgram(PATH) -> bool:
    processo = subprocess.Popen(PATH)
    time.sleep(50)

    try:
        hwnd = win32gui.GetForegroundWindow()
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        win32gui.SetForegroundWindow(hwnd)
        return True
        
    except Exception as e:
        print(f"Erro ao tentar trazer a janela para o primeiro plano: {e}")
        return False