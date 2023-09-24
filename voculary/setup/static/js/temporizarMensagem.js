function mostrarMensagem(mensagem, tipo='success') {

    if (!mensagem) {
        return;  
    }

    const divMensagem = document.createElement('div');
    divMensagem.classList.add('mensagem', 'ativo', tipo);

    const divConteudo = document.createElement('div');
    divConteudo.classList.add('mensagem__conteudo');
    const iIcon = document.createElement('i');
    iIcon.classList.add('icon');
    const spanTexto = document.createElement('span');
    spanTexto.classList.add('mensagem__conteudo__texto');
    spanTexto.textContent = mensagem;

    divConteudo.appendChild(iIcon);
    divConteudo.appendChild(spanTexto);

    const iFechar = document.createElement('i');
    iFechar.classList.add('fechar');

    const divProgresso = document.createElement('div');
    divProgresso.classList.add('progresso');

    divMensagem.appendChild(divConteudo);
    divMensagem.appendChild(iFechar);
    divMensagem.appendChild(divProgresso);

    document.body.appendChild(divMensagem);

    iFechar.addEventListener("click", () => {
        divMensagem.classList.remove('ativo');
        setTimeout(() => {
            divMensagem.remove();
        }, 300);
    });

    setTimeout(() => {
        divMensagem.classList.remove('ativo');
        setTimeout(() => {
            divMensagem.remove();
        }, 300);
    }, 5000);
}
