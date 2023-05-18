// Pegar todos os inputs que tem o tipo 'password'
const senhaInput = document.querySelectorAll('input[type="password"]');

// Pegar todos os elementos do html que possuem a classe abaixo
const visualizarSenha = document.querySelectorAll('.formulario__botao--senha');


/* 
    Como podem existir mais de um botão, é necessáeio fazer um for para percorrer toda a lista visualizarSenha
*/
for (let i = 0; i < visualizarSenha.length; i++) {
visualizarSenha[i].addEventListener('click', () => {

        // Já sabendo qual botão foi clicado, pega-se o elemento anterior (input)
        const senhaInput = visualizarSenha[i].previousElementSibling;
        const tipoSenha = senhaInput.type === 'password' ? 'text' : 'password';
        senhaInput.type = tipoSenha; // altera o tipo do input
        visualizarSenha[i].classList.toggle('formulario__botao--senha-ativo'); // adiciona ou retira a classe do botão
    });
}