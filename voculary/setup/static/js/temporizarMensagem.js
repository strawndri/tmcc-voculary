window.setTimeout(function() {
    let djangoMessages = document.getElementById('django-messages');
    djangoMessages.style.transition = "all 1s ease-in-out";
    djangoMessages.style.transform = 'translateX(100%)';
    djangoMessages.style.right = '0';
  }, 5000); // desaparecerá após 10000 milissegundos ou 10 segundos.
  