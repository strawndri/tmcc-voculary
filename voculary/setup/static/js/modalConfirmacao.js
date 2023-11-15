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

function desativarTextos(ids) {
    const data = new URLSearchParams();
    ids.forEach(id => data.append('ids_imagem', id));

    fetch('/desativar-textos/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken
        },
        body: data
    })
    .then(response => response.json())
    .then(data => {
        toggleModal('none');
        window.location.reload();
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
            toggleModal('none');
            window.location.reload();
        }
    })
    .catch(() => {
        toggleModal('none');
    });
}

const modal = document.getElementById('modalConfirmacao');
const btnAcao = document.querySelectorAll('.botao-excluir, .botao-perfil-config, .botao-perfil-senha, .botao-perfil-excluir');
const confirmarAcao = document.getElementById('confirmarAcao');
const cancelarAcao = document.querySelectorAll('#cancelarAcao, .fechar');
const checkboxSelecionarTodos = document.getElementById("selecionar-todos");
const checkboxElementos = document.querySelectorAll(".tabela__checkbox input");
const btnBulk = document.getElementById("botao-bulk");
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
        desativarTextos([textoIdParaExcluir]);
    } else {
        enviarPerfilForm();
    }
});

cancelarAcao.forEach(botaoCancelarAcao => {
    botaoCancelarAcao.addEventListener('click', () => toggleModal('none'));
})

checkboxSelecionarTodos.addEventListener("change", function() {
    const checkboxes = document.querySelectorAll('.tabela__checkbox input[type="checkbox"]');
    checkboxes.forEach(checkbox => {
        checkbox.checked = this.checked;
    });

    btnBulk.disabled = !this.checked;
});

checkboxElementos.forEach(checkbox => {
    checkbox.addEventListener("change", function() {
        let selecionados = 0; 

        for (var i = 0; i < checkboxElementos.length; i++) {
            if (checkboxElementos[i].checked) {
                selecionados++;
            }
        }

        if (selecionados > 0) {
            btnBulk.disabled = false;
        } else {
            btnBulk.disabled = true;
        }
    });
});

btnBulk.addEventListener("click", function() {
    const itensSelecionados = Array.from(document.querySelectorAll('input[type="checkbox"][data-texto]:checked'))
    .map(checkbox => checkbox.getAttribute('data-texto'));

    if (itensSelecionados.length) {
        // Armazena os itens selecionados em uma variável de escopo mais amplo
        textoIdParaExcluir = itensSelecionados;

        // Configura a mensagem da modal
        const mensagemParagrafo = modal.querySelector('.mensagem-confirmacao');
        mensagemParagrafo.textContent = "Tem certeza de que deseja excluir os textos selecionados?";

        toggleModal('block');
    }
});
