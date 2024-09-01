document.addEventListener('DOMContentLoaded', function() {
    const notificationToggle = document.querySelector('.notification-toggle');
    const notificationDropdown = document.querySelector('.notification-dropdown');
    const notificationCount = document.querySelector('.notification-count');

    notificationToggle.addEventListener('click', function() {
        notificationDropdown.style.display = notificationDropdown.style.display === 'block' ? 'none' : 'block';
    });

    function actualizarNotificaciones() {
        fetch('/obtener-notificaciones/')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                const notificacionesDiv = document.getElementById('notificaciones');
                notificacionesDiv.innerHTML = '';
                const notificacionesNoLeidas = data.filter(n => !n.leido);
                notificationCount.textContent = notificacionesNoLeidas.length;

                if (data.length > 0) {
                    data.forEach(notif => {
                        const notifElem = document.createElement('div');
                        notifElem.className = `notification-item ${notif.leido ? 'leido' : ''}`;
                        notifElem.setAttribute('data-id', notif.id);
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
            })
            .catch(error => {
                console.error('Error fetching notifications:', error);
            });
    }

    function formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleString();
    }

    window.marcarLeida = function(id) {
        console.log(`Marcar como leída: ${id}`); // Depuración

        fetch(`/marcar-leida/${id}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json',
            },
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                actualizarNotificaciones();
                const notificationElement = document.querySelector(`.notification-item[data-id="${id}"]`);
                if (notificationElement) {
                    notificationElement.classList.add('leido');
                }
            } else {
                console.error('Server responded with an error:', data);
            }
        })
        .catch(error => {
            console.error('There was a problem with your fetch operation:', error);
        });
    };

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

    setInterval(actualizarNotificaciones, 180000); // Actualiza cada 3 minutos
    actualizarNotificaciones(); // Llamada inicial
});
