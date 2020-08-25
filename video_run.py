import pyautogui as pygui
import pygetwindow as gw
import clipboard
import time
import sys
import os

track_total_time = None
current_time = 0


class FinishProgram(Exception):
    pass


# Obter informações sobre quando o último vídeo visualizado parou
def last_time():
    manager_data = open('manager_data.txt','r', encoding='utf-8')
    last_time = manager_data.read().split('\n')
    manager_data.close()

    return last_time


# Abrir vídeo
def open_video(last_time):
    # Comando para abrir vídeo varia de acordo com o sistema
    if sys.platform == 'win32':
        os.startfile(last_time[0])


# Espera a janela do vídeo abrir para dar continuidade
def wait_open(window_title):
    opened = False
    while opened is False:
        try:
            video_window = gw.getWindowsWithTitle(window_title)[0]
            opened = True
        except IndexError:
            pass


# Avançar para o período em que parou na última vez
def time_adjust(last_time):
    #Obtendo foco
    video_window = gw.getWindowsWithTitle(last_time[0])[0]
    video_window.minimize()
    video_window.maximize()
    
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
    time.sleep(0.5)
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


# Espera foco da janela para realizar uma ação
def focus(action):
    # Obtendo nome da janela
    manager_data = open('manager_data.txt','r', encoding='utf-8')
    track_title = manager_data.read().split('\n')[0]
    manager_data.close()
    
    # Obtendo informações da janela do vídeo e a janela atualmente em foco
    active_window = gw.getActiveWindow()
    try:
        video_window = gw.getWindowsWithTitle(track_title)[0]
    except IndexError:
        raise FinishProgram()
    
    # Se a janela em foco não for a do vídeo, espera até que seja
    if active_window != video_window:
        while not video_window.isActive:
            pass
    
    # Atualiza o tempo gravado
    if action == 'update_time()':
        update_time()


# Abrindo vídeo e ajustando tempo
last_time = last_time()
open_video(last_time)
wait_open(last_time[0])
time_adjust(last_time)

# Ciclo principal
# Atualizando tempo atual a cada 10 segundos
while True:
    try:
        # Repete enquanto o episódio não acaba
        while int(current_time) < int(track_total_time)-1000.0:
            time.sleep(10)
            # Espera até ter foco na janela do vídeo para atualizar o tempo
            focus('update_time()')

            print(current_time, track_total_time)
        next_track()

    #Quando não consegue achar a janela no vídeo durante o focus(), sai do programa
    except FinishProgram:
        print('Até a próxima!!!')
        exit(0)
