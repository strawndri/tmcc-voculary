document.addEventListener("DOMContentLoaded", function() {
    let cards = document.querySelectorAll(".meus-textos__card, .tabela__body__item");
    let abaLateral = document.querySelector(".aba-lateral");
    let fechar = document.querySelector(".aba-lateral .fechar");

    cards.forEach(card => {
        card.addEventListener("click", function() {
            let id_imagem = card.getAttribute('data-texto');
            
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
        if (!abaLateral.contains(event.target) &&
            !event.target.matches(".meus-textos__card, .tabela__body__item, #btnExtrair") &&
            event.target !== fechar) {
            
            document.querySelector('.overlay').style.display = 'none';
            abaLateral.classList.remove("mostrar");
        }
    });
    
});


