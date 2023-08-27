from langdetect import detect
import pytesseract as pt
import cv2

import numpy as np

pt.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

def detectar_idioma(imagem):
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
    
    try:
        cod_idioma = codigos[detect(pt.image_to_string(imagem))]
    except:
        cod_idioma = 'eng'

    return cod_idioma

def determinar_psm(imagem):
    pixels_pretos = imagem.size - cv2.countNonZero(imagem)
    proporcao_preto = pixels_pretos / imagem.size

    if proporcao_preto > 0.2:
        return '6'
    else:
        return '1'

def realcar_detalhes(imagem):
    img_redimensionada = cv2.resize(imagem, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
    img_suavizada = cv2.GaussianBlur(img_redimensionada, (5, 5), 0)
    img_detalhes = 12 * cv2.subtract(img_redimensionada, img_suavizada)
    
    return cv2.add(img_redimensionada, img_detalhes)

def ajustar_brilho(imagem, threshold=128, alpha=1.5, beta=50):
    if np.mean(imagem) < threshold:
        return cv2.convertScaleAbs(imagem, alpha=alpha, beta=beta)
    return imagem

def binarizar(imagem):
    _, img_threshold = cv2.threshold(imagem, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    if cv2.countNonZero(img_threshold) < (img_threshold.size / 2):
        return 255 - img_threshold
    return img_threshold

def extrair_texto(imagem):
    
    imagem = cv2.imread(imagem)
    imagem = realcar_detalhes(imagem)
    imagem = ajustar_brilho(imagem)
    img_cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
    img_binarizada = binarizar(img_cinza)

    psm_valor = determinar_psm(img_binarizada)
    cod_idioma = detectar_idioma(img_binarizada)

    texto = pt.image_to_string(img_binarizada, lang=cod_idioma, config=f'--psm {psm_valor}')

    return texto
