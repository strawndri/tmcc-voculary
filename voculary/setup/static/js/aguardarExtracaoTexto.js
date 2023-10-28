document.addEventListener("DOMContentLoaded", function() {
    let btnExtrair = document.querySelector('#btnExtrair');

    if (btnExtrair) {
        btnExtrair.addEventListener('click', function() {
            let loadingElement = document.querySelector('.loading');
            let overlayElement = document.querySelector('.overlay');
            
            if (loadingElement && overlayElement) {
                loadingElement.style.display = 'block';
                overlayElement.style.display = 'block';
            }
        });
    }
});