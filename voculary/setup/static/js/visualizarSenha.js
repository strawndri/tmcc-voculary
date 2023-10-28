document.addEventListener('DOMContentLoaded', function() {
    const senhaInput = document.querySelectorAll('input[type="password"]');
    const visualizarSenha = document.querySelectorAll('.formulario__botao--senha');

    for (let i = 0; i < visualizarSenha.length; i++) {
        visualizarSenha[i].addEventListener('click', () => {
            const senhaInput = visualizarSenha[i].previousElementSibling;
            const tipoSenha = senhaInput.type === 'password' ? 'text' : 'password';
            senhaInput.type = tipoSenha; 
            visualizarSenha[i].classList.toggle('formulario__botao--senha-ativo'); 
        });
    }
});