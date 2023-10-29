let inputImagem = document.querySelector('.input-imagem');
let inputImagemDisplays = document.querySelectorAll('.imagem-display');

let zoomImagemElementos = document.querySelectorAll('.reconhecimento-texto__imagem-zoom')
let zoomBotoes = document.querySelectorAll('.btn-zoom-in, .btn-zoom-out');

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

function atualizarZoom(tipo, valor) {
    alturaImagem += valor;
    inputImagemDisplays.forEach(inputImagemDisplay => {
        console.log(tipo, inputImagemDisplay.dataset.tipo, alturaImagem)
        if (!inputImagemDisplay.classList.contains('icone-padrao') && tipo === inputImagemDisplay.dataset.tipo) {
            inputImagemDisplay.style.backgroundSize = `auto ${alturaImagem}%`;
        }
    });
}

zoomBotoes.forEach(zoomBotao => {
    zoomBotao.addEventListener('click', function() {
        const tipo = this.dataset.tipo;
        const valor = this.classList.contains("btn-zoom-in") ? 10 : -10;
        atualizarZoom(tipo, valor);
    });
});

function resetarZoom() {
    alturaImagem = 100; 
    inputImagemDisplays.forEach(inputImagemDisplay => {
        if (!inputImagemDisplay.classList.contains('icone-padrao')) {
            inputImagemDisplay.style.backgroundSize = `auto 100%`;
        }
    });
}