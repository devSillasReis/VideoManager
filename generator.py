from tkinter import Tk
from tkinter.filedialog import askopenfilename
from shutil import copyfile

# Obter primeira faixa de vídeo da sessão
def get_file():
    # Abrir janela de seleção de arquivo
    Tk().withdraw()
    filename = askopenfilename(title="Selecione o primeiro vídeo da série", filetypes=(('mp4 files', '*.mp4'), ('mkv files', '*.mkv'), ('avi files', '*.avi')))

    return filename


# Gerar arquivo de sessão
def generate(section_name):
    # Separar nome da pasta e nome do arquivo
    folder_path = get_file().split('/')
    file_name = folder_path.pop()
    folder_path = f'{"/".join(folder_path)}/'

    # Criando arquivo de sessão com informações recolhidas
    with open(f'./sections/{section_name}.fmng', 'w', encoding='utf-8') as section_data:
        section_data.write(f'{folder_path}\n{file_name}\n000000')
