document.addEventListener("DOMContentLoaded", function() {
    const botaoRenomear = document.querySelectorAll('.botao-renomear');
    
    botaoRenomear.forEach(btn => {
        btn.addEventListener('click', handleRenomearClick);
    });
});

function handleRenomearClick() {
    const idTexto = this.closest('[data-texto]').getAttribute('data-texto');
    let seletor;

    if (this.classList.contains('tabela__botao-renomear')) {
        seletor = `.tabela__nome-arquivo[data-texto="${idTexto}"]`;
    } else if (this.classList.contains('aba-lateral__botao-renomear')) {
        seletor = `.aba-lateral[data-texto="${idTexto}"] .aba-lateral__titulo`;
    }

    const celulaNome = document.querySelector(seletor);
    transformarCelulaEmInput(celulaNome, idTexto);
}

function transformarCelulaEmInput(celula, idTexto) {
    const nomeAtual = celula.textContent;
    celula.innerHTML = `<input type="text" value="${nomeAtual}" onblur="salvarNome(this, ${idTexto})">`;

    const inputElement = celula.querySelector('input');
    inputElement.focus();
    inputElement.addEventListener('keypress', function(e) {
        if (e.key == "Enter") {
            e.preventDefault();
            salvarNome(this, idTexto);
        }
    });

    inputElement.setSelectionRange(inputElement.value.length, inputElement.value.length);
}

function salvarNome(inputElement, idImagem) {
    const novoNome = inputElement.value;
    const tokenCSRF = getCookie('csrftoken');
    
    fetch(`/alterar_nome/${idImagem}/`, {
        method: 'POST',
        body: new URLSearchParams(`novo_nome=${novoNome}`),
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': tokenCSRF
        }
    })
    .then(response => response.json())
    .then(data => atualizarNome(data, inputElement, idImagem))
    .catch(error => console.error('Erro ao atualizar o nome:', error));
}

function atualizarNome(data, inputElement, idImagem) {
    if (data.success) {
        const nomeFinal = inputElement.value || 'Sem título';
        inputElement.parentElement.textContent = nomeFinal;
        
        const celulaNomeTabela = document.querySelector(`.tabela__nome-arquivo[data-texto="${idImagem}"], .meus-textos__card[data-texto="${idImagem}"] h3 `);
        if (celulaNomeTabela) {
            celulaNomeTabela.textContent = nomeFinal;
        }
    }
    
    mostrarMensagem(data.message, data.message_type);
}