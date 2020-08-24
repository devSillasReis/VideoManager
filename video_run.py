import pyautogui as pygui
import time
import sys
import os


# Obter informações sobre quando o último vídeo visualizado parou
def last_time():
    manager_data = open('manager_data.txt','r', encoding='utf-8')
    last_time = manager_data.read().split('\n')
    manager_data.close()

    return last_time


# Abrir vídeo em tempo específico
def open_video(last_time):
    # Comando para abrir vídeo varia de acordo com o sistema
    if sys.platform == 'win32':
        os.startfile(last_time[0])

    # Espera para dar tempo do vídeo abrir
    time.sleep(5)

    # Sequência de comandos para avançar para tempo específico dentro do VLC Media Player
    pygui.hotkey('ctrl', 't')
    time.sleep(0.2)
    pygui.write(last_time[1])
    pygui.press(['tab', 'tab', 'enter'])

