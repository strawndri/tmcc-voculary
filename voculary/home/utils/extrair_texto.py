import cv2
import pytesseract as pt
pt.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

def extrair_texto(imagem):
    img = cv2.imread(imagem)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    texto = pt.image_to_string(gray)

    return texto