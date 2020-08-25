from tkinter import Tk
from tkinter.filedialog import askopenfilename
from shutil import copyfile

# Obter primeira faixa de vídeo da série
def get_file():
    # Abrir janela de seleção de arquivo
    Tk().withdraw()
    filename = askopenfilename(title="Selecione o primeiro vídeo da série", filetypes=(('mp4 files', '*.mp4'), ('mkv files', '*.mkv'), ('avi files', '*.avi')))

    return filename


# Gerar arquivos na pasta
def generate(file_path):
    # Separar nome da pasta e nome do arquivo
    folder_path = file_path.split('/')
    file_name = folder_path.pop()
    folder_path = f'{"/".join(folder_path)}/'

    # Criando manager_data.txt com informações recolhidas
    manager_data = open(f'{folder_path}/manager_data.txt', 'w', encoding='utf-8')
    manager_data.write(f'{file_name}\n0000000')
    manager_data.close()

    # Copiar executável do video_run.py para pasta destino
    copyfile('dist/video_run.exe', f'{folder_path}VideoManager.exe')


generate(get_file())