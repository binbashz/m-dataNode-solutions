// Carrusel 14  tarjetas en home 
// Seleccionamos el contenedor de las tarjetas
const tarjetasContainer = document.querySelector('.tarjetas-grid-container');

// Clonamos las tarjetas y las añadimos al final para crear un efecto infinito
const tarjetas = tarjetasContainer.innerHTML;
tarjetasContainer.innerHTML = tarjetas + tarjetas;

// Establecemos la anchura total del conjunto de tarjetas
const totalWidth = tarjetasContainer.scrollWidth;

// Establecemos la velocidad de desplazamiento (pixels por segundo)
const velocidadDesplazamiento = 68; // Ajusta este valor según prefieras

// Función para desplazar las tarjetas automáticamente
function desplazarTarjetas() {
  if (tarjetasContainer.scrollLeft >= totalWidth / 2) {
    tarjetasContainer.scrollLeft = 0;
  } else {
    tarjetasContainer.scrollLeft += 1;
  }
}

// Iniciamos el desplazamiento automático
setInterval(desplazarTarjetas, 1500 / velocidadDesplazamiento);

// Ajustamos el estilo del contenedor para el desplazamiento continuo
tarjetasContainer.style.display = 'flex';
tarjetasContainer.style.overflow = 'hidden';