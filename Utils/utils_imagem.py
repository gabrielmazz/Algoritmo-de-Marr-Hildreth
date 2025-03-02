import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
from rich.console import Console
from rich.prompt import Prompt
import os
import cv2

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
    axs[2].set_title('Imagem Filtrada')
    
    # Remove os eixos dos subplots
    for ax in axs.flat:
        ax.set(xticks=[], yticks=[])
    
    # Mostra a figura com os subplots
    plt.show()
    
def salvar_imagem(Imagem_Binaria, nome):
    
    plt.imsave(nome, Imagem_Binaria, cmap='Greys')
    
def lista_imagens_pasta(pasta, console):
    
    # Lista as imagens disponíveis na pasta
    imagens = [f for f in os.listdir(pasta)]
    
    # Printa as imagens
    for i, imagem in enumerate(imagens):
        console.print('{}. {}'.format(i+1, imagem))
        
    return imagens

def escolher_imagens(imagens, console):
    
    # Escolhe uma imagem para aplicar o filtro Box
    while True:
        escolha = int(Prompt.ask('Escolha uma imagem para aplicar o [bold purple]Filtro Box[/bold purple]:', console=console))
        
        if escolha > 0 and escolha <= len(imagens):
            return imagens[escolha-1]
        else:
            console.print('Escolha inválida. Tente novamente.')
    