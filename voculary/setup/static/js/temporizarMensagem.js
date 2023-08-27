const mensagens = document.querySelectorAll(".mensagem");
const iconesFechar = document.querySelectorAll(".fechar");
const progressos = document.querySelectorAll(".progresso");

mensagens.forEach((mensagem, index) => {
    setTimeout(() => {
        mensagem.classList.remove("ativo");
    }, 5000);

    iconesFechar[index].addEventListener("click", () => {
        mensagem.classList.remove("ativo");
        setTimeout(() => {
            progressos[index].classList.remove("ativo");
        }, 300);
    });
});
