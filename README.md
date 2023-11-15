# 👁️| Voculary: reconhecimento de textos com visão computacional

![Licença](https://img.shields.io/badge/Licen%C3%A7a-MIT-f5b5ca.svg)
![Status](https://img.shields.io/badge/Status-Concluído-abf285.svg)

## Índice

- [Sobre o projeto](#sobre-o-projeto)
- [Como acessar o projeto?](#como-acessar-o-projeto)
- [Licença](#licença)

## Sobre o projeto

A Voculary foi desenvolvida como trabalho multidisciplinar de conclusão do curso técnico integrado em Informática do Colégio Estadual Pedro Macedo, de Curitiba, PR.

A obtenção de textos presentes em imagens é um processo que desempenha um papel fundamental em diferentes contextos das atividades cotidianas. Nesse sentido, a Voculary tem como objetivo facilitar a forma com que pessoas extraem informações textuais contidas em imagens, por meio da tecnologia de Reconhecimento Óptico de Caracteres (OCR). 

A Voculary é uma continuação do [Tsi.py](https://github.com/strawndri/tca-tsi.py), projeto desenvolvido em 2022 para a disciplina de Linguagem de Programação.

## Como acessar o projeto?

1. Instalar, em seu computador, o [Tesseract OCR](https://sourceforge.net/projects/tesseract-ocr.mirror/);
2. Baixar o arquivo [`por.traineddata`](https://tesseract-ocr.github.io/tessdoc/Data-Files#data-files-for-version-400-november-29-2016) e adicioná-lo à pasta `TESSERACT-OCR/tessdata`;
3. Clonar o repositório
```
git clone git@github.com:strawndri/tmcc-voculary.git
```
4. Acessar, a partir do terminal, a pasta `tmcc-voculary`
5. Acessar a pasta `voculary`:
```
cd voculary
```
6. Instalar as dependências do projeto:
```
pip install -r requirements.txt
```
7. Em `voculary/gerenciamento_texto/utils/extrair_texto.py`, atualizar o caminho de `pt.pytesseract.tesseract_cmd` para corresponder ao local da pasta `tesseract` em seu computador. Exemplo:
```
# Configuração do caminho para o executável Tesseract-OCR
pt.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
```
8. Inicializar o servidor:
```
py manage.py runserver
```

⭐ Observação: antes de realizar a instalação, recomenda-se criar um ambiente virtual, evitando inconsistências e possíveis incompatibilidades entre as tecnologias presentes em seu computador. 

## Licença

Este projeto está licenciado sob a [Licença MIT](https://opensource.org/licenses/MIT). Consulte o arquivo `LICENSE` para obter mais informações sobre os termos de licenciamento.

---

✨ Feito com carinho por [Andrieli Gonçalves](https://github.com/strawndri).
