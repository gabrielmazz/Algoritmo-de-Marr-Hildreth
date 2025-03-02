import matplotlib.pyplot as plt
import argparse
from rich.console import Console
from rich.prompt import Prompt
import Detector.detector as detector
import Utils.utils_imagem as ut_img
import Utils.utils_code as ut_code

# Variáveis para passagem de argumentos via terminal
parser = argparse.ArgumentParser()

# Argumento para salvar a imagem na pasta de resultados
SAVE = parser.add_argument('--save', action='store_true', help='Salvar a imagem na pasta de resultados')

def marr(imagem_escolhida, tipo):
    
    # Leitura da imagem com o matplotlib para a plotagem depois
    Imagem_Original_Mat = ut_img.leitura_Imagem_Matplotlib('./imagens/{}'.format(imagem_escolhida))
    
    # Leitura da imagem
    Imagem_Original = ut_img.leitura_Imagem('./imagens/{}'.format(imagem_escolhida))    

    # Filtro de Marr-Hildreth
    Imagem_Filtrada = detector.marrhildreth(Imagem_Original, 3.5, 0.7)
    
    
    # Realiza a plotagem das imagens
    ut_img.plotagem_imagem(Imagem_Original_Mat, Imagem_Original, Imagem_Filtrada)
    
    # Salva a imagem na pasta de resultados
    # if SAVE:
    #     for tamanho in tamanhos:
    #         ut_img.salvar_imagem(Imagens_Binarias['{}'.format(tamanho)], './resultados/{}_box_{}x{}.png'.format(imagem_escolhida.split('.')[0], tamanho, tamanho))
        
if __name__ == '__main__':
    
    ut_code.clear_terminal()
    ut_code.print_title()
    
    # Inicializa a console
    console = Console()
    
    # Lista as imagens disponíveis na pasta
    imagens_disponiveis = ut_img.lista_imagens_pasta('./imagens', console)
    
    # Escolhe uma imagem para aplicar o método de Otsu
    imagem_escolhida = ut_img.escolher_imagens(imagens_disponiveis, console)
        
    marr(imagem_escolhida, 'marr-hildreth')