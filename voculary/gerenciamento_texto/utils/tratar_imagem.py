import cv2
import numpy as np

from .detectar_caracteristicas import avaliar_qualidade_ocr


def realcar_detalhes(imagem):
    """
    Enfatiza os detalhes da imagem.

    :param imagem: ndarray
        Imagem a ser processada.
    :return: ndarray
        Imagem com detalhes enfatizados.
    """

    # ampliação da imagem em largura e altura, que se tornam o dobro do estado original
    imagem_redimensionada = cv2.resize(imagem, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
    
    # redução de ruídos + leve desfoque
    imagem_suavizada = cv2.GaussianBlur(imagem_redimensionada, (5, 5), 0)
    
    # remoção das partes suavizadas de imagem_redimensionada
    img_detalhes = 12 * cv2.subtract(imagem_redimensionada, imagem_suavizada)

    return cv2.add(imagem_redimensionada, img_detalhes)


def ajustar_brilho(imagem, threshold=128, alpha=1.5, beta=50):
    """
    Aprimora o brilho da imagem com base na média de pixels.

    :param imagem: ndarray
        Imagem a ser processada.
    :param threshold: int, opcional
        Limite de brilho.
    :param alpha: float, opcional
        Valor de escala. Ajuste de intensidade dos pixels.
    :param beta: float, opcional
        Delta adicionado a todos os pixels. Ajuste de brilho dos pixels.
    :return: ndarray
        Imagem com brilho ajustado.
    """

    # Verifica se a intensidade média da imagem é menor que o limiar estipulado
    if np.mean(imagem) < threshold:
        return cv2.convertScaleAbs(imagem, alpha=alpha, beta=beta)
    return imagem


def remover_sombra(imagem):
    """
    Remove sombras de imagens claras com detalhes mais escurecidos.

    :param imagem: ndarray
        Imagem a ser processada.
    :return: ndarray
        Imagem sem sombras.
    """

    # Altera a escala de cores da imagem para cinza.
    imagem_cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

    # Calcula a média de intensidade dos pixels da imagem em escala de cinza.
    intensidade_media_pixel = np.mean(imagem_cinza)

    # Verifica se a média de intensidade está em um intervalo específico.
    # Este intervalo foi escolhido para detectar imagens que são predominantemente claras,
    # mas que podem ter áreas de sombra ou detalhes escuros.
    if 150 < intensidade_media_pixel < 230:

        #Aplica uma desfocagem mediana na imagem em tons de cinza.
        fundo = cv2.medianBlur(imagem_cinza, 21)

        # Calcula a proporção entre a imagem original em tons de cinza e o fundo,
        # a fim de encontrar pontos específicos mas escurecidos
        proporcao = imagem_cinza.astype(np.float32) / fundo.astype(np.float32)

        # Normaliza a proporção de tonalidades
        imagem_corrigida = cv2.normalize(proporcao, None, 0, 255, cv2.NORM_MINMAX)

        # Converte a imagem para o formato 'uint8', para uso posterior
        imagem_corrigida = imagem_corrigida.astype(np.uint8)

        return imagem_corrigida
    else:
        # Caso a imagem não tenha 'sombras', retorna-se a imagem original.
        return imagem_cinza


def binarizar(imagem):
    """
    Binariza a imagem.

    :param imagem: ndarray
        Imagem a ser binarizada.
    :return: ndarray
        Imagem binarizada.
    """

    # Aplica o método de limiarização de Otsu para binarizar a imagem.
    # O cv2.threshold retorna dois valores: o limiar usado (que será descartado) e a imagem binarizada.
    # Neste caso, estamos separando os pixels da imagem em duas categorias distintas: preto e branco.
    _, imagem_binarizada = cv2.threshold(imagem, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Quantidade de pixels brancos
    numero_pixels_zero = cv2.countNonZero(imagem_binarizada)

    # Se a quantidade de pixels brancos for menor que a metade do total de pixels,
    # inverte as cores da imagem.
    # Isso é feito para garantir que o fundo seja sempre a cor predominante.
    if numero_pixels_zero < (imagem_binarizada.size / 2):
        return 255 - imagem_binarizada
    return imagem_binarizada


def calcula_angulo(imagem):
    """
    Calcula o ângulo de rotação para alinhar a imagem.

    :param imagem: ndarray
        Imagem a ser analisada.
    :return: float
        Ângulo de rotação em graus.
    """

    # Aplica novamente um desfoque gaussiano para suavizar a imagem e reduzir ruídos.
    imagem_desfocada = cv2.GaussianBlur(imagem, (5, 5), 0)

    # Detecção das bordas da imagem, com base no algortimo de Canny.
    bordas = cv2.Canny(imagem_desfocada, 50, 150, apertureSize=3)

    # Usa a transformada de Hough para detectar linhas na imagem.
    linhas = cv2.HoughLines(bordas, 1, np.pi/180, 200)

    # Se nenhuma linha for detectada, retorna 0.
    if linhas is None:
        return 0
    
    # Calcula os ângulos das linhas detectadas em relação ao eixo horizontal.
    # O ajuste de "-90" é usado para alinhar o ângulo ao eixo horizontal.
    # Os ajustes subsequentes são para garantir que o ângulo esteja no intervalo [0, 180].
    angulos = [np.degrees(theta) - 90 if np.degrees(theta) - 90 >= 0 else np.degrees(theta) - 90 + 180 for _, theta in linhas[:, 0]]

    # Com base nos ângulos obtidos em cada linha, retorna-se um valor médio.
    return np.median(angulos)


def rotaciona_imagem(imagem, angulo):
    """
    Rotaciona a imagem pelo ângulo especificado.

    :param imagem: ndarray
        Imagem a ser rotacionada.
    :param angulo: float
        Ângulo de rotação em graus.
    :return: ndarray
        Imagem rotacionada.
    """
    
    # Obtém as dimensões da imagem.
    altura, largura = imagem.shape[:2]
    
    # Calcula o centro da imagem.
    centro = (largura // 2, altura // 2)
    
    # Obtém a matriz de transformação de rotação usando o centro e o ângulo.
    # O valor "1.0" é o fator de escala, que mantém o tamanho original da imagem em processamento.
    matriz_rotacao = cv2.getRotationMatrix2D(centro, angulo, 1.0)
    
    # Aplica a matriz de transformação na imagem para rotacioná-la.
    imagem_rotacionada = cv2.warpAffine(
        imagem, matriz_rotacao, (largura, altura), 
        flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE
    )
    
    return imagem_rotacionada


def ajustar_orientacao(imagem):
    """
    Ajusta a orientação da imagem para otimizar o reconhecimento de OCR.

    :param imagem: ndarray
        Imagem a ser ajustada.
    :return: ndarray
        Imagem com orientação ajustada.
    """
    
    # Inicializa a imagem rotacionada com a imagem original.
    imagem_rotacionada = imagem
    
    # Define a qualidade mínima desejada para o OCR.
    qualidade_desejada = 50.0
    
    tentativas = 0
    
    # Calcula o ângulo de rotação inicial da imagem.
    angulo = calcula_angulo(imagem_rotacionada)
    
    # Avalia a qualidade do OCR na imagem rotacionada.
    max_qualidade = avaliar_qualidade_ocr(imagem_rotacionada)

    # Enquanto a qualidade do OCR for inferior à desejada (50.0), rotaciona-se novamente a imagem.
    while max_qualidade < qualidade_desejada:
        imagem_rotacionada = rotaciona_imagem(imagem_rotacionada, angulo)
        max_qualidade = avaliar_qualidade_ocr(imagem_rotacionada)
        tentativas += 1
        angulo += 90

        # Se atingir o limite de tentativas, interrompe o loop.
        if tentativas == 2:
            break

    return imagem_rotacionada