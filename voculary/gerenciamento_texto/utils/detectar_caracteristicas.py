import cv2
import pytesseract as pt
from langdetect import detect


def detectar_idioma(imagem):
    """
    :param imagem:
    """
    codigos = {
        'en': 'eng',
        'pt': 'por'
    }

    try:
        cod_idioma = codigos[detect(pt.image_to_string(imagem))]
    except:
        cod_idioma = 'eng'

    return cod_idioma

def determinar_psm(imagem):
    """
    :param imagem:
    """
    pixels_pretos = imagem.size - cv2.countNonZero(imagem)
    proporcao_preto = pixels_pretos / imagem.size

    if proporcao_preto > 0.2:
        return '6'
    else:
        return '1'

def avaliar_qualidade_ocr(imagem):
    """
    :param imagem:
    """
    resultado = pt.image_to_data(imagem, output_type=pt.Output.DICT)
    confiancas = [int(val) for val in resultado['conf'] if str(val).isdigit()]
    if confiancas:
        return sum(confiancas) / len(confiancas)
    return 0