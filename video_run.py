import pyautogui as pygui
import clipboard
import time
import sys
import os

track_total_time = None
current_time = 0


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

    # Obtendo tempo total do vídeo
    global track_total_time
    track_total_time = total_time()
    

    # Sequência de comandos para avançar para tempo específico dentro do VLC Media Player
    pygui.hotkey('ctrl', 'g')
    pygui.write(last_time[1])
    pygui.press('enter')

# Formatar para padrão de tempo do projeto
def format_time(time):
    return ''.join(x for x in time if x.isnumeric())


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
    global current_time
    current_time = format_time(clipboard.paste())
    manager_data.write(f'{last_time[0]}\n{current_time}')
    manager_data.close()


# Obter tempo total do vídeo    
def total_time():
    # Obtendo tempo total
    pygui.hotkey('shift', 'f10')
    pygui.press(['tab', 'tab', 'tab', 'tab'])
    pygui.hotkey('ctrl', 'c')
    pygui.press('esc')
    total_time = clipboard.paste()

    # Convertendo pra valores utilizados
    total_time = total_time.split(':')
    minutes = int(total_time[0]) * 60 + int(total_time[1])
    seconds = total_time[2]
    
    return format_time(f'{minutes}:{seconds}.000')


# Pular para próxima faixa
def next_track():
    global current_time
    current_time = 0

    # Obtendo nome da faixa
    pygui.press('pagedown')
    time.sleep(2)
    pygui.hotkey('shift', 'f10')
    pygui.press('tab')
    pygui.hotkey('ctrl', 'c')
    pygui.press('esc')

    # Atualizando arquivo manager_data.txt
    manager_data = open('manager_data.txt','w', encoding='utf-8')
    manager_data.write(f'{clipboard.paste()}\n0000000')
    manager_data.close()

    # Obtendo tempo total do vídeo
    global track_total_time
    track_total_time = total_time()


# Abrindo vídeo
last_time = last_time()
open_video(last_time)

# Atualizando tempo atual a cada 10 segundos
while True:
    while int(current_time) < int(track_total_time)-1000.0:
        time.sleep(10)
        update_time()

        print(current_time, track_total_time)

    next_track()

