import cv2
import pytesseract as pt
from langdetect import detect

def detectar_idioma(imagem):
    """
    Detecta o idioma principal de uma imagem.

    :param imagem: ndarray
        Imagem a ser analisada.
    :return: str
        Código do idioma detectado.
    """

    # Dicionário com os idiomas a serem usados.
    # Criado porque há uma divergência entre o padrão estipulado pelas bibliotecas 'langdetect' e 'pytesseract'
    # en/eng: Inglês
    # pt/por: Português
    codigos = {
        'en': 'eng',
        'pt': 'por'
    }

    # Tentativa de detecção de idioma.
    try:
        cod_idioma = codigos[detect(pt.image_to_string(imagem))]
    except:
        # Em caso de erro na detecção, retorna inglês como padrão.
        cod_idioma = 'eng'

    return cod_idioma


def determinar_psm(imagem):
    """
    Determina o modo de segmentação de página (PSM) para OCR baseado na proporção de pixels pretos.

    :param imagem: ndarray
        Imagem a ser analisada.
    :return: str
        Modo de segmentação de página recomendado para OCR.
    """

    # Calcula a quantidade de pixels pretos na imagem.
    pixels_pretos = imagem.size - cv2.countNonZero(imagem)
    
    # Calcula a proporção de pixels pretos em relação ao total.
    proporcao_preto = pixels_pretos / imagem.size

    # Define o PSM com base na proporção calculada.
    if proporcao_preto > 0.2:
        # Bloco de texto simples e uniforme.
        return '6'
    else:
        # Segmentação automática de páginas com OSD (Orientation and Script Detection).
        return '1'


def avaliar_qualidade_ocr(imagem):
    """
    Avalia a qualidade do OCR em uma imagem com base na confiança das palavras detectadas.

    :param imagem: ndarray
        Imagem a ser avaliada.
    :return: float
        Média de confiança no reconhecimento de texto da imagem.
    """

    # Realiza o OCR na imagem e obtém os resultados.
    resultado = pt.image_to_data(imagem, output_type=pt.Output.DICT)
    
    # Extrai os valores de confiança para cada palavra detectada.
    confiancas = [int(val) for val in resultado['conf'] if str(val).isdigit()]
    
    # Calcula e retorna a média das confianças.
    if confiancas:
        return sum(confiancas) / len(confiancas)
    
    return 0