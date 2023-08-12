import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# get grayscale image


def get_grayscale(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Save the processed image to a file
    output_filename = input("Please enter the name of output with extension: ")
    cv2.imwrite(output_filename, gray_image)
    print(f"Processed grayscale image saved as '{output_filename}'.")

    return gray_image

# noise removal


def remove_noise(image):
    processed_image = cv2.medianBlur(image, 5)

    # Save the processed image to a file
    output_filename = input("Please enter the name of output with extension: ")
    cv2.imwrite(output_filename, processed_image)
    print(f"Processed image with noise removed saved as '{output_filename}'.")

    return processed_image


# thresholding


def thresholding(image):
    processed_image = cv2.threshold(
        image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # Save the processed image to a file
    output_filename = input("Please enter the name of output with extension: ")
    cv2.imwrite(output_filename, processed_image)
    print(f"Processed thresholded image saved as '{output_filename}'.")

    return processed_image

# dilation


def dilate(image):
    kernel = np.ones((5, 5), np.uint8)
    dilated_image = cv2.dilate(image, kernel, iterations=1)

    # Save the processed image to a file
    output_filename = input("Please enter the name of output with extension: ")
    cv2.imwrite(output_filename, dilated_image)
    print(f"Processed dilated image saved as '{output_filename}'.")

    return dilated_image

# erosion


def erode(image):
    kernel = np.ones((5, 5), np.uint8)
    eroded_image = cv2.erode(image, kernel, iterations=1)

    # Save the processed image to a file
    output_filename = input("Please enter the name of output with extension: ")
    cv2.imwrite(output_filename, eroded_image)
    print(f"Processed eroded image saved as '{output_filename}'.")

    return eroded_image

# opening - erosion followed by dilation


def opening(image):
    kernel = np.ones((5, 5), np.uint8)
    opened_image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

    # Save the processed image to a file
    output_filename = input("Please enter the name of output with extension: ")
    cv2.imwrite(output_filename, opened_image)
    print(f"Processed opened image saved as '{output_filename}'.")

    return opened_image

# canny edge detection


def canny(image):
    edges = cv2.Canny(image, 100, 200)

    # Save the processed image to a file
    output_filename = input("Please enter the name of output with extension: ")
    cv2.imwrite(output_filename, edges)
    print(f"Processed edge-detected image saved as '{output_filename}'.")

    return edges

# skew correction


def deskew(image):
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

    # Save the processed image to a file
    output_filename = input("Please enter the name of output with extension: ")
    cv2.imwrite(output_filename, rotated)
    print(f"Processed deskewed image saved as '{output_filename}'.")

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
    target_width_inch = 8.5
    target_height_inch = 11
    target_width = int(target_width_inch * 300)
    target_height = int(target_height_inch * 300)

    img_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    img_resized = img_pil.resize(
        (target_width, target_height), Image.ANTIALIAS)

    output_filename = input(
        "Por favor, insira o nome do arquivo de saída com extensão: ")
    img_resized.save(output_filename, dpi=(300, 300))
    print(
        f"Imagem redimensionada para 300 DPI e salva como '{output_filename}'.")

# Checar formato da imagem


def remove_alpha_channel(image):
    if image.shape[2] == 4:
        image_rgb = image[:, :, :3]

        # Save the processed image to a file
        output_filename = input(
            "Please enter the name of output with extension: ")
        cv2.imwrite(output_filename, image_rgb)
        print(
            f"Processed image with alpha channel removed saved as '{output_filename}'.")

        return image_rgb
    else:
        print("A imagem não possui um canal alfa.")
        return image


def check_image_format(image):
    if image.shape[2] == 3:
        print("A imagem está no formato JPEG.")
    elif image.shape[2] == 4:
        print("A imagem está no formato PNG.")
    else:
        print("O formato da imagem não é JPEG nem PNG.")
