import pyautogui as pygui
import clipboard
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
    pygui.hotkey('ctrl', 'g')
    pygui.write(last_time[1])
    pygui.press('enter')


# Obter tempo atual do vídeo
def update_time():
    # Obtendo tempo
    pygui.hotkey('ctrl', 'g')
    pygui.hotkey('ctrl', 'a')
    pygui.hotkey('ctrl', 'c')
    pygui.press('esc')

    # Atualizando manager_data
    manager_data = open('manager_data.txt','r', encoding='utf-8')
    last_time = manager_data.read().split('\n')
    manager_data.close()

    manager_data = open('manager_data.txt','w', encoding='utf-8')
    manager_data.write(f'{last_time[0]}\n{clipboard.paste()}')
    manager_data.close()

    
last_time = last_time()
open_video(last_time)

while True:
    time.sleep(10)
    update_time()