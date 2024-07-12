document.addEventListener('DOMContentLoaded', function() {
    const notificationToggle = document.querySelector('.notification-toggle');
    const notificationDropdown = document.querySelector('.notification-dropdown');
    const notificationCount = document.querySelector('.notification-count');

    notificationToggle.addEventListener('click', function() {
        notificationDropdown.style.display = notificationDropdown.style.display === 'block' ? 'none' : 'block';
    });

    function actualizarNotificaciones() {
        fetch('/obtener-notificaciones/')  
            .then(response => response.json())
            .then(data => {
                const notificacionesDiv = document.getElementById('notificaciones');
                notificacionesDiv.innerHTML = '';
                notificationCount.textContent = data.length;

                if (data.length > 0) {
                    data.forEach(notif => {
                        const notifElem = document.createElement('div');
                        notifElem.className = 'notification-item';
                        notifElem.innerHTML = `
                            <p>${notif.mensaje}</p>
                            <small>${formatDate(notif.fecha)}</small>
                            <button onclick="marcarLeida(${notif.id})">Marcar como leída</button>
                        `;
                        notificacionesDiv.appendChild(notifElem);
                    });
                } else {
                    notificacionesDiv.innerHTML = '<p>No hay notificaciones nuevas.</p>';
                }
            });
    }

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString();
}

function marcarLeida(id) {
    fetch(`/marcar-leida/${id}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            actualizarNotificaciones();
        }
    });
}

// Función para obtener el valor de una cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Iniciar la actualización de notificaciones
setInterval(actualizarNotificaciones, 60000); // Actualiza cada minuto
actualizarNotificaciones(); // Llamada inicial
});