import pyautogui as pygui
import time
import sys
import os


# Obter informações sobre quando o último vídeo visualizado parou
def last_time():
    manager_data = open('manager_data.txt','r')
    last_time = manager_data.read()
    manager_data.close()

    return last_time

