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

const modal = document.getElementById('modalConfirmacao');
const btnAcao = document.querySelectorAll('.botao-excluir, .botao-perfil-config, .botao-perfil-senha, .botao-perfil-excluir');
const confirmarAcao = document.getElementById('confirmarAcao');
const cancelarAcao = document.getElementById('cancelarAcao');
const selectAllCheckbox = document.getElementById("selecionar-todos");
const checkboxElementos = document.querySelectorAll(".tabela__checkbox input");
const bulkDeleteBtn = document.getElementById("bulk-delete");
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

cancelarAcao.addEventListener('click', () => toggleModal('none'));

// Logic for bulk delete
selectAllCheckbox.addEventListener("change", function() {
    const checkboxes = document.querySelectorAll('.tabela__checkbox input[type="checkbox"]');
    checkboxes.forEach(checkbox => {
        checkbox.checked = this.checked;
    });

    bulkDeleteBtn.disabled = !this.checked;
});

checkboxElementos.forEach(checkbox => {
    checkbox.addEventListener("change", function() {
        bulkDeleteBtn.disabled = !this.checked;
    })
})

bulkDeleteBtn.addEventListener("click", function() {
    const selectedItems = Array.from(document.querySelectorAll('input[type="checkbox"][data-texto]:checked'))
    .map(checkbox => checkbox.getAttribute('data-texto'));

    if (selectedItems.length) {
        // Armazena os itens selecionados em uma variável de escopo mais amplo
        textoIdParaExcluir = selectedItems;

        // Configura a mensagem da modal
        const mensagemParagrafo = modal.querySelector('.mensagem-confirmacao');
        mensagemParagrafo.textContent = "Tem certeza de que deseja excluir os textos selecionados?";

        // Mostra a modal
        toggleModal('block');
    }
});