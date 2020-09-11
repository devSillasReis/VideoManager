import pyautogui as pygui
import pygetwindow as gw
import clipboard
import time
import sys
import os
import re


class ClosedSection(Exception):
    pass


class WrongFormatException(Exception):
    pass


def show_format_time(time_variable):
    str_time = ''

    if len(time_variable) < 6:
        full_time = '00' + time_variable
    else:
        full_time = time_variable

    for i in range(len(full_time)):
        str_time = str_time + full_time[i]
        if(i%2 != 0 and i != len(full_time)-1):
            str_time = str_time + ':'

    return str_time


class VideoRun():
    # Definição de variáveis estáticas
    formats = {
        'time': '^\d\d:\d\d(:\d\d){0,1}$',
        'name': '^[^\.]+\.[^\.]+$'
    }
    
    def __init__(self, section_data):
        
        self.section_data = section_data
        self.track_total_time = None
        
        self.open_video()
        self.wait_open()
        self.time_adjust()

        # Ciclo principal
        # Atualizando tempo atual a cada 10 segundos
        while True:
            try:
                # Repete enquanto o episódio não acaba
                while int(self.section_data[2]) < int(self.track_total_time)-1:
                    try:
                        time.sleep(10)
                        # Espera até ter foco na janela do vídeo para atualizar o tempo
                        self.focus('update_time()')

                        print(self.section_data[2], self.track_total_time)
                    except WrongFormatException:
                        pass
                
                self.next_track()

            #Quando não consegue achar a janela no vídeo durante o focus(), sai do programa
            except ClosedSection:
                return

                
    # Abrir vídeo
    def open_video(self):
        # Comando para abrir vídeo varia de acordo com o sistema
        if sys.platform == 'win32':
            os.startfile(self.section_data[0]+self.section_data[1])


    # Espera a janela do vídeo abrir para dar continuidade
    def wait_open(self):
        opened = False
        while opened is False:
            try:
                video_window = gw.getWindowsWithTitle(self.section_data[1])[0]
                opened = True
            except IndexError:
                pass


    # Avançar para o período em que parou na última vez
    def time_adjust(self):
        #Obtendo foco
        video_window = gw.getWindowsWithTitle(self.section_data[1])[0]
        video_window.minimize()
        video_window.restore()
        
        # Obtendo tempo total do vídeo
        self.track_total_time = VideoRun.total_time()

        # Sequência de comandos para avançar para tempo específico dentro do VLC Media Player
        pygui.press('esc')
        pygui.hotkey('ctrl', 'g')
        pygui.write(self.section_data[2])
        pygui.press('enter')


    # Formatar para padrão de tempo do projeto
    @staticmethod
    def __format_time(time):
        return ''.join(x for x in time if x.isnumeric())


    # Obter tempo atual do vídeo
    def update_time(self):
        # Obtendo tempo
        pygui.hotkey('ctrl', 'g')
        pygui.hotkey('ctrl', 'a')
        pygui.hotkey('ctrl', 'c')
        pygui.press('esc')

        # Atualizando o tempo
        current_time = clipboard.paste().split('.')[0]
        VideoRun.valid_format(current_time, 'time')
        self.section_data[2] = VideoRun.__format_time(current_time)


    # Obter tempo total do vídeo
    @staticmethod    
    def total_time():
        # Obtendo tempo total
        pygui.press('esc')
        pygui.hotkey('shift', 'f10')
        pygui.press(['tab', 'tab', 'tab', 'tab'])
        pygui.hotkey('ctrl', 'c')
        pygui.press('esc')
        time.sleep(0.5)
        total_time = clipboard.paste()
        VideoRun.valid_format(total_time, 'time')

        # Convertendo pra valores utilizados
        total_time = total_time.split(':')
        total_time = [x for x in total_time if int(x) > 0]
        
        return VideoRun.__format_time(f'{"".join(total_time)}')


    # Pular para próxima faixa
    def next_track(self):
        self.section_data[2] = '000000'

        # Obtendo nome da faixa
        pygui.press('pagedown')
        time.sleep(2)
        pygui.hotkey('shift', 'f10')
        pygui.press('tab')
        pygui.hotkey('ctrl', 'c')
        pygui.press('esc')

        
        # Atualizando nome do vídeo
        name = clipboard.paste()
        self.section_data[1] = name

        # Obtendo tempo total do vídeo
        self.track_total_time = VideoRun.total_time()


    # Espera foco da janela para realizar uma ação
    def focus(self, action):
        # Obtendo nome da janela
        track_title = self.section_data[1]
        
        # Obtendo informações da janela do vídeo e a janela atualmente em foco
        active_window = gw.getActiveWindow()
        try:
            video_window = gw.getWindowsWithTitle(track_title)[0]
        except IndexError:
            raise ClosedSection()
        
        # Se a janela em foco não for a do vídeo, espera até que seja
        if active_window != video_window:
            while not video_window.isActive:
                pass
        
        # Atualiza o tempo gravado
        if action == 'update_time()':
            self.update_time()

    
    # Levanta a exceção WrongFormatException se o formato não for válido
    @staticmethod
    def valid_format(text, text_type):
        valid = re.search(VideoRun.formats[text_type], text)
        if valid is None:
            raise WrongFormatException()
