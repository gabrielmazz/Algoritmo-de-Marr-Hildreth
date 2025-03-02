import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np


def marrhildreth(image, sigma, threshold, laplacian_kernel):
    
    # Aplicar o filtro Gaussiano para suavizar a imagem,
    # Cria o kernel Gaussiano
    g_kernel = gaussian_kernel(sigma)  
    
    # Aplica a convolução com o kernel Gaussiano
    blurred = convolve(image, g_kernel)  

    # Aplicar o filtro Laplaciano para detectar bordas, aplicando a convolução 
    # com o kernel Laplaciano ([1, 1, 1], [1, -8, 1], [1, 1, 1])
    laplacian = convolve(blurred, laplacian_kernel)  

    # Detectar cruzamentos por zero para identificar bordas
    edges = zero_crossing(laplacian, threshold=threshold) 

    # Retorna a imagem com as bordas
    return edges

import numpy as np

def convolve(image, kernel):

    krows, kcols = kernel.shape  # Dimensões do kernel
    rows, cols = image.shape  # Dimensões da imagem

    # Adiciona padding à imagem para tratar bordas
    pad_rows = krows // 2
    pad_cols = kcols // 2
    padded = np.pad(image, ((pad_rows, pad_rows), (pad_cols, pad_cols)), mode="constant")

    # Inicializa o array de saída
    conv = np.empty_like(image, dtype=np.float32)

    # Verifica o tamanho da imagem para escolher o método de convolução
    if rows * cols < 2**20:  # Para imagens pequenas, usa uma abordagem vetorizada
        
        # Cria uma matriz onde cada linha é uma janela do kernel na imagem
        stacked = np.array(
            [
                padded[i : i + krows, j : j + kcols].ravel()
                for i in range(rows)
                for j in range(cols)
            ],
            dtype=np.float32,
        )

        # Aplica a convolução como um produto matricial
        conv = (stacked @ kernel.ravel()).reshape(rows, cols)
        
    else:  # Para imagens grandes, usa uma abordagem iterativa para economizar memória
        for i in range(rows):
            for j in range(cols):
                # Extrai a região da imagem correspondente ao kernel e aplica a convolução
                conv[i, j] = np.sum(padded[i : i + krows, j : j + kcols] * kernel)

    return conv

def gaussian_kernel(sigma):
   
    # Define o tamanho do kernel como 6 * sigma + 1 (garante um tamanho ímpar)
    size = int(np.ceil(6 * sigma)) // 2 * 2 + 1  # Tamanho ímpar centralizado

    # Cria um grid de coordenadas centradas em zero
    x = np.arange(-size // 2, size // 2 + 1)
    X, Y = np.meshgrid(x, x)

    # Calcula o kernel Gaussiano usando a fórmula
    kernel = np.exp(-(X**2 + Y**2) / (2 * sigma**2))
    kernel /= (2 * np.pi * sigma**2)  # Normaliza o kernel

    return kernel


def zero_crossing(image, threshold):
    
    N, M = image.shape  # Dimensões da imagem
    edges = np.zeros_like(image, dtype=np.uint8)  # Inicializa a imagem de bordas

    # Percorre a imagem (exceto as bordas)
    for i in range(1, N - 1):
        for j in range(1, M - 1):
            # Verifica cruzamentos por zero nas direções horizontal, vertical e diagonais
            neighbors = [
                (image[i - 1, j], image[i + 1, j]),  # Vizinhos horizontal
                (image[i, j - 1], image[i, j + 1]),  # Vizinhos vertical
                (image[i - 1, j - 1], image[i + 1, j + 1]),  # Diagonal principal
                (image[i - 1, j + 1], image[i + 1, j - 1]),  # Diagonal secundária
            ]

            for a, b in neighbors:
                if a * b < 0 and np.abs(a - b) > threshold:  # Cruzamento por zero válido
                    edges[i, j] = 255
                    break  # Se um cruzamento válido for encontrado, não precisa verificar os outros

    return edges