// lockslogg.js
(function(window) {
    function initializeCards() {
        var isAuthenticated = window.isAuthenticated;
        var cardUrls = window.cardUrls;

        if (typeof isAuthenticated === 'undefined' || !Array.isArray(cardUrls)) {
            console.error('Variables necesarias no definidas correctamente');
            return;
        }

        var cards = [
            { title: "Registrar Variedades", urlIndex: 0 },
            { title: "Condiciones de Cultivo", urlIndex: 1 },
            { title: "Tratamiento Fitofarmacéutico", urlIndex: 2 },
            { title: "Información de Análisis", urlIndex: 3 },
            { title: "Recomendaciones de Cultivo", urlIndex: 4 },
            { title: "Información en PDF", urlIndex: 5 },
            { title: "Simulación de Rendimiento", urlIndex: 6 },
            { title: "Análisis de Costos", urlIndex: 7 },
            { title: "Registro de Clientes", urlIndex: 8 },
            { title: "Clientes y Análisis", urlIndex: 9 },
            { title: "Recepción de Muestras", urlIndex: 10 },
            { title: "Resultados y Observaciones", urlIndex: 11 },
            { title: "Códigos de Barra", urlIndex: 12 },
            { title: "Favoritos", urlIndex: 13 }
        ];

        if (isAuthenticated) {
            cards.forEach(function(card, index) {
                var cardElement = document.getElementById('card-' + (index + 1));
                if (cardElement) {
                    var titleElement = cardElement.querySelector('.card-title');
                    if (titleElement) {
                        titleElement.textContent = card.title;
                    }
                    cardElement.addEventListener('click', function() {
                        if (cardUrls[card.urlIndex]) {
                            window.location.href = cardUrls[card.urlIndex];
                        }
                    });
                    cardElement.style.cursor = 'pointer';
                }
            });
        }
    }

    // Intentar inicializar cuando el DOM esté listo
    document.addEventListener('DOMContentLoaded', initializeCards);

})(window);