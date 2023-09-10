let imagemInputs = document.querySelectorAll('.input-imagem');
let textoElemento = document.querySelector('.texto');
let botoes = [document.getElementById('btnBaixar'), 
              document.getElementById('btnCopiar'), 
              document.getElementById('btnSalvar')];

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

