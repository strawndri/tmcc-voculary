let inputImagem = document.querySelector('.input-imagem');
let inputImagemPadrao = document.querySelector('.imagem-padrao');

let zoomImagemElementos = document.querySelector('.reconhecimento-texto__imagem-zoom')
let zoomInBotao = document.getElementById('btnZoomIn')
let zoomOutBotao = document.getElementById('btnZoomOut')

let alturaImagem = 100
let limiteZoom = 5;

inputImagem.addEventListener('change', function() {
    if (this.files && this.files[0]) {

        zoomImagemElementos.classList.toggle("zoom-inativo");
        let reader = new FileReader();

        reader.onload = function(e) {
            inputImagemPadrao.style.backgroundImage = `url('${e.target.result}')`;
            inputImagemPadrao.style.backgroundSize = `auto 100%`;
        }

        // Este é o código que faltava para iniciar a leitura do arquivo
        reader.readAsDataURL(this.files[0]);

        console.log('Imagem sendo lida...');
    }
});

zoomInBotao.addEventListener('click', function() {
    alturaImagem += 10
    inputImagemPadrao.style.backgroundSize = `auto ${alturaImagem}%`;
});

zoomOutBotao.addEventListener('click', function() {
    alturaImagem -= 10
    inputImagemPadrao.style.backgroundSize = `auto ${alturaImagem}%`;
});
