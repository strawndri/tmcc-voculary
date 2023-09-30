function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const modal = document.getElementById('modalConfirmacao');
const btnAcao = document.querySelectorAll('.botao-excluir, .botao-perfil-config, .botao-perfil-senha');
const confirmarAcao = document.getElementById('confirmarAcao');
const cancelarAcao = document.getElementById('cancelarAcao');
let csrftoken = getCookie('csrftoken');
let mensagemConfirmacao = ''; // Armazena a mensagem de confirmação
let textoIdParaAcao = null; // Armazena o ID do texto para ação

let perfilForm = document.querySelector('.perfil-form');

let currentForm = null;

btnAcao.forEach(button => {
    button.addEventListener('click', function(event) {
        event.preventDefault(); // Impedir o comportamento padrão do botão

        modal.style.display = 'block';
        mensagemConfirmacao = this.getAttribute('data-message'); 
        const mensagemParagrafo = modal.querySelector('.mensagem-confirmacao');
        let closestElement = this.closest('[data-texto]');
        textoIdParaExcluir = closestElement ? closestElement.getAttribute('data-texto') : null;
        
        currentForm = this.closest('.perfil-form');
        
        mensagemParagrafo.textContent = mensagemConfirmacao;
    });
});


confirmarAcao.addEventListener('click', function() {
    if (textoIdParaExcluir) {
        fetch(`/desativar-texto/${textoIdParaExcluir}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                modal.style.display = 'none';
                textoIdParaExcluir = null; 
                window.location.reload();
            } else {
                modal.style.display = 'none';
            }
        })
        .catch(error => {
            console.error('Erro:', error);
            modal.style.display = 'none';
        });
    } else {
        currentForm.submit()
        fetch('/perfil', {
            method: 'POST',
            body: new FormData(currentForm),
            headers: {
                'X-CSRFToken': csrftoken
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                modal.style.display = 'none';
                window.location.reload();
            } else {
                alert("Erro: " + data.message);
                modal.style.display = 'none';
            }
        })
        .catch(error => {
            modal.style.display = 'none';
        });
    }
});

cancelarAcao.addEventListener('click', function() {
    modal.style.display = 'none';
});
