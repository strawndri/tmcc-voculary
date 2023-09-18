import cv2
from .detectar_caracteristicas import *

def realcar_detalhes(imagem):
    img_redimensionada = cv2.resize(imagem, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
    img_suavizada = cv2.GaussianBlur(img_redimensionada, (5, 5), 0)
    img_detalhes = 12 * cv2.subtract(img_redimensionada, img_suavizada)

    return cv2.add(img_redimensionada, img_detalhes)
import cv2
import numpy as np

def ajustar_brilho(imagem, threshold=128, alpha=1.5, beta=50):
    if np.mean(imagem) < threshold:
        return cv2.convertScaleAbs(imagem, alpha=alpha, beta=beta)
    return imagem

def remover_sombra(img):
    cinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    media_pixel = np.mean(cinza)
    if 150 < media_pixel < 230:
        bg = cv2.medianBlur(cinza, 21)
        ratio = cinza.astype(np.float32) / bg.astype(np.float32)
        corrigida = cv2.normalize(ratio, None, 0, 255, cv2.NORM_MINMAX)
        corrigida = corrigida.astype(np.uint8)
        return corrigida
    else:
        return cinza

def binarizar(imagem):
    _, img_threshold = cv2.threshold(imagem, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    if cv2.countNonZero(img_threshold) < (img_threshold.size / 2):
        return 255 - img_threshold
    return img_threshold

def calcula_angulo(imagem):
    desfocado = cv2.GaussianBlur(imagem, (5, 5), 0)
    bordas = cv2.Canny(desfocado, 50, 150, apertureSize=3)
    linhas = cv2.HoughLines(bordas, 1, np.pi/180, 200)
    if linhas is None:
        return 0
    angulos = [np.degrees(theta) - 90 if np.degrees(theta) - 90 >= 0 else np.degrees(theta) - 90 + 180 for _, theta in linhas[:, 0]]
    return np.median(angulos)

def rotaciona_imagem(imagem, angulo):
    (h, w) = imagem.shape[:2]
    centro = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(centro, angulo, 1.0)
    rotacionada = cv2.warpAffine(imagem, M, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    return rotacionada

def ajustar_orientacao(imagem):

    imagem_rotacionada = imagem
    qualidade_desejada = 50.0
    tentativas = 0
    angulo = calcula_angulo(imagem_rotacionada)
    max_qualidade = avaliar_qualidade_ocr(imagem_rotacionada)

    while (max_qualidade < qualidade_desejada):
      imagem_rotacionada = rotaciona_imagem(imagem_rotacionada, angulo)
      max_qualidade = avaliar_qualidade_ocr(imagem_rotacionada)
      tentativas += 1
      angulo += 90

      if tentativas == 2:
        break

    return imagem_rotacionada