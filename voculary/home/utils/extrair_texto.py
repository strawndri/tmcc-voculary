import cv2
import pytesseract as pt
pt.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

def extrair_texto(imagem):
    # Carregar a imagem usando OpenCV
    img = cv2.imread(imagem)

    # Converter a imagem para escala de cinza
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Usar o Tesseract para fazer OCR na imagem
    texto = pt.image_to_string(gray)

    return texto