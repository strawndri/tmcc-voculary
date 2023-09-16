let imagemInputs = document.querySelectorAll('.input-imagem');
let textoElemento = document.querySelector('.texto');
let cardFieldElement = document.querySelector('[data-origin="card-field"]');

let btnBaixar = cardFieldElement.querySelector('.btn-baixar');
let btnCopiar = cardFieldElement.querySelector('.btn-copiar');
let btnSalvar = cardFieldElement.querySelector('#btnSalvar');

let botoes = [btnBaixar, btnCopiar, btnSalvar];

function atualizaEstadoDosBotoes() {
    if (textoElemento.textContent.trim()) {
        botoes.forEach(btn => btn.disabled = false);
    } else {
        botoes.forEach(btn => btn.disabled = true);
    }
}

atualizaEstadoDosBotoes();
textoElemento.addEventListener('input', atualizaEstadoDosBotoes);

imagemInputs.forEach(function(input) {
    input.addEventListener('input', function() {
        document.getElementById('btnExtrair').disabled = !this.value;
    });
});