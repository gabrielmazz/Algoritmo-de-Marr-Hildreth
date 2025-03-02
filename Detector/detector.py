import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

laplacian_kernel = np.array([[1, 1, 1], [1, -8, 1], [1, 1, 1]])

def marrhildreth(image, sigma, threshold):
    
    g_kernel = gaussian_kernel(sigma)
    blurred = convolve(image, g_kernel)

    laplacian = convolve(blurred, laplacian_kernel)

    edges = zero_crossing(laplacian, threshold=threshold)
    return edges

def convolve(image, kernel):

    krows, kcols = kernel.shape
    rows, cols = image.shape

    padded = np.pad(image, (krows // 2, kcols // 2), mode="constant")
    conv = np.empty_like(image, dtype=np.float32)
    if rows * cols < 2**20:  # Fast convolution for small images
        stacked = np.array(
            [
                np.ravel(padded[i : i + krows, j : j + kcols])
                for i in range(rows)
                for j in range(cols)
            ],
            dtype=np.float32,
        )

        conv = (stacked @ np.ravel(kernel)).reshape(rows, cols)
    else:  # Memory efficient convolution for large images
        for i in range(rows - krows // 2):
            for j in range(cols - kcols // 2):
                conv[i][j] = np.sum(padded[i : i + krows, j : j + kcols] * kernel)

    return conv


def gaussian_kernel(sigma):
   
    size = np.ceil(3 * sigma).astype(int)

    x = np.arange(-size, size + 1)

    X, Y = np.meshgrid(x, x)

    kernel = np.exp(-(X**2 + Y**2) / (2 * sigma**2))
    kernel = kernel / (2 * np.pi * sigma**2)

    return kernel


def zero_crossing(image, threshold):
   
    N, M = image.shape

    edges = np.zeros_like(image, dtype=np.uint8)
    for i in range(N):
        for j in range(M):
            if i > 0 and i < N - 1:
                left = image[i - 1, j]
                right = image[i + 1, j]
                if left * right < 0 and np.abs(left - right) > threshold:
                    edges[i, j] = 255
            if j > 0 and j < M - 1:
                up = image[i, j + 1]
                down = image[i, j - 1]
                if up * down < 0 and np.abs(up - down) > threshold:
                    edges[i, j] = 255
            if (i > 0 and i < N - 1) and (j > 0 and j < M - 1):
                up_left = image[i - 1, j - 1]
                down_right = image[i + 1, j + 1]
                down_left = image[i - 1, j + 1]
                up_right = image[i + 1, j - 1]
                if (
                    up_left * down_right < 0
                    and np.abs(up_left - down_right) > threshold
                ):
                    edges[i, j] = 255
                elif (
                    down_left * up_right < 0
                    and np.abs(down_left - up_right) > threshold
                ):
                    edges[i, j] = 255
    return edges

    