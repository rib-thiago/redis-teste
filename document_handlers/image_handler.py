import cv2
import numpy as np
from PIL import Image


class ImageHandler:
    def get_grayscale(self, image, output_filename):
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(output_filename, gray_image)
        return gray_image

    def remove_noise(self, image, output_filename):
        processed_image = cv2.medianBlur(image, 5)
        cv2.imwrite(output_filename, processed_image)
        return processed_image

    def thresholding(self, image, output_filename):
        processed_image = cv2.threshold(
            image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        cv2.imwrite(output_filename, processed_image)
        return processed_image

    def dilate(self, image, output_filename):
        kernel = np.ones((5, 5), np.uint8)
        dilated_image = cv2.dilate(image, kernel, iterations=1)
        cv2.imwrite(output_filename, dilated_image)
        return dilated_image

    def erode(self, image, output_filename):
        kernel = np.ones((5, 5), np.uint8)
        eroded_image = cv2.erode(image, kernel, iterations=1)
        cv2.imwrite(output_filename, eroded_image)
        return eroded_image

    def opening(image):
        kernel = np.ones((5, 5), np.uint8)
        opened_image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

        output_filename = input(
            "Informe o nome do arquivo de saída com a extensão: ")
        cv2.imwrite(output_filename, opened_image)
        print(
            f"Imagem processada pela abertura foi salva como '{output_filename}'.")

        return opened_image

    def canny(image):
        edges = cv2.Canny(image, 100, 200)

        output_filename = input(
            "Informe o nome do arquivo de saída com a extensão: ")
        cv2.imwrite(output_filename, edges)
        print(
            f"Imagem com detecção de bordas processada foi salva como '{output_filename}'.")

        return edges

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

        output_filename = input(
            "Informe o nome do arquivo de saída com a extensão: ")
        cv2.imwrite(output_filename, rotated)
        print(
            f"Imagem com correção de inclinação processada foi salva como '{output_filename}'.")

        return rotated

    def match_template(image, template):
        result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)

        # ... (restante da lógica para encontrar correspondências e processar os resultados)

        # Save the processed image to a file
        output_filename = input(
            "Please enter the name of output with extension: ")
        cv2.imwrite(output_filename, result)
        print(f"Processed image saved as '{output_filename}'.")

        return result

    def resize_to_300_dpi(self, image, output_filename):
        target_width_inch = 8.5
        target_height_inch = 11
        target_width = int(target_width_inch * 300)
        target_height = int(target_height_inch * 300)

        img_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        img_resized = img_pil.resize(
            (target_width, target_height), Image.ANTIALIAS)

        img_resized.save(output_filename, dpi=(300, 300))

    def remove_alpha_channel(self, image, output_filename):
        if image.shape[2] == 4:
            image_rgb = image[:, :, :3]
            cv2.imwrite(output_filename, image_rgb)
            return image_rgb
        else:
            print("A imagem não possui um canal alfa.")
            return image

    def check_image_format(self, image):
        if image.shape[2] == 3:
            print("A imagem está no formato JPEG.")
        elif image.shape[2] == 4:
            print("A imagem está no formato PNG.")
        else:
            print("O formato da imagem não é reconhecido (não é JPEG nem PNG).")
