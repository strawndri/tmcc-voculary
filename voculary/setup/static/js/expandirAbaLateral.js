document.addEventListener("DOMContentLoaded", function() {
    const cards = document.querySelectorAll(".meus-textos__card, .tabela__body__item");
    const abaLateral = document.querySelector(".aba-lateral");
    const fechar = document.querySelector(".aba-lateral .fechar");
    const overlay = document.querySelector('.overlay');

    function mostrarAbaLateral(data) {
        overlay.style.display = 'block';
        abaLateral.querySelector("h4").textContent = data.nome;
        abaLateral.querySelector("p").textContent = `Gerado em: ${data.data_geracao}`;
        abaLateral.querySelector(".imagem-display").style.backgroundImage = `url(${data.imagem_url})`;
        abaLateral.querySelector("textarea").textContent = data.texto;
    }

    function esconderAbaLateral() {
        overlay.style.display = 'none';
        abaLateral.classList.remove("mostrar");
        resetarZoom();  // Fazer com que a imagem retorne ao seu estado inicial
    }

    cards.forEach(card => {
        card.addEventListener("click", function(e) {
            if (e.target.tagName === 'INPUT' || e.target.closest('INPUT')) return;
            const id_imagem = card.getAttribute('data-texto');
            abaLateral.setAttribute('data-texto', id_imagem);
            abaLateral.classList.add("mostrar");
            fetch(`/obter-info-texto/${id_imagem}/`)
                .then(response => response.json())
                .then(mostrarAbaLateral);
        });
    });

    fechar.addEventListener("click", esconderAbaLateral);
    overlay.addEventListener("click", function(event) {
        if (event.target === overlay) esconderAbaLateral();
    });
});