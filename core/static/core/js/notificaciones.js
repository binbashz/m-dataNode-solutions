document.addEventListener('DOMContentLoaded', () => {
    const notificationToggle = document.querySelector('.notification-toggle');
    const notificationDropdown = document.querySelector('.notification-dropdown');
    const notificationCount = document.querySelector('.notification-count');
    const notificacionesDiv = document.getElementById('notificaciones');

    notificationToggle.addEventListener('click', () => {
        notificationDropdown.classList.toggle('show');
    });

    async function actualizarNotificaciones() {
        try {
            const response = await fetch('/obtener-notificaciones/');
            const data = await response.json();
            notificacionesDiv.innerHTML = '';
            const notificacionesNoLeidas = data.filter(n => !n.leido);
            notificationCount.textContent = notificacionesNoLeidas.length;

            if (data.length > 0) {
                data.forEach(notif => {
                    const notifElem = document.createElement('div');
                    notifElem.className = `notification-item ${notif.leido ? 'leido' : ''}`;
                    notifElem.innerHTML = `
                        <p>${notif.mensaje}</p>
                        <small>${formatDate(notif.fecha)}</small>
                        ${!notif.leido ? `<button onclick="marcarLeida(${notif.id})">Marcar como leída</button>` : ''}
                    `;
                    notificacionesDiv.appendChild(notifElem);
                });
            } else {
                notificacionesDiv.innerHTML = '<p>No hay notificaciones.</p>';
            }
        } catch (error) {
            console.error('Error al obtener notificaciones:', error);
        }
    }

    function formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleString();
    }

    async function marcarLeida(id) {
        try {
            const response = await fetch(`/marcar-leida/${id}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json',
                },
            });
            const data = await response.json();
            if (data.success) {
                actualizarNotificaciones();
            }
        } catch (error) {
            console.error('Error al marcar notificación como leída:', error);
        }
    }

    function getCookie(name) {
        const cookieValue = document.cookie.split('; ').find(row => row.startsWith(name + '='));
        return cookieValue ? decodeURIComponent(cookieValue.split('=')[1]) : null;
    }

    setInterval(actualizarNotificaciones, 60000); // Actualiza cada minuto
    actualizarNotificaciones(); // Llamada inicial
});


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

    setInterval(actualizarNotificaciones, 60000); // Actualiza cada minuto
    actualizarNotificaciones(); // Llamada inicial
