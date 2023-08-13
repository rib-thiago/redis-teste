import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# get grayscale image


def get_grayscale(image):
    """
 Converte uma imagem colorida em escala de cinza.

    Esta função recebe uma imagem colorida e a converte para uma imagem em escala de cinza
    utilizando a biblioteca OpenCV.

    Args:
        image (numpy.ndarray): A imagem colorida de entrada representada como uma matriz NumPy.

    Returns:
        numpy.ndarray: A imagem em escala de cinza resultante, representada como uma matriz NumPy.

    Note:
        Certifique-se de que a biblioteca OpenCV (cv2) esteja instalada para usar esta função.
        A imagem em escala de cinza resultante será salva em um arquivo cujo nome é inserido pelo usuário.

        Esta função é projetada para ser usada em conjunto com um aplicativo Flask que permite ao usuário
        aplicar várias funções de edição de imagem em imagens carregadas. A imagem em escala de cinza resultante
        será salva em um arquivo e o caminho do arquivo será atualizado no banco de dados, se necessário.

"""
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Save the processed image to a file
    output_filename = input("Please enter the name of output with extension: ")
    cv2.imwrite(output_filename, gray_image)
    print(f"Processed grayscale image saved as '{output_filename}'.")

    return gray_image

# noise removal


def remove_noise(image):
    """
    Remove o ruído de uma imagem.

    Esta função recebe uma imagem e aplica um filtro de mediana para remover o ruído.
    A imagem processada resultante terá o ruído reduzido.

    Args:
        image (numpy.ndarray): A imagem de entrada representada como uma matriz NumPy.

    Returns:
        numpy.ndarray: A imagem processada com o ruído removido, representada como uma matriz NumPy.

    Note:
        Certifique-se de que a biblioteca OpenCV (cv2) esteja instalada para usar esta função.
        A imagem processada com o ruído removido será salva em um arquivo cujo nome é inserido pelo usuário.

        Esta função é projetada para ser usada em conjunto com um aplicativo Flask que permite ao usuário
        aplicar várias funções de edição de imagem em imagens carregadas. A imagem processada com o ruído removido
        será salva em um arquivo e o caminho do arquivo será atualizado no banco de dados, se necessário.
    """
    processed_image = cv2.medianBlur(image, 5)

    # Save the processed image to a file
    output_filename = input("Please enter the name of output with extension: ")
    cv2.imwrite(output_filename, processed_image)
    print(f"Processed image with noise removed saved as '{output_filename}'.")

    return processed_image


# thresholding


def thresholding(image):
    """
    Aplica a técnica de thresholding a uma imagem em escala de cinza.

    Esta função recebe uma imagem em escala de cinza e aplica a técnica de thresholding
    para binarizá-la, tornando os objetos em primeiro plano mais visíveis.

    Args:
        image (numpy.ndarray): A imagem em escala de cinza de entrada representada como uma matriz NumPy.

    Returns:
        numpy.ndarray: A imagem binarizada resultante após a aplicação da técnica de thresholding,
                       representada como uma matriz NumPy.

    Note:
        Certifique-se de que a biblioteca OpenCV (cv2) esteja instalada para usar esta função.
        A imagem binarizada resultante será salva em um arquivo cujo nome é inserido pelo usuário.

        Esta função é projetada para ser usada em conjunto com um aplicativo Flask que permite ao usuário
        aplicar várias funções de edição de imagem em imagens carregadas. A imagem binarizada resultante
        será salva em um arquivo e o caminho do arquivo será atualizado no banco de dados, se necessário.

        Certifique-se de que a imagem de entrada já esteja em escala de cinza ou tenha sido processada pela função get_grayscale.
    """
    processed_image = cv2.threshold(
        image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    output_filename = input(
        "Informe o nome do arquivo de saída com a extensão: ")
    cv2.imwrite(output_filename, processed_image)
    print(
        f"Imagem processada com a técnica de thresholding foi salva como '{output_filename}'.")

    return processed_image


# dilation


def dilate(image):
    """
    Aplica a operação de dilatação a uma imagem.

    Esta função recebe uma imagem e aplica a operação de dilatação para expandir as áreas brancas
    ou claras na imagem. Isso pode ser útil para realçar ou engrossar áreas específicas da imagem.

    Args:
        image (numpy.ndarray): A imagem de entrada representada como uma matriz NumPy.

    Returns:
        numpy.ndarray: A imagem dilatada resultante após a aplicação da operação de dilatação,
                       representada como uma matriz NumPy.

    Note:
        Certifique-se de que a biblioteca OpenCV (cv2) e a biblioteca NumPy (np) estejam instaladas
        para usar esta função.
        A imagem dilatada resultante será salva em um arquivo cujo nome é inserido pelo usuário.

        Esta função é projetada para ser usada em conjunto com um aplicativo Flask que permite ao usuário
        aplicar várias funções de edição de imagem em imagens carregadas. A imagem dilatada resultante
        será salva em um arquivo e o caminho do arquivo será atualizado no banco de dados, se necessário.
    """
    kernel = np.ones((5, 5), np.uint8)
    dilated_image = cv2.dilate(image, kernel, iterations=1)

    output_filename = input(
        "Informe o nome do arquivo de saída com a extensão: ")
    cv2.imwrite(output_filename, dilated_image)
    print(f"Imagem dilatada processada foi salva como '{output_filename}'.")

    return dilated_image


# erosion


def erode(image):
    """
    Aplica a operação de erosão a uma imagem.

    Esta função recebe uma imagem e aplica a operação de erosão para reduzir as áreas brancas
    ou claras na imagem, muitas vezes usada para afinar estruturas ou remover pequenos detalhes.

    Args:
        image (numpy.ndarray): A imagem de entrada representada como uma matriz NumPy.

    Returns:
        numpy.ndarray: A imagem erodida resultante após a aplicação da operação de erosão,
                       representada como uma matriz NumPy.

    Note:
        Certifique-se de que a biblioteca OpenCV (cv2) e a biblioteca NumPy (np) estejam instaladas
        para usar esta função.
        A imagem erodida resultante será salva em um arquivo cujo nome é inserido pelo usuário.

        Esta função é projetada para ser usada em conjunto com um aplicativo Flask que permite ao usuário
        aplicar várias funções de edição de imagem em imagens carregadas. A imagem erodida resultante
        será salva em um arquivo e o caminho do arquivo será atualizado no banco de dados, se necessário.
    """
    kernel = np.ones((5, 5), np.uint8)
    eroded_image = cv2.erode(image, kernel, iterations=1)

    output_filename = input(
        "Informe o nome do arquivo de saída com a extensão: ")
    cv2.imwrite(output_filename, eroded_image)
    print(f"Imagem erodida processada foi salva como '{output_filename}'.")

    return eroded_image


# opening - erosion followed by dilation


def opening(image):
    """
    Aplica a operação de abertura a uma imagem.

    Esta função recebe uma imagem e aplica a operação de abertura, que consiste em primeiro
    aplicar a operação de erosão e, em seguida, a operação de dilatação. Isso pode ser usado para
    remover ruídos e pequenos objetos brancos ou claros na imagem.

    Args:
        image (numpy.ndarray): A imagem de entrada representada como uma matriz NumPy.

    Returns:
        numpy.ndarray: A imagem resultante após a aplicação da operação de abertura,
                       representada como uma matriz NumPy.

    Note:
        Certifique-se de que a biblioteca OpenCV (cv2) e a biblioteca NumPy (np) estejam instaladas
        para usar esta função.
        A imagem resultante da abertura será salva em um arquivo cujo nome é inserido pelo usuário.

        Esta função é projetada para ser usada em conjunto com um aplicativo Flask que permite ao usuário
        aplicar várias funções de edição de imagem em imagens carregadas. A imagem resultante da abertura
        será salva em um arquivo e o caminho do arquivo será atualizado no banco de dados, se necessário.
    """
    kernel = np.ones((5, 5), np.uint8)
    opened_image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

    output_filename = input(
        "Informe o nome do arquivo de saída com a extensão: ")
    cv2.imwrite(output_filename, opened_image)
    print(
        f"Imagem processada pela abertura foi salva como '{output_filename}'.")

    return opened_image


# canny edge detection


def canny(image):
    """
    Detecta bordas em uma imagem usando o algoritmo Canny.

    Esta função recebe uma imagem e aplica o algoritmo Canny para detectar bordas na imagem.
    O algoritmo Canny é uma técnica amplamente usada para detecção de bordas em imagens.

    Args:
        image (numpy.ndarray): A imagem de entrada representada como uma matriz NumPy.

    Returns:
        numpy.ndarray: A imagem resultante após a detecção de bordas usando o algoritmo Canny,
                       representada como uma matriz NumPy.

    Note:
        Certifique-se de que a biblioteca OpenCV (cv2) esteja instalada para usar esta função.
        A imagem resultante da detecção de bordas será salva em um arquivo cujo nome é inserido pelo usuário.

        Esta função é projetada para ser usada em conjunto com um aplicativo Flask que permite ao usuário
        aplicar várias funções de edição de imagem em imagens carregadas. A imagem resultante da detecção de bordas
        será salva em um arquivo e o caminho do arquivo será atualizado no banco de dados, se necessário.
    """
    edges = cv2.Canny(image, 100, 200)

    output_filename = input(
        "Informe o nome do arquivo de saída com a extensão: ")
    cv2.imwrite(output_filename, edges)
    print(
        f"Imagem com detecção de bordas processada foi salva como '{output_filename}'.")

    return edges


# skew correction


def deskew(image):
    """
    Corrige a inclinação de uma imagem.

    Esta função recebe uma imagem e corrige a inclinação da imagem para que linhas horizontais
    fiquem niveladas. Isso é útil para melhorar a legibilidade e análise de documentos ou imagens.

    Args:
        image (numpy.ndarray): A imagem de entrada representada como uma matriz NumPy.

    Returns:
        numpy.ndarray: A imagem resultante após a correção de inclinação, representada como uma matriz NumPy.

    Note:
        Certifique-se de que a biblioteca OpenCV (cv2) e a biblioteca NumPy (np) estejam instaladas
        para usar esta função.
        A imagem resultante após a correção de inclinação será salva em um arquivo cujo nome é inserido pelo usuário.

        Esta função é projetada para ser usada em conjunto com um aplicativo Flask que permite ao usuário
        aplicar várias funções de edição de imagem em imagens carregadas. A imagem resultante após a correção de inclinação
        será salva em um arquivo e o caminho do arquivo será atualizado no banco de dados, se necessário.
    """
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(
        image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    output_filename = input(
        "Informe o nome do arquivo de saída com a extensão: ")
    cv2.imwrite(output_filename, rotated)
    print(
        f"Imagem com correção de inclinação processada foi salva como '{output_filename}'.")

    return rotated


# template matching


def match_template(image, template):
    result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)

    # ... (restante da lógica para encontrar correspondências e processar os resultados)

    # Save the processed image to a file
    output_filename = input("Please enter the name of output with extension: ")
    cv2.imwrite(output_filename, result)
    print(f"Processed image saved as '{output_filename}'.")

    return result

# Definição da função resize_to_300_dpi


def resize_to_300_dpi(image):
    """
    Redimensiona uma imagem para 300 DPI (pontos por polegada).

    Esta função recebe uma imagem e a redimensiona para ter uma resolução de 300 DPI,
    o que é comumente usado para impressões de alta qualidade.

    Args:
        image (numpy.ndarray): A imagem de entrada representada como uma matriz NumPy.

    Returns:
        None

    Note:
        Certifique-se de que a biblioteca OpenCV (cv2), a biblioteca NumPy (np) e a biblioteca
        Python Imaging Library (PIL) estejam instaladas para usar esta função.
        A imagem redimensionada para 300 DPI será salva em um arquivo cujo nome é inserido pelo usuário.

        Esta função é projetada para ser usada em conjunto com um aplicativo Flask que permite ao usuário
        aplicar várias funções de edição de imagem em imagens carregadas. A imagem redimensionada para 300 DPI
        será salva em um arquivo e o caminho do arquivo será atualizado no banco de dados, se necessário.
    """
    target_width_inch = 8.5
    target_height_inch = 11
    target_width = int(target_width_inch * 300)
    target_height = int(target_height_inch * 300)

    img_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    img_resized = img_pil.resize(
        (target_width, target_height), Image.ANTIALIAS)

    output_filename = input(
        "Informe o nome do arquivo de saída com a extensão: ")
    img_resized.save(output_filename, dpi=(300, 300))
    print(
        f"Imagem redimensionada para 300 DPI foi salva como '{output_filename}'.")


def remove_alpha_channel(image):
    """
    Remove o canal alfa de uma imagem.

    Esta função recebe uma imagem e verifica se ela possui um canal alfa (canal de transparência).
    Se a imagem possuir um canal alfa, o canal alfa será removido, resultando em uma imagem RGB.
    Caso contrário, a função informará que a imagem não possui um canal alfa e retornará a imagem original.

    Args:
        image (numpy.ndarray): A imagem de entrada representada como uma matriz NumPy.

    Returns:
        numpy.ndarray: A imagem resultante após a remoção do canal alfa (se aplicável),
                       representada como uma matriz NumPy.

    Note:
        Certifique-se de que a biblioteca OpenCV (cv2) esteja instalada para usar esta função.
        A imagem resultante após a remoção do canal alfa será salva em um arquivo cujo nome é inserido pelo usuário,
        se aplicável.

        Esta função é projetada para ser usada em conjunto com um aplicativo Flask que permite ao usuário
        aplicar várias funções de edição de imagem em imagens carregadas. A imagem resultante (sem canal alfa)
        será salva em um arquivo e o caminho do arquivo será atualizado no banco de dados, se necessário.
    """
    if image.shape[2] == 4:
        image_rgb = image[:, :, :3]

        output_filename = input(
            "Informe o nome do arquivo de saída com a extensão: ")
        cv2.imwrite(output_filename, image_rgb)
        print(
            f"Imagem processada com o canal alfa removido foi salva como '{output_filename}'.")
        return image_rgb
    else:
        print("A imagem não possui um canal alfa.")
        return image


def check_image_format(image):
    """
    Verifica o formato da imagem com base na quantidade de canais de cores.

    Esta função recebe uma imagem e verifica seu formato com base na quantidade de canais de cores.
    Ela informará se a imagem está no formato JPEG (3 canais) ou no formato PNG (4 canais),
    e se a imagem não se encaixar em nenhum dos formatos mencionados, indicará que o formato não é reconhecido.

    Args:
        image (numpy.ndarray): A imagem de entrada representada como uma matriz NumPy.

    Returns:
        None

    Note:
        Esta função não requer bibliotecas adicionais, pois usa apenas recursos do NumPy.
        Ela é projetada para ser usada em conjunto com um aplicativo Flask que permite ao usuário
        aplicar várias funções de edição de imagem em imagens carregadas.
    """
    if image.shape[2] == 3:
        print("A imagem está no formato JPEG.")
    elif image.shape[2] == 4:
        print("A imagem está no formato PNG.")
    else:
        print("O formato da imagem não é reconhecido (não é JPEG nem PNG).")
