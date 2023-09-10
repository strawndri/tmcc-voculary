let btnCopiar = document.getElementById("btnCopiar");
let btnDownload = document.getElementById("btnBaixar");
let textoElement = document.querySelector(".texto");
let texto = textoElement.innerHTML;

function handleMutations(mutationsList, observer) {
    for (let mutation of mutationsList) {
        if (mutation.type === 'childList') {
            texto = textoElement.innerHTML;
            console.log('Texto atualizado:', texto);
        }
    }
}

const observer = new MutationObserver(handleMutations);

observer.observe(textoElement, { childList: true });

btnCopiar.addEventListener('click', () => {
    navigator.clipboard.writeText(texto)
});

btnDownload.addEventListener('click', function() {
    var doc = new jsPDF()
    doc.text(10, 10, doc.splitTextToSize(texto, 180));
    doc.save('download.pdf');
})