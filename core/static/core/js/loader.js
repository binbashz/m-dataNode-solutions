window.addEventListener('load', function() {
    document.getElementById('loader').style.display = 'none';
});

// Mostrar el loader antes de cargar la página
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('loader').style.display = 'flex';
});