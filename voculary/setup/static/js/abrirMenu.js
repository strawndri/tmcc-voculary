document.addEventListener("DOMContentLoaded", function() {
    var button = document.getElementById('toggleMenu');
    var menu = document.querySelector('.menu-lateral');
    var nav = menu.querySelector('.menu-lateral__navegacao');
    var padding = document.querySelector('.padding');

    var isOpen = localStorage.getItem('menuOpen');
    if (isOpen === 'true') {
        menu.classList.add('open');
        if (window.innerWidth > 768) {
            padding.style.paddingLeft = '20rem';
        }
    } else {
        menu.classList.remove('open');
        padding.style.paddingLeft = '8rem';
    }

    button.addEventListener('click', function() {
        menu.classList.toggle('open');
        
        if (window.innerWidth > 768) {
            if (menu.classList.contains('open')) {
                padding.style.paddingLeft = '20rem';
                localStorage.setItem('menuOpen', 'true');
            } else {
                padding.style.paddingLeft = '8rem';
                localStorage.setItem('menuOpen', 'false');
            }
        }
    });
});
