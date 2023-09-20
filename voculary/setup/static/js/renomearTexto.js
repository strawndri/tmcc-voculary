document.addEventListener("DOMContentLoaded", function() {
    const renomearBtns = document.querySelectorAll('.botao-renomear');
    
    renomearBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const textoId = this.getAttribute('data-texto');
            const nomeCelula = document.querySelector(`.tabela__nome-arquivo[data-texto="${textoId}"]`);
            const nomeAtual = nomeCelula.textContent;
            
            nomeCelula.innerHTML = `<input type="text" value="${nomeAtual}" onblur="salvarNome(this, ${textoId})">`;
            nomeCelula.querySelector('input').focus();
        });
    });
});

function salvarNome(inputElement, textoId) {
    const novoNome = inputElement.value;
    inputElement.parentElement.textContent = novoNome;
}
