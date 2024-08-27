document.addEventListener('DOMContentLoaded', function() {
    const filtro = document.getElementById('filtro-cuotas');
    const cuotas = document.querySelectorAll('.cuota-item');

    filtro.addEventListener('change', function() {
        const valorFiltro = this.value;
        cuotas.forEach(cuota => {
            if (valorFiltro === 'todos' || cuota.dataset.estado === valorFiltro) {
                cuota.style.display = '';
            } else {
                cuota.style.display = 'none';
            }
        });
    });
});