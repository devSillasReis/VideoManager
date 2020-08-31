import generator
import video_run
import tkinter as tk
from tkinter import *
from os import listdir
from os.path import isfile, join
from glob import glob


class ScrollableFrame(Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        canvas = Canvas(container, bg='purple')
        scrollbar = Scrollbar(container, orient='vertical', command=canvas.yview)
        self.scrollable = Frame(canvas)

        self.scrollable.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")


class Menu(Frame):
    def __init__(self):
        super().__init__()

        self.scrollable_frame = None
        self.message_label = None

        self.initUI()
    
    def initUI(self):
        self.master.title('Video Manager')

        # Criação de espaço para alertas da UI
        self.message_label = Label(self, text='Bem vindo!', bg='blue', height=1)
        self.message_label.pack(side=BOTTOM, fill=BOTH)

        # Criação da parte principal onde se encontram as seções do usuário
        sect_frame = Frame(self, relief=RAISED, bg='purple')
        self.scrollable_frame = ScrollableFrame(sect_frame)
        sect_frame.pack(fill=BOTH, expand=True, side=BOTTOM)
        
        self.pack(fill=BOTH, expand=True)

        # Botões para adicionar e remover seções
        new_section_bt = Button(self, text='+ Nova seção', bg='lightgreen', height=1)
        new_section_bt.pack(side=LEFT, fill=BOTH, expand=True)
        remove_section_bt = Button(self, text='- Remover seção', bg='red', height=1)
        remove_section_bt.pack(side=RIGHT, fill=BOTH, expand=True)


    def initSections(self):
        sections_path = glob('./sections/*.fmng')
        self.sections_data = list()

        # Carregar dados das seções
        for section in sections_path:
            sect_name = section.split('\\')[-1].split('.')[0]

            with open(section, 'r', encoding='utf-8') as sect:
                sect_data = sect.read().split('\n')
                sect_data.append(sect_name)
            
            self.sections_data.append(sect_data)
                
        # Exibir seções no scrollable frame
        for section in self.sections_data:
            sect_frame = Frame(self.scrollable_frame.scrollable, bg='purple')
            Label(sect_frame, text=f'{section[3]}', bg='purple').grid(row=0, column=1, sticky='w')
            Label(sect_frame, text=f'Episódio atual: {section[1]}', bg='purple').grid(row=1, column=1, sticky='w')
            Label(sect_frame, text=f'Momento atual: {section[2]}', bg='purple').grid(row=2, column=1, sticky='w')
            Label(sect_frame, text=f'', bg='purple').grid(row=3, column=1, columnspan=2)
            Button(sect_frame, text='Continuar\nassistindo', bg='grey').grid(row=0, column=0, rowspan=3)
            sect_frame.pack(fill=BOTH)



root = Tk()
root.geometry('500x800')
main_view = Menu()
main_view.initSections()
root.mainloop()