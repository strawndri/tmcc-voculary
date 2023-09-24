document.addEventListener("DOMContentLoaded", function() {
    let cards = document.querySelectorAll(".meus-textos__card, .tabela__body__item");
    let abaLateral = document.querySelector(".aba-lateral");
    let fechar = document.querySelector(".aba-lateral .fechar");
    let overlay = document.querySelector('.overlay');

    cards.forEach(card => {
        card.addEventListener("click", function(e) {
            if (e.target.tagName === 'INPUT' || e.target.closest('INPUT')) {
                return; 
            }

            let id_imagem = card.getAttribute('data-texto');
            abaLateral.setAttribute('data-texto', id_imagem);
            
            fetch(`/obter-info-texto/${id_imagem}/`)
                .then(response => response.json())
                .then(data => {
                    overlay.style.display = 'block';
                    abaLateral.querySelector("h4").textContent = data.nome;
                    abaLateral.querySelector("p").textContent = `Gerado em: ${data.data_geracao}`;
                    abaLateral.querySelector(".imagem-display").style.backgroundImage = `url(${data.imagem_url})`
                    abaLateral.querySelector("textarea").textContent = data.texto;

                    abaLateral.classList.add("mostrar");
                });
        });
    });
    
    fechar.addEventListener("click", function() {
        overlay.style.display = 'none';
        abaLateral.classList.remove("mostrar");
    });

    overlay.addEventListener("click", function(event) {
        if (event.target === overlay) {
            overlay.style.display = 'none';
            abaLateral.classList.remove("mostrar");
        }
    });
});
