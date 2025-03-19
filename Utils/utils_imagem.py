import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
from rich.console import Console
from rich.prompt import Prompt
import os
import cv2
import requests
from PIL import Image
from io import BytesIO

# Leitura da imagem com o matplotlib
def leitura_Imagem_Matplotlib(nome):
    
    # Carrega a imagem
    Imagem = mpimg.imread(nome)
    
    # Retorna a imagem
    return Imagem

# Leitura da imagem
def leitura_Imagem(nome):
    
    # Carrega a imagem
    Imagem = cv2.imread(nome, cv2.IMREAD_GRAYSCALE)
    
    # Retorna a imagem
    return Imagem

# Realiza a plotagem das imagens com o matplotlib
def plotagem_imagem(Imagem_Original_Mat, Imagem_Original, Imagem_Filtrada):
    
    # Cria a figura com os subplots
    fig, axs = plt.subplots(1, 3, figsize=(10, 5))
    
    # Adiciona as imagens nos subplots
    axs[0].imshow(Imagem_Original_Mat)
    axs[0].set_title('Imagem Original')
    
    axs[1].imshow(Imagem_Original)
    axs[1].set_title('Imagem Original em Escala de Cinza')
    
    axs[2].imshow(Imagem_Filtrada, cmap='Greys')
    axs[2].set_title('Imagem com Filtro Marr-Hildreth')
    
    # Remove os eixos dos subplots
    for ax in axs.flat:
        ax.set(xticks=[], yticks=[])
    
    # Mostra a figura com os subplots
    plt.show()
    
def salvar_imagem(Imagem, nome):
    
    plt.imsave(nome, Imagem, cmap='Greys')
    
def lista_imagens_pasta(pasta, console):
    
    # Lista as imagens disponíveis na pasta
    imagens = [f for f in os.listdir(pasta)]
    
    # Printa as imagens
    for i, imagem in enumerate(imagens):
        
        # Extrai o nome da imagem a sua extensão
        nome, extensao = os.path.splitext(imagem)
        
        if nome == "IMAGEM_BAIXADA_URL":  # Verifica se é a imagem_baixada
            console.print(f'{i+1}. [bold green]{nome}{extensao}[/bold green]')  # Imprime em verde
        else:
            console.print(f'{i+1}. {nome}{extensao}')  # Imprime normalmente
        
    return imagens

def escolher_imagens(imagens, console):
    
    # Escolhe uma imagem para aplicar o metodo de Marr-Hildreth
    while True:
        escolha = int(Prompt.ask('Escolha uma imagem para aplicar o [bold purple]Marr-Hildreth[/bold purple]', console=console))
        
        if escolha > 0 and escolha <= len(imagens):
            return imagens[escolha-1]
        else:
            console.print('Escolha inválida. Tente novamente.')
    
    
def download_imagem(args):
    
    # Baixa a imagem da URL
    response = requests.get(args.url)
    
    # Verifica se a requisição foi bem sucedida
    if response.status_code == 200:
        # Lê a imagem
        Imagem = Image.open(BytesIO(response.content))
        
        # Define o nome da imagem
        nome_imagem = "IMAGEM_BAIXADA_URL"  # Nome fixo
        extensao = args.url.split('.')[-1]  # Extrai a extensão da URL (ex: jpg, png, etc.)
        
        # Salva a imagem com o novo nome
        Imagem.save(f'./imagens/{nome_imagem}.{extensao}')
        
    else:
        console.print('Erro ao baixar a imagem. Tente novamente.')

def deletar_imagem(nome):
    
    # Deleta a imagem
    os.remove('./imagens/{}'.format(nome))