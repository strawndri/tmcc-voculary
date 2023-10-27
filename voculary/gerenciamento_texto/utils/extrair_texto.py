import pytesseract as pt

from .detectar_caracteristicas import *
from .tratar_imagem import *

pt.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

def extrair_texto(img_original):
    """
    :param img_original:
    """

    min_conf = 50
    
    # img_original = cv2.imread(img_original)
    img_original = cv2.imdecode(np.frombuffer(img_original.read(), np.uint8), -1)
    img_realcada = realcar_detalhes(img_original)
    img_com_brilho = ajustar_brilho(img_realcada)
    img_sem_sombra = remover_sombra(img_com_brilho)
    img_binarizada = binarizar(img_sem_sombra)
    img_final = ajustar_orientacao(img_binarizada)

    psm_valor = determinar_psm(img_final)
    cod_idioma = detectar_idioma(img_final)

    resultado_qualidade = avaliar_qualidade_ocr(img_final)
    print(resultado_qualidade)

    if resultado_qualidade >= 50:
        resultado = pt.image_to_data(img_final,
                                lang=cod_idioma,
                                config=f'--psm {psm_valor}',
                                output_type=pt.Output.DICT)
        texto_filtrado = [resultado['text'][i] for i in range(len(resultado['conf'])) if int(resultado['conf'][i] >= min_conf)]
        texto = ' '.join(texto_filtrado)
        return texto, cod_idioma

    else:
        return None, None
