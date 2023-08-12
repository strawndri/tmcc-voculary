from langdetect import detect
import pytesseract as pt
import cv2
pt.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

def extrair_texto(imagem):

    codigos = {
        'en': 'eng',
        'es': 'spa',
        'fr': 'fra',
        'id': 'ind',
        'it': 'ita',
        'ja': 'jpn',
        'pt': 'por',
        'th': 'tha',
        'uk': 'ukr',
        'zh-cn': 'chi_sim',
        'zh-tw': 'chi_tra'
    }

    img = cv2.imread(imagem)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)

    try:
        idioma = codigos[detect(pt.image_to_string(img))]
    except:
        idioma = "eng"  

    texto = pt.image_to_string(img, lang=idioma)

    return texto
