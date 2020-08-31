import generator
import video_run
import tkinter as tk
from tkinter import *
from tkinter import messagebox
import os
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


class NewSectionWindow(Toplevel):
    def __init__(self, transient):
        super().__init__()

        self.transient = transient
        self.focus_force()
        self.grab_set()

        #self.sect_name = StringVar()
        self.sect_path = None

        self.resizable(False, False)

        self.initInputWindow()
    
    def initInputWindow(self):
        self.title('Nova sessão')

        Label(self, text='Nome da sessão:').grid(row=1)
        self.sect_name_entry = Entry(self)
        self.sect_name_entry.grid(row=1, column=1, columnspan=2)
        Label(self, text='').grid(row=3, columnspan=3)
        Button(self, text='Cancelar', command=self.cancel_btn).grid(row=4, column=1, sticky='e')
        Button(self, text='Continuar', command=self.continue_btn).grid(row=4, column=2)

    def cancel_btn(self):
        self.destroy()

    def continue_btn(self):
        sect_name = self.sect_name_entry.get()
        
        if len(sect_name) != 0:
            generator.generate(sect_name)
            self.transient.clear_sections_frames()
            self.transient.initSections()
            self.destroy()
        else:
            messagebox.showwarning(title='Nome inválido', message='Você precisa escolher um nome para a sessão!')


class Menu(Frame):
    def __init__(self):
        super().__init__()

        self.scrollable_frame = None
        self.message_label = None
        self.test = Frame()
        self.test.pack()
        self.initUI()
    
    def initUI(self):
        self.master.title('Video Manager')

        # Criação de espaço para alertas da UI
        self.message_label = Label(self, text='Bem vindo!', bg='lightgreen', height=1)
        self.message_label.pack(side=BOTTOM, fill=BOTH)

        # Criação da parte principal onde se encontram as seções do usuário
        sect_frame = Frame(self, relief=RAISED, bg='purple')
        self.scrollable_frame = ScrollableFrame(sect_frame)
        sect_frame.pack(fill=BOTH, expand=True, side=BOTTOM)
        
        self.pack(fill=BOTH, expand=True)

        # Botões para adicionar e remover seções
        self.new_section_bt = Button(self, text='+ Nova seção', bg='lightgreen', height=1, command=self.add_section)
        self.new_section_bt.pack(side=LEFT, fill=BOTH, expand=True)
        self.remove_section_bt = Button(self, text='- Remover seção', bg='red', height=1, command=self.remove_section)
        self.remove_section_bt.pack(side=RIGHT, fill=BOTH, expand=True)

    def initSections(self):
        sections_path = glob('./sections/*.fmng')
        self.sections_data = list()
        self.sections_frames = list()
        self.checkbuttons = list()

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
            Label(sect_frame, text=f'{section[3]}', bg='purple').grid(row=0, column=2, sticky='w')
            Label(sect_frame, text=f'Episódio atual: {section[1]}', bg='purple').grid(row=1, column=2, sticky='w')
            Label(sect_frame, text=f'Momento atual: {section[2]}', bg='purple').grid(row=2, column=2, sticky='w')
            Label(sect_frame, text=f'', bg='purple').grid(row=3, column=2, columnspan=2)
            
            index = len(self.sections_frames)
            Button(sect_frame, text='Continuar\nassistindo', bg='grey', command=lambda index=index: self.keep_watching(index)).grid(row=0, column=1, rowspan=3)

            self.checkbuttons.append(IntVar())
            checkbutton = Checkbutton(sect_frame, bg='purple', variable=self.checkbuttons[len(self.checkbuttons)-1])
            checkbutton.grid(row=0, column=0, rowspan=3)
            checkbutton.grid_forget()

            sect_frame.pack(fill=BOTH)
            self.sections_frames.append(sect_frame)

    def clear_sections_frames(self):
        for frame in self.sections_frames:
            frame.destroy()
        self.sections_frames = list()
        self.sections_data = list()

    def add_section(self):
        NewSectionWindow(self)

    def keep_watching(self, section_index):
        print(self.sections_data[section_index])
        root.withdraw()
        video_run.VideoRun(self.sections_data[section_index])
        root.deiconify()
        print(self.sections_data[section_index])
        self.update_section(self.sections_data[section_index])

    def update_section(self, section_data):
        with open(f'./sections/{section_data[3]}.fmng', 'w', encoding='utf-8') as section_file:
            section_file.write(f'{section_data[0]}\n{section_data[1]}\n{section_data[2]}')

        self.clear_sections_frames()
        self.initSections()
        
    def remove_section(self):
        def cancel():
            self.new_section_bt.pack(side=LEFT, fill=BOTH, expand=True)
            self.remove_section_bt.pack(side=RIGHT, fill=BOTH, expand=True)

            self.message_label.config(bg='lightgreen', text='Bem-vindo!')

            confirm_bt.pack_forget()
            cancel_bt.pack_forget()

            self.clear_sections_frames()
            self.initSections()
        
        def confirm():
            option = messagebox.askokcancel(title='Excluir sessões', message='Excluirá as sessões selecionadas permanentemente.\nDeseja continuar?')

            if option == True:
                for i in range(len(self.checkbuttons)):
                    if self.checkbuttons[i].get() == 1:
                        sect_path = f'./sections/{self.sections_data[i][3]}.fmng'
                        if os.path.isfile(sect_path):
                            os.remove(sect_path)
                
            self.message_label.config(bg='lightgreen', text='Bem-vindo!')
            
            self.clear_sections_frames()
            self.initSections()
            
            self.new_section_bt.pack(side=LEFT, fill=BOTH, expand=True)
            self.remove_section_bt.pack(side=RIGHT, fill=BOTH, expand=True)

            confirm_bt.pack_forget()
            cancel_bt.pack_forget()
        
        self.message_label.config(bg='red', text='Removendo sessões...')

        for frame in self.sections_frames:
            for widget in frame.winfo_children():
                if type(widget) == Checkbutton:
                    widget.grid(row=0, column=0, rowspan=3)
        
        self.new_section_bt.pack_forget()
        self.remove_section_bt.pack_forget()

        cancel_bt = Button(self, text='Cancelar', bg='lightgreen', height=1, command=cancel)
        cancel_bt.pack(side=LEFT, fill=BOTH, expand=True)
        confirm_bt = Button(self, text='Confirmar', bg='red', height=1, command=confirm)
        confirm_bt.pack(side=RIGHT, fill=BOTH, expand=True)



root = Tk()
root.geometry('500x800')
main_view = Menu()
main_view.initSections()
root.mainloop()