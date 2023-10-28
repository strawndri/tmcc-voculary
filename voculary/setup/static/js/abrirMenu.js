document.addEventListener("DOMContentLoaded", function() {
    // Selecionando os elementos
    var button = document.getElementById('toggleMenu');
    var menu = document.querySelector('.menu-lateral');
    var padding = document.querySelector('.padding');

    // Função para atualizar o estado e estilo do menu
    function updateMenuState(isOpen) {
        if (isOpen) {
            menu.classList.add('open');
            if (window.innerWidth > 768) {
                padding.style.paddingLeft = '20rem';
            }
            localStorage.setItem('menuOpen', 'true');
        } else {
            menu.classList.remove('open');
            padding.style.paddingLeft = '8rem';
            localStorage.setItem('menuOpen', 'false');
        }
    }

    // Checar o status inicial do menu no localStorage e atualizar o estado do menu
    var initialOpenState = localStorage.getItem('menuOpen') === 'true';
    updateMenuState(initialOpenState);

    // Atualiza o estado do menu quando o botão é clicado
    button.addEventListener('click', function() {
        var isOpen = menu.classList.contains('open');
        updateMenuState(!isOpen);
    });
});