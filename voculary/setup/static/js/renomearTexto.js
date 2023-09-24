document.addEventListener("DOMContentLoaded", function() {
    const renomearBtns = document.querySelectorAll('.botao-renomear');
    
    renomearBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const textoId = this.closest('[data-texto]').getAttribute('data-texto');
            let selector;
            if (this.classList.contains('tabela__botao-renomear')) {
                selector = `.tabela__nome-arquivo[data-texto="${textoId}"]`;
            } else if (this.classList.contains('aba-lateral__botao-renomear')) {
                selector = `.aba-lateral[data-texto="${textoId}"] .aba-lateral__titulo`;
            }

            const nomeCelula = document.querySelector(selector);
            const nomeAtual = nomeCelula.textContent;
            nomeCelula.innerHTML = `<input type="text" value="${nomeAtual}" onblur="salvarNome(this, ${textoId})">`;
            nomeCelula.querySelector('input').focus();
        });
    });
});


function salvarNome(inputElement, textoId) {
    const novoNome = inputElement.value;
    csrftoken = getCookie('csrftoken');
    
    fetch(`/alterar_nome/${textoId}/`, {
        method: 'POST',
        body: new URLSearchParams(`novo_nome=${novoNome}`),
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrftoken
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Atualizar o nome na aba lateral
            inputElement.parentElement.textContent = novoNome;
            
            // Atualizar o nome na tabela (opcional, se necessário)
            const nomeCelulaTabela = document.querySelector(`.tabela__nome-arquivo[data-texto="${textoId}"], .meus-textos__card[data-texto="${textoId}"] h3 `);
            if (nomeCelulaTabela) {
                nomeCelulaTabela.textContent = novoNome;
            }
        }
        
        mostrarMensagem(data.message, data.message_type);
        console.log(data.message, data.message_type)
    })
    .catch(error => console.error('Erro ao atualizar o nome:', error));
}

