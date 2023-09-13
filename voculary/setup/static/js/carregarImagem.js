let inputImagem = document.querySelector('.input-imagem');
let inputImagemDisplay = document.querySelector('.imagem-display');

let zoomImagemElementos = document.querySelector('.reconhecimento-texto__imagem-zoom')
let zoomInBotao = document.getElementById('btnZoomIn')
let zoomOutBotao = document.getElementById('btnZoomOut')

let alturaImagem = 100
let limiteZoom = 5;

inputImagem.addEventListener('change', function() {
    if (this.files && this.files[0]) {

        zoomImagemElementos.classList.remove("zoom-inativo");
        inputImagemDisplay.classList.remove("icone-padrao");

        let reader = new FileReader();

        reader.onload = function(e) {
            inputImagemDisplay.style.backgroundImage = `url('${e.target.result}')`;
            inputImagemDisplay.style.backgroundSize = `auto 100%`;
        }

        // Este é o código que faltava para iniciar a leitura do arquivo
        reader.readAsDataURL(this.files[0]);

        console.log('Imagem sendo lida...');
    }
});

zoomInBotao.addEventListener('click', function() {
    alturaImagem += 10
    inputImagemDisplay.style.backgroundSize = `auto ${alturaImagem}%`;
});

zoomOutBotao.addEventListener('click', function() {
    alturaImagem -= 10
    inputImagemDisplay.style.backgroundSize = `auto ${alturaImagem}%`;
});
