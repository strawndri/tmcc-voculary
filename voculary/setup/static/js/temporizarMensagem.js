document.addEventListener("DOMContentLoaded", function() {
    const mensagensDjango = document.querySelectorAll('.mensagem');
    mensagensDjango.forEach(iniciarTemporizadorMensagem);
});

function iniciarTemporizadorMensagem(mensagemElement) {
    const iFechar = mensagemElement.querySelector('.fechar');
    iFechar.addEventListener("click", () => {
        mensagemElement.classList.remove('ativo');
        setTimeout(() => {
            mensagemElement.remove();
        }, 300);
    });

    const divProgresso = mensagemElement.querySelector('.progresso');
    
    // Adicione uma classe 'finalizado' após a animação do progresso
    divProgresso.addEventListener('animationend', () => {
        divProgresso.classList.add('finalizado');
    });

    setTimeout(() => {
        mensagemElement.classList.remove('ativo');
        setTimeout(() => {
            mensagemElement.remove();
        }, 300);
    }, 5000);
}


function mostrarMensagem(mensagem, tipo='success') {
    if (!mensagem) {
        return;  
    }

    const divMensagem = document.createElement('div');
    divMensagem.classList.add('mensagem', 'ativo');

    const divConteudo = document.createElement('div');
    divConteudo.classList.add('mensagem__conteudo');
    const iIcon = document.createElement('i');
    iIcon.classList.add('icon');
    iIcon.dataset.status = tipo;
    const spanTexto = document.createElement('span');
    spanTexto.classList.add('mensagem__conteudo__texto');
    spanTexto.textContent = mensagem;

    divConteudo.appendChild(iIcon);
    divConteudo.appendChild(spanTexto);

    const iFechar = document.createElement('i');
    iFechar.classList.add('fechar');

    const divProgresso = document.createElement('div');
    divProgresso.classList.add('progresso');
    divProgresso.dataset.status = tipo;

    divMensagem.appendChild(divConteudo);
    divMensagem.appendChild(iFechar);
    divMensagem.appendChild(divProgresso);

    document.body.appendChild(divMensagem);

    iniciarTemporizadorMensagem(divMensagem);
}