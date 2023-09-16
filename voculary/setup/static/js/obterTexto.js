let btnCopiarList = document.querySelectorAll(".btn-copiar");
let btnDownloadList = document.querySelectorAll(".btn-baixar");

btnCopiarList.forEach(btn => {
    btn.addEventListener('click', function(event) {
        event.preventDefault();
        let origin = this.closest('[data-origin]').getAttribute('data-origin');
        let textoElement = this.closest('[data-origin]').querySelector('.texto');
        let texto = textoElement.innerHTML;
        console.log(`Copiando texto da origem: ${origin}`);
        navigator.clipboard.writeText(texto);
    });
});

btnDownloadList.forEach(btn => {
    btn.addEventListener('click', function(event) {
        event.preventDefault();
        let origin = this.closest('[data-origin]').getAttribute('data-origin');
        let textoElement = this.closest('[data-origin]').querySelector('.texto');
        let texto = textoElement.innerHTML;
        console.log(`Baixando texto da origem: ${origin}`);
        
        let doc = new jsPDF();
        doc.text(10, 10, doc.splitTextToSize(texto, 180));
        doc.save('download.pdf');
    });
});
