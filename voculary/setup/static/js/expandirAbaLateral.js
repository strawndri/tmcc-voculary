document.addEventListener("DOMContentLoaded", function() {
    let cards = document.querySelectorAll(".meus-textos__card, .tabela__body__item");
    let abaLateral = document.querySelector(".aba-lateral");
    let fechar = document.querySelector(".aba-lateral .fechar");

    cards.forEach(card => {
        card.addEventListener("click", function() {
            let id_imagem = card.getAttribute('data-texto');
            abaLateral.setAttribute('data-texto', id_imagem)
            
            fetch(`/obter-info-texto/${id_imagem}/`)
                .then(response => response.json())
                .then(data => {
                    document.querySelector('.overlay').style.display = 'block';
                    document.querySelector(".aba-lateral h4").textContent = data.nome;
                    document.querySelector(".aba-lateral p").textContent = `Gerado em: ${data.data_geracao}`;
                    document.querySelector(".aba-lateral .imagem-display").style.backgroundImage = `url(${data.imagem_url})`
                    document.querySelector(".aba-lateral textarea").textContent = data.texto;

                    abaLateral.classList.add("mostrar");
                });
        });
    });
    
    fechar.addEventListener("click", function() {
        document.querySelector('.overlay').style.display = 'none';
        abaLateral.classList.remove("mostrar");
    });

    document.addEventListener("click", function(event) {
        if (
            !abaLateral.contains(event.target) && // Se o clique não foi na aba lateral
            !event.target.matches(".meus-textos__card, .tabela__body__item, button") && // Se o clique não foi em um card, item ou botão
            event.target.closest('button') === null && // Se o clique não foi dentro de um botão
            event.target !== fechar // Se o clique não foi no elemento fechar
        ) {
            document.querySelector('.overlay').style.display = 'none';
            abaLateral.classList.remove("mostrar");
        }
    });
    
    
});


