// Función para abrir el modal
function openModal(clienteId) {
    var modal = document.getElementById('myModal' + clienteId);
    modal.style.display = 'block';
  }
  
  // Función para cerrar el modal
  function closeModal(clienteId) {
    var modal = document.getElementById('myModal' + clienteId);
    modal.style.display = 'none';
  }
  