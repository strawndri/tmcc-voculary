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

document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('modalConfirmacao');
    const btnExcluir = document.querySelectorAll('.botao-excluir');
    const confirmarExclusao = document.getElementById('confirmarExclusao');
    const cancelarExclusao = document.getElementById('cancelarExclusao');
    let csrftoken = getCookie('csrftoken');

    btnExcluir.forEach(button => {
        button.addEventListener('click', function() {
            modal.style.display = 'block';
            textoIdParaExcluir = this.closest('[data-texto]').getAttribute('data-texto')
        });
    });

    confirmarExclusao.addEventListener('click', function() {
        if (!textoIdParaExcluir) {
            console.error("Nenhum ID de texto para excluir foi definido!");
            modal.style.display = 'none';
            return;
        }
    
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
                alert("Erro: " + data.message);
                modal.style.display = 'none';
            }
        })
        .catch(error => {
            console.error('Erro:', error);
            modal.style.display = 'none';
        });
    });
    

    cancelarExclusao.addEventListener('click', function() {
        modal.style.display = 'none';
    });
});
