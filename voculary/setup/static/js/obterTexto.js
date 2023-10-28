let btnCopiarList = document.querySelectorAll(".btn-copiar");
let btnDownloadList = document.querySelectorAll(".btn-baixar");

function handleBotaoClick(event, action) {
    event.preventDefault();
    let parentElement = this.closest('[data-origin]');
    let origin = parentElement.getAttribute('data-origin');
    let textoElement = parentElement.querySelector('.texto');
    let texto = textoElement.innerHTML;

    switch(action) {
        case 'copy':
            console.log(`Copiando texto da origem: ${origin}`);
            navigator.clipboard.writeText(texto);
            break;
        case 'download':
            console.log(`Baixando texto da origem: ${origin}`);
            let doc = new jsPDF();
            doc.text(10, 10, doc.splitTextToSize(texto, 180));
            doc.save('download.pdf');
            break;
    }
}

btnCopiarList.forEach(btn => {
    btn.addEventListener('click', function(event) {
        handleButtonClick.call(this, event, 'copy');
    });
});

btnDownloadList.forEach(btn => {
    btn.addEventListener('click', function(event) {
        handleButtonClick.call(this, event, 'download');
    });
});
