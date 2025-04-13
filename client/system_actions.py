# client/system_actions.py
import ctypes
import pyautogui
import os

# Lock system
def lock_system():
    ctypes.windll.user32.LockWorkStation()

# Block website (modifies hosts file to block access)
def block_website(domain="www.youtube.com"):
    hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
    redirect = "127.0.0.1"
    with open(hosts_path, 'a') as file:
        file.write(f"\n{redirect} {domain}\n")
