let btnCopiar = document.getElementById("copiarTexto");
let btnDownload = document.getElementById("baixarTexto");

// Selecionando o elemento
let textoElement = document.querySelector(".texto");
let texto = textoElement.innerHTML;

// Criando uma função para lidar com as mutações
function handleMutations(mutationsList, observer) {
    for (let mutation of mutationsList) {
        if (mutation.type === 'childList') {
            texto = textoElement.innerHTML;
            console.log('Texto atualizado:', texto);
        }
    }
}

// Inicializando o MutationObserver
const observer = new MutationObserver(handleMutations);

// Configuração para observar apenas mudanças de filhos do elemento
observer.observe(textoElement, { childList: true });

btnCopiar.addEventListener('click', () => {
    navigator.clipboard.writeText(texto)
});

btnDownload.addEventListener('click', function() {
    var doc = new jsPDF()
    doc.text(10, 10, doc.splitTextToSize(texto, 180));
    doc.save('download.pdf');
})