document.addEventListener("DOMContentLoaded", function() {
    var button = document.getElementById('toggleMenu');
    var menu = document.querySelector('.menu-lateral');
    var nav = menu.querySelector('.menu-lateral__navegacao');
    var padding = document.querySelector('.padding');

    var isOpen = localStorage.getItem('menuOpen');
    if (isOpen === 'true') {
        menu.classList.add('open');
        nav.style.alignItems = 'flex-start';
        padding.style.paddingLeft = '20rem';
    } else {
        menu.classList.remove('open');
        padding.style.paddingLeft = '8rem';
        nav.style.alignItems = 'center';
    }

    button.addEventListener('click', function() {
        menu.classList.toggle('open');
        
        if (menu.classList.contains('open')) {
            padding.style.paddingLeft = '20rem';
            nav.style.alignItems = 'flex-start';
            localStorage.setItem('menuOpen', 'true');
        } else {
            padding.style.paddingLeft = '8rem';
            nav.style.alignItems = 'center';
            localStorage.setItem('menuOpen', 'false');
        }
    });
});
