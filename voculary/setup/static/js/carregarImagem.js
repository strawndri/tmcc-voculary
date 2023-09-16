let inputImagem = document.querySelector('.input-imagem');
let inputImagemDisplays = document.querySelectorAll('.imagem-display');

let zoomImagemElementos = document.querySelectorAll('.reconhecimento-texto__imagem-zoom')
let zoomInBotoes = document.querySelectorAll('#btnZoomIn')
let zoomOutBotoes = document.querySelectorAll('#btnZoomOut')

let alturaImagem = 100;

inputImagem.addEventListener('change', function() {
    if (this.files && this.files[0]) {
        let reader = new FileReader();

        reader.onload = function(e) {
            inputImagemDisplays.forEach(inputImagemDisplay => {
                inputImagemDisplay.style.backgroundImage = `url('${e.target.result}')`;
                inputImagemDisplay.style.backgroundSize = `auto 100%`;
                inputImagemDisplay.classList.remove("icone-padrao");
            });
            zoomImagemElementos.forEach(zoomEl => zoomEl.classList.remove("zoom-inativo"));
        }

        reader.readAsDataURL(this.files[0]);
    }
});

zoomInBotoes.forEach(zoomInBotao => {
    zoomInBotao.addEventListener('click', function() {
        alturaImagem += 10;
        inputImagemDisplays.forEach(inputImagemDisplay => {
            if (!inputImagemDisplay.classList.contains('icone-padrao')) {
                inputImagemDisplay.style.backgroundSize = `auto ${alturaImagem}%`;
            }
        });
    });
});

zoomOutBotoes.forEach(zoomOutBotao => {
    zoomOutBotao.addEventListener('click', function() {
        alturaImagem -= 10;
        inputImagemDisplays.forEach(inputImagemDisplay => {
            if (!inputImagemDisplay.classList.contains('icone-padrao')) {
                inputImagemDisplay.style.backgroundSize = `auto ${alturaImagem}%`;
            }
        });
    });
});
