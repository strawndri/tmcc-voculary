let imagemElemento = document.querySelector('.imagem')
let imagemDiv = document.getElementById('selecionarImagem')
let zoomImagemElementos = document.querySelector('.reconhecimento-texto__imagem-zoom')
let zoomInBotao = document.getElementById('btnZoomIn')
let zoomOutBotao = document.getElementById('btnZoomOut')

let tamanhoImagem = 100
let limiteZoom = 5;

imagemDiv.addEventListener('click', function() {
    document.getElementById('imagem-upload').click()
    
});

document.getElementById('imagem-upload').addEventListener('change', function(event) {
    
    let arquivo = event.target.files[0]
    
    imagemDiv.classList.toggle("sem-imagem");
    zoomImagemElementos.classList.toggle("zoom-inativo");
    
    if (arquivo) {
        let leitor = new FileReader();
        
        leitor.onload = function(e) {
            imagemElemento.src = e.target.result;
            imagemElemento.style.height = tamanhoImagem + '%';
            imagemElemento.style.width = 'auto';
            imagemDiv.style.overflow = 'hidden';
        };
        
        leitor.readAsDataURL(arquivo);
    }
});

zoomInBotao.addEventListener('click', function() {
    tamanhoImagem += 10
    imagemElemento.style.height = (tamanhoImagem) + '%';
});

zoomOutBotao.addEventListener('click', function() {
    tamanhoImagem -= 10
    imagemElemento.style.height = (tamanhoImagem) + '%';
});