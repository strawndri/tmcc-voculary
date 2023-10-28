document.addEventListener("DOMContentLoaded", function() {
    const mensagensDjango = document.querySelectorAll('.mensagem');
    mensagensDjango.forEach(iniciarTemporizadorMensagem);
});

function criarElemento(classe, tipo='div') {
    const elemento = document.createElement(tipo);
    if (classe) {
        elemento.classList.add(...classe.split(' '));
    }
    return elemento;
}

function adicionarEventosMensagem(mensagemElement) {
    const iFechar = mensagemElement.querySelector('.fechar');
    iFechar.addEventListener("click", () => removerMensagem(mensagemElement));

    const divProgresso = mensagemElement.querySelector('.progresso');
    divProgresso.addEventListener('animationend', () => divProgresso.classList.add('finalizado'));

    setTimeout(() => removerMensagem(mensagemElement), 5000);
}

function removerMensagem(mensagemElement) {
    mensagemElement.classList.remove('ativo');
    setTimeout(() => mensagemElement.remove(), 300);
}

function mostrarMensagem(mensagem, tipo='success') {
    if (!mensagem) return;

    const divMensagem = criarElemento('mensagem ativo');
    divMensagem.innerHTML = `
        <div class="mensagem__conteudo">
            <i class="icon" data-status="${tipo}"></i>
            <span class="mensagem__conteudo__texto">${mensagem}</span>
        </div>
        <i class="fechar"></i>
        <div class="progresso" data-status="${tipo}"></div>
    `;

    document.body.appendChild(divMensagem);
    adicionarEventosMensagem(divMensagem);
}