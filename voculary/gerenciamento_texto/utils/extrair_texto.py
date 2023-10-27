import cv2
import numpy as np
import pytesseract as pt

from .detectar_caracteristicas import (avaliar_qualidade_ocr, detectar_idioma,
                                       determinar_psm)
from .tratar_imagem import (ajustar_brilho, ajustar_orientacao, binarizar,
                            realcar_detalhes, remover_sombra)

# Configuração do caminho para o executável Tesseract-OCR.
pt.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'


def extrair_texto(imagem_original):
    """
    Extrai o texto de uma imagem usando técnicas de pré-processamento e OCR.

    :param imagem_original: File object
        Imagem a ser processada.
    :return: tuple
        Texto extraído e código do idioma detectado.
    """
    
    # Limite mínimo de confiança para aceitar um texto detectado pelo OCR.
    confianca_minima = 50
    
    # Converte a imagem original em formato de matriz.
    imagem_matriz = cv2.imdecode(np.frombuffer(imagem_original.read(), np.uint8), -1)
    
    # Realça os detalhes da imagem.
    imagem_realcada = realcar_detalhes(imagem_matriz)
    
    # Ajusta o brilho da imagem.
    imagem_com_brilho = ajustar_brilho(imagem_realcada)
    
    # Remove sombras da imagem.
    imagem_sem_sombra = remover_sombra(imagem_com_brilho)
    
    # Binariza a imagem.
    imagem_binarizada = binarizar(imagem_sem_sombra)
    
    # Ajusta a orientação da imagem.
    imagem_final = ajustar_orientacao(imagem_binarizada)

    # Determina o modo de segmentação de página para o OCR.
    psm_valor = determinar_psm(imagem_final)
    
    # Detecta o idioma da imagem.
    codigo_idioma = detectar_idioma(imagem_final)

    # Avalia a qualidade do OCR na imagem.
    resultado_qualidade = avaliar_qualidade_ocr(imagem_final)
    print(resultado_qualidade)

    # Se a qualidade do OCR for aceitável, extrai o texto.
    if resultado_qualidade >= 50:
        resultado = pt.image_to_data(imagem_final,
                                     lang=codigo_idioma,
                                     config=f'--psm {psm_valor}',
                                     output_type=pt.Output.DICT)
        
        # Filtra os resultados com base na confiança.
        texto_filtrado = [resultado['text'][i] for i in range(len(resultado['conf'])) if int(resultado['conf'][i] >= confianca_minima)]
        
        # Une as palavras filtradas, em uma única string, para formar o texto final.
        texto = ' '.join(texto_filtrado)
        
        return texto, codigo_idioma
    else:
        return None, None
