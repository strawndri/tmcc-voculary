function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) {
        return decodeURIComponent(parts.pop().split(';').shift());
    }
    return null;
}

function toggleModal(displayStatus) {
    modal.style.display = displayStatus;
}

function desativarTexto() {
    fetch(`/desativar-texto/${textoIdParaExcluir}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            toggleModal('none');
            window.location.reload();
        } else {
            toggleModal('none');
        }
    })
    .catch(error => {
        console.error('Erro:', error);
        toggleModal('none');
    });
}

function enviarPerfilForm() {
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
            toggleModal('none');
            window.location.reload();
        } else {
            alert("Erro: " + data.message);
            toggleModal('none');
        }
    })
    .catch(() => {
        toggleModal('none');
    });
}

const modal = document.getElementById('modalConfirmacao');
const btnAcao = document.querySelectorAll('.botao-excluir, .botao-perfil-config, .botao-perfil-senha, .botao-perfil-excluir');
const confirmarAcao = document.getElementById('confirmarAcao');
const cancelarAcao = document.getElementById('cancelarAcao');
const csrftoken = getCookie('csrftoken');

let textoIdParaExcluir = null;
let currentForm = null;

btnAcao.forEach(button => {
    button.addEventListener('click', event => {
        event.preventDefault(); 
        toggleModal('block');

        const mensagemParagrafo = modal.querySelector('.mensagem-confirmacao');
        mensagemParagrafo.textContent = button.getAttribute('data-message');

        let closestElement = button.closest('[data-texto]');
        textoIdParaExcluir = closestElement ? closestElement.getAttribute('data-texto') : null;
        
        currentForm = button.closest('.perfil-form');
    });
});

confirmarAcao.addEventListener('click', () => {
    if (textoIdParaExcluir) {
        desativarTexto();
    } else {
        enviarPerfilForm();
    }
});

cancelarAcao.addEventListener('click', () => toggleModal('none'));