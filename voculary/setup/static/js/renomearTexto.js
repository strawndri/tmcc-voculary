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
    csrftoken = getCookie('csrftoken');
    
    // Enviar requisição para o servidor
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
            inputElement.parentElement.textContent = novoNome;
            location.reload(); 
        } else {
            location.reload(); 
        }
    })
    .catch(error => console.error('Erro ao atualizar o nome:', error));
}


